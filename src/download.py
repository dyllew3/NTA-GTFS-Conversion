import io
import logging
from xmlrpc.client import boolean
import requests
import zipfile

def download_GTFS_zip(zip_url: str):
    """Download a GTFS zip file at the specified url.

    Arguments:
        zip_url:    Url where the zipped folder is.
    Returns:
        Zipfile or None if unable to retrieve the zip file.
    """
    resp = requests.get(zip_url, stream=True)
    if not resp.ok:
        logging.error(f"Got invalid response {resp.status_code} from url {zip_url}")
        return None
    return zipfile.ZipFile(io.BytesIO(resp.content))

def get_GTFS_files(zip_url: str, directory: str = ".\\GTFS") -> str:
    """Download and extract the GTFS files from a zip file at the
    specified url.

    Arguments:
        zip_url:    Url where the zipped folder is.
        directory:  Name of the directory to store extracted files in.

    Returns:
        A string with where the folder is however if an error occurs
        it will return an empty string
    """
    zip_file = download_GTFS_zip(zip_url)
    if zip_file == None:
        return ""
    logging.debug("Extracting zip file")
    zip_file.extractall(directory)
    logging.debug("Finished extracting zip file")
    zip_file.close()
    return directory
