from fastapi import FastAPI, Request, HTTPException
import httpx
import pandas as pd
from pymongo import MongoClient
import traceback
from bson.regex import Regex

# Configurar la conexión a MongoDB
client = MongoClient("mongodb://mongodb:27017/")
db = client["mydatabase"]
matches_collection = db["matches"]

app = FastAPI()

API_KEY = "d75e1a9df5b24ef7b38212d36842ecde"  # key api.football

@app.get("/")
async def root():
    return {"message": "¡Bienvenido a tu aplicación de FastAPI!"}



@app.get("/filter_matches_date_goals/")
async def get_matches(request: Request):
    date_init = request.query_params.get("date_init")
    date_end = request.query_params.get('date_end')
    goals = request.query_params.get('goals')

    # Verificar si los parámetros obligatorios están presentes
    if not date_init or not date_end:
        raise HTTPException(status_code=400, detail="Parameters 'date_init' and 'date_end' are obligatory.")

    async with httpx.AsyncClient() as client:
        url = f"https://api.football-data.org/v4/matches?competitions=PL&status=FINISHED&dateFrom={date_init}&dateTo={date_end}"
        headers = {"X-Auth-Token": API_KEY}
        response = await client.get(url, headers=headers)
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


@app.get("/list")
async def get_list(request: Request):
    # Consultar todos los registros de la colección de MongoDB
    
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

