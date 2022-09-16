# gt-backend

## 运行

```bash
pip3 install -r requirements.txt
export GTSERVER=PRODUCTION  # DEVELOPMENT/TEST/PRODUCTION
export GTPOSTGRESQLHOST=127.0.0.1
export GTPOSTGRESQLPORT=5432
export GTPOSTGRESQLUSER=postgres
export GTPOSTGRESQLPASSWORD=******
python3 manage.py collectstatic
python3 manage.py makemigrations gt_user
python3 manage.py makemigrations gt_article
python3 manage.py makemigrations gt_tape
python3 manage.py makemigrations gt_admin
python3 manage.py makemigrations gt_utils
python3 manage.py makemigrations gt_form
python3 manage.py makemigrations gt_school
python3 manage.py makemigrations gt_notice
python3 manage.py makemigrations gt_im
python3 manage.py migrate

python3 manage.py runserver 0.0.0.0:8000
# or
# uwsgi uwsgi.ini
```
