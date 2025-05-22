#!/bin/sh

sleep 30

# Run the DB fill script
echo "Running refresh_data.py..."
python refresh_data.py --elastic-search-host $ELASTICSEARCH_HOSTS

# Start the Flask app
echo "Starting Flask app..."
python app.py -d 