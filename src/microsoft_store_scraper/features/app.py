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
    return parse_dom(dom=dom, app_id=app_id)


def parse_dom(dom: str, app_id: str) -> Dict[str, Any]:
    matches = Regex.SCRIPT.findall(dom)

    if matches:
        try:
            metadata_dict = json.loads(matches[0])
        except json.JSONDecodeError:
            raise NotFoundError("Failed to decode JSON from the app details.")
        metadata_dict['platform'] = "store"
        return metadata_dict
    
    matches = Regex.XBOX_SCRIPT.findall(dom)

    if matches:
        metadata_dict = json.loads(matches[0])
        upper_app_id = app_id.upper()
        result = {}
        result["productSummaries"] = metadata_dict.get('core2', {}).get('products', {}).get('productSummaries', {}).get(upper_app_id, {})
        result["additionalInformation"] = metadata_dict.get('core2', {}).get('products', {}).get('additionalInformation', {}).get(upper_app_id, {})
        result["availabilitySummaries"] = metadata_dict.get('core2', {}).get('products', {}).get('availabilitySummaries', {}).get(upper_app_id, {})
        result["skuSummaries"] = metadata_dict.get('core2', {}).get('products', {}).get('skuSummaries', {}).get(upper_app_id, {})
        result['platform'] = "xbox"

        return result

    else:
        raise NotFoundError("The app was not found.")