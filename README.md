# django-drf-tutorials

### install
```sh
python -m venv .venv

. .venv/bin/activate

pip install -r requirements.txt

pip install --upgrade pip

python manage.py migrate

python manage.py runserver_plus
```

### commands (django-extensions)

```sh
# route url list
python manage.py show_urls

# shell
python manage.py shell_plus

# run scripts/categories.py 
python manage.py runscript categories
```

커밋 테스트