from fastapi.testclient import TestClient
from main import app, httpx, get_prod_client
import json
import unittest 
from unittest.mock import patch
from utils import mock_matches
import mongomock 

mock_json = mock_matches

test_client = mongomock.MongoClient()
async def get_test_client():
    return test_client




async def mocked_get(*args, **kwargs):
    response = httpx.Response(status_code=200)
    response._content = json.dumps(mock_json).encode('utf-8')
    # Configura una instancia de solicitud en la respuesta mockeada
    response._request = httpx.Request("GET", "https://api.football-data.org")
    return response

client = TestClient(app)

app.dependency_overrides[get_prod_client] = get_test_client

class test_matches(unittest.TestCase):

    def test_root(self):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "¡Bienvenido a tu aplicación de FastAPI!"}

    def test_filter_matches_missing_params(self):
        response = client.get("/filter_matches/?date_init=&date_end=&goals=0")
        assert response.status_code == 400
        assert "date_init' and 'date_end' are obligatory" in  json.loads(response.text).get('detail')
    
    def test_filter_matches_date_range_check(self):
        response = client.get("/filter_matches/?date_init=2024-03-15&date_end=2024-03-30&goals=3")
        # Verifica que la excepción tenga el código de estado y el detalle correctos
        assert response.status_code == 400
        assert "Parameter 'date_end' cannot be more than 10 days after 'date_init'." in  json.loads(response.text).get('detail')
    

    @patch('main.httpx.AsyncClient.get', side_effect=mocked_get)
    def test_filter_matches(self, mock_get):
        response = client.get("/filter_matches/?date_init=2024-03-15&date_end=2024-03-25&goals=3")
        assert response.status_code == 200
        assert "Tottenham Hotspur" in response.text

    # Mockea la función que configuraría la conexión a la base de datos
    def test_list_no_team_name(self):
        response = client.get("/list/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "total_count" in data
        assert "page" in data
        assert "has_next_page" in data
        assert "matches" in data
        assert len(data["matches"]) == 2  # Verifica que haya dos documentos en la base de datos simulada

    
    def test_list_team_name(self):
        db = test_client["mydatabase"]
        matches_collection = db["matches"]
        # Inserta algunos datos de prueba
        matches_collection.insert_many([
            {"HomeTeam": {"id": 1, "name": "Team A"}, "AwayTeam": {"id": 2, "name": "Team B"}, "Matchday": 1, "Score": "2 - 1", "When": "2024-01-01 12:00:00"},
            {"HomeTeam": {"id": 3, "name": "Team C"}, "AwayTeam": {"id": 4, "name": "Team D"}, "Matchday": 1, "Score": "1 - 1", "When": "2024-01-02 12:00:00"}
        ])
        response = client.get("/list?team_name=Team A")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "total_count" in data
        assert "page" in data
        assert "has_next_page" in data
        assert "matches" in data
        assert len(data["matches"]) == 1  # Verifica que haya dos documentos en la base de datos simulada

    
    
