from setuptools import setup, find_packages

setup(
    name='httpie-signature',
    description='Http Signature Authentication plugin for HTTPie.',
    long_description=open('README.rst').read().strip(),
    version='0.0.1',
    author='Ryan McCarter',
    author_email='ryanmccarter721@gmail.com',
    license='MIT',
    url='https://github.com/rymccarter721/httpie-signature',
    download_url='https://github.com/rymccarter721/httpie-signature',
    py_modules=['httpie_signature', 'httpSignature'],
    packages=find_packages(),
    entry_points={
        'httpie.plugins.auth.v1': [
            'httpie_signature = httpie_signature:HttpSignatureAuthPlugin'
        ]
    },
    install_requires=[
        'httpie',
        'requests'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers'
    ]
)