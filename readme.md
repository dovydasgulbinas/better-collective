# Better Collective Homework task

## TL;DR

Run required analysis by printing JSON to the terminal:

    python program.py --run-analysis --skip-lines=1 data/sportwettentest.csv

Run required analysis by storing JSON file to file:

    python program.py --run-analysis --skip-lines=1 --output-file=data/results.json  data/sportwettentest.csv

Get help about this CLI utility:

    python program.py --run-analysis --skip-lines=1 --output_file data/sportwettentest.csv

## About this program

This program is a comman line utility, that borrows heavily from the `csvkit.cli` base class.
The Idead begin this program can be boiled down to 3 simple steps:

1. Load CSV to SQLITE database (using sqlalchemy)
2. Run queries on SQLITE database (using sqlalchemy) & package the data to a
   serializable datatype using pythonic struture  list of Dicts `List[Dict]`
3. Reserialize to JSON format and dump it to a file or print it to the terminal.

## About the output result (report)  file

Why did I choose JSON file?

* Least verbose compared to (html, xml, csv & similar datatypes) 
* Is human readable
* Can be easily imported and navigated compared with XPATH notation.

considerations:

* report could be generated in any other serializable filetype simply by
    overloading `BetterCollectiveReporter.serialize_and_store()` method.
 
## What aspects could be improved?

* I could of used SQLAlchemy's ORM `Table` primitive and write data queries that way, but for purposes of this
demonstration I wanted do not abstract away the fact that I can write simple SQL
queries.
* Add a command line argument that would allow to execute and arbitrary query on
    the loaded data.

