# modifipic_app
Simple web app modifying image uploaded by user. Served as a platform to work with Django Rest Framework and OpenCV.

## How does it work?
1. Upload an image and choose how you want to modify it (e.g. blur, sepia etc.).
2. You can use use REST API endpoints or use app interface - depending on your needs.

a) This is REST API VIEW

<p align="center">
<img src="modifipic_app/frontend_modifipic/static/img/modifipic_app API view.png" alt="app screen"
	title="modifipic_app API view" width="750" align="center"/>
</p>

b) and this is app view

<p align="center">
<img align="center" src="modifipic_app/frontend_modifipic/static/img/modifipic_app user friendly app.png" alt="app screen"
	title="modifipic_app user friendly app" width="750"/>
</p>

3. Simply download modified file.


### Getting Started

Install dependencies to your virtualenv, using requirements.txt

```
pip install -r requirements.txt
```

Create new database in PostgreSQL

Create new .py file in modifipic_app/modifipic_app/ folder and name it local_settings.py

Paste there the below:

```
SECRET_KEY = ''

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '',
        'HOST': '',
        'PASSWORD': '',
        'USER': '',
    }
}

```
Fill in missing parameteres with your secret key and your database credentials.


#### Installing

While in directory:

```
modifipic_app/modifipic_app/
```

Run migrations:

```
python3 manage.py migrate
```
Run server

```
python3 manage.py runserver
```

## Built With

* [Python 3.7.5](https://www.python.org/)
* [Django Rest Framework 3.11.0](https://www.django-rest-framework.org/) -  powerful and flexible toolkit for building Web APIs
* [Django 3.0.3](https://www.djangoproject.com/)  - high-level Python Web framework that encourages rapid development and clean, pragmatic design.
* [Open CV 4.2.0.32](https://opencv.org/) - open source computer vision and machine learning software library
* [Numpy 1.18.1](https://numpy.org/) - the fundamental package for scientific computing with Python
* [PostgreSQL](https://www.postgresql.org/) -  open source object-relational database system


## Author

[ZuzannaP](https://github.com/ZuzannaP)

## License

This project is licensed under the GNU AFFERO GENERAL PUBLIC LICENSE - see the [LICENSE.md](https://github.com/ZuzannaP/shall_we_meet_app/blob/master/LICENSE) file for details

