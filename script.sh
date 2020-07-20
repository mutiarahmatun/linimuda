MAKEMIGRATIONS="python manage.py makemigrations"
MIGRATE="python manage.py migrate"
RUNSERVER="python manage.py runserver"
# COLLECTSTATIC="python manage.py collectstatic"

# formatter
black .

$MAKEMIGRATIONS && $MIGRATE && $RUNSERVER