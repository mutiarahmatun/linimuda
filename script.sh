# ----- ONLY USING GIT BASH -----

# -- first time after creating virtual environment --
# python -m pip install --upgrade pip

MAKEMIGRATIONS="python manage.py makemigrations"
MIGRATE="python manage.py migrate"
RUNSERVER="python manage.py runserver"
UPDATEINDEX="python manage.py update_index"
COLLECTSTATIC="python manage.py collectstatic"

# -- linter --
# flake8 .

# -- formatter --
# black .

$MAKEMIGRATIONS && $MIGRATE && $UPDATEINDEX && $RUNSERVER
# -- collectstatic, do this if you want --
# $COLLECTSTATIC