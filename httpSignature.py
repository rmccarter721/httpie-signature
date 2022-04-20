from datetime import datetime
from urllib.parse import urlparse
import os
import requests.auth
import requests
import configparser
import hashlib
import base64
import hmac

def get_date():
    os.environ["TZ"] = "UTC"
    return datetime.now().strftime("%a, %d %b %Y %H:%M:%S UTC")

def get_hmacAlgorithm(algorithm: str):

    options = {
        "hmacsha256": hashlib.sha256,
        "hmacsha512": hashlib.sha512
    }

    return options[algorithm.lower()]


def get_host(uri: str):
    return '{uri.netloc}'.format(uri=urlparse(uri))

def get_resource(uri: str):
    return '{uri.path}'.format(uri=urlparse(uri))

def get_digest(payload: str):
    hashobj = hashlib.sha256()
    hashobj.update(payload.encode('utf-8'))
    hash_data = hashobj.digest()
    digest = base64.b64encode(hash_data)

    return digest

class HttpSignatureAuth(requests.auth.AuthBase):
    def __init__(self):
        rc_path = os.path.expanduser("~/.httpsigrc")
        config = configparser.RawConfigParser()
        config.read(rc_path)

        self.config = config

    def __call__(self, request: requests.PreparedRequest) -> requests.PreparedRequest:

        host = get_host(request.url)
        resource = get_resource(request.url)
        method = request.method
        payload = request.body
        date = get_date()

        try:
            rc = dict(self.config.items(host))
        except configparser.NoSectionError:
            print("Please create ~/.httpsig.rc with key, secret, algorithm and headers.")

        key=rc.get('key')
        secret=base64.b64decode(rc.get('secret'))
        algorith=rc.get('algorithm')
        headersSupplied=rc.get('headers')

        rawHeaderString = ([])
        signature = ([])

        headers = {}
        for header in request.headers:
            headers[header.lower()] = request.headers[header] 

        rawHeaderString.append("keyid=\"" + key + "\"")
        rawHeaderString.append(", algorithm=\"" + algorith + "\"")
        rawHeaderString.append(", headers=\"")

        headerList = ([])
        for header in headersSupplied.split( ):
            if header == "host":
                headerList.append("host")
                signature.append("host: " + host)
            elif header == "date":
                request.headers["Date"] = date
                headerList.append("date")
                signature.append("date: " + date)
            elif header == "(request-target)":
                headerList.append("(request-target)")
                signature.append("(request-target): " + method.lower() + " " + resource)
            elif header != "digest" and header.lower() in headers:
                headerList.append(header)
                signature.append(header + ": " + headers[header.lower()].decode("utf-8"))
            elif header == "digest" and payload != None:
                digest = "SHA-256=" + get_digest(payload.decode("utf-8")).decode("utf-8")
                request.headers["Digest"] = digest
                headerList.append("digest")
                signature.append("digest: " + digest)
        
        rawHeaderString.append(" ".join(headerList))
        rawHeaderString.append("\"")

        hasedSignature = hmac.new(secret, bytes(str("\n".join(signature)), encoding='utf-8'), get_hmacAlgorithm(algorith))
        encodedSignature = base64.b64encode(hasedSignature.digest()).decode("utf-8")

        rawHeaderString.append(", signature=\"" + encodedSignature + "\"")
        request.headers['Signature'] = f'{"".join(rawHeaderString)}'
        return request