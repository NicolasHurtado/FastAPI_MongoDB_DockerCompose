from fastapi import FastAPI
import httpx
import pandas as pd

app = FastAPI()
API_KEY = "d75e1a9df5b24ef7b38212d36842ecde"  # Reemplaza "TU_CLAVE_DE_API" con tu propia clave

@app.get("/")
async def root():
    return {"message": "¡Bienvenido a tu aplicación de FastAPI!"}



@app.get("/matches")
async def get_matches():
    async with httpx.AsyncClient() as client:
        url = "https://api.football-data.org/v4/matches?competitions=PL&status=FINISHED&dateFrom=2024-04-13&dateTo=2024-04-15"
        headers = {"X-Auth-Token": API_KEY}
        response = await client.get(url, headers=headers)
        data = response.json()
        filtered_matches = []
    
    matches_df = pd.DataFrame(data["matches"])
    matches_df["total_goals"] = matches_df.apply(lambda row: row["score"]["fullTime"]["home"] + row["score"]["fullTime"]["away"], axis=1)
    filtered_matches_df = matches_df[matches_df["total_goals"] >= 2]

    filtered_matches = filtered_matches_df[["homeTeam", "awayTeam", "matchday", "score", "utcDate"]]
    filtered_matches["Marcador_final"] = filtered_matches.apply(lambda row: f"{row['score']['fullTime']['home']} - {row['score']['fullTime']['away']}", axis=1)
    filtered_matches["Cuando"] = pd.to_datetime(filtered_matches["utcDate"]).dt.strftime('%Y-%m-%d %H:%M:%S')
    filtered_matches["Local"] = filtered_matches["homeTeam"].apply(lambda x: x["name"])
    filtered_matches["Visitante"] = filtered_matches["awayTeam"].apply(lambda x: x["name"])
    filtered_matches = filtered_matches[["Local", "Visitante", "matchday", "Marcador_final", "Cuando"]]
    filtered_matches = filtered_matches.rename(columns={"matchday": "Fecha"})

    return filtered_matches.to_dict(orient="records")

