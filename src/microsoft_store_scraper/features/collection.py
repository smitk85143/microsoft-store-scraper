import json
from typing import Any, Dict

from microsoft_store_scraper.constants.request import Formats
from microsoft_store_scraper.exceptions import NotFoundError
from microsoft_store_scraper.utils.request import get

def collection(list_name: str, media_type: str, n_hits: int = 24, lang: str = "en-us", country: str = "US") -> Dict[str, Any]:
    """
    Get the publisher details based on the publisher name.

    :param list_name: The list name. Possible Values: TopFree, TopPaid, bestRated, deal, newAndRising, TopGrossing, mostPopular, Recommendedforcohort
    :param media_type: The media type. Possible Values: apps, games
    :param lang: The language.
    :param country: The country.

    :return: The publisher details.

    """
    if n_hits <= 0:
        return []
    data = []
    pg_no = 1
    while True:

        url = Formats.Collectionresults.build(list_name=list_name, media_type=media_type, lang=lang, country=country, pg_no=pg_no)
        try:
            dom = get(url)
        except NotFoundError:
            url = Formats.Collectionresults.fallback_build(list_name=list_name, media_type=media_type, lang=lang, pg_no=pg_no)
            dom = get(url)
        dom_data = json.loads(dom)
        data += dom_data['productsList']
        if n_hits <= len(data):
            data = data[:n_hits]
            break
        if not dom_data['hasMorePages']:
            break
        pg_no = dom_data['nextPageNumber']
    return data