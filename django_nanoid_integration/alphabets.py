# django_nanoid_integration/alphabets.py

"""
Predefined alphabets for NanoID generation in the django-nanoid-upload package.

This module provides various sets of characters categorized as safe and unsafe for use
in generating NanoID strings. It facilitates the creation of identifiers with specific
requirements or constraints.

Character sets are divided into uppercase and lowercase, further categorized as safe or unsafe.
Safe characters are those that minimize confusion (e.g., excluding similar-looking characters
like '1' and 'I' or '0' and 'O). The module also includes combined sets for easy reference and
an alphabet configuration dictionary that consolidates these sets for various use cases.

Constants:
    UPPERCASE_NUMBERS_SAFE (str): Safe uppercase numbers.
    UPPERCASE_NUMBERS_UNSAFE (str): Potentially confusing uppercase numbers.
    UPPERCASE_LETTERS_SAFE (str): Safe uppercase letters.
    UPPERCASE_LETTERS_UNSAFE (str): Potentially confusing uppercase letters.
    LOWERCASE_NUMBERS_SAFE (str): Safe lowercase numbers.
    LOWERCASE_NUMBERS_UNSAFE (str): Potentially confusing lowercase numbers.
    LOWERCASE_LETTERS_SAFE (str): Safe lowercase letters.
    LOWERCASE_LETTERS_UNSAFE (str): Potentially confusing lowercase letters.
    NUMBERS (str): All numbers.
    SAFE_NUMBERS (str): Combined safe numbers from uppercase and lowercase.
    SAFE_UPPERCASE (str): Safe uppercase letters.
    SAFE_LOWERCASE (str): Safe lowercase letters.
    UNSAFE_NUMBERS (str): Combined unsafe numbers from uppercase and lowercase.
    UNSAFE_UPPERCASE (str): Unsafe uppercase letters.
    UNSAFE_LOWERCASE (str): Unsafe lowercase letters.

    ALPHABET_CONFIG (dict): A dictionary of predefined alphabet configurations for various use cases.

Usage:
    Import the desired alphabet or use ALPHABET_CONFIG to get a predefined set:
    
    from django_nanoid_integration.alphabets import ALPHABET_CONFIG
    safe_alphabet = ALPHABET_CONFIG['safe']
"""


# UPPERCASE
UPPERCASE_NUMBERS_SAFE = "34679"
UPPERCASE_NUMBERS_UNSAFE = "01258"
UPPERCASE_LETTERS_SAFE = "ACDEFGHKLMNPRTUVWXY"
UPPERCASE_LETTERS_UNSAFE = "BIJOQSZ"

# LOWERCASE
LOWERCASE_NUMBERS_SAFE = "347"
LOWERCASE_NUMBERS_UNSAFE = "0125689"
LOWERCASE_LETTERS_SAFE = "acdefhjkmnprtuvwxy"
LOWERCASE_LETTERS_UNSAFE = "bgiloqsz"

# NUMBERS
NUMBERS = "0123456789"

# Combine safe characters for easy reference
SAFE_NUMBERS = UPPERCASE_NUMBERS_SAFE + LOWERCASE_NUMBERS_SAFE
SAFE_UPPERCASE = UPPERCASE_LETTERS_SAFE
SAFE_LOWERCASE = LOWERCASE_LETTERS_SAFE

# Combine unsafe characters for reference
UNSAFE_NUMBERS = UPPERCASE_NUMBERS_UNSAFE + LOWERCASE_NUMBERS_UNSAFE
UNSAFE_UPPERCASE = UPPERCASE_LETTERS_UNSAFE
UNSAFE_LOWERCASE = LOWERCASE_LETTERS_UNSAFE


# ALPHABET CONFIGURATION
ALPHABET_CONFIG = {
    "safe": SAFE_UPPERCASE + SAFE_LOWERCASE + LOWERCASE_NUMBERS_SAFE,
    "unsafe": SAFE_NUMBERS + UNSAFE_NUMBERS + SAFE_UPPERCASE + UNSAFE_UPPERCASE + SAFE_LOWERCASE + UNSAFE_LOWERCASE,
    "numbers": NUMBERS,
    "safe_letters": SAFE_UPPERCASE + SAFE_LOWERCASE,
    "safe_letters_uppercase": SAFE_UPPERCASE,
    "safe_letters_lowercase": SAFE_LOWERCASE,
    "safe_letters_uppercase_and_numbers": SAFE_UPPERCASE + UPPERCASE_NUMBERS_SAFE,
    "safe_letters_lowercase_and_numbers": SAFE_LOWERCASE + LOWERCASE_NUMBERS_SAFE,   
}
