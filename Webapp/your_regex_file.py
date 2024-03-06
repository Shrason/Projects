import re

def regex(input_string, pattern):
    """
    Searches for occurrences of the specified pattern in the input string.

    Args:
        input_string (str): The string to search within.
        pattern (str): The regular expression pattern to match.

    Returns:
        list: A list of matched substrings.
    """

    compiled_pattern = re.compile(pattern)
    matches = compiled_pattern.findall(input_string)

    return matches
