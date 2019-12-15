import time

import requests
import requests_cache


allowable_codes=(200,404,)
requests_cache.install_cache(
    'request_cache',
    backend='redis',
    allowable_codes=allowable_codes
)


def make_throttle_hook(per_second=1):
    """
    Returns a response hook function which sleeps for `timeout` seconds if
    response is not cached
    """
    last_request_time = 0
    rate = 1 / per_second
    def hook(response, *args, **kwargs):
        nonlocal last_request_time
        if not getattr(response, 'from_cache', False):
            now = time.time()
            diff = now - last_request_time
            last_request_time = now
            if diff < rate:
                time.sleep(rate - diff)
        return response
    return hook


def make_session(rate: int = 300) -> requests.Session:
    s = requests.Session()
    s.headers.update({
        'User-Agent': 'CLI library info getter. Email: chrahunt@gmail.com'
    })

    s.hooks['response'].append(make_throttle_hook(rate))
    return s
