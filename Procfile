release: python manage.py makemigrations journalbuddy
release: python manage.py migrate journalbuddy
release: python manage.py migrate
release: python manage.py collectstatic --noinput
web: gunicorn mysite.wsgi