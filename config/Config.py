import os
from enum import Enum

from flask import jsonify


class EndpointSecurityTypes(Enum):
    BASIC_HTTP = "BASIC_HTTP"
    TOKEN = "TOKEN"
    OTP = "OTP"


class EndpointSecurityDecorators(Enum):
    EndpointSecurityTypes.BASIC_HTTP = None
    EndpointSecurityTypes.TOKEN = None
    EndpointSecurityTypes.OTP = None


class ConfigEntry:
    def __init__(self, json_dump):
        self.security_type = json_dump.get('auth_type', None)
        self.token = json_dump.get('token', None)
        self.credentials = json_dump.get('credentials', None)
        self.endpoint = json_dump.get('endpoint', None)
        self.script = json_dump.get('script', None)


class JunkinsConfig:
    def __init__(self, json_dump):
        self.port = json_dump.get('port', 80)
        self.host = json_dump.get('host', '0.0.0.0')
        self.scripts = list(map(lambda x: ConfigEntry(x), json_dump.get('scripts', [])))

    def registerEndpoints(self, app):
        # TODO add security decorators
        for script in self.scripts:
            @app.route(script.endpoint)
            def resolver():
                result = os.popen(script.script)
                output = result.read()
                return jsonify({"output": output})
