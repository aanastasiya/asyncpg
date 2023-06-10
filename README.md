# Asynchronous data retrieval
There are three data sources and a single common access point to these data sources that provides a correlated result. The access point is available via HTTP.
This access point makes requests to all data sources "asynchronously" and waits for the results from all of them. Upon receiving the results from all sources, the data is returned sorted by ID.

*An error/timeout from any of the sources is ignored and interpreted as missing data.*

# Start
Run PostgreSQL Server and create some database. 
Install dependencies from requirements.txt.
Create .env file with `DB_USERNAME`, `DB_PASSWORD` and `DB_NAME` variables.
Launch the app with `uvicorn main:app`.

# Test
`python -m unittest tests`

# Retrieve data via HTTP
Send GET request to http://127.0.0.1:8000/data/.

