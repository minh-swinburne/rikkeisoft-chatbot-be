from datetime import timedelta
import re


def extract_content(
    regex: str, text: str, flag: re.RegexFlag = re.MULTILINE
) -> list[str]:
    """
    Extracts content from a text using a regular expression.

    Args:
        - regex (str): Regular expression pattern to match and extract content.
        - text (str): Text to extract content from.
        - flag (re.RegexFlag): Regex flag to enable additional matching modes.

    Returns:
        - list[str]: List of extracted content from the text.
    """
    return re.findall(regex, text, flag)


def parse_timedelta(time_str: str):
    """
    Parse a time string into a timedelta object.

    Args:
        time_str (str): Time string to parse.

    Returns:
        timedelta: Parsed timedelta object.
    """
    # Regex to match numbers followed by 'd', 'h', 'm' (days, hours, minutes)
    match = re.match(r"(\d+)([dhm])", time_str)

    if not match:
        raise ValueError(f"Invalid time format: {time_str}")

    quantity, unit = match.groups()
    quantity = int(quantity)

    # Convert based on unit
    if unit == "d":  # days
        return timedelta(days=quantity)
    elif unit == "h":  # hours
        return timedelta(hours=quantity)
    elif unit == "m":  # minutes
        return timedelta(minutes=quantity)
    else:
        raise ValueError(f"Unsupported unit: {unit}")
