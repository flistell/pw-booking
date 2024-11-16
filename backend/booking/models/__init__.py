import logging
import pprint
from pprint import pformat
from booking import db

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

registered_resources = {}
protected_resources = {}

### DECORATORS ###

def resource(c):
    registered_resources[c.__name__.lower()] = c
    return c


def protected_resource(c):
    registered_resources[c.__name__.lower()] = c
    protected_resources[c.__name__.lower()] = c
    return c


### UTILITY FUNCTIONS ###

def _dict_factory(cursor, row, mapper=None):
    # sarebbe meglio avere qui un mapper che formatti in modo particolare
    # alcune righe, as esempio item_details come json
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


### BASE CLASSES ###

class CollectionBase():
    """Una classe base che rappresenta un insieme di Resources. Mappa su un tabella."""
    _db = None                                  #  connessione al DB
    _pkey = 'id'                                #  chiave primaria della tabella
    _tablename = 'dual'                         #  nome della tabella sottostante
    _kind = object                              #  classe dei singoli oggetti che compongono la collection
    _query = "SELECT * FROM {tablename}"        #  template della query di base per la lista complete delle risorse
    _query_filter = "SELECT * FROM {tablename}" #  template della premessa della query di base da utilizzare per la lista parziale di risorse
    _user_fkey = 'user_id'                      #  nome del campo nella tabella che referenzia gli utenti: serve per la sicurezza di accesso al dato
    _extra_operations = []                      

    def __init__(self):                         #  costruttore dell'istanza
        logger.debug(self.__class__.__name__ + ".__init__")
        self._db = db.get_db()
        self._db.row_factory = _dict_factory
        desc = self._db.execute(
            f"pragma table_info('{self._tablename}')").fetchall()
        self._columns = [d['name'] for d in desc]

    def __call__(self, *args, **kwds):          
        logger.debug("args: " + repr(args))
        logger.debug("kwds: " + repr(kwds))
        pass

    def get_all(self):      # restituisce il contenuto della tabella (o tabelle) usando la query definita nel campo _query
        logger.debug(self.__class__.__name__ + ".get_all();")
        query = self._query.format(tablename=self._tablename)
        rows = self._db.execute(query).fetchall()
        return self._format(rows)

    def has(self, id):      # controlla se la riga con _pkey == id sia presente nella tabella
        logger.debug(f"{self.__class__.__name__}.has({id});")
        query = f"SELECT id FROM {self._tablename} WHERE id = '{id}'"
        result = self._db.execute(query).fetchone()
        if result:
            return True
        return False

    def new_element(self, **kwargs):
        """Crea una nuova istanza di un oggetto della classe di risorse (_kind) assegnata alla collection"""
        logger.debug(f"{self.__class__.__name__}.new_element())")
        if self._kind:
            return self._kind(**kwargs)

    def kind(self):
        """Restituisce il NOME della classe di oggetti contenuti nella collezione"""
        return self.__class__.__name__

    def get(self, value):
        """Restituisce un oggetto che ha _pkey == value"""
        if self._kind:
            return self._kind(id=value)

    def find(self, **kwargs):
        """Restituisce una singola riga della tablla sottostante che soddisfano i criteri espressi negli argomenti (kwargs)"""
        logger.debug(self.__class__.__name__ + f".filter({kwargs});")
        query_prefix = f"SELECT id FROM {self._tablename} WHERE "
        query_where_list = set()
        for p, v in kwargs.items():
            if p in self._columns:
                query_where_list.add(f"{p} = '{v}'")
        query = query_prefix + ' AND '.join(query_where_list)
        logger.debug("query: " + query)
        cursor = self._db.execute(query)
        resultset = cursor.fetchone()
        logger.debug("resultset: " + pformat(resultset))
        result_obj = self._kind(id=resultset.get('id'))
        return result_obj

    def filter(self, **kwargs):
        """Restituisce come list of dict tutte le righe della tablla sottostante che soddisfano i criteri espressi negli argomenti (kwargs)"""
        logger.debug(self.__class__.__name__ + f".filter({kwargs});")
        query = self._query_filter.format(tablename=self._tablename) + " WHERE "
        if 'user' in kwargs:
            query = f"{query} {self._user_fkey} = '{kwargs['user']}'"
        query_where_list = set()
        for p, v in kwargs.items():
            if p in self._columns:
                query_where_list.add(f"{p} LIKE '{v}'")
        query = query + ' AND '.join(query_where_list)
        logger.debug("query: " + query)
        cursor = self._db.execute(query)
        resultset = cursor.fetchall()
        logger.debug("resultset: " + pformat(resultset))
        return self._format(resultset)

    def delete(self, **kwargs):
        """Operazione di cancellazione di una o più risorse dalla collezione.
           Per questioni di sicurezza, non ha una implementazione di default.
        """
        raise NotImplementedError

    def _format(self, data):
        return data

    # def add(self, **kwargs):
    #     logger.debug(self.__class__.__name__ + f".add({kwargs});")
    #     return { 'query': query }


class ResourceBase():
    """Classe base per una sinogla risorsa. Rappresenta una riga in una tabella (o join tra tabelle)"""
    _db = None
    "protetto: Connessione al DB."
    _pkey = 'id'
    "protetto: chiave primaria della riga."
    _tablename = 'dual'
    "protetto: nome della tabella della risorsa."
    _extra_operations = []
    _collection = CollectionBase
    "protetto: nome della collezione a cui questa risorsa appartiene."
    _id = None
    "protetto: identificativo dell'oggetto."
    # _query = "SELECT * FROM {self._tablename} WHERE {self._pkey} = {value}"
    _query = "SELECT * FROM {tablename} WHERE {pkey} = {value}"
    "protetto: template della query sul db per recuperare il singolo oggetto."
    _data = dict()  # contains data to/from table
    "protetto: dati dell'oggetto, sono i valori delle colonne recuperate con la query"
    _owner = None
    "protetto: proprietario del dato. Usato per le funzionalità di sicurezza, se implementata"
    _user_fkey = 'user_id'
    "protetto: campo sulal tabella che indica il riferimento all'utente. Usato per la sicurezza, se implementata."

    def __init__(self, id=None, data=dict()):
        """Costruttore dell'oggetto. Crea o ottiene un oggetto:
            - se è specificato `id`: si leggono i dati dalla tabella dove _pkey == id e si inizializza l'oggetto con essi.
            - se è specficiato `data`: si crea un nuovo oggetto (non ancora persistente) con i dati specificati."""
        logger.debug(self.__class__.__name__ + ".__init__")
        self._db = db.get_db()
        self._db.row_factory = _dict_factory
        desc = self._db.execute(
            f"pragma table_info('{self._tablename}')").fetchall()
        self._columns = [d['name'] for d in desc]
        if id and data:
            raise ValueError(
                "'id' and 'data' argument cannot be used together.")
        if id and not data:  # Read object from table
            query = self._query.format(
                tablename=self._tablename, pkey=self._pkey, value=id)
            data_from_table = self._from_table(id, query)
            if not data_from_table:
                msg = f"Object with id {id} does not exists."
                logger.error(msg)
                raise ValueError(msg)
            self._data = self._format(data_from_table)
            self._id = self._data[self._pkey]
            logger.debug("Object read from table: " + pformat(self._data))
        if data and not id:  # New object
            for c in data:
                if c in self._columns:
                    self._data[c] = data[c]
            logger.debug("Created new (unsaved) object: " + pformat(self._data))
        logger.debug("Object: " + pformat(self.serialize()))

    def _sync_obj(self):
        query = self._query.format(
        tablename=self._tablename, pkey=self._pkey, value=self._id)
        self._data = self._format(self._from_table(id, query))
        self._id = self._data[self._pkey]

    def _format(self, data):
        return data

    def _from_table(self, value, query=None):
        """Funzione di comodo che esegu una query sulla tabella sottostante."""
        logger.debug("query: " + query)
        resultset = self._db.execute(query).fetchone()
        logger.debug("resultset: " + pformat(resultset))
        return resultset

    def serialize(self):
        """Funzionae che può essere sovrascritta per restituire una cerca rappresentazione dell'oggetto."""
        return self._data

    def operation(self, op_name):
        logger.debug(f"op_name='{op_name}'")
        if op_name in self._extra_operations:
            return getattr(self, op_name)
        else:
            return None

    def owned_by(self, user_id):
        """Restituisce i dati dell'utente a cui questo oggetto appartiene."""
        logger.debug(self.__class__.__name__ + f".owned_by({user_id})")
        if self._data.get(self._user_fkey, False) == user_id:
            return True
        return False

    def save(self, **kwargs):
        """Salva l'oggetto sul database. Non ha un'implementazione di default per scelta."""
        raise NotImplementedError

    def update(self, **kwargs):
        """Aggiorna l'oggetto sul database. Non ha un'implementazione di default per scelta."""
        raise NotImplementedError

    def get_id(self):
        """Restituisce l'identificativo primario di questo oggetto. Corrisponde alla primary key sul db."""
        return self._id

    def get(self, attribute):
        """Recupera l'attributo specificato dai dati dell'oggetto stesso, ovvero restituisce il valore della colonna specificata per questa riga."""
        return self._data.get(attribute, None)

    def delete(self, **kwargs):
        """Elimina l'oggetto. Non ha un'implementazione di default per scelta."""
        raise NotImplementedError


CollectionBase._kind = ResourceBase

from . import resources
from . import bookings