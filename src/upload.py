import os
from pymongo import database
from .download import DownloadService
from .gtfs import *
from .translation import connect_route_stops, group_by
from typing import List, Dict

COLLECTION_NAME = "routes"
SERVICE_CALENDAR = "service_calendar"

def get_calendar_range(service_id: str, calendar_dates: Dict[str, List[Calendar]]):
    """Get the calendar range for a given service along

    Parameters:
        service_id:     Id of the service
        calendar_dates: Dictionary mapping date to list of calendar objects

    Returns
        Calendar object as a dictionary or an empty
    """
    for cal_date in calendar_dates:
        calendar_obj = calendar_dates[cal_date][0]
        if calendar_obj.service_id == service_id:
            return calendar_obj.__dict__
    return {}

def download_and_insert(data_sets: List[Dict[str, str]], download_service: DownloadService,
    mongo_db: database.Database, collection: str = COLLECTION_NAME):
    """Take a list of GTFS zip urls and download, extract and merge GTFS data. Then upload the merged data

    Parameters:
        data_sets:          Dictionary with name and url of GTFS data { name: string, url: string }
        download_service:   Service used to download data if there is a difference
        mongo_db:           Database to upload to
        collection:         Optional, name of the collection to upload to
    
    Returns:
        Mapping of name of download to the list of new IDs in mongo database.
    """
    results: Dict[str, str] = {}
    for info in data_sets:
        name, url = info["name"], info["url"]
        logging.info(f"Starting to download {name} GTFS dataset with url {url}")

        # Downloading and extracting zip folder
        zip_dir = os.path.join(os.path.curdir, name)
        result = insert_routes_to_db(url, zip_dir, download_service, mongo_db, collection)
        results[name] = result

        logging.debug("Deleting unneeded files")
        # Deleting files and folder
        for filename in os.listdir(zip_dir):
            os.remove(os.path.join(zip_dir, filename))
        os.rmdir(zip_dir)
    return results


# Function to run loop of downloading zip and uploading translated object to mongodb
def insert_routes_to_db(zip_url: str, directory: str, download_service: DownloadService, mongo_db: database.Database,
    coll_name: str):
    """Download and extract routes from a given url and then insert them into a Mongo database

    Parameters:
        zip_url:            Url of the zip to download and extract
        directory:          Directory to unzip into
        download_service:   Service that downloads and extracts zip if there is a difference
        mongo_db:           Mongo database
        coll_name:          Name of the collection to add to

    Returns:
        List of IDs if its inserted into the database  
    """
    extracted = download_service.extract_if_diff(zip_url, directory)
    if not extracted:
        logging.info("No difference not extracting")
        return []
    parameters = {}

    for k in FILE_TO_OBJECT_MAPPINGS:
        obj_type = FILE_TO_OBJECT_MAPPINGS[k]
        loaded_obj = load_gtfs_from_file(os.path.join(directory, k), obj_type)
        parameters[FILE_TO_PARAMETER_NAME[k]] = loaded_obj
    logging.info("Joining routes and trips to their stops")

    # Connect routes to their stops and what days they are running on
    connections = connect_route_stops(routes=parameters["routes"], stop_times=parameters["stop_times"],
                                      trips=parameters["trips"])
    calendar_dates = group_by("service_id", parameters["calendar"])
    ride_with_calendar = list(map(lambda x:  get_calendar_range(
        x["service_id"], calendar_dates) | x, connections))
    
    # Collection to store data under
    collection = mongo_db[coll_name]

    logging.info("Inserting data to database") 
    result = collection.insert_many(ride_with_calendar)
    return result.inserted_ids


