import re


class Regex:
    SCRIPT = re.compile(r"window\.pageMetadata\s*=\s*({.*?});", re.DOTALL)