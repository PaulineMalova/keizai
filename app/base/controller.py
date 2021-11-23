import json

from fastapi.encoders import jsonable_encoder
from fastapi import status, HTTPException

from app.utils import get_or_create


class BaseController:
    model = None
    schema = None
    hide_fields = None

    @classmethod
    def get_json_compatible_data(cls, item):
        data = jsonable_encoder(item)
        return data

    @classmethod
    def as_view(cls, session, request, item=None, pk=None, response=None):
        user_id = request.headers.get("Userid", "Unknown")

        if request.method == "POST":
            data = cls.get_json_compatible_data(item)
            data["created_by"] = user_id
            data["updated_by"] = user_id
            return cls.post_record(session, data, response)

        if request.method == "PUT":
            data = item.dict(exclude_unset=True)
            data["updated_by"] = user_id
            return cls.update_record(session, data, pk, response)

        if request.method == "GET":
            return cls.fetch_records(session, pk, response)

        if request.method == "DELETE":
            return cls.soft_delete(session, pk, user_id, response)

    @classmethod
    def post_record(cls, session, data, response=None):
        schema = cls.schema()
        created, item = cls.perform_post(session, data, schema)
        if created and response is not None:
            response.status_code = status.HTTP_201_CREATED
        if isinstance(cls.hide_fields, list):
            schema = cls.schema(exclude=(field for field in cls.hide_fields))
        return schema.dumps(item)

    @classmethod
    def perform_post(cls, session, data, schema):
        created, item = get_or_create(session, cls.model, schema, data)
        return created, item

    @classmethod
    def fetch_records(cls, session, pk=None, response=None):
        if pk is not None:
            return cls.fetch_single_record(session, pk, response)
        model = cls.model
        query = session.query(model).filter(model.deleted_at.is_(None))
        result = query.all()
        schema = cls.schema(many=True)
        if isinstance(cls.hide_fields, list):
            schema = cls.schema(
                exclude=(field for field in cls.hide_fields), many=True
            )
        result = schema.dumps(result)
        return result

    @classmethod
    def fetch_object(cls, session, pk):
        item = session.query(cls.model).get(pk)
        if item is None or item.deleted_at is not None:
            raise HTTPException(status_code=404, detail="Record not Found")
        return item

    @classmethod
    def fetch_single_record(cls, session, pk, response):
        item = cls.fetch_object(session, pk)
        schema = cls.schema()
        if isinstance(cls.hide_fields, list):
            schema = cls.schema(exclude=(field for field in cls.hide_fields))
        return schema.dumps(item)

    @classmethod
    def update_record(cls, session, data, pk, response=None):
        validation_errors = cls.schema(partial=True).validate(data)
        if validation_errors:
            raise HTTPException(status_code=422, detail=validation_errors)
        item = cls.fetch_object(session, pk)
        item.set_model_dict(data)
        item.save(session)
        schema = cls.schema()
        if isinstance(cls.hide_fields, list):
            schema = cls.schema(exclude=(field for field in cls.hide_fields))
        return schema.dumps(item)

    @classmethod
    def soft_delete(cls, session, pk, user_id, response=None):
        item = cls.fetch_object(session, pk)
        item.delete(session, user_id)
        return json.dumps({"deleted": True})
