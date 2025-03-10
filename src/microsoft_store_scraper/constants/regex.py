import re


class Regex:
    SCRIPT = re.compile(r"window\.pageMetadata\s*=\s*({.*?});", re.DOTALL)
    XBOX_SCRIPT = re.compile(r"window\.__PRELOADED_STATE__\s*=\s*({.*?});", re.DOTALL)