import os
from .WebAPI import *

__all__ = [
    "ChemSpiderAPI",
    "PubChemAPI"
]

class ChemSpiderAPI(WebAPIConnection):
    """
    It is better in general to just use the ChemSpiderPy package, but this works for now
    """

    request_base = 'https://api.rsc.org/compounds/v1'
    api_key_env_var = "CHEM_SPIDER_APIKEY"
    def __init__(self, token=None, request_delay_time=None,  **opts):
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
        token = self.get_chemspider_apikey(token)
        super().__init__({'header':'apikey', 'value':token}, request_delay_time=request_delay_time, **opts)

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
        if token is None:
            token = os.environ.get(cls.api_key_env_var)
        return token

    @property
    def filter(self):
        """
        **LLM Docstring**

        The `filter` sub-API (asynchronous compound-search queries).

        :return: the sub-API connection
        :rtype: object
        """
        return self.get_subapi('filter')

    @property
    def records(self):
        """
        **LLM Docstring**

        The `records` sub-API (compound record lookups).

        :return: the sub-API connection
        :rtype: object
        """
        return self.get_subapi('records')

    @property
    def lookups(self):
        """
        **LLM Docstring**

        The `lookups` sub-API (controlled-vocabulary lookups).

        :return: the sub-API connection
        :rtype: object
        """
        return self.get_subapi('lookups')

    @property
    def tool(self):
        """
        **LLM Docstring**

        The `tool` sub-API (utility endpoints).

        :return: the sub-API connection
        :rtype: object
        """
        return self.get_subapi('tool')

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
        res = self.filter.get(f'{query_id}/results', query=dict(count=count, start=start))
        return res
        # https: // api.rsc.org / compounds / v1
        # / filter / {queryId} / results

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
        base_query = self.filter.post(filter_path, json=opts)
        if 'queryId' in base_query:
            # TODO: handle status?
            request_delay_time = request_delay_time
            return self.handle_filter_query(base_query['queryId'], retries=retries, timeout=timeout)
        else:
            raise ValueError("`queryId` not in filter JSON")

    default_molecule_fields = [
        "CommonName",
        "SMILES",
        "InChI"
    ]
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
        if fields is None:
            fields = self.default_molecule_fields
        elif isinstance(fields, str):
            fields = [fields]
        return self.records.post("batch", json=dict(recordIds=ids, fields=fields), **opts)['records']

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
        if name not in self._name_cache:
            self._name_cache[name] = self.apply_filter_query('name', name=name, **opts)
        ids = self._name_cache[name]['results']
        if return_ids:
            return ids
        else:
            return self.get_info(ids, fields=fields)


        # payload = {"name": "aspirin",
        #            "orderBy": "default",
        #            "orderDirection": "default"}
        #
        # headers = {"apikey": "*your_API_Key*",
        #            "Content-Type": "application/json",
        #            "Accept": "application/json"}
        #
        # response = requests.post(url, json=payload, headers=headers)
        # print(response.json())
        # )


class PubChemAPI(WebAPIConnection):
    """
        It is better in general to just use the ChemSpiderPy package, but this works for now
        """

    request_base = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"

    def __init__(self, request_delay_time=None, **opts):
        """
        **LLM Docstring**

        Set up a connection to the PubChem PUG REST API.

        :param request_delay_time: minimum delay between requests
        :type request_delay_time: float | None
        :param opts: extra options for the base connection
        """
        super().__init__(None, request_delay_time=request_delay_time, **opts)

    @property
    def compound(self):
        """
        **LLM Docstring**

        The `compound` sub-API.

        :return: the sub-API connection
        :rtype: object
        """
        return self.get_subapi('compound')

    @property
    def name(self):
        """
        **LLM Docstring**

        The `compound/name` sub-API (lookups by compound name).

        :return: the sub-API connection
        :rtype: object
        """
        return self.get_subapi('compound/name')

    class Compound:
        def __init__(self, cid, **opts):
            """
            **LLM Docstring**

            Hold a PubChem compound id and its associated property values.

            :param cid: the PubChem compound id
            :type cid: int
            :param opts: the compound's property values
            """
            self.cid = cid
            self.opts = opts
        def __repr__(self):
            """
            **LLM Docstring**

            Return a representation showing the compound id and its stored properties.

            :return: the representation
            :rtype: str
            """
            return f"{type(self).__name__}(cid={self.cid}, opts={self.opts})"
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
            if 'Properties' in data:
                data = data['Properties']
            data = data.copy()
            cid = data.pop('CID')
            return cls(cid=cid, **data)
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
            pl = PubChemAPI.get_property_list()
            item = pl[item.casefold()]
            return self.opts[item]

    IDENTITY_PROPERTIES = frozenset({
        "MolecularFormula", "MolecularWeight", "SMILES", "ConnectivitySMILES",
        "InChI", "InChIKey", "IUPACName", "Title",
    })

    DESCRIPTOR_PROPERTIES = frozenset({
        "XLogP", "ExactMass", "MonoisotopicMass", "TPSA", "Complexity", "Charge",
    })

    COUNT_PROPERTIES = frozenset({
        "HBondDonorCount", "HBondAcceptorCount", "RotatableBondCount",
        "HeavyAtomCount", "IsotopeAtomCount", "AtomStereoCount",
        "DefinedAtomStereoCount", "UndefinedAtomStereoCount", "BondStereoCount",
        "DefinedBondStereoCount", "UndefinedBondStereoCount", "CovalentUnitCount",
    })

    ANNOTATION_PROPERTIES = frozenset({
        "PatentCount", "PatentFamilyCount", "AnnotationTypes",
        "AnnotationTypeCount", "SourceCategories", "LiteratureCount",
    })

    CONFORMER_3D_PROPERTIES = frozenset({
        "Volume3D", "XStericQuadrupole3D", "YStericQuadrupole3D",
        "ZStericQuadrupole3D", "FeatureCount3D", "FeatureAcceptorCount3D",
        "FeatureDonorCount3D", "FeatureAnionCount3D", "FeatureCationCount3D",
        "FeatureRingCount3D", "FeatureHydrophobeCount3D", "ConformerModelRMSD3D",
        "EffectiveRotorCount3D", "ConformerCount3D",
    })

    FINGERPRINT_PROPERTIES = frozenset({"Fingerprint2D"})

    _property_list = (
            IDENTITY_PROPERTIES
            | DESCRIPTOR_PROPERTIES
            | COUNT_PROPERTIES
            | ANNOTATION_PROPERTIES
            | CONFORMER_3D_PROPERTIES
            | FINGERPRINT_PROPERTIES
    )
    property_aliases = {
        'name':'Title'
    }
    @classmethod
    def get_property_list(cls):
        """
        **LLM Docstring**

        Return (and cache) the mapping of case-folded property names to their canonical
        PubChem spellings.

        :return: the property-name mapping
        :rtype: dict
        """
        if not isinstance(cls._property_list, dict):
            cls._property_list = {
                k.casefold():k for k in cls._property_list
            }
        return cls._property_list
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
        fields = [cls.property_aliases.get(f, f) for f in fields]
        pl = cls.get_property_list()
        _ = []
        for f in fields:
            f = f.casefold()
            if f not in pl:
                raise ValueError(f"unknown property {f}")
            f = pl[f]
            _.append(f)
        return ",".join(sorted(_))

    _name_cache = {}
    default_fields = ["smiles", "name"]
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
        if query is None: query = {}
        query = {'limit': limit} | query
        if fields is None:
            fields = self.default_fields
        if len(fields) > 0:
            if not isinstance(fields, str):
                fields = self._format_property_list(fields)
        else:
            fields = None
        key = (name, subfield, fields)
        if key not in self._name_cache:
            if fields is None:
                 res = self.name.get(name, subfield, query=query, **opts)
            else:
                 res = self.name.get(name, "property", fields, subfield, query=query, **opts)
            self._name_cache[key] = res
        res = self._name_cache[key]
        if 'PC_Compounds' in res:
            data = res['PC_Compounds']
            if wrap:
                data = [self.Compound.from_identifiers(d) for d in data]
        else:
            data = res['PropertyTable']
            if 'Properties' in data:
                data = data['Properties']
            if wrap:
                data = [self.Compound.from_identifiers(d) for d in data]
        return data