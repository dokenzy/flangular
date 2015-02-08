# FlangularMongo

FlangularMongo is forked from [flangular@uvc-ingenieure](https://github.com/uvc-ingenieure/flangular). The main purpose of this project is using MongoDB for several reasons.

FlangularMongo is Flask based Angularjs template app with authentication for private CRUD applications.

It provides a good startind point for private Angularjs apps:

* Flask-Restful Backend
* Authentication with CSRF protection
* Protects private code components until logged in
* Angularjs service for basic CRUD
* Example model included
* MIT License

## Installation

There is a simple `bootstrap.sh` shell script included which sets up
a virtualenv and downloads the bower dependencies.

The script expects a working bower and virtualenv installation.


    ./bootstrap.sh
    ./server.py

Then browse to `http://localhost:5000/` and log in with:

**E-Mail:** admin@flangular.js

**Password:** admin

footer:: Copyright (c) UVC Ingenieure http://uvc.de/