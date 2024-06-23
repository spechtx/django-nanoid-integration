# django_nanoid_integration/helpers.py

"""
HELPER FUNCTIONS
"""

# Local application imports
from .alphabets import ALPHABET_CONFIG

def get_alphabet_characters(alphabet: str = None, alphabet_predefined: str = None) -> str:
    """
    Determine the alphabet characters to use for NanoID generation.

    This function selects the appropriate alphabet based on the provided parameters.
    It prioritizes a custom alphabet if provided, then a predefined alphabet,
    and finally defaults to the 'safe' alphabet.

    Args:
        alphabet (str, optional): A custom alphabet string to use. Defaults to None.
        alphabet_predefined (str, optional): The name of a predefined alphabet to use. Defaults to None.

    Returns:
        str: The selected alphabet characters to use for NanoID generation.

    Raises:
        ValueError: If the specified predefined alphabet does not exist in ALPHABET_CONFIG.

    Examples:
        >>> get_alphabet_characters(alphabet="ABC123")
        'ABC123'
        >>> get_alphabet_characters(alphabet_predefined="numbers")
        '0123456789'
        >>> get_alphabet_characters()
        '347ACDEFGHKLMNPRTUVWXYacdefhjkmnprtuvwxy'
    """
    # Use the custom alphabet if provided
    if alphabet:
        return alphabet
    else:
        # If not, use the predefined alphabet (if provided and valid)
        if alphabet_predefined:
            if alphabet_predefined in ALPHABET_CONFIG:
                return ALPHABET_CONFIG[alphabet_predefined]
            else:
                raise ValueError(
                    f"Predefined alphabet '{alphabet_predefined}' does not exist. Please choose a valid predefined alphabet.")
        else:
            # Default to 'safe' alphabet if neither is provided
            return ALPHABET_CONFIG['safe']
