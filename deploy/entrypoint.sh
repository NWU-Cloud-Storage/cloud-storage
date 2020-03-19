BACKEND=/root/backend
cd $BACKEND
python3 manage.py migrate
gunicorn backend.wsgi
