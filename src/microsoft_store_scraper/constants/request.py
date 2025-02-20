from abc import ABC, abstractmethod

MICROSOFT_STORE_BASE_URL = "https://apps.microsoft.com"


class Format(ABC):
    @abstractmethod
    def build(self, *args):
        raise NotImplementedError

    @abstractmethod
    def build_body(self, *args):
        raise NotImplementedError
    

class Formats:
    class _Detail(Format):
        URL_FORMAT = (
            "{}/detail/{{app_id}}/?hl={{lang}}&gl={{country}}".format(
                MICROSOFT_STORE_BASE_URL
            )
        )
        FALLBACK_URL_FORMAT = "{}/detail/{{app_id}}/?hl={{lang}}".format(
            MICROSOFT_STORE_BASE_URL
        )

        def build(self, app_id: str, lang: str, country: str) -> str:
            return self.URL_FORMAT.format(app_id=app_id, lang=lang, country=country)

        def fallback_build(self, app_id: str, lang: str) -> str:
            return self.FALLBACK_URL_FORMAT.format(app_id=app_id, lang=lang)

        def build_body(self, *args):
            return None
        

    class _Searchresults(Format):
        URL_FORMAT = (
            "{}/api/products/search?query={{query}}&mediaType={{media_type}}&age={{user_age}}&price={{price_type}}&category=all&subscription=all&hl={{lang}}&gl={{country}}".format(
                MICROSOFT_STORE_BASE_URL
            )
        )
        FALLBACK_URL_FORMAT = "{}/api/products/search?query={{query}}&mediaType={{media_type}}&age={{user_age}}&price={{price_type}}&category=all&subscription=all&hl={{lang}}".format(
            MICROSOFT_STORE_BASE_URL
        )

        def build(self, query: str, lang: str, country: str, media_type: str, user_age:str, price_type: str, cursor: str = None) -> str:
            if cursor:
                return self.URL_FORMAT.format(query=query, lang=lang, country=country, price_type=price_type, user_age=user_age, media_type=media_type) + f"&cursor={cursor}"
            return self.URL_FORMAT.format(query=query, lang=lang, country=country, price_type=price_type, user_age=user_age, media_type=media_type)

        def fallback_build(self, query: str, lang: str, media_type: str, user_age:str, price_type: str, cursor: str = None) -> str:
            if cursor:
                return self.URL_FORMAT.format(query=query, lang=lang, price_type=price_type, user_age=user_age, media_type=media_type) + f"&cursor={cursor}"
            return self.FALLBACK_URL_FORMAT.format(query=query, lang=lang, price_type=price_type, user_age=user_age, media_type=media_type)

        def build_body(self, *args):
            return None
        

    Detail = _Detail()
    Searchresults = _Searchresults()