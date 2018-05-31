# sp_test
* git clone git@github.com:poc-sp/sp_test.git /tmp/sp_test
* virtualenv /tmp/sp_env
* source /tmp/sp_env/bin/activate
* cd /tmp/sp_test
* pip install -r requirements.txt
* python manage.py makemigrations profiles blog
* python manage.py migrate
* python manage.py createsuperuser 
* python manage.py runserver
