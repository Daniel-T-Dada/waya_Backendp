#!/usr/bin/env bash
# build.sh - Render build script

set -o errexit  # exit on error

pip install --upgrade pip
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate
