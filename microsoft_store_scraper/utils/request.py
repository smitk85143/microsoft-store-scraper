import ssl
from urllib.error import HTTPError
from urllib.request import urlopen

from microsoft_store_scraper.exceptions import ExtraHTTPError, NotFoundError

ssl._create_default_https_context = ssl._create_unverified_context

def _urlopen(obj):
    try:
        resp = urlopen(obj)
    except HTTPError as e:
        if e.code == 404:
            raise NotFoundError("App not found(404).")
        else:
            raise ExtraHTTPError(
                "App not found. Status code {} returned.".format(e.code)
            )

    return resp.read().decode("UTF-8")


def get(url: str) -> str:
    return _urlopen(url)