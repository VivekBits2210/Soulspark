# SoulSpark


Backend setup (Ideally use Python 3.9.13)
```
$ python -m venv python_venv
$ source python_venv/bin/activate
$ python -m pip install --upgrade pip setuptools
$ python -m pip install -r requirements.txt
$ python manage.py makemigrations chat_module ai_profiles 
$ python manage.py migrate
$ python manage.py createsuperuser
```

Create a super user with name 'admin' and an email that is NOT a real email

```
$ python3 manage.py runserver localhost:8000
-> Run REST API:  /fill-db
```

Go to url /admin and login with your super user credentials. \
Under 'Sites', edit the 'example' entry to look like this:
```
Domain: localhost:8000
Display: localhost
```

Under "Social Application", add the entry below:
```
Provider: Google
Client ID: 485503899387-03u1pvv94g1k01tf9rhv7nno51tbfmls.apps.googleusercontent.com
Client Secret: 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
Key: (blank)
Selected hosts: localhost:8000
```

After logging out of /admin,
```
-> REST: /accounts/login
```
click on "Google" to sign in (make sure your email address is a valid test email for this project -> [ask a dev to add you if it is not])

To sign out,
```
-> REST: /accounts/logout
```

Swagger
```
-> REST: /
```

API Documentation
```
-> REST: /admin/doc/views
```
Model Documentation
```
-> REST: /admin/doc/models
```
Run all tests
```
$ python3 manage.py test
```

Limited testing example (only tests from tests_urls.py under chat_module folder):
```
$ python3 manage.py test chat_module.tests.test_urls
```

*Unfixed bug: Firing the test suite creates dummy images inside the images folder, clear this folder between testing runs.*

