# -*- coding: utf-8 -*-
from requests.auth import AuthBase
import hashlib
import base64


class AuthAD(AuthBase):
    """Classe para autenticacao de Assinatura Digital."""

    def __init__(self, url, query, token, secret):
        """Construtor da classe de autenticacao."""
        self.URL_REQUEST = url
        self.QUERY_REQUEST = query

        self.TOKEN = token
        self.SECRET = secret

    def __call__(self, r):
        """Caller method.

        Adiciona a security_hash no header.
        """

        _hash_m = (
            self.URL_REQUEST +
            self.SECRET +
            self.QUERY_REQUEST
        )
        _hash_m = _hash_m.encode('utf-8')

        _hash_to_encode = '%s:%s' % (
            self.TOKEN,
            hashlib.sha256(_hash_m).hexdigest()
        )
        _hash_to_encode = _hash_to_encode.encode()

        r.headers['security-hash'] = base64.b64encode(_hash_to_encode)

        return r
