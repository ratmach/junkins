import os
from base64 import b64encode
from enum import Enum

from flask import jsonify, request, make_response, abort
from werkzeug.exceptions import HTTPException
from werkzeug.security import check_password_hash


class EndpointSecurityTypes(Enum):
    BASIC_HTTP = "BASIC_HTTP"
    TOKEN = "TOKEN"
    OTP = "OTP"


class EndpointSecurityDecorators(Enum):
    BASIC_HTTP = lambda username, password: check_password_hash(username, password)
    TOKEN = lambda x: x == request.form.get("token", "") if "token" in request.form else lambda \
            x: jsonify({"reason": "token not provided"}), 403
    OTP = lambda x: jsonify({"reason": "not implemented yet"}), 502


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
        for count, script in enumerate(self.scripts):
            def security_decorator(f):
                def wrapper(*args, **kwargs):
                    try:
                        if script.security_type == EndpointSecurityTypes.BASIC_HTTP.value:
                            pass
                        elif script.security_type == EndpointSecurityTypes.TOKEN.value:
                            pass
                        elif script.security_type == EndpointSecurityTypes.OTP.value:
                            pass
                        return f(*args, **kwargs)
                    except HTTPException as e:
                        raise
                    except Exception as e:
                        response = jsonify({"reason": str(e)})
                        response.status_code = 400

                return wrapper

            def basic_http_login_required(security_type, credentials):
                def decorator(f):
                    def wrapper(*args, **kwargs):
                        print(security_type)
                        if security_type == EndpointSecurityTypes.BASIC_HTTP.value:
                            username = request.authorization.get('username', None) if request.authorization else None
                            password = request.authorization.get('password', None) if request.authorization else None
                            if username != credentials.get("username", None) or password != credentials.get("password",
                                                                                                            None):
                                return ('Unauthorized', 401, {
                                    'WWW-Authenticate': 'Basic realm="Login Required"'
                                })
                        return f(*args, **kwargs)

                    return wrapper

                return decorator

            @security_decorator
            @basic_http_login_required(script.security_type, script.credentials)
            def resolver():
                result = os.popen(script.script)
                output = result.read()
                return jsonify({"output": output})
            resolver.__name__ = "resolver_{0}".format(count)
            app.add_url_rule(script.endpoint, view_func=resolver)
