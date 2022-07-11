
import dataclasses
from os import getenv
from pyArango.connection import *


@dataclasses.dataclass
class Config:
    url: str | None = "http://127.0.0.1:8529"
    user: str | None = "root"
    password: str | None = ""
    database: str | None = "InsightsNet"
    graph: str | None = "InsightsNetGraph"
    autoconnect: bool = True

    def __post_init__(self):
        if self.url is None:
            self.url = getenv("ARANGO_URL")
        if self.user is None:
            self.url = getenv("ARANGO_USER")
        if self.password is None:
            self.password = getenv("ARANGO_PW")
        if self.database is None:
            self.database = getenv("ARANGO_DB")
        if self.graph is None:
            self.graph = getenv("ARANGO_GRAPH")
        if self.autoconnect:
            self.__connect()

    def __connect(self):
        self.db: Database = None
        self.__connection = Connection(self.url, self.user, self.password)
        if self.__connection.hasDatabase(self.database):
            self.db = self.__connection[self.database]
        else:
            self.db: Database = self.__connection.createDatabase(
                self.database)


def configuration(url: str | None = "http://127.0.0.1:8529",
                  user: str | None = "root",
                  password: str | None = "",
                  database: str | None = "InsightsNet",
                  graph: str | None = "InsightsNetGraph", connect=True, use_global_conf=False) -> Config:
    global global_conf
    if use_global_conf:
        if global_conf is not None:
            return global_conf
    conf = Config(url, user, password, database, graph, autoconnect=connect)
    if use_global_conf:
        global_conf = conf
    return conf