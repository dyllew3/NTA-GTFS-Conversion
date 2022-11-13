import os
from pymongo import database
from .download import DownloadService
from .gtfs import *
from .translation import connect_route_stops


# Function to run loop of downloading zip and uploading translated object to mongodb
def temp_name(zip_url: str, name: str, download_service: DownloadService, mongo_db: database.Database) -> None:
    extracted = download_service.extract_if_diff(zip_url, name)
    if not extracted:
        return
    parameters = {}

    for k in FILE_TO_OBJECT_MAPPINGS:
        obj_type = FILE_TO_OBJECT_MAPPINGS[k]
        loaded_obj = load_gtfs_from_file(os.path.join(name, k), obj_type)
        parameters[FILE_TO_PARAMETER_NAME[k]] = loaded_obj
    connections = connect_route_stops(routes=parameters["routes"], stop_times=parameters["stop_times"],
                        trips=parameters["trips"])
