## Bootstrap

This file provides a short description on steps which need to be taken in order to properly set up this application.

## Depencencies

This project requires Python3.7+

This project requires a PosgreSQL database to run.

Install those packages:

```
apt install gdal-bin libgdal-dev python3-gdal binutils libproj-dev
```

Install the `postgis` extension to postgres:
```
sudo add-apt-repository ppa:ubuntugis/ppa
sudo apt install postgis
```

With postgreSQL installed and running, create a new user:

```
sudo runuser -l postgres -c "createuser -D -E -l -P -R -S 'myuser'"
```

Create the database:
```
sudo runuser -l postgres -c "createdb -E UTF8 --lc-collate=en_US.UTF-8 --lc-ctype=en_US.UTF-8 -O \"myuser\" \"roy_db\" \"Roy db\""
```

Assign superuser permissions to that user (required for enabling the `postgis` extension).

```
sudo su postgres
psql
ASTER ROLE myuser WITH SUPERUSER;
\q
psql roy_db myuser
CREATE EXTENSION postgis;
```
You can use a file named `local_settings.py`, placed in the `roy` directory (the one containing the `settings.py` file) to insert your private database credentials. Git is set up to ignore that file.

## Heroku setup

To run on Heroku, remember to set up the environment variable: `BUILD_WITH_GEO_LIBRARIES` to `1`.

```
heroku login
heroku config:set BUILD_WITH_GEO_LIBRARIES=1
```