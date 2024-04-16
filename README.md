  #### Python (FastAPI) + MongoDB + DockerCompose
### Query matches by range date and minimum goals in match
## Requisitos previos / Previous requirements

- Docker
- Python
- Mongo DB

# Desplegar la app / Deploy app
- docker compose up --build

# Verificar información del servicio desplegado / Verify deployed service information
- http://127.0.0.1:8000/ in your browser
  
## Ejemplos de uso / Use examples
- http://127.0.0.1:8000/filter_matches_date_goals/?date_init=2024-04-05&date_end=2024-04-10&goals=3 
# set date_init and date_end for range query ( Obligatory )
# set minimum goals in match for query ( Obligatory )

## Listar documentos creados en db / list documents created on db
- http://127.0.0.1:8000/list?team_name=liverpool&page=1
# set team_name for the query filter ( No Obligatory )
# set page for the query filter ( Obligatory )



***Nicolas Hurtado C***
