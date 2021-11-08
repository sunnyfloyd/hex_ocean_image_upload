# hexocean_image_upload

[![Build Status](https://travis-ci.org/sunnyfloyd/hexocean_image_upload.svg?branch=master)](https://travis-ci.org/sunnyfloyd/hexocean_image_upload)
[![Built with](https://img.shields.io/badge/Built_with-Cookiecutter_Django_Rest-F7B633.svg)](https://github.com/agconti/cookiecutter-django-rest)

Image storing application for HexOcean recruitment process.. Check out the project's [documentation](http://sunnyfloyd.github.io/hexocean_image_upload/).

# Prerequisites

- [Docker](https://docs.docker.com/docker-for-mac/install/)

# Initialize the project

Start the dev server for local development:

```bash
docker-compose up
```

Create a superuser to login to the admin:

```bash
docker-compose run --rm web ./manage.py createsuperuser
```
