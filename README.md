# ENSF 619 02

A repo for storing the code for ENSF 619 02 (Geo AI Course)

## Lab 1: Geospatial Data Ingestion

Student: Ali Khalili Tazehkandgheshlagh

REQUIREMENTS:
This pipeline requires standard Python 3.9+ and the following libraries:

- requests

(No specialized geospatial libraries like GDAL or GeoPandas are required for this specific ingestion script, ensuring it runs easily on any TA machine).

HOW TO RUN:

1. Ensure you have an active internet connection.
2. Open a terminal and navigate to the directory containing `ingestion.py`.
3. Run the script using: `python ingestion.py`

EXPECTED BEHAVIOR:

- The script uses relative paths and will automatically create a `data/raw/` directory in the same folder as the script.
- It will execute an API-based GET request to download USGS GeoJSON data.
- It will download a zipped archive of Natural Earth coastlines and extract them directly to the local directory.
- It will print the file size, row/feature counts, and bounding box CRS information directly to the console.

API KEYS:
No API keys are required to run this demonstration script. It utilizes open public endpoints to ensure seamless execution.
