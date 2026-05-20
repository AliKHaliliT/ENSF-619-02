from io import BytesIO
import json
import logging
import os
import zipfile

import requests

# Set up logging for the pipeline
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Define paths for local execution
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_DIR = os.path.join(DATA_DIR, "raw")


def ingest_geojson_api() -> None:
    
    """

    Retrieve GeoJSON Vector Data via API.

    This function fulfills Task 1.3 by hitting a live HTTP endpoint
    to retrieve a GeoJSON file, saving it locally, and printing
    the required validation metrics (size, row count).


    Parameters
    ----------
    None.


    Returns
    -------
    None.
        Outputs are written directly to the local filesystem.

    """
    
    os.makedirs(RAW_DIR, exist_ok=True)
    
    logging.info("Starting API-based retrieval (USGS GeoJSON)...")
    url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"
    output_path = os.path.join(RAW_DIR, "usgs_earthquakes.geojson")
    

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        

        with open(output_path, 'w') as f:
            json.dump(data, f)
            

        file_size = os.path.getsize(output_path) / 1024
        feature_count = len(data.get('features', []))
        

        logging.info(f"SUCCESS: Saved GeoJSON to {output_path}")
        print(f"\n--- GeoJSON API Stats ---")
        print(f"File Size: {file_size:.2f} KB")
        print(f"Row/Feature Count: {feature_count}")
        print(f"Native CRS: EPSG:4326 (WGS 84)\n")
        

    except requests.exceptions.RequestException as e:
        logging.error(f"API Ingestion failed: {e}")


def ingest_zipped_shapefile() -> None:
    
    """

    Retrieve and extract Zipped Spatial Data via URL.

    This function fulfills Task 1.3 by downloading a zipped archive
    of vector Shapefiles directly into memory, extracting them to 
    the raw data directory, and validating the output.


    Parameters
    ----------
    None.


    Returns
    -------
    None.
        Extracted files are written directly to the local filesystem.

    """
    
    os.makedirs(RAW_DIR, exist_ok=True)
    
    logging.info("Starting File-based retrieval (Zipped Shapefile)...")
    url = "https://naciscdn.org/naturalearth/110m/physical/ne_110m_coastline.zip"
    extract_dir = os.path.join(RAW_DIR, "ne_coastlines")
    

    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        

        with zipfile.ZipFile(BytesIO(response.content)) as z:
            z.extractall(extract_dir)
            

        files_extracted = os.listdir(extract_dir)
        total_size = sum(os.path.getsize(os.path.join(extract_dir, f)) for f in files_extracted) / 1024
        

        logging.info(f"SUCCESS: Extracted Zip to {extract_dir}")
        print(f"\n--- File Download Stats ---")
        print(f"Total Extracted Size: {total_size:.2f} KB")
        print(f"Files extracted: {', '.join(files_extracted)}\n")
        

    except Exception as e:
        logging.error(f"File Ingestion failed: {e}")


if __name__ == "__main__":
    
    print("\nStarting Geospatial Ingestion Pipeline...\n")
    ingest_geojson_api()
    ingest_zipped_shapefile()
    print("Pipeline Execution Complete.\n")