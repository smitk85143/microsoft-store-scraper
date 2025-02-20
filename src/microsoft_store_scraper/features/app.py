import json
from typing import Any, Dict

from microsoft_store_scraper.constants.regex import Regex
from microsoft_store_scraper.constants.request import Formats
from microsoft_store_scraper.exceptions import NotFoundError
from microsoft_store_scraper.utils.request import get


def app(app_id: str, lang: str = "en-us", country: str = "US") -> Dict[str, Any]:
    """
    Get the app details based on the app id.

    :param app_id: The app id.
    :param lang: The language.
    :param country: The country.

    :return: The app details.

    """
    url = Formats.Detail.build(app_id=app_id, lang=lang, country=country)

    try:
        dom = get(url)
    except NotFoundError:
        url = Formats.Detail.fallback_build(app_id=app_id, lang=lang)
        dom = get(url)
    return parse_dom(dom=dom, app_id=app_id, url=url)


def parse_dom(dom: str, app_id: str, url: str) -> Dict[str, Any]:
    
    matches = Regex.SCRIPT.findall(dom)

    if matches:
        metadata_dict = json.loads(matches[0])
        metadata_dict["appId"] = app_id
        metadata_dict["url"] = url

        return metadata_dict
    else:
        raise NotFoundError("The app was not found.")