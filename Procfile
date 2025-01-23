web: python manage.py collectstatic --no-input && python manage.py migrate && gunicorn BirdModelDeploy.wsgi --bind 0.0.0.0:$PORT
