# Fields

This submodule combines the electric and magnetic fields.

## List of Functions

| Function Name           | Description                                                             |
| ----------------------- | ----------------------------------------------------------------------- |
| `DataAvailability()`    | Checks what dates have data.                                            |
| `CalculateEx()`		  | Calculates the missing E field component in MGSE.						|
| `CombineFields()`		  | Combined electric and magnetic field data into one object.				|
| `GetData()`			  | Get data for more than one date.										|
| `ModelField()`		  | Uses Tsyganenko field models to obtain model magnetic field vectors.	|
| `ReadData()`			  | Reads a single data file.												|


## Usage

Get a list of dates where we have field data:
```python
dates = RBSP.Fields.DataAvailability(sc)
```

Combine electric and magnetic fields for a single date (note that EMFISIS, EFW data and field traces are needed):
```python
RBSP.Fields.CombineFields(20150101,'a')
```

Read combined field for a date:
```python
data = RBSP.Fields.ReadData(20140503,'b')
```

Read data between date/time limits of 20140101 12:30 to 20140103 8:15:
```python
data = RBSP.Fields.GetData([20140101,20140103],ut=[12.5,8.25],sc='a')
```