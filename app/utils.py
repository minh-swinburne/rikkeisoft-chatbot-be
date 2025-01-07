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
