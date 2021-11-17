from fastapi.encoders import jsonable_encoder
from fastapi import status, HTTPException
from typing import List

from app.utils import get_or_create


class BaseController:
    model = None
    schema = None

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
    def post_record(cls, session, data, response):
        created, item = get_or_create(session, cls.model, cls.schema, data)
        if created:
            response.status_code = status.HTTP_201_CREATED
        return item

    @classmethod
    def fetch_records(cls, session, pk=None, response=None):
        if pk is not None:
            return cls.fetch_single_record(session, pk, response)
        model = cls.model
        query = session.query(model).filter(model.deleted_at.is_(None))
        result: List[cls.schema] = query.all()
        return result

    @classmethod
    def fetch_single_record(cls, session, pk, response):
        item = session.query(cls.model).get(pk)
        if item is None or item.deleted_at is not None:
            raise HTTPException(status_code=404, detail="Record not Found")
        return item

    @classmethod
    def update_record(cls, session, data, pk, response):
        item = cls.fetch_single_record(session, pk, response)
        item.set_model_dict(data)
        item.save(session)
        result: cls.schema = item
        return result

    @classmethod
    def soft_delete(cls, session, pk, user_id, response):
        item = cls.fetch_single_record(session, pk, response)
        item.delete(session, user_id)
        return {"deleted": True}
