# NTA-GTFS-Conversion

Takes data from the NTA https://www.transportforireland.ie/transitData/PT_Data.html and converts it into other formats. At the moment the main.py takes in GTFS txt files and connects
stop times to the route they belong to.

## Running
First you will need python 3 to be installed.
Then it should be as simple as running
```shell
python main.py {input_folder} {output_folder}
```
Where input_folder is where all the GTFS txt files are present,
output_folder is where all the json output will go.
It should parse the GTFS txt files into corresponding python objects
then output results of each parsed txt file to a json folder.

## Testing

All unit tests should reside in the test/ folder and make use of the unittest framework.
The module they are testing should be in the form test_{module_name}.py
When running tests can run them all at once with command:

```shell
python -m unittest
```

If you want to run a specific module you will need to something in the form

```shell
 python -m unittest -v src.tests.{module_path}
```
