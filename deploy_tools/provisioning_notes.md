## Requiremed packages

* nginx
* Python >= 3.6
* virtualenv + pip
* git

## nginx config

* Place `nginx.template.conf` in `/etc/nginx/sites-available/$DOMAIN`, and link to it from `/etc/nginx/sites-enabled/`
* Replace every occurrence of DOMAIN with the domain name


## gunicorn config

* put `gunicorn-systemd.template.service` in `/etc/systemd/system/$DOMAIN.service`
* Replace every occurrence of DOMAIN with the domain name

Das it
