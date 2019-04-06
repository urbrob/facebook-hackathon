import graphene
from collections import OrderedDict
from sourcecracker.types import ErrorType

NON_FIELD_ERRORS_FIELD = "nonFieldErrors"


def underscore_to_camel_case(key):
    """Convert underscore to camel case e.g. field_name to fieldName."""
    words = key.split("_")
    return "{}{}".format(words[0], "".join([word.title() for word in words[1:]]))


def format_error(err):
    """Join an error into one if iterable, otherwise displays it directly."""
    if hasattr(err, "__iter__"):
        return " / ".join(err)
    else:
        err


def errors_from_dict(errors, field=None):
    """Return a joined a dict of errors."""
    errors_dict = {}
    for key, err in errors:
        # Handle nested_serializer situation
        if isinstance(err, dict):
            # Fetch all errors from nested serializer
            nested_errors = [
                (underscore_to_camel_case(key_nes), err_nes)
                for key_nes, err_nes in err.items()
            ]
            # Create dict from errors in pattern: {'field': error, ...}
            nested_errors_fields = errors_from_dict(
                OrderedDict(nested_errors).items(), key
            )[1]
            # Append errors to main error_dict
            for key_field, err_field in nested_errors_fields.items():
                errors_dict[underscore_to_camel_case(key_field)] = err_field
        else:
            errors_dict[underscore_to_camel_case(key)] = format_error(err)

    # Extract non-field-errors message
    general_message = None
    if NON_FIELD_ERRORS_FIELD in errors_dict:
        # If non-field-error comes from nested_serializer, add it under the same name as nested_serializer belongs to
        if field is not None:
            errors_dict[underscore_to_camel_case(field)] = errors_dict.get(
                NON_FIELD_ERRORS_FIELD
            )
        else:
            general_message = errors_dict.get(NON_FIELD_ERRORS_FIELD)
        del errors_dict[NON_FIELD_ERRORS_FIELD]
    return general_message, (errors_dict if len(errors_dict) > 0 else None)


class MutationErrorMixin(object):
    """Error helper to use with graphene.Mutation."""

    errors = graphene.Field(ErrorType)

    @classmethod
    def error(cls, fields, **kwargs):
        """Return a mutation with an Error.
        Keyword arguments:
        fields      -- dict or OrderedDict of fields with errors, or string for a general message
        **kwargs    -- list of additional fields passed to the mutation class
        """
        field_errors = fields

        if isinstance(fields, str):
            formated_errors = None
            general_message = fields
        else:
            if isinstance(fields, OrderedDict):
                field_errors = fields.items()
            general_message, formated_errors = errors_from_dict(field_errors)

        return cls(
            errors=ErrorType(fields=formated_errors, message=general_message), **kwargs
        )
