Using Postgres instead of MongoDB for a NoSQL db
================================================

The sample Emporium application used for this presentation has one version
using SQLAlchemy and a second version using the Django ORM. Please see the
Pyramid_SQLAlchemy and Django_ORM subfolders for the code.

Postgres version 9.4 running on localhost with the default port was used for
the presentation. You will need to create databases called emporium_alchemy
and emporium_django, and export these environment variables for the database
connection string:

| ``export DBUSER=your_postgres_username``
| ``export DBPASSWORD=your_postgres_password``
