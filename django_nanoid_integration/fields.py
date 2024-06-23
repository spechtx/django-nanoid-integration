# django_nanoid_integration/fields.py

"""
NanoID Field for Django

Provides functions and utilities for handling NanoID Fields.
Inspired by [Gökhan Öztürk's django-nanoid-field](https://github.com/goztrk/django-nanoid-field)
"""

# Django imports
from django.conf import settings
from django.db import models

# Third-party imports
from nanoid import generate

# Local application imports
from .helpers import get_alphabet_characters


class NanoIDField(models.CharField):
    """
    Custom Django field for generating and storing NanoID strings.

    This field extends Django's CharField to provide automatic generation
    of NanoID strings. It allows customization of the alphabet and size
    of the generated NanoIDs.

    Attributes:
        alphabet (str): Custom alphabet to use for NanoID generation.
        alphabet_predefined (str): Name of a predefined alphabet to use.
        size (int): Length of the NanoID to generate.

    Args:
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.
            - alphabet (str, optional): Custom alphabet for NanoID generation.
            - alphabet_predefined (str, optional): Name of predefined alphabet.
            - size (int, optional): Length of NanoID. Defaults to settings.NANOID_SIZE or 5.
            - editable (bool, optional): Whether the field is editable. Defaults to False.
            - unique (bool, optional): Whether the field should be unique. Defaults to True.
    """

    def __init__(self, *args, **kwargs) -> None:
        """
        Initialize the NanoIDField with custom settings.

        Sets up the field with the specified alphabet, size, and other
        CharField properties.
        """

        self.alphabet = kwargs.pop("alphabet", None)

        if self.alphabet:
            self.alphabet_predefined = kwargs.pop("alphabet_predefined", None)
        else:
            self.alphabet_predefined = kwargs.pop("alphabet_predefined", 'safe')

        self.size = kwargs.pop(
            "size", getattr(settings, 'NANOID_SIZE', 5)
        )

        # CharField required
        kwargs["max_length"] = self.size
        kwargs["default"] = None

        # Editable and unique properties
        editable = kwargs.pop("editable", False)
        kwargs["editable"] = editable

        unique = kwargs.pop("unique", True)
        kwargs["unique"] = unique

        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        """
        Generate a NanoID if the field value is None before saving.

        Args:
            model_instance: The model instance being saved.
            add (bool): Whether this is a new instance.

        Returns:
            str: The current value of the field or a newly generated NanoID.
        """        
        value = getattr(model_instance, self.attname)
        if value is None:
            value = self.nanoid()
            setattr(model_instance, self.attname, value)
        return value

    def nanoid(self):
        """
        Generate a NanoID using the specified alphabet and size.

        Returns:
            str: A newly generated NanoID.
        """
        return generate(get_alphabet_characters(
            self.alphabet,
            self.alphabet_predefined
        ), self.size)

    def get_internal_type(self):
        """
        Return the internal Django field type.

        Returns:
            str: Always returns "CharField".
        """
        return "CharField"

    def deconstruct(self):
        """
        Deconstruct the field for Django migrations.

        Returns:
            tuple: A tuple containing the field's name, path, args, and kwargs.
        """
        name, path, args, kwargs = super().deconstruct()
        kwargs['alphabet'] = self.alphabet
        kwargs['alphabet_predefined'] = self.alphabet_predefined
        kwargs['size'] = self.size
        kwargs["editable"] = self.editable
        kwargs["unique"] = self.unique
        kwargs['max_length'] = self.max_length
        kwargs.pop('default', None)

        return name, path, args, kwargs
