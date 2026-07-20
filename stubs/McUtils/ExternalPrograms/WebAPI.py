from __future__ import annotations
import abc
import base64
import time
import urllib.parse
import collections
import weakref
from ..Scaffolding import ResourceManager
import hashlib
import zipfile
import os
__all__ = ['WebRequestHandler', 'WebAPIConnection', 'WebSubAPIConnection', 'WebResourceManager', 'GitHubReleaseManager', 'ReleaseZIPManager']

class WebAPIError(IOError):
    ...

class WebRequestHandler:

    @classmethod
    def resolve_handler(cls, handler):
        ...

    @classmethod
    def request(cls, method, url, json=None, handler=None, **params):
        ...

    @classmethod
    def requests_request(cls, method, url, **params):
        ...

    @classmethod
    def urllib3_request(cls, method, url, **params):
        ...

    @classmethod
    def default_request(cls, method, url, data=None, headers=None, origin_req_host=None, unverifiable=False, json=None, **params):
        ...

    @classmethod
    def handle_response(cls, resp, headers):
        ...

    @classmethod
    def read_response(cls, resp, decode=True):
        ...

class APIAuthentication(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def prep_request(self, url_params, **kwargs):
        ...

    @classmethod
    def resolve_auth(cls, auth_data):
        ...
    auth_types = {}

    @classmethod
    def get_auth_dispatch(cls):
        ...

    @classmethod
    def dispatch_auth(cls, opts):
        ...

class NoAuth(APIAuthentication):

    def prep_request(self, url_params, **kwargs):
        ...

class HeaderValueAuth(APIAuthentication):

    def __init__(self, header, value):
        ...

    def prep_request(self, url_params, headers=None, **kwargs):
        ...

class BasicAuth(APIAuthentication):
    """
    Does any site still use this???
    """

    def __init__(self, username, password):
        ...

    def prep_request(self, url_params, headers=None, **kwargs):
        ...

class BearerTokenAuth(APIAuthentication):

    def __init__(self, token, encoded=True):
        ...

    def prep_request(self, url_params, headers=None, **kwargs):
        ...

class WebAPIConnection:
    """
    Base class for super simple web api interactions, use something better designed in general
    """

    def __init__(self, auth_info, history_length=None, log_requests=False, request_delay_time=None):
        ...
    default_content_type = 'application/json'
    default_return_type = 'application/json'

    def prep_headers(self, headers, content_type=None, return_type=None):
        ...
    default_request_handler = WebRequestHandler

    def do_request(self, method, root, *path, query=None, headers=None, content_type=None, return_type=None, handler=None, delay_time=None, json=None, data=None, **urllib3_request_kwargs):
        ...

    def get(self, root, *path, query=None, **urllib3_request_kwargs):
        ...

    def post(self, root, *path, query=None, **urllib3_request_kwargs):
        ...

    def delete(self, root, *path, query=None, **urllib3_request_kwargs):
        ...
    request_base = None

    def get_endpoint_params(self, root, path, query=None, base=None, fragment=None):
        ...

    def get_subapi(self, extension) -> WebSubAPIConnection:
        ...

class WebSubAPIConnection(WebAPIConnection):

    def __init__(self, path_extension, root_api: WebAPIConnection):
        ...

class WebResourceManager(ResourceManager):
    default_resource_name = 'links'
    default_request_handler = WebRequestHandler

    def __init__(self, *, request_handler=None, **opts):
        ...

    def get_resource_filename(self, name):
        ...

    def download_link(self, link):
        ...
    resource_function = download_link

class ReleaseZIPManager(WebResourceManager):
    default_resource_name = 'releases'
    location_env_var = 'GITHUB_RELEASE_DIR'
    use_temporary = True

    @classmethod
    def parse_semver(cls, version_string):
        ...

    @classmethod
    def make_semver(cls, version):
        ...

    @classmethod
    def parse_name_version(cls, filename):
        ...

    def list_resources(self):
        ...

    def save_resource(self, loc, val):
        ...

class GitHubReleaseManager(WebAPIConnection):
    request_base = 'https://api.github.com/'
    resource_key = 'zipball_url'
    release_manager_class = ReleaseZIPManager

    def __init__(self, token=None, request_delay_time=None, release_manager=None, **opts):
        ...
    blacklist_repos = ['.github']

    def list_repos(self, owner):
        ...

    def list_releases(self, owner, repo):
        ...

    def latest_release(self, owner, repo):
        ...
    release_cache = {}

    def update_existing_releases(self):
        ...

    @classmethod
    def format_repo_key(cls, owner, name):
        ...

    def resolve_resource_url(self, v):
        ...

    def get_release_list(self, owner, name, update=None):
        ...