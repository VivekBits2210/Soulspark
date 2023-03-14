# Soulspark


Backend setup
```
$ python3 -m venv python_venv
$ source python_venv/bin/activate
$ python3 -m pip install --upgrade pip setuptools
$ python3 -m pip install -r requirements.txt
$ python3 manage.py makemigrations
$ python3 manage.py migrate
$ python3 manage.py createsuperuser
```

Create a super user with name 'admin' and an email that is NOT a real email

```
$ python3 manage.py runserver localhost:8000
REST:  /fill-db
```

Go to /admin and login with your super user credentials. \
Under 'Sites'
```
Domain: localhost:8000
Display: localhost
```

Under "Social Application",
```
Provider: Google
Client ID: 485503899387-03u1pvv94g1k01tf9rhv7nno51tbfmls.apps.googleusercontent.com
Client Secret: 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
Key: (blank)
Selected hosts: localhost:8000
```

After logging out of /admin,
```
REST: /accounts/login
```
click on "Google" to sign in (make sure your email address is part of the project -> [ask a dev to do this])

To sign out,
```
REST: /accounts/logout
```

Swagger
```
REST: /
```

Testing
```
$ python3 manage.py test
```
