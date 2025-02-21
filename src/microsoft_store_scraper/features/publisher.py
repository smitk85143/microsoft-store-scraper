import json
from typing import Any, Dict

from microsoft_store_scraper.constants.request import Formats
from microsoft_store_scraper.exceptions import NotFoundError
from microsoft_store_scraper.utils.request import get

def publisher(publisher_name: str, lang: str = "en-us", country: str = "US") -> Dict[str, Any]:
    """
    Get the publisher details based on the publisher name.

    :param publisher_name: The publisher name.
    :param lang: The language.
    :param country: The country.

    :return: The publisher details.

    """
    publisher_name = publisher_name.replace(" ", "+")
    cursor = None
    data = []
    while True:

        url = Formats.PublisherResults.build(publisher_name=publisher_name, lang=lang, country=country, cursor=cursor)
        try:
            dom = get(url)
        except NotFoundError:
            url = Formats.PublisherResults.fallback_build(publisher_name=publisher_name, lang=lang, cursor=cursor)
            dom = get(url)
        dom_data = json.loads(dom)
        data += dom_data['productsList']
        cursor = dom_data['cursor']
        if cursor is None:
            break
    return data