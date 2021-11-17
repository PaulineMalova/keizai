from marshmallow import Schema, fields, pre_load, post_load
from marshmallow.exceptions import ValidationError


class BaseSchema(Schema):
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    created_by = fields.Str(
        required=True, error_messages={"required": "Created by is required"}
    )
    updated_by = fields.Str(
        required=True, error_messages={"required": "Created by is required"}
    )
    is_active = fields.Bool(required=False)
    deleted_by = fields.Str(allow_none=True)
    deleted_at = fields.DateTime(allow_none=True)

    class Meta:
        model = None
        ordered = True
        unique_fields = None

    @classmethod
    @pre_load
    def pre_load(cls, data):
        """-."""
        for k, v in data.items():
            if isinstance(v, str):
                data[k] = v.strip()
        return data

    @post_load
    def load(self, data, many=None):
        """Load schema data using model."""
        # Infer many from the schema class if many is None
        many = self.many if many is None else bool(many)
        if self.Meta.model is None:
            raise ValidationError(
                "A schema must define a model attribute under Meta "
            )
        if many:
            if not isinstance(data, list):
                raise ValidationError(
                    "data must be a list of objects if many=True"
                )
            # pylint: disable=not-callable
            return [self.Meta.model(**item_data) for item_data in data]
        # pylint: disable=not-callable
        return self.Meta.model(**data)
