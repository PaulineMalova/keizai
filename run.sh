#!/bin/sh
export PYTHONPATH=.
alembic upgrade head
uvicorn app.main:app
