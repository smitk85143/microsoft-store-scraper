import json
from typing import Any, Dict, List
from urllib.parse import quote

from microsoft_store_scraper.constants.request import Formats
from microsoft_store_scraper.exceptions import NotFoundError
from microsoft_store_scraper.utils.request import get

def search(
    query: str, n_hits: int = 20, lang: str = "en-us", country: str = "US"
) -> List[Dict[str, Any]]:
    
    if n_hits <= 0:
        return []

    query = quote(query)
    cursor = None
    data = []
    while True:

        url = Formats.Searchresults.build(query=query, lang=lang, country=country, cursor=cursor)
        try:
            dom = get(url)
        except NotFoundError:
            url = Formats.Searchresults.fallback_build(query=query, lang=lang, cursor=cursor)
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