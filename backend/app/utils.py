DEFAULT_ENCODING = "utf-8"
import base64

DEFAULT_ENCODING = "utf-8"


def is_base64(s: str, encoding: str = DEFAULT_ENCODING) -> bool:
    """
    Check if a string is valid Base64.

    Args:
        s (str): The string to check.

    Returns:
        bool: True if the string is valid Base64, False otherwise.
    """
    try:
        # Decode and re-encode to verify Base64 validity
        return base64.b64encode(base64.b64decode(s)).decode(encoding=encoding) == s
    except Exception:
        return False


def to_base64(s: str, encoding: str = DEFAULT_ENCODING) -> str:
    """
    Convert a string to Base64.

    Args:
        s (str): The string to convert.
        encoding (str): The encoding to use. Defaults to 'utf-8'.

    Returns:
        str: The Base64 encoded string.
    """
    return base64.b64encode(s.encode(encoding=encoding)).decode(encoding=encoding)


def from_base64(s: str, encoding: str = DEFAULT_ENCODING) -> str:
    """
    Convert a Base64 string to its original form.

    Args:
        s (str): The Base64 string to convert.
        encoding (str): The encoding to use. Defaults to 'utf-8'.

    Returns:
        str: The decoded string.
    """
    return base64.b64decode(s.encode(encoding=encoding)).decode(encoding=encoding)
