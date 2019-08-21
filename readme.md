# Better Collective Homework task

## TL;DR

Run required analysis by printing JSON to the terminal:

    python program.py --run-analysis --skip-lines=1 data/sportwettentest.csv

Run required analysis by storing JSON file to file:

    python program.py --run-analysis --skip-lines=1 --output-file=data/results.json  data/sportwettentest.csv

Get help about this CLI utility:

    python program.py --run-analysis --skip-lines=1 --output_file data/sportwettentest.csv

## About this program

This program is a command line utility, that borrows heavily from the `csvkit.cli.CSVKitUtility` base class.
The Idea behind this program can be boiled down to 3 simple steps:

1. Load CSV to SQLITE database (using SQLAlchemy)
2. Run queries on SQLITE database (using SQLAlchemy) & package the data to a
   serializable datatype using pythonic structure  list of Dicts `List[Dict]`
3. Reserialize to JSON format and dump it to a file or print it to the terminal.

## Why did I chose [`csvkit`][url-csvkit] ?

csvkit library is extremely well rounded and filled with various utilities.  Additionally csvkit uses [`agate`][url-agate] which is implemented purely in python this means that no additional dependency building will be required.


## About the output result (report)  file

Why did I choose JSON file?

* Least verbose compared to (html, xml, csv & similar data types)
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


[url-csvkit]: https://csvkit.readthedocs.io/en/0.9.0/index.html 
[url-agate]: https://agate.readthedocs.io/en/1.6.1/about.html