# django_nanoid_integration/__init__.py

"""
django_nanoid_integration

A Django package for integrating NanoID functionality, providing custom fields,
upload utilities, and mixins for unique ID generation.

This package includes:
- NanoIDField: A custom Django field for NanoID generation
- upload_to_nanoid: A utility function for NanoID-based file uploads
- UniqueNanoIDMixin: A mixin for ensuring unique NanoIDs in Django models
"""

from importlib.metadata import version, PackageNotFoundError
from typing import List

from .upload import upload_to_nanoid
from .fields import NanoIDField
from .mixins import UniqueNanoIDMixin

try:
    __version__: str = version("django-nanoid-integration")
except PackageNotFoundError:
    __version__: str = "0.1.0"

__all__: List[str] = [
    "upload_to_nanoid",
    "NanoIDField",
    "UniqueNanoIDMixin"
]

__author__: str = "Christian H. Specht"
__license__: str = "MIT"
