import requests
from requests.sessions import Session
from concurrent.futures import ThreadPoolExecutor
from threading import local

thread_local = local()


def get_session() -> Session:
    if not hasattr(thread_local, 'session'):
        thread_local.session = requests.Session()
    return thread_local.session


def download_link(url: str):
    session = get_session()
    with session.get(url) as response:
        try:
            return len(response.json()['album']['tracks']['track'])
        except KeyError:
            return 0


def download_all(urls: list, arr: list) -> None:
    with ThreadPoolExecutor(max_workers=10) as executor:
        arr.extend(executor.map(download_link, urls))
