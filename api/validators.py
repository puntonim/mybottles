"""
Validators to be used in DJRF serializers and in Django db models.

These validators should be typically used to validate a model in 3 spots:
- DJRF api model serializer
- db model full_clean(): that's the validation for Model and Django Admin forms
- db model save(): that's a forced validation for an obj.save()
"""


def validate_purchase(data, validation_error_class):
    if data.get('is_gift') and data.get('store'):
        raise validation_error_class(dict(store='Store must be empty if it is a gift.'))
    if not data.get('is_gift') and not data.get('store'):
        raise validation_error_class(dict(store='Store is required if is not a gift.'))
    return data
