Using Postgres instead of MongoDB for a NoSQL db
================================================

This is a demo application called Emporium that I created for a Python
meetup presentation. There is one version using SQLAlchemy and a second
version using the Django ORM. Please see the Pyramid_SQLAlchemy and
Django_ORM subfolders respectively.

Postgres version 9.4 running on localhost with the default port was used for
the presentation. You will need to create databases called emporium_alchemy
and emporium_django, and export these environment variables for the database
connection string:

| ``export DBUSER=your_postgres_username``
| ``export DBPASSWORD=your_postgres_password``
