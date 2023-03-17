# SoulSpark


Backend setup (Ideally use Python 3.9.13)
```
$ python -m venv python_venv
$ source python_venv/bin/activate
$ python -m pip install --upgrade pip setuptools
$ python -m pip install -r requirements.txt
$ python manage.py makemigrations chat_module ai_profiles 
$ python manage.py migrate
```
Create a superuser with name 'admin' and an email that is NOT a real email
```
$ python manage.py createsuperuser
```

Run the server and load DB by opening the /fill-db URL
```
$ python3 manage.py runserver localhost:8000
-> Run REST API:  /fill-db
-> REST: /admin
```

Go to the admin URL and login with your superuser credentials. \
Under 'Sites', edit the 'example' entry to look like this:
```
Domain name: "localhost:8000"
Display name: "localhost"
```

Under "Social Application", add the entry below:
```
Provider: Google (drop-down)
Name: SSO
Client ID: 485503899387-03u1pvv94g1k01tf9rhv7nno51tbfmls.apps.googleusercontent.com
Client Secret: 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
Key: (blank)
Selected hosts: localhost:8000 (select this)
```

After logging out of /admin,
```
-> REST: /accounts/login
```
Click on "Google" to sign in (make sure your email address is a valid test email for this project -> [ask a dev to add you as test user])

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
$ python3 manage.py test
```

Limited testing example (only tests from tests_urls.py under chat_module folder):
```
$ python3 manage.py test chat_module.tests.test_urls
```

*Unfixed bug: Firing the test suite creates many dummy images prefixed with 'test'/'trial' inside the images folder, clear this folder between testing runs.*

