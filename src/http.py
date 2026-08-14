from threading import local

from requests import Session
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

RETRY_STATUS_CODES = (429, 500, 502, 503, 504)
DEFAULT_TIMEOUT = 20


def create_session() -> Session:
    retry = Retry(
        total=3,
        connect=3,
        read=3,
        status=3,
        backoff_factor=0.5,
        status_forcelist=RETRY_STATUS_CODES,
        allowed_methods=frozenset({"GET", "POST"}),
        respect_retry_after_header=True,
    )
    session = Session()
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    session.headers.update({"User-Agent": "F500Tracker/2.0"})
    return session


_THREAD_STATE = local()


def get_session() -> Session:
    session = getattr(_THREAD_STATE, "session", None)
    if session is None:
        session = create_session()
        _THREAD_STATE.session = session
    return session


def get(url: str, **kwargs):
    kwargs.setdefault("timeout", DEFAULT_TIMEOUT)
    return get_session().get(url, **kwargs)


def post(url: str, **kwargs):
    kwargs.setdefault("timeout", DEFAULT_TIMEOUT)
    return get_session().post(url, **kwargs)
