# Image Upload DRF API for Hex Ocean Recruitment

Image storing application for HexOcean recruitment process.

## How to Set-up a Project Locally

1. Run initial migration:

```bash
docker-compose run --rm web python manage.py migrate
# OR
docker-compose up
```

2. Set up initial project structure (default plans with thumbnail options) run:

```bash
docker-compose run --rm web python manage.py set_up_default_plans
```

3. Run a server:

```bash
docker-compose up
```

4. For convenience following accounts are created with corresponding plans:

- login: admin; password: 123 (superuser)
- login: basic; password: 123 
- login: premium; password: 123 
- login: enterprise; password: 123 

- To run tests run a following command:

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
