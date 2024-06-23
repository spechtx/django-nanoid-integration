# django_nanoid_integration/upload.py

"""
NanoID Upload Handling

Provides functions and utilities for handling file uploads
using NanoID for generating unique filenames.
Inspired by [Ilya Semenov's django-uuid-upload](https://github.com/IlyaSemenov/django-uuid-upload)
"""

# Standard library imports
import os
import re
import functools

# Django imports
from django.conf import settings
from django.core.files.storage import default_storage

# Third-party imports
from nanoid import generate

# Local application imports
from .helpers import get_alphabet_characters

# Configure logging
import logging
logging.basicConfig(level=logging.DEBUG)



def upload_to_nanoid(
    path: str,
    preserve_original_filename: bool = False,
    remove_query_strings: bool = True,
    alphabet: str = getattr(settings, 'NANOID_ALPHABET', None),
    alphabet_predefined: str = getattr(settings, 'NANOID_ALPHABET_PREDEFINED', None),
    size: int = getattr(settings, 'NANOID_SIZE', 5)
) -> callable:
    """
    Returns a callable function that generates a unique file path using a NanoID.

    This function is intended to be used as the `upload_to` parameter in Django model fields
    to generate unique file names for uploads, improving file organization.

    Args:
        path (str): The base path where the file will be uploaded.
        preserve_original_filename (bool): If True, the original filename is preserved in a subdirectory.
        remove_query_strings (bool): If True, query strings are removed from the filename.
        alphabet (str): Custom alphabet to use for generating the NanoID. If None, uses the default.
        alphabet_predefined (str): Predefined alphabet to use. If None, uses the custom alphabet or default.
        size (int): The length of the NanoID.

    Returns:
        callable: A function that generates a unique file path with a NanoID.
    """

    # Use functools.partial to create a callable function with the specified parameters
    return functools.partial(
        _upload_to_nanoid_impl,
        path=path,
        preserve_original_filename=preserve_original_filename,
        remove_query_strings=remove_query_strings,
        alphabet=alphabet,
        alphabet_predefined=alphabet_predefined,
        size=size
    )

def _upload_to_nanoid_impl(
    instance,
    filename,
    path,
    preserve_original_filename,
    remove_query_strings,
    alphabet,
    alphabet_predefined,
    size
) -> str:
    """
    Generates a unique file path using a NanoID, with options for subdirectory creation and query string removal.
    
    This is the implementation function called by `upload_to_nanoid`.

    Args:
        instance: The model instance that the file is being attached to.
        filename (str): The original filename of the uploaded file.
        path (str): The base directory where files will be uploaded.
        preserve_original_filename (bool): Whether to create a subdirectory with the NanoID and keep the original filename.
        remove_query_strings (bool): Whether to remove query strings from the filename.
        alphabet (str): Custom alphabet to use for generating the NanoID.
        alphabet_predefined (str): Predefined alphabet to use for generating the NanoID.
        size (int): The length of the NanoID.
    
    Returns:
        str: A unique file path.

    Raises:
        ValueError: If a unique NanoID cannot be generated after 10 attempts.
    """

    # Remove query strings from the filename if required
    if remove_query_strings:
        filename = re.sub(r'\?.*', '', filename)

    attempts = 0
    while attempts < 10:
        # Generate a NanoID
        nanoid = generate(get_alphabet_characters(alphabet, alphabet_predefined), size)

        # Construct the unique file path
        if preserve_original_filename:
            sanitized_filename = filename.replace(' ', '_')
            unique_path = os.path.join(path, nanoid, sanitized_filename)
        else:
            ext = os.path.splitext(filename)[-1].lower()
            unique_path = os.path.join(path, nanoid + ext)

        # Check if the file path is unique within the storage
        if not default_storage.exists(unique_path):
            return unique_path

        attempts += 1
        logging.debug("NanoID '%s' is already taken for the filename '%s'. Attempting to generate another NanoID.", nanoid, filename)

    logging.debug("NanoID '%s' is already taken for the filename '%s'. Giving up.", nanoid, filename)
    raise ValueError(
        f"No unique NanoID could be generated for the filename '{filename}'. "
        "To resolve this issue, consider increasing the NanoID size in your model's field definition using a different alphabet to improve uniqueness. "
        "Run the following commands to apply the changes: 'python manage.py makemigrations' and then 'python manage.py migrate'."
    )
