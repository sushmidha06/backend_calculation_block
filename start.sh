#!/usr/bin/env bash
gunicorn -k uvicorn.workers.UvicornWorker app:app --bind 0.0.0.0:$PORT --workers 4
