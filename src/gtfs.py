import csv
import logging
from typing import List, TypeVar

T = TypeVar('T')

STOP_HEADERS = ["stop_id", "stop_name", "stop_lat", "stop_lon"] # Stop csv headers

# Headers for Route csv
ROUTE_HEADERS = ["route_id", "agency_id",
                 "route_short_name", "route_long_name", "route_type"]
STOP_TIMES_HEADERS = ["trip_id", "arrival_time", "departure_time", "stop_id",
                      "stop_sequence", "stop_headsign", "pickup_type", "drop_off_type", "shape_dist_traveled"]

TRIP_HEADERS = ["route_id", "service_id", "trip_id",
                "shape_id", "trip_headsign", "direction_id"]

AGENCY_HEADERS = ["agency_id", "agency_name", "agency_url",
                  "agency_timezone", "agency_lang", "agency_phone"]


class Stop:
    """Class representing GTFS stop

    Attributes:
        stop_id:    ID of the stop.
        stop_name:  Name of the stop.
        stop_lat:   Latitude of the stop.
        stop_lon:   Longitude of the stop.
    """
    stop_id: str
    stop_name: str
    stop_lat: float
    stop_lon: float

    def __init__(self, stop_id: str = "",
                 stop_name: str = "",
                 stop_lat: float = "",
                 stop_lon: float = "") -> None:
        """Constructor"""
        self.stop_id = stop_id
        self.stop_name = stop_name
        self.stop_lat = stop_lat
        self.stop_lon = stop_lon


class Route:
    """Route, doesn't contain list of stops.

    Attributes:
        route_id:           Route ID.
        agency_id:          Agency ID.
        route_short_name:   Route's short name.
        route_long_name:    Route's long name.
        route_type:         Route type.
    """
    route_id: str
    agency_id: str
    route_short_name: str
    route_long_name: str
    route_type: str

    def __init__(self, route_id: str = "",
                 agency_id: str = "",
                 route_short_name: str = "",
                 route_long_name: str = "",
                 route_type: str = ""
                 ) -> None:
        """Constructor"""
        self.route_id = route_id
        self.agency_id = agency_id
        self.route_short_name = route_short_name
        self.route_long_name = route_long_name
        self.route_type = route_type


class StopTime:
    """Class representing time a particular trip arrives at a stop.
    
    Attributes:
        trip_id:                Trip ID.
        arrival_time:           Arrival time.
        departure_time:         Departure time.
        stop_id:                Stop ID.
        stop_sequence:          Stop Sequence.
        stop_headsign:          Stop Headsign.
        pickup_type:            Pickup type.
        drop_off_type:          Drop off type.
        shape_dist_traveled:    Shape distance travelled.
    """
    trip_id: str
    arrival_time: str
    departure_time: str
    stop_id: str
    stop_sequence: int
    stop_headsign: str
    pickup_type: str
    drop_off_type: str
    shape_dist_traveled: float

    def __init__(self, trip_id: str = "",
                 arrival_time: str = "",
                 departure_time: str = "",
                 stop_id: str = "",
                 stop_sequence: int = 0,
                 stop_headsign: str = "",
                 pickup_type: str = "",
                 drop_off_type: str = "",
                 shape_dist_traveled: float = 0) -> None:
        """Contructor"""
        self.trip_id = trip_id
        self.arrival_time = arrival_time
        self.departure_time = departure_time
        self.stop_id = stop_id
        self.stop_sequence = stop_sequence
        self.stop_headsign = stop_headsign
        self.pickup_type = pickup_type
        self.drop_off_type = drop_off_type
        self.shape_dist_traveled = shape_dist_traveled


class Trip:
    """Trip class, keeps track of related route, service, direction and shapes

    Attributes:
        route_id:       ID of route associated with trip.
        service_id:     ID of service associated with trip
        trip_id:        ID of trip
        shape_id:       ID of shape associated with trip
        trip_headsign:  Trip head sign
        direction_id:   ID of the direction of the trip
    """
    route_id: str
    service_id: str
    trip_id: str
    shape_id: str
    trip_headsign: str
    direction_id: str

    def __init__(self, route_id: str = "",
                 service_id: str = "",
                 trip_id: str = "",
                 shape_id: str = "",
                 trip_headsign: str = "",
                 direction_id: str = "") -> None:
        """Constructor"""
        self.route_id = route_id
        self.service_id = service_id
        self.trip_id = trip_id
        self.shape_id = shape_id
        self.trip_headsign = trip_headsign
        self.direction_id = direction_id


class Agency:
    """Class representing the agency which operates a service.
    
    Attributes:
        agency_id:          Agency id.
        agency_name:        Agency name.
        agency_url:         Agency url.
        agency_timezone:    Agency timezone.
        agency_lang:        Agency language.
        agency_phone:       Agency phone number.
    """
    agency_id: str
    agency_name: str
    agency_url: str
    agency_timezone: str
    agency_lang: str
    agency_phone: str

    def __init__(self, agency_id: str = "",
                 agency_name: str = "",
                 agency_url: str = "",
                 agency_timezone: str = "",
                 agency_lang: str = "",
                 agency_phone: str = "") -> None:
        """Constructor"""
        self.agency_id = agency_id
        self.agency_name = agency_name
        self.agency_url = agency_url
        self.agency_timezone = agency_timezone
        self.agency_lang = agency_lang
        self.agency_phone = agency_phone


def load_gtfs_from_file(filename: str, obj_type: T) -> List[T]:
    """Loads the GTFS data from a file into a list of a particular object type i.e. Stop
    
    Parameters:
        filename:   Name of the file should be csv format.
        obj_type:   Type of object should have constructor that takes no parameters.

    Throws:
        Exception:  When it encounters an error parsing csv file it logs it then throws exception.
        ValueError: When incorrect parameters are given.
    Returns:
        List of objects.
    """
    if filename is None or filename == "":
        raise ValueError("Filename must not be blank")
    if obj_type is None:
        raise ValueError("Must give a non None value for object type")
    try:
        results: List[T] = []
        with open(filename, 'r', encoding="utf-8-sig") as csvfile:
            for row in csv.DictReader(csvfile):
                inst: T = obj_type()
                inst.__dict__.update(row)
                results.append(inst)
        return results
    except Exception as err:
        logging.error(f"Encountered error when loading from file {err}")
        raise err


FILE_TO_OBJECT_MAPPINGS = {
    "stops.txt": Stop,
    "routes.txt": Route,
    "agency.txt": Agency,
    "stop_times.txt": StopTime,
    "trips.txt": Trip
}

FILE_TO_PARAMETER_NAME = {
    "stops.txt": "stops",
    "routes.txt": "routes",
    "agency.txt": "agency",
    "stop_times.txt": "stop_times",
    "trips.txt": "trips"
}