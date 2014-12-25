__author__ = 'kbroughton'

from sqlalchemy import Column, Table, MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum
from sqlalchemy.engine.reflection import Inspector

from functools import lru_cache
from datetime import datetime


engine = create_engine("postgresql://scott:tiger@localhost/test")
with engine.connect() as conn:
    conn.execute("SET search_path TO test_schema, public")
    meta = MetaData()
    referring = Table('referring', meta,
                      autoload=True, autoload_with=conn)


class Topology(object):
    """
    Extracts and holds information about relations in a schema.

    Uses column types, names, ddl's and primary/foreign key information
    to narrow the search of potential relations and then column x column
    intersections to determine degree and type of relatedness.


    If columns X and Y are related by a function T(X) -> Y,
    (usually the identity map), then the relation types are
    surjective -> for every y in Y,  there is an x in X with T(x) = y
                  If T = I, Y is a subset of X or equal to X
    injective -> the mapping is one to one
    bijective -> surjective and injective
    subset -> Y-X if X is a subset of Y, otherwise null
    superset -> X-Y if Y is a subset of X, otherwise null
    intersect -> X intersect Y

    If the intersect of X and Y is non-zero, then tables containing X and Y
    may be joined in a query.

    If X is a subset of Y then it is possible that Table(X) is generated
    by Table(Y).
    """

    def __init__(self, engine, schema):
        self._engine = engine
        self._schema = schema
        self._schema_tables=None

    @property
    def schema_tables(self):
        return self._schema_tables or Inspector.get_table_names(self._schema)

    def refresh_schema_tables(self):
        """
        Call to the database even if value is set
        :return: list of tables in schema
        """
        self._schema_tables = None
        return self.schema_tables

    def get_potential_constraints(self, strategy, table_pairs):
        """
        If a table ddl does not declare
        primary, foreign, unique, non null constraints
        suggest them.
        :param strategy:
        :table_pairs: list of table pairs to check for column relations
        :return: dictionary {(left_table,right_table): {
                                (left_column,right_column):
                                    ColumnRelations }
                                    }
        """

    def get_table_pairs(self, left_table_excludes = None,
                              right_table_excludes = None,
                              filter=None):
        """
        :param left_table_excludes: tables not to consider
        :param right_table_excludes: tables not to consider
        :return: list of table pairs
        """
        pairs = []
        for l_table in self.tables - left_table_excludes:
           for r_table in self.tables - right_table_excludes:
               if filter and filter(l_table, r_table):
                   pairs.append((l_table, r_table))
        return pairs


    def check_projections(self):
        """
        START_REFRESH is asynchronous and we need to wait
        until it projection creation is complete before
        using the projections
        """
        sql = "SELECT get_projections('customer_dimension');"


    def cardinality_fraction(self):
        """
        Cardinality measures the uniqueness of a column.
        0 = all repeated.  1 = all unique
        cardinality = COUNT(DISTINCT(Column))/COUNT(Column)
        """
        pass

    def create_simple_projection(self, table, columns):
        """
        Vertica uses projections instead of indexes.
        Leverage projections for doing column intersections.
        We probably want a projection on all columns we plan
        to intersect on.  We do not expose all the options
        of CREATE PROJECTION
        :param table: table name
        :param columns: list of columns
        """
        sql = """CREATE PROJECTION IF NOT EXISTS
                    :schema.:table.{projection_name}
                    AS SELECT {columns}
                    FROM {table}
            """.format(projection_name=str(datetime.now())+table,
                        columns=",".join(columns),
                        table=table
                       )

        cursor = conn.execute(
            sql.text(
                query,
                bindparams=[
                    sql.bindparam(
                        'schema', util.text_type(schema.lower()),
                        type_=sqltypes.Unicode)]
            )
        )
class TopoColumn(Column):
    """
    ABC for SqlAlchemy column with topological knowledge
    """

    def __init__(self, db_conn, column_id=None, schema=None, table=None, column=None):

        self.conn = db_conn
        if column_id in self.kwargs:
            self._orm_column_id = column_id
        else:
            if schema == None or table == None or column == None:
                raise
            self._orm_column_id = self._get_orm_column_id(schema, table, column)

        """number of columns in schema related to column"""
        self._link_rank = 0
        self._relations = self.find_column_relations(column_id, schema, table=None, column=None)

    @property
    def _get_orm_column_id(self, schema, table, column):
        raise NotImplementedError

    class RELATION_STRATEGY(Enum):
        COMPATIBLE_TYPES = 1
        SQL_HINTS = 2

    def get_link_rank(self, relation_strategy=RELATION_STRATEGY.COMPATIBLE_TYPES):
        """
        Link Rank is the number of columns in a schema that are related

        :param relation_strategy: Parameter indicating how to cacluate relations.  One of
         COMPATIBLE_TYPES = columns are of same type
         This will miss some relations if the JOIN ON includes a transformed column.
         This could be fixed by passing a second argument (column_transforms(type_src, type_dest))
         SQL_HINTS = ddl or query sql with join statements
        :return:
        """
        if relation_strategy == self.RELATION_STRATEGY.COMPATIBLE_TYPES:
            self._get_link_rank


    def find_column_relations(self, strelation_strategy):
        """
        Calculate the columns related to column_id

        :param column_id: unique identifier of column in database
        :param schema:
        :param table:
        :param column:
        :return: dictionary of {column_id: ColumnRelations object}
        """

class ColumnRelations(object):
    """
    Result from comparing/intersecting two columns returns
    ColumnRelations object
    """
    l_col = None
    r_col = None
    counts = {
        'left_minus_right': 0,
        'right_minus_left': 0,
        'left_total': 0,
        'left_distinct': 0,
        'right_total': 0,
        'right_distinct': 0,
        'intersect': 0
    }
    measures = {
        'left_cardinality': counts.left_distinct/counts.left_total,
        'right_cardinality': counts.right_distinct/counts.right_total,
        'left_in_over_out': counts.intersect/counts.left_minus_right,
        'right_in_over_out': counts.intersect/counts.right_minus_left
    }
    right_is_subset = False
    left_is_subset = False

