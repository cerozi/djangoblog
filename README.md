# DjangoBlog

A simple blog made using Django 3.2.10 and Python 3.7.6. For this blog, i took Twitter as a big reference (you can see by the bird logo), and tried to made my own version of it. I will be greateful for any suggestion or appointment, so if you have one, please leave it to me. :)

# Features

This blog contains the following features:

* Likes
* Replys
* Notifications
* Follow system
* User searching
* Edit and delete your own posts
* Newsfeed posts based on users that you follow


# To run you need to..

Clone this repo:
```python
git clone https://github.com/cerozi/djangoblog.git
```

With your virtual enviroment on, install all packages and modules found in requirements.txt:
```python
pip install requirements.txt
```

Make the database migrations:

```
python manage.py makemigrations
python manage.py migrate
```

Now, run the server and the project can be found on your localhost(http://127.0.0.1:8000/):
```python
python manage.py runserver
```
