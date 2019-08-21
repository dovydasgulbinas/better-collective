import os
import time
import json
from collections import namedtuple

import agate
import agatesql  # this import is needed since it overrides agate namespace
from csvkit.cli import CSVKitUtility
from sqlalchemy import create_engine


class CSVDBLoader(CSVKitUtility):

    DB_NAME = '.database.db'
    Field = namedtuple('Field', 'name is_multi')

    def add_arguments(self):
        """We Add or Override CLI flags here"""
        self.argparser.add_argument('--run-analysis', dest='run_analysis',
                                    help='Executes Better Collective Analysis',
                                    action='store_true')

        self.argparser.add_argument('--output-file', dest='output_file',
                                    help='Where the analysis file will be stored if path is not supplied the output will be printed')

        self.argparser.add_argument('-y', '--snifflimit', dest='sniff_limit',
                                    type=int,
                                    help='Limit CSV dialect sniffing to the specified number of bytes. Specify "0" to disable sniffing entirely.')

        self.argparser.add_argument('--chunk-size', dest='chunk_size',type=int,
                                    help='Chunk size for batch insert into the table.')

        self.argparser.add_argument('-I', '--no-inference', dest='no_inference', action='store_true',
                                    help='Disable type inference when parsing the input.')


    def _init_connection(self):

        try:
            engine = create_engine(self.connection_string)
        except ImportError:
            raise ImportError("Wrong database dialect selected")
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
            sniff_limit=self.args.sniff_limit,
            column_types=self.get_column_types(),
            skip_lines=self.args.skip_lines,
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

    def serialize_and_store(self, serializable_ob):

        json_ob = json.dumps(serializable_ob,  indent=4, sort_keys=True)
        # let's prettify the json

        if self.args.output_file:
            print(f'Exported JSON to: {self.args.output_file}')
            with open(self.args.output_file, 'w') as file:
                file.write(json_ob)
        else:
            print(json_ob)

    def select_and_restructure(self, query: str, description: str,
                               fields: list):
        result = dict()
        result['__meta__'] = {}
        meta = result['__meta__']
        meta['query'] = query
        meta['description'] = description

        start = self.time_it()
        rows = self.connection.execute(query)
        delta = self.time_it(start)
        meta['duration_s'] = delta

        # Initialize fields arrays since .append() will not work for None type
        for field in fields:
            result[field.name] = list()

        for row in rows:
            for field in fields:
                result[field.name].append(row[field.name])

        # Let's squash lists since methods like count(*) generate same values
        # In the whole table
        for field in fields:
            if not field.is_multi:
                # Extract only 1st element because others repeat themselves.
                result[field.name] = result[field.name][0]

        return result

    def query_list(self):

        result = list()
        result.append(self.select_and_restructure(
            f'''select "Address" from "{self.table_name}" \
where "Address" LIKE "%interwetten-news%";''',
            "contains: `interwetten-news`",
            [self.Field("Address", is_multi=True)]
        ))

        result.append(self.select_and_restructure(
        f'''select count(*) as "Number Of Pages", "Address" from "{self.table_name}" \
where  "Inlinks" > 1 and "Status Code" = 302 and \
"Redirect URL" like "%plus.google.com%";''',
            "Inlinks to plus.google.com",
            [
                self.Field("Address", is_multi=True),
                self.Field("Number Of Pages", is_multi=False),
            ]
        ))

        result.append(self.select_and_restructure(
            f'''select "Title 1" from "{self.table_name}" where \
"Title 1 Length" > 65 and \
("Title 1 Pixel Width" < 550 or "Title 1 Pixel Width" > 700 ) \
and "Title 1" like "%2018%"''',
            "Titles with length > 65 ...",
            [
                self.Field("Title 1", is_multi=True),
            ]
        ))

        return result

    def run_analysis(self):
        print("Running Tasked Analysis...")
        # Let's create a table name
        self.connection_string = f'sqlite:///{self.DB_NAME}'
        self._build_table_name()
        self._init_connection()
        print("Building Database...")
        self._build_db()
        result_list = self.query_list()
        self.serialize_and_store(result_list)

        if self.connection:
            self.connection.close()

    def main(self):
        if self.args.run_analysis:
            self.run_analysis()


def launch_new_instance():
    utility = CSVDBLoader()
    utility.run()


if __name__ == "__main__":
    launch_new_instance()
