class MicrosoftScraperException(Exception):
    pass


class NotFoundError(MicrosoftScraperException):
    pass


class ExtraHTTPError(MicrosoftScraperException):
    pass