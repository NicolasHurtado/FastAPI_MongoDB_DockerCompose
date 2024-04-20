from fastapi import FastAPI, Request, HTTPException, Query, Depends
import httpx
import pandas as pd
from pymongo import MongoClient
import traceback
from bson.regex import Regex
import asyncio
from datetime import datetime, timedelta
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.instrumentation.pymongo import PymongoInstrumentor
from utils import MatchesQueryParams, ListQueryParams

# Configurar la conexión a MongoDB
PymongoInstrumentor().instrument()

def get_prod_client():
    return MongoClient("mongodb://mongodb:27017/")


# Set up the tracer provider
trace.set_tracer_provider(
    TracerProvider(resource=Resource.create({SERVICE_NAME: "FastAPI-Matches"}))
)
tracer_provider = trace.get_tracer_provider()

#Configure Jaeger exporter
jaeger_exporter = JaegerExporter(
    agent_host_name="jaeger",
    agent_port=6831
)

#Add the Jaeger exporter to the tracer provider
tracer_provider.add_span_processor(BatchSpanProcessor(jaeger_exporter))
app = FastAPI()
FastAPIInstrumentor.instrument_app(app)

API_KEY = "d75e1a9df5b24ef7b38212d36842ecde"  # key api.football

@app.get("/")
async def root():
    return {"message": "¡Bienvenido a tu aplicación de FastAPI!"}


@app.get("/filter_matches/")
async def get_matches(request: Request, params: MatchesQueryParams = Depends(), client: MongoClient = Depends(get_prod_client)):
    date_init_str = request.query_params.get("date_init")
    date_end_str = request.query_params.get('date_end')
    goals = request.query_params.get('goals')
    db = client["mydatabase"]
    matches_collection = db["matches"]
    # Verificar si los parámetros obligatorios están presentes
    if not date_init_str or not date_end_str:
        raise HTTPException(status_code=400, detail="Parameters 'date_init' and 'date_end' are obligatory.")
    
    # Convertir las cadenas de fecha en objetos de fecha
    date_init = datetime.strptime(date_init_str, '%Y-%m-%d')
    date_end = datetime.strptime(date_end_str, '%Y-%m-%d')

    # Verificar si date_end es mayor a 10 días después de date_init
    if date_end > date_init + timedelta(days=10):
        raise HTTPException(status_code=400, detail="Parameter 'date_end' cannot be more than 10 days after 'date_init'.")


    
    # Inicializar el trazador
    tracer = tracer_provider.get_tracer(__name__)
    span_attributes = {
        "date_init_str": date_init_str,
        "date_end_str": date_end_str,
        "goals": goals
    }
    with tracer.start_as_current_span("fetch_matches", attributes=span_attributes):
        while True:  # Bucle infinito para reintentar la solicitud
            try:
                print('paso1')
                async with httpx.AsyncClient() as client:
                    url = f"https://api.football-data.org/v4/matches?competitions=PL&status=FINISHED&dateFrom={date_init_str}&dateTo={date_end_str}"
                    headers = {"X-Auth-Token": API_KEY}
                    response = await client.get(url, headers=headers)
                    response.raise_for_status()  # Lanza una excepción si hay un error en la respuesta HTTP
                    data = response.json()
                    filtered_matches = []

                    matches_df = pd.DataFrame(data["matches"])
                    matches_df["total_goals"] = matches_df.apply(lambda row: row["score"]["fullTime"]["home"] + row["score"]["fullTime"]["away"], axis=1)
                    filtered_matches_df = matches_df[matches_df["total_goals"] >= int(goals)] if goals else matches_df    
                    filtered_matches = filtered_matches_df[["homeTeam", "awayTeam", "matchday", "score", "utcDate"]]
                    filtered_matches["Score"] = filtered_matches.apply(lambda row: f"{row['score']['fullTime']['home']} - {row['score']['fullTime']['away']}", axis=1)
                    filtered_matches["When"] = pd.to_datetime(filtered_matches["utcDate"]).dt.strftime('%Y-%m-%d %H:%M:%S')
                    filtered_matches["HomeTeam"] = filtered_matches.apply(lambda row: {"id": row["homeTeam"]["id"], "name": row["homeTeam"]["name"]}, axis=1)
                    filtered_matches["AwayTeam"] = filtered_matches.apply(lambda row: {"id": row["awayTeam"]["id"], "name": row["awayTeam"]["name"]}, axis=1)
                    filtered_matches = filtered_matches[["HomeTeam", "AwayTeam", "matchday", "Score", "When"]]
                    filtered_matches = filtered_matches.rename(columns={"matchday": "Matchday"})
                    # Convertir los datos filtrados a una lista de diccionarios
                    matches_data = filtered_matches.to_dict(orient="records")
                    # Insertar los registros en la colección de MongoDB
                    matches_collection.insert_many(matches_data)
                    return filtered_matches.to_dict(orient="records")
            except httpx.HTTPError as e:
                print(f"Ocurrió un error al hacer la solicitud: {e}")
                await asyncio.sleep(2)  # Espera un segundo antes de reintentar


@app.get("/list")
async def get_list(request: Request, params: ListQueryParams = Depends(), client: MongoClient = Depends(get_prod_client) ):
    db = client["mydatabase"]
    matches_collection = db["matches"]
    team_name = request.query_params.get("team_name")
    page = int(request.query_params.get("page", 1))  # Página actual (por defecto 1)
    page_size = 5  # Tamaño de la página
    
    # Calcular el número de documentos que se deben omitir para esta página
    skip = (page - 1) * page_size
    # Si se proporciona el parámetro de consulta "team_name", filtrar los registros
    if team_name:
        query = {}
        regex = Regex(team_name, "i")  # "i" para que sea insensible a mayúsculas y minúsculas
        query["$or"] = [
            {"HomeTeam.name": {"$regex": regex}},
            {"AwayTeam.name": {"$regex": regex}}
        ]
        # Consultar la base de datos con el filtro aplicado
        total_count = matches_collection.count_documents(query)
        matches_data = list(matches_collection.find(query).skip(skip).limit(page_size))
    else:
        total_count = matches_collection.count_documents({})
        matches_data = list(matches_collection.find().skip(skip).limit(page_size))
    # Convertir ObjectId a cadenas en los diccionarios
    for match in matches_data:
        match["_id"] = str(match.get("_id"))
    
    # Calcular si existe una página siguiente
    has_next_page = (skip + page_size) < total_count

    return {
        "total_count": total_count,
        "page": page,
        "has_next_page": has_next_page,
        "matches": matches_data
    }

