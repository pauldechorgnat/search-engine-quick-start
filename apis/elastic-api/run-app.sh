#!/bin/sh

sleep 30

# Run the DB fill script
echo "Inserting data into Elsastic ..."
python refresh_data.py --elastic-search-host $ELASTICSEARCH_HOSTS

# Start the Flask app
echo "Starting API..."
python -m uvicorn api:api --host 0.0.0.0 --port 8000