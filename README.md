# Golden Raspberry Awards API
### What is this project

This project exposes a REST API that calculates the minimum and maximum intervals between consecutive wins for movie producers at the Golden Raspberry Awards.

The data is loaded from a CSV file at startup, stored in a database, and exposed through a single HTTP endpoint.

The project is designed to run using Docker only.

## Mandatory requirements

Docker installed

### How to run the project (step by step)
1. Build the Docker image: docker build -t golden-raspberry-api .

2. Run integration tests: docker run --rm golden-raspberry-api pytest -q

### Expected output (example): 2 passed in X.XXs

3. Start the API container: docker run --rm -p 8000:8000 golden-raspberry-api

4. Access the API
Open your browser:

Swagger UI
http://localhost:8000/docs

Endpoint
http://localhost:8000/api/producers/awards-intervals

## API endpoint
GET /api/producers/awards-intervals

Returns the producers with the shortest and longest intervals between consecutive wins.

Example response:

{
  "min": [
    {
      "producer": "Joel Silver",
      "interval": 1,
      "previousWin": 1990,
      "followingWin": 1991
    }
  ],
  "max": [
    {
      "producer": "Matthew Vaughn",
      "interval": 13,
      "previousWin": 2002,
      "followingWin": 2015
    }
  ]
}

### Notes:

The application loads the CSV file automatically at startup.
Only integration tests are implemented, as required.
The project works with any CSV following the same structure.