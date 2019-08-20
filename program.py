import os
import time

import agate
import agatesql  # noqa
from csvkit.cli import CSVKitUtility
from sqlalchemy import create_engine, dialects


class CSVDBLoader(CSVKitUtility):
    DB_NAME = 'database.db'

    def add_arguments(self):
        """We Add or Override CLI flags here"""
        self.argparser.add_argument('--run-analysis', dest='run_analysis',
                                    help='Executes Better Collective Analysis',
                                    action='store_true')

        self.argparser.add_argument('-y', '--snifflimit', dest='sniff_limit',
                                    type=int,
                                    help='Limit CSV dialect sniffing to the specified number of bytes. Specify "0" to disable sniffing entirely.')

        self.argparser.add_argument('--chunk-size', dest='chunk_size', type=int,
                                    help='Chunk size for batch insert into the table.')

        self.argparser.add_argument('-I', '--no-inference', dest='no_inference', action='store_true',
                                    help='Disable type inference when parsing the input.')

    def _init_connection(self):

        try:
            engine = create_engine(self.connection_string)
        except ImportError:
            raise ImportError(
                'You don\'t appear to have the necessary database backend installed for connection string you\'re trying to use. Available backends include:\n\nPostgresql:\tpip install psycopg2\nMySQL:\t\tpip install mysql-connector-python\n\nFor details on connection strings and other backends, please see the SQLAlchemy documentation on dialects at: \n\nhttp://www.sqlalchemy.org/docs/dialects/\n\n')
        except Exception as e:
            print(f'Could not init db engine: {e}')
        self.connection = engine.connect()

    def _build_table_name(self):
        filename = os.path.splitext(os.path.basename(self.args.input_path))[0]
        self.table_name = f'{filename}_{int(time.time())}'

    def _build_db(self):
        table = None

        table = agate.Table.from_csv(
            self.args.input_path,
            skip_lines=self.args.skip_lines,
            sniff_limit=self.args.sniff_limit,
            column_types=self.get_column_types(),
            **self.reader_kwargs
        )

        if table:
            table.to_sql(
                self.connection,
                self.table_name,
                create=True,
                create_if_not_exists=True,
                insert=len(table.rows) > 0,
                chunk_size=self.args.chunk_size
            )

    def time_it(self, start_time=None):

        if start_time:
            return time.perf_counter() - start_time
        else:
            return time.perf_counter()


    def run_analysis(self):
        print("Running Tasked Analysis")
        # Let's create a table name
        self.connection_string = f'sqlite:///{self.DB_NAME}'
        self._build_table_name()
        self._init_connection()
        print("Building Database")
        self._build_db()

        q1 = f'''select "Address" from "{self.table_name}" \
where "Address" LIKE "%interwetten-news%";'''


        start = self.time_it()
        rows = self.connection.execute(q1)
        delta = self.time_it(start)
        print(f'The query `{q1}` took: {delta} seconds')

        for row in rows:
            # TODO: Add to json
            print(row['Address'])

        q2 = f'''select count(*) as _count, "Address" from "{self.table_name}" \
where  "Inlinks" > 1 and "Status Code" = 302 and \
"Redirect URL" like "%plus.google.com%";'''


        start = self.time_it()
        rows = self.connection.execute(q2)
        delta = self.time_it(start)
        print(f'The query `{q2}`\ntook: {delta} seconds')

        for row in rows:
            # TODO: Add to json general function keys {colname, [values], many}
            print(row['_count'], row['Address'])


        q3 = f'''select "Title 1" from "{self.table_name}" where \
"Title 1 Length" > 65 and \
("Title 1 Pixel Width" < 550 or "Title 1 Pixel Width" > 700 ) \
and "Title 1" like "%2018%"'''


    def main(self):
        if self.args.run_analysis:
            self.run_analysis()


def launch_new_instance():
    utility = CSVDBLoader()
    utility.run()


if __name__ == "__main__":
    launch_new_instance()
