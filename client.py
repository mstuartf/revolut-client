import os
from collections import OrderedDict
from datetime import datetime, timedelta

import jwt
import pem
import requests
from jwt.contrib.algorithms.pycrypto import RSAAlgorithm


# Revolut auth requires RS256 algorithm need to enable here via pycrypto (can't use cryptography on GAE)
jwt.register_algorithm('RS256', RSAAlgorithm(RSAAlgorithm.SHA256))


class RevolutClient:

    def __init__(self):
        self.base_url = os.environ.get('REVOLUT_URL')

    def generate_jwt(self):

        # args must be in this exact order for the JWT to be valid
        token_args = OrderedDict([
            ("iss", os.environ.get('REVOLUT_JWT_ISSUER')),
            ("sub", os.environ.get('REVOLUT_CLIENT_ID')),
            ("aud", "https://revolut.com"),
            ("iat", datetime.now()),
            ("exp", datetime.now() + timedelta(minutes=60))
        ])

        cert = pem.parse_file(os.environ.get('REVOLUT_PRIVATE_KEY_PATH'))
        key_bytes = cert[0].as_bytes()

        return jwt.encode(token_args, key_bytes, algorithm='RS256')

    def get_access_token(self, code):

        url = u'{}/auth/token'.format(self.base_url)

        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'client_id': os.environ.get('REVOLUT_CLIENT_ID'),
            'client_assertion_type': 'urn:ietf:params:oauth:client-assertion-type:jwt-bearer',
            'client_assertion': self.generate_jwt()
        }

        # don't json.dumps the data so that it will be sent as Content-Type application/x-www-form-urlencoded
        request = requests.post(url, data=data)
        request.raise_for_status()

        return request.json()

    def refresh_access_token(self, refresh_token):

        url = u'{}/auth/token'.format(self.base_url)

        data = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'client_id': os.environ.get('REVOLUT_CLIENT_ID'),
            'client_assertion_type': 'urn:ietf:params:oauth:client-assertion-type:jwt-bearer',
            'client_assertion': self.generate_jwt()
        }

        # don't json.dumps the data so that it will be sent as Content-Type application/x-www-form-urlencoded
        request = requests.post(url, data=data)
        request.raise_for_status()

        return request.json()
