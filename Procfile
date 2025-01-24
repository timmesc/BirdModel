web: python manage.py collectstatic --no-input && python manage.py migrate && gunicorn --bind 0.0.0.0:8080 BirdModelDeploy.wsgi:application
