# SoulSpark


Backend setup (Ideally use Python 3.9.13)
```
$ python3 -m venv python_venv
$ source python_venv/bin/activate
$ python -m pip install --upgrade pip setuptools
$ python -m pip install -r requirements.txt
$ python manage.py migrate
```
Create a superuser with name 'admin' and an email that is NOT a real email
```
$ python manage.py createsuperuser
```

Run the server and load DB by opening the /fill-db URL
```
$ python manage.py runserver localhost:8000
-> Run REST API:  /fill-db
-> REST: /admin
```

Go to the admin URL and login with your superuser credentials. \
In the 'Sites' table, edit the 'example' entry to look like this:
```
Domain name: "localhost:8000"
Display name: "localhost"
```

After logging out of /admin,
```
-> REST: /accounts/login
```
Click on "Google" to sign in. Make sure your email address is a valid test email for this project. *If not, ask a dev to add you as test user*.

To sign out,
```
-> REST: /accounts/logout
```

Swagger
```
-> REST: /
```

Database Documentation
```
-> REST: /admin/doc/models
```
Run all tests
```
$ python manage.py test
```

Limited testing example (only tests from tests_urls.py under chat_module folder):
```
$ python manage.py test chat_module.tests.test_urls
```

*Unfixed bug: Firing the test suite creates many dummy images prefixed with 'test'/'trial' inside the images folder, clear this folder between testing runs.*

Valid way to count lines of code    
```
$cloc ./soulspark-backend --exclude-dir=images,python_venv,.idea,migrations -v --by-file --exclude_ext=json
```