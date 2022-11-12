
import json
import logging
import sys
import os
from typing import List
from src.gtfs import FILE_TO_PARAMETER_NAME, load_gtfs_from_file, FILE_TO_OBJECT_MAPPINGS
from src.translation import connect_route_stops


def get_folder_files(folder_path: str) -> List[str]:
    items = sorted(os.listdir(folder_path))
    return items


def main(args):
    output_folder: str = args[2]
    files = get_folder_files(args[1])
    parameters = {}
    for k in FILE_TO_OBJECT_MAPPINGS:
        if k in files:
            obj_type = FILE_TO_OBJECT_MAPPINGS[k]
            loaded_obj = load_gtfs_from_file(os.path.join(args[1], k), obj_type)
            output_file = os.path.join(output_folder,  k.replace(".txt", ".json"))
            parameters[FILE_TO_PARAMETER_NAME[k]] = loaded_obj
            with open(output_file, 'w') as f:
                json.dump([x.__dict__ for x in loaded_obj], f)
    connections = connect_route_stops(routes=parameters["routes"], stop_times=parameters["stop_times"],
                        trips=parameters["trips"])
    with open(os.path.join(output_folder,"connected.json"), 'w') as f:
        json.dump(connections, f)


if __name__ == "__main__":
    main(sys.argv)
