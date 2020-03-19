BACKEND=/app/backend
DATA=/data

mkdir -p $DATA/log

cd $BACKEND
python3 manage.py migrate
exec supervisord -c /app/deploy/supervisord.conf