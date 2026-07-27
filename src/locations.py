import re

US_COUNTRY_PATTERN = re.compile(
    r"\b("
    r"united states(?: of america)?|"
    r"usa|u\.s\.a\.|"
    r"us|u\.s\."
    r")\b",
    re.IGNORECASE,
)

US_STATE_NAMES_PATTERN = re.compile(
    r"\b("
    r"alabama|alaska|arizona|arkansas|california|colorado|"
    r"connecticut|delaware|florida|georgia|hawaii|idaho|"
    r"illinois|indiana|iowa|kansas|kentucky|louisiana|maine|"
    r"maryland|massachusetts|michigan|minnesota|mississippi|"
    r"missouri|montana|nebraska|nevada|new hampshire|"
    r"new jersey|new mexico|new york|north carolina|"
    r"north dakota|ohio|oklahoma|oregon|pennsylvania|"
    r"rhode island|south carolina|south dakota|tennessee|"
    r"texas|utah|vermont|virginia|washington|"
    r"west virginia|wisconsin|wyoming|district of columbia"
    r")\b",
    re.IGNORECASE,
)

US_STATE_CODES = {
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE",
    "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS",
    "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS",
    "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY",
    "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
    "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV",
    "WI", "WY", "DC",
}


def is_us_location(location: str) -> bool:
    if not location:
        return False

    if US_COUNTRY_PATTERN.search(location):
        return True

    if US_STATE_NAMES_PATTERN.search(location):
        return True

    location_parts = re.split(
        r"[,./|();:\-]+",
        location,
    )

    for part in location_parts:
        value = part.strip()

        if value.upper() in US_STATE_CODES:
            return True

        words = value.split()

        if words and words[-1].upper() in US_STATE_CODES:
            return True

    return False