# NTA-GTFS-Conversion

Takes data from the NTA https://www.transportforireland.ie/transitData/PT_Data.html and converts it into other formats

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
