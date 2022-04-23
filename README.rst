=================
httpie-signature
=================

.. image:: https://badge.fury.io/py/httpie-signature.svg
    :target: https://badge.fury.io/py/httpie-signature
    :alt: Latest Version on PyPI


An Http Signature Authentication plugin for `HTTPie <https://httpie.io>` .

HTTP Signatures describe a method of creating, encoding and verifying a signature within an HTTP request.
Http Signature Authentication is described in the following working document https://tools.ietf.org/id/draft-cavage-http-signatures-12.html

How to install
===============

.. code-block:: bash

    $ pip install httpie-signature

How to use
==========

.. code-block:: bash

    $ https --auth-type=signature https://apitest.cybersource.com/pts/v2/payments 'v-c-merchant-id: test'


~/.httpsigrc file
==================

Format:
-------

.. code-block:: bash

    [URL]
    key = <key>
    secret = <secret>
    headers = <String value of headers used in signatur>


Sample ~/.httpsigrc file
-------------------------

.. code-block:: bash

    [mywebsite.com]
    key = e3e0e662-0187-49d3-b4ba-09dcf4649a91
    secret = EcLO2Ybb7ChSLeQsAIPqEBnJpAm1Y3ypw2b4n4RqWnw=
    algorithm = HmacSHA256
    headers = host date (request-target) digest

    [anotherwebsite.com]
    key = 51da5b74-34b9-4dc0-9330-3fc4e9fbac03
    secret = ASDOASFKAFasd3rtsfasfWZFAFDWTRWFSGDFSDsds35=
    algorithm = HmacSHA256
    headers = host date (request-target) digest


If your request does not contain a body digest will automatically be removed from the header list.
