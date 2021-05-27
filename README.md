Mifos X Credit Scoring Module
============

The project consisted of providing an AI powered solution to the users for credit assessment of loans. The project covered various aspects from classical AI, considering various statistical models, to the modern day neural network. The project is enriched with various credit modeling techniques, giving access to the user to choose one or any from them. It also takes care of the different data sources from which data can be fetched and has been fully incorporated to handle data coming from various sources like JSON/XML or SQL.

It is a RESTFUL API module written in [django](https://www.djangoproject.com/) and [Django Rest framework](https://www.django-rest-framework.org/)


Getting started
============

1. Ensure you have the following installed in your system:

    [`git`](https://git-scm.com/downloads)


Requirements
============
* python 3.6.8+

You can install python for your platform by following the python getting started [guide](https://wiki.python.org/moin/BeginnersGuide/Download).

Setting up a local server
============

To set up server locally you need to install all the requirements listed in requirements.txt.
But first, you need to create and activate your project virtual environment by using the commands:
    
    python -m venv env

For Linux or MacOS environment:
    
    source env/bin/activate

For windows environment:

    ./env/bin/activate

You can then install project dependencies using the following command:

    pip install -r requirements.txt

Once you have successfully installed all the dependencies, you can run the database migrations by running the command:

    python manage.py migrate

You can run the API server by running the command:

    python manage.py serve

## Want to help? [![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/openMF/web-app/issues)

Want to file a bug, request a feature, contribute some code, or improve documentation? Excellent! Read up on our guidelines for [contributing](.github/CONTRIBUTING.md) and then check out one of our [issues](https://github.com/openMF/web-app/issues). Make sure you follow the guidelines before sending a contribution!
