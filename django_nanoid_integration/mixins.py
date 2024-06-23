# django_nanoid_integration/mixins.py

"""
Mixins for NanoID Fields
"""

# Django Imports
from django.db import models, transaction
from django.db.utils import IntegrityError

# Logging
import logging

logging.basicConfig(level=logging.DEBUG)


class UniqueNanoIDMixin(models.Model):
    """
    Mixin to ensure unique NanoIDs for fields in a Django model.

    This mixin provides functionality to generate and manage unique NanoID fields
    in Django models. It handles the generation of unique NanoIDs, ensures their
    uniqueness, and provides methods for regenerating NanoIDs.

    Attributes:
        nanoid_max_attempts (int): The maximum number of attempts to generate a unique NanoID.

    Note:
        This is an abstract base class and should be used as a mixin in other models.
    """

    # UniqueNanoIDMixin inherits from models.Model.
    # This ensures that it has access to all the necessary model methods and attributes.

    nanoid_max_attempts = 10

    class Meta:
        """
        Make this an abstract base class.
        This prevents Django from creating a database table for the mixin itself.
        """

        abstract = True

    def get_unique_nanoid_fields(self):
        """
        Retrieve a list of fields that have unique=True and are instances of NanoIDField.

        Returns:
            list: List of field names with unique=True and instances of NanoIDField.
        """
        return [
            field.name
            for field in self._meta.get_fields()
            if hasattr(field, "unique") and field.unique and hasattr(field, "nanoid")
        ]

    def get_all_nanoid_fields(self):
        """
        Retrieve a list of all fields that are instances of NanoIDField.

        Returns:
            list: List of field names of NanoIDField instances.
        """
        return [
            field.name for field in self._meta.get_fields() if hasattr(field, "nanoid")
        ]

    def ensure_unique_nanoids(self):
        """
        Ensure unique NanoIDs for fields specified as unique NanoID fields in the model.

        This method generates and assigns unique NanoIDs to fields that require them.
        It retrieves the fields marked for unique NanoID generation and attempts to generate
        a unique NanoID for each. If a field already has a NanoID or if the record is being updated,
        it will check for the uniqueness of the NanoID. If the NanoID is not unique, it will
        attempt to generate a new one up to a maximum number of attempts.

        Raises:
            ValueError: If a unique NanoID cannot be generated within the max. number of attempts.
        """

        unique_nanoid_fields = self.get_unique_nanoid_fields()
        fields_to_generate = []

        for field_name in unique_nanoid_fields:
            field_instance = self._meta.get_field(field_name)
            field_value = getattr(self, field_name)

            if field_value is None:
                fields_to_generate.append((field_name, field_instance))
            elif not self.pk:  # Only check existence for new records
                if type(self).objects.filter(**{field_name: field_value}).exists():
                    fields_to_generate.append((field_name, field_instance))

        for field_name, field_instance in fields_to_generate:
            for _ in range(self.nanoid_max_attempts):
                field_value_new = field_instance.nanoid()
                if (
                    not type(self)
                    .objects.filter(**{field_name: field_value_new})
                    .exists()
                ):
                    setattr(self, field_name, field_value_new)
                    logging.debug(
                        "Successfully set unique NanoID '%s' for field '%s'.",
                        field_value_new,
                        field_instance,
                    )
                    break

                logging.debug(
                    "NanoID '%s' is already taken in the field '%s'. Attempting to generate another NanoID.",
                    field_value_new,
                    field_instance,
                )
            else:
                logging.debug(
                    "NanoID '%s' is already taken in the field '%s'. Giving up.",
                    field_value_new,
                    field_instance,
                )
                raise ValueError(
                    f"No unique NanoID could be generated for the field '{field_name}'. The current NanoID size is {field_instance.size}. "
                    "To resolve this issue, consider increasing the NanoID size in your model's field definition or using a different alphabet to improve uniqueness. "
                    "Run the following commands to apply the changes: 'python manage.py makemigrations' and then 'python manage.py migrate'."
                )

    def save(self, *args, **kwargs):
        """
        Override the save method to ensure unique NanoIDs before saving.

        This method wraps the save operation in a transaction and handles potential
        IntegrityErrors by retrying with a new NanoID.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        with transaction.atomic():
            try:
                self.ensure_unique_nanoids()
                super().save(*args, **kwargs)
            except IntegrityError:
                # If an IntegrityError occurs, retry with a new NanoID
                self.ensure_unique_nanoids()
                super().save(*args, **kwargs)

    def regenerate_nanoid(self, field_name, force=False):
        """
        Regenerate the NanoID for a specified field.

        This method can be used for both unique and non-unique NanoID fields,
        but not for the primary key. It also updates any reverse relations.

        Args:
            field_name (str): The name of the field to regenerate.
            force (bool): If True, skips the safety confirmation (for operator use only).

        Returns:
            self: The updated instance.

        Raises:
            ValueError: If the field is not a NanoID field or if it's the primary key.
            UserWarning: If the user doesn't confirm the operation when force is False.
        """
        if field_name not in self.get_all_nanoid_fields():
            raise ValueError(f"'{field_name}' is not a NanoID field.")

        if field_name == self._meta.pk.name:
            raise ValueError(
                "Cannot regenerate the primary key field."
            )

        if not force:
            confirmation = input(
                "WARNING: The current implementation doesn't update foreign key relations, which could lead to data integrity issues.\n"
                "Are you sure you want to proceed? Type 'y' to confirm: "
            )
            if confirmation.lower() != "y":
                raise UserWarning("Operation cancelled by the user.")

        field_instance = self._meta.get_field(field_name)
        old_value = getattr(self, field_name)

        with transaction.atomic():
            if field_instance.unique:
                setattr(
                    self, field_name, None
                )  # This will force a new unique NanoID to be generated
                self.save(force_update=True)
            else:
                # For non-unique fields, we can simply generate a new NanoID
                new_value = field_instance.nanoid()
                setattr(self, field_name, new_value)
                self.save(update_fields=[field_name])

            new_value = getattr(self, field_name)

            # Update any reverse relations
            for related_object in self._meta.related_objects:
                if (
                    related_object.field.related_model == self.__class__
                    and related_object.field.to_fields[0] == field_name
                ):
                    related_model = related_object.related_model
                    filter_kwargs = {
                        f"{related_object.field.name}__{field_name}": old_value
                    }
                    update_kwargs = {related_object.field.name: self}
                    related_model.objects.filter(**filter_kwargs).update(
                        **update_kwargs
                    )

        logging.debug(
            "Regenerated NanoID for field '%s'. Old value: '%s', New value: '%s'",
            field_instance,
            old_value,
            new_value,
        )

        return self
