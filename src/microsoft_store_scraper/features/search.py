import json
from typing import Any, Dict, List
from urllib.parse import quote

from microsoft_store_scraper.constants.request import Formats
from microsoft_store_scraper.exceptions import NotFoundError
from microsoft_store_scraper.utils.request import get

def search(
    query: str, n_hits: int = 20, lang: str = "en-us", country: str = "US", price_type: str = "all", user_age: str = "all", media_type: str = "all"
) -> List[Dict[str, Any]]:
    """
    Search for apps based on the query.

    :param query: The search query.
    :param n_hits: The number of hits.
    :param lang: The language.
    :param country: The country.
    :param price_type: The price type. Possible values: all, Free, Paid, Sale
    :param user_age: The user age. Possible values: all, TO3, TO4, TO5, TO6, TO7, TO8, TO9, TO10, TO11, TO12, TO13, TO14, TO15, TO16, TO17
    :param media_type: The media type. Possible values: all, apps, games, movies, devices, passes, fonts, themes

    :return: The search results.
    """
    
    if n_hits <= 0:
        return []

    query = quote(query)
    cursor = None
    data = []
    while True:

        url = Formats.Searchresults.build(query=query, lang=lang, country=country, cursor=cursor, price_type=price_type, user_age=user_age, media_type=media_type)
        try:
            dom = get(url)
        except NotFoundError:
            url = Formats.Searchresults.fallback_build(query=query, lang=lang, cursor=cursor, price_type=price_type, user_age=user_age, media_type=media_type)
            dom = get(url)
        dom_data = json.loads(dom)
        data += dom_data['productsList']
        if n_hits <= len(data):
            data = data[:n_hits]
            break
        cursor = dom_data['cursor']
        if cursor is None:
            break
    return data