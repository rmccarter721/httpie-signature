from httpie.plugins import AuthPlugin
import os
import configparser

from httpSignature import HttpSignatureAuth

__version__ = '0.0.1'
__author__ = 'Ryan McCarter'
__licence__ = 'Apache 2.0'

class HttpSignatureAuthPlugin(AuthPlugin):

    name = 'Http Signature Authenticaiton'
    auth_type = 'signature'
    auth_require = False
    auth_parse = False
    prompt_password = False
    description = ''

    def get_auth(self, username: str = None, password: str = None):
        return HttpSignatureAuth()