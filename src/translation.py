from typing import Any, Dict, List, TypeVar
from .gtfs import *

T = TypeVar('T')


def group_by(field: str, obj_list: List[T]) -> Dict[str, List[T]]:
    """Group a list of objects by a field's value.
    
    Arguments:
        field:      Field with values we are grouping by.
        obj_list:   List of objects to group.

    Returns:
        Mapping of field value to list of objects with value for that field.
    """
    result: Dict[str, List[T]] = {}
    for obj in obj_list:
        if field not in obj.__dict__:
            logging.warning(f"Field not found in obj {type(obj)}")
            continue
        value: str = obj.__dict__[field]
        if value not in result:
            result[value] = []
        result[value].append(obj)
    return result


def connect_route_stops(routes: List[Route], stop_times: List[StopTime],
                        trips: List[Trip]):
    """Connect trip stops to the route they are associated with.

    Parameters:
        routes:         List of routes.
        stop_times:     List of stop times.
        trips:          List of trips.

    Returns:
        List with mappings of route to a given  trip_stops
        in format {"stops": trip_stops, "route": route} .
    """
    results = []
    route_ids = group_by("route_id", routes)
    times_by_trip_id = group_by("trip_id", stop_times)
    for trip in trips:
        trip_stops = [x.__dict__ for x in times_by_trip_id[trip.trip_id]]
        route_list = [x.__dict__ for x in route_ids[trip.route_id]]
        if len(route_list) > 1:
            logging.warning(f"route list for trip {trip} is bigger than 1")
        results.append({"stops": trip_stops, "route": route_list[0]})
    return results
