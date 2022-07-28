import dataclasses
from os import getenv
from pyArango.connection import *
from arango import ArangoClient


@dataclasses.dataclass
class Config:

    url: "str | None" = None
    user: "str | None" = None
    password: "str | None" = None
    database: "str | None" = None
    graph: "str | None" = None
    autoconnect: bool = True

    def __post_init__(self):
        if self.url is None:
            self.url = getenv("ARANGO_URL", "http://127.0.0.1:8529")
        if self.user is None:
            self.user = getenv("ARANGO_USER", "root")
        if self.password is None:
            self.password = getenv("ARANGO_PW", "")
        if self.database is None:
            self.database = getenv("ARANGO_DB",  "_system")
        if self.graph is None:
            self.graph = getenv("ARANGO_GRAPH", "GenericGraph")
        if self.autoconnect:
            self.__connect()

    def __connect(self):
        self.db: Database = None
        self.__connection = Connection(self.url, self.user, self.password)
        self.arango_client = ArangoClient(self.url)
        if self.__connection.hasDatabase(self.database):
            self.db = self.__connection[self.database]
        else:
            self.db: Database = self.__connection.createDatabase(
                self.database)

        self.arango_db = self.arango_client.db(name=self.database,
                                               username=self.user,
                                               password=self.password)


global_conf = None


def configuration(url: "str | None" = None,
                  user: "str | None" = None,
                  password: "str | None" = None,
                  database: "str | None" = None,
                  graph: "str | None" = None, connect=True, use_global_conf=False) -> Config:
    """Start a new conenction using the provided config

    :param url: _description_, defaults to "http://127.0.0.1:8529"
    :type url: _type_, optional
    :param user: _description_, defaults to "root"
    :type user: str | None, optional
    :param password: _description_, defaults to ""
    :type password: str | None, optional
    :param database: _description_, defaults to "_system"
    :type database: str | None, optional
    :param graph: _description_, defaults to "GenericGraph"
    :type graph: str | None, optional
    :param connect: _description_, defaults to True
    :type connect: bool, optional
    :param use_global_conf: if you want re-use one global config, defaults to False
    :type use_global_conf: bool, optional 
    :return: the connected config
    :rtype: Config
    """
    global global_conf
    if use_global_conf:
        if global_conf is not None:
            return global_conf
    conf = Config(url, user, password, database, graph, autoconnect=connect)
    if use_global_conf:
        global_conf = conf
    return conf
