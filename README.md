# Image Upload DRF API for Hex Ocean Recruitment

[![Build Status](https://travis-ci.org/sunnyfloyd/hexocean_image_upload.svg?branch=master)](https://travis-ci.org/sunnyfloyd/hexocean_image_upload)
[![Built with](https://img.shields.io/badge/Built_with-Cookiecutter_Django_Rest-F7B633.svg)](https://github.com/agconti/cookiecutter-django-rest)

Image storing application for HexOcean recruitment process.
 

## How to Set-up a Project Locally

- To start a project use:
```bash
docker-compose up
```

- To run tests run a following command inside the docker container:

```bash
docker-compose run --rm web python manage.py test
```

## Time Spent on Development

- Setting up a development environment with a cookiecutter: 2h (comms: apparently inconsistent linebreaks make it difficult to share Dockerfiles between Windows and Unix OS)
- Creating required models with validations: 2.5h
- Creating API endpoints: 2h
- Creating tests: 2h

**Total: ~8.5h** (comms: working with API that handles files was quite specific)

## Not-Implemented Project Enhancements

- If business requirement would allow for delayed thumbnail generation I would delegate this task to a background processing with Redis Queue/Celery
- Deployment should be done with Nginx or other load balancer with capability to serve static files
