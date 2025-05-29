web: gunicorn waya_backend.wsgi:application --bind 0.0.0.0:$PORT
worker: celery -A waya_backend worker --loglevel=info
beat: celery -A waya_backend beat --loglevel=info
