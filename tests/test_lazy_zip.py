import io
import logging
import zipfile

import requests
from cached_property import cached_property

from packages.network import HttpFile

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_a_zipfile():
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, mode='w') as z:
        for name in ['a', 'b', 'c']:
            with z.open(name, 'w') as f:
                text = name + ' contents'
                f.write(text.encode('utf-8'))

    with zipfile.ZipFile(buf) as z:
        pass


def test_http_zipfile():
    link = (
        "https://files.pythonhosted.org/packages/00/b6/"
        "9cfa56b4081ad13874b0c6f96af8ce16cfbc1cb06bedf8e9164ce5551ec1/"
        "pip-19.3.1-py2.py3-none-any.whl"
    )
    f = HttpFile(link, requests.Session())
    with zipfile.ZipFile(f) as z:
        names = z.namelist()
