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

Go to /admin and login with your super user credentials. Under "Social Application", you should now see "Google SSO"
Under 'Bot Profiles', re-upload images for the tinder profiles using images from /static.

```
REST: /accounts/login
```
After logging out of /admin, 
click on "Google" to sign in (first make sure to add your email address to test Google Credentials -> [ask a dev to do this])

To sign out,
```
REST: /accounts/logout
```