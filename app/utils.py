import random
import string

from sqlalchemy.sql.expression import ClauseElement

from app.exceptions import ValidationFailed


def number_id_generator(
    session, model, column_name, size=6, chars=string.digits[1:]
):
    random_number = "".join(
        random.SystemRandom().choice(chars) for _ in range(size)
    )
    column = getattr(model, column_name, None)
    number_ex = session.query(model).filter(column == random_number).first()
    if number_ex:
        return number_id_generator(session, model, column_name)
    return random_number


def get_or_create(session, model, schema, data):
    """Get an existing model or create a new one if it does not exist."""
    kwargs = {}
    unique_fields = schema.Meta.unique_fields

    instance = None
    if unique_fields is not None and isinstance(unique_fields, (list, tuple)):
        for field in unique_fields:
            field_value = data.get(field)
            if field_value is not None:
                kwargs[field] = field_value

        query = session.query(model)

        # Filter only if kwargs is not empty
        if kwargs:
            query = query.filter_by(**kwargs)
            instance = query.first()

        if instance is not None:
            return False, instance

    params = dict(
        (k, v) for k, v in data.items() if not isinstance(v, ClauseElement)
    )
    instance = load_schema(schema, params)
    instance.save(session)
    return True, instance


def load_schema(schema, data, many=None):
    """Load schema data using model."""
    # Infer many from the schema class if many is None
    many = many if many is None else bool(many)
    if schema.Meta.model is None:
        raise ValidationFailed(
            "A schema must define a model attribute under Meta "
        )
    if many:
        if not isinstance(data, list):
            raise ValidationFailed(
                "data must be a list of objects if many=True"
            )
        # pylint: disable=not-callable
        return [schema.Meta.model(**item_data) for item_data in data]
    # pylint: disable=not-callable
    return schema.Meta.model(**data)
