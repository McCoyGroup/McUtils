import os
from .WebAPI import *
__all__ = ['ChemSpiderAPI', 'PubChemAPI']

class ChemSpiderAPI(WebAPIConnection):
    """
    It is better in general to just use the ChemSpiderPy package, but this works for now
    """
    request_base = 'https://api.rsc.org/compounds/v1'
    api_key_env_var = 'CHEM_SPIDER_APIKEY'

    def __init__(self, token=None, request_delay_time=None, **opts):
        """
        **LLM Docstring**

        Set up a connection to the RSC ChemSpider compounds API, resolving and sending
        the API key as the `apikey` header.

        :param token: the API key (falls back to the environment variable)
        :type token: str | None
        :param request_delay_time: minimum delay between requests
        :type request_delay_time: float | None
        :param opts: extra options for the base connection
        """
        ...

    @classmethod
    def get_chemspider_apikey(cls, token):
        """
        **LLM Docstring**

        Resolve the ChemSpider API key, falling back to the `CHEM_SPIDER_APIKEY`
        environment variable when none is given.

        :param token: an explicit API key (or `None`)
        :type token: str | None
        :return: the resolved API key
        :rtype: str | None
        """
        ...

    @property
    def filter(self):
        """
        **LLM Docstring**

        The `filter` sub-API (asynchronous compound-search queries).

        :return: the sub-API connection
        :rtype: object
        """
        ...

    @property
    def records(self):
        """
        **LLM Docstring**

        The `records` sub-API (compound record lookups).

        :return: the sub-API connection
        :rtype: object
        """
        ...

    @property
    def lookups(self):
        """
        **LLM Docstring**

        The `lookups` sub-API (controlled-vocabulary lookups).

        :return: the sub-API connection
        :rtype: object
        """
        ...

    @property
    def tool(self):
        """
        **LLM Docstring**

        The `tool` sub-API (utility endpoints).

        :return: the sub-API connection
        :rtype: object
        """
        ...

    def handle_filter_query(self, query_id, count=1, start=0, **polling_opts):
        """
        **LLM Docstring**

        Fetch a page of results for a completed filter query.

        :param query_id: the filter query id
        :type query_id: str
        :param count: the number of results to fetch
        :type count: int
        :param start: the result offset
        :type start: int
        :param polling_opts: extra polling options
        :return: the query results
        :rtype: dict
        """
        ...

    def apply_filter_query(self, filter_path, retries=None, timeout=None, request_delay_time=None, **opts):
        """
        **LLM Docstring**

        Submit a filter query and return its results, raising if the API doesn't return a
        query id.

        :param filter_path: the filter endpoint (e.g. `'name'`)
        :type filter_path: str
        :param retries: the retry count forwarded to the results fetch
        :type retries: int | None
        :param timeout: the timeout forwarded to the results fetch
        :type timeout: float | None
        :param request_delay_time: a per-query request delay
        :type request_delay_time: float | None
        :param opts: the query payload fields (posted as JSON)
        :return: the query results
        :rtype: dict
        :raises ValueError: if no `queryId` is returned
        """
        ...
    default_molecule_fields = ['CommonName', 'SMILES', 'InChI']

    def get_info(self, ids, fields=None, **opts):
        """
        **LLM Docstring**

        Fetch the requested fields for a batch of compound record ids.

        :param ids: the compound record ids
        :type ids: list
        :param fields: the fields to return (defaults to common name, SMILES, InChI)
        :type fields: list | str | None
        :param opts: extra request options
        :return: the compound records
        :rtype: list
        """
        ...
    _name_cache = {}

    def get_compounds_by_name(self, name, return_ids=False, fields=None, **opts):
        """
        **LLM Docstring**

        Look up compounds by name (via a cached name filter query), returning either the
        matching record ids or their full field info.

        :param name: the compound name
        :type name: str
        :param return_ids: return only the record ids
        :type return_ids: bool
        :param fields: the fields to return
        :type fields: list | str | None
        :param opts: extra query options
        :return: the record ids, or the compound records
        :rtype: list
        """
        ...

class PubChemAPI(WebAPIConnection):
    """
        It is better in general to just use the ChemSpiderPy package, but this works for now
        """
    request_base = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug'

    def __init__(self, request_delay_time=None, **opts):
        """
        **LLM Docstring**

        Set up a connection to the PubChem PUG REST API.

        :param request_delay_time: minimum delay between requests
        :type request_delay_time: float | None
        :param opts: extra options for the base connection
        """
        ...

    @property
    def compound(self):
        """
        **LLM Docstring**

        The `compound` sub-API.

        :return: the sub-API connection
        :rtype: object
        """
        ...

    @property
    def name(self):
        """
        **LLM Docstring**

        The `compound/name` sub-API (lookups by compound name).

        :return: the sub-API connection
        :rtype: object
        """
        ...

    class Compound:

        def __init__(self, cid, **opts):
            """
            **LLM Docstring**

            Hold a PubChem compound id and its associated property values.

            :param cid: the PubChem compound id
            :type cid: int
            :param opts: the compound's property values
            """
            ...

        def __repr__(self):
            """
            **LLM Docstring**

            Return a representation showing the compound id and its stored properties.

            :return: the representation
            :rtype: str
            """
            ...

        @classmethod
        def from_identifiers(cls, data):
            """
            **LLM Docstring**

            Build a `Compound` from a PubChem property record, pulling the `CID` out as the
            id and keeping the rest as properties.

            :param data: the property record (optionally nested under `Properties`)
            :type data: dict
            :return: the compound
            :rtype: PubChemAPI.Compound
            """
            ...

        def __getitem__(self, item):
            """
            **LLM Docstring**

            Look up a stored property by name (case-insensitively, via the canonical
            property list).

            :param item: the property name
            :type item: str
            :return: the property value
            :rtype: Any
            """
            ...
    DESCRIPTOR_PROPERTIES = frozenset({'XLogP', 'ExactMass', 'MonoisotopicMass', 'TPSA', 'Complexity', 'Charge'})
    FINGERPRINT_PROPERTIES = frozenset({'Fingerprint2D'})
    property_aliases = {'name': 'Title'}

    @classmethod
    def get_property_list(cls):
        """
        **LLM Docstring**

        Return (and cache) the mapping of case-folded property names to their canonical
        PubChem spellings.

        :return: the property-name mapping
        :rtype: dict
        """
        ...

    @classmethod
    def _format_property_list(cls, fields):
        """
        **LLM Docstring**

        Canonicalize and validate a set of property names (resolving aliases) into the
        comma-separated, sorted string PubChem expects.

        :param fields: the requested property names
        :type fields: list[str]
        :return: the formatted property list
        :rtype: str
        :raises ValueError: if a property is unknown
        """
        ...
    _name_cache = {}
    default_fields = ['smiles', 'name']

    def get_compounds_by_name(self, name, fields=None, subfield='json', limit=10, query=None, wrap=True, **opts):
        """
        **LLM Docstring**

        Look up compounds by name via the PubChem name endpoint (with result caching),
        returning the requested properties as `Compound` objects (or the raw records).

        :param name: the compound name
        :type name: str
        :param fields: the properties to fetch (defaults to SMILES and name)
        :type fields: list | str | None
        :param subfield: the response format sub-path (e.g. `'json'`)
        :type subfield: str
        :param limit: the maximum number of records
        :type limit: int
        :param query: extra query parameters
        :type query: dict | None
        :param wrap: wrap the records as `Compound` objects
        :type wrap: bool
        :param opts: extra request options
        :return: the compounds (or raw records)
        :rtype: list
        """
        ...