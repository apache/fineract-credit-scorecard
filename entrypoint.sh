#!/bin/bash
python manage.py migrate
python manage.py runserver 0:8000
echo Running Django on the local host at http://localhost:8000