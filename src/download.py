import io
import logging
from typing import Dict
import os
import requests
import zipfile

class DownloadService:
    """The purpose of this service is to allow for conditional download of certain files.
    It will store list of urls it has previously visited.

    Attributes:
        url_to_hash:    Dictionary mapping url to its most recent hashed content.
    """
    url_to_hash: Dict[str, int]

    def __init__(self) -> None:
        self.url_to_hash = {}

    def clear_dict(self):
        self.url_to_hash.clear()

    @staticmethod
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

    @staticmethod
    def get_GTFS_files(zip_url: str, directory: str = ".\\GTFS") -> bool:
        """Download and extract the GTFS files from a zip file at the
        specified url.

        Arguments:
            zip_url:    Url where the zipped folder is.
            directory:  Name of the directory to store extracted files in.

        Returns:
            A boolean, true if it was successful however if an error occurs
            it will return false.
        """
        zip_file = DownloadService.download_GTFS_zip(zip_url)
        if zip_file == None:
            return False
        logging.debug("Extracting zip file")
        zip_file.extractall(directory)
        logging.debug("Finished extracting zip file")
        zip_file.close()
        return True

    def get_if_diff(self, zip_url: str):
        """Get the Zip file from a given url but only if it is different to
        a previous download. It will get content from url, hash the content
        then compare it to a previous hash if it exists. If it has no previous hash
        or the hashes differ then it returns a zipfile.

        Arguments:
            zip_url:    Url where the zipped folder is.

        Returns:
            Zipfile if it differs otherwise None value
        
        Throws:
            Exception:  If the response returns a not OK result. 
        """
        resp = requests.get(zip_url, stream=True)
        if not resp.ok:
            error_str = f"Got invalid response {resp.status_code} from url {zip_url}"
            logging.error(error_str)
            raise Exception(error_str)
        original: int = None
        if zip_url in self.url_to_hash:
            original = self.url_to_hash[zip_url]
        new_hash = hash(resp.content)
        if new_hash == original:
            logging.info("No changes to content not redownloading it")
            return None
        self.url_to_hash[zip_url] = new_hash
        return zipfile.ZipFile(io.BytesIO(resp.content))

    def extract_if_diff(self, zip_url: str, directory: str = os.path.join(os.curdir, "GTFS")) -> bool:
        """Download and extract the GTFS files from a zip file at the
        specified url if download differs from previous download.

        Arguments:
            zip_url:    Url where the zipped folder is.
            directory:  Name of the directory to store extracted files in.
        Returns:
            A boolean, true if it was different and extracted into directory otherwise false
        """
        zip_file = self.get_if_diff(zip_url)
        if zip_file == None:
            logging.info("No difference between zips, not extracting")
            return False
        logging.debug("Extracting zip file")
        zip_file.extractall(directory)
        logging.debug("Finished extracting zip file")
        zip_file.close()
        return True