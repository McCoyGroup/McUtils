
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
        token = self.get_chemspider_apikey(token)
        super().__init__({'header':'apikey', 'value':token}, request_delay_time=request_delay_time, **opts)

    @classmethod
    def get_chemspider_apikey(cls, token):
        if token is None:
            token = os.environ.get(cls.api_key_env_var)
        return token

    @property
    def filter(self):
        return self.get_subapi('filter')

    @property
    def records(self):
        return self.get_subapi('records')

    @property
    def lookups(self):
        return self.get_subapi('lookups')

    @property
    def tool(self):
        return self.get_subapi('tool')

    def handle_filter_query(self, query_id, count=1, start=0, **polling_opts):
        res = self.filter.get(f'{query_id}/results', query=dict(count=count, start=start))
        return res
        # https: // api.rsc.org / compounds / v1
        # / filter / {queryId} / results

    def apply_filter_query(self, filter_path, retries=None, timeout=None, request_delay_time=None, **opts):
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
        if fields is None:
            fields = self.default_molecule_fields
        elif isinstance(fields, str):
            fields = [fields]
        return self.records.post("batch", json=dict(recordIds=ids, fields=fields), **opts)['records']

    _name_cache = {}
    def get_compounds_by_name(self, name, return_ids=False, fields=None, **opts):
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
        super().__init__(None, request_delay_time=request_delay_time, **opts)

    @property
    def compound(self):
        return self.get_subapi('compound')

    @property
    def name(self):
        return self.get_subapi('compound/name')

    class Compound:
        def __init__(self, cid, **opts):
            self.cid = cid
            self.opts = opts
        def __repr__(self):
            return f"{type(self).__name__}(cid={self.cid}, opts={self.opts})"
        @classmethod
        def from_identifiers(cls, data):
            if 'Properties' in data:
                data = data['Properties']
            data = data.copy()
            cid = data.pop('CID')
            return cls(cid=cid, **data)
        def __getitem__(self, item):
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
        if not isinstance(cls._property_list, dict):
            cls._property_list = {
                k.casefold():k for k in cls._property_list
            }
        return cls._property_list
    @classmethod
    def _format_property_list(cls, fields):
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