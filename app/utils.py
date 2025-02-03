from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta
import re


executor = ThreadPoolExecutor(max_workers=5)


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


def get_file_type(mime_type: str) -> str:
    """
    Get the file type based on the MIME content type.

    Args:
        - mime_type (str): MIME type to get the content type for.

    Returns:
        - str: Content type based on the MIME type.
    """
    # Define supported MIME types
    supported_types = {
        "application/pdf": "pdf",
        # "application/msword": "doc",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx",
        # "application/vnd.ms-excel": "xls",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "xlsx",
        "text/html": "html",
    }
    if mime_type not in supported_types:
        raise ValueError(f"Unsupported MIME type: {mime_type}")
    return supported_types[mime_type]
