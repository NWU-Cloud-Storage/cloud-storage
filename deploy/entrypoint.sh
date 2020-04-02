BACKEND=/app/backend
DATA=/data

mkdir -p $DATA/log

ls -al /app

cd $BACKEND
python3 manage.py migrate
exec supervisord -c /app/deploy/supervisord.conf