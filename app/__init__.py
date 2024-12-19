from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from apispec import APISpec
from flask_restful import Resource, Api
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec

application = Flask(__name__)
application.secret_key = 'stock application by shubham '

api = Api(application)

application.config.update(
    {
        'APISPEC_SPEC': APISpec(
            title = 'Stock Application',
            version = 'v1',
            plugins = [MarshmallowPlugin()],
            openapi_version = '2.0.0'
        ),
        'APISPEC_SWAGGER_URL': '/swagger/',  # uri to access API Docs
        'APISPEC_SWAGGER_UI_URL': '/swagger-ui/' #uri to access UI of API Doc
    }
)

docs = FlaskApiSpec(application)

from app.models import *