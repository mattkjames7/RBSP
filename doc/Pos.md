# Pos

This submodule get positional data for each spacecraft and can save field traces.

## List of Functions

| Function | Description |
|:---------|:------------|
| `CalculateVelocity()` | Calculate orbital velocity. |
| `ConvertH5toBinary()` | Converts the downloaded position data to binary. |
| `DownloadData()` | Downloads MagEph data. |
| `GetPos()` | Get all position data for a spacecraft. |
| `GetVelocity()` | Get all spacecraft velocities. |
| `PlotL()` | Plot the $L$-shell. |
| `PlotMLT()` | Plot magnetic local time. |
| `ReadFieldTraces()` | Read the field line footprints for a date. |
| `ReadAllFieldTraces()` | Real all the traces for a spacecraft. |
| `ReadH5()` | Read the downloaded H5 data directly. |
| `ReadPos()` | Read converted position binary data. |
| `SaveFieldTraces()` | Saves the field line footprints. |
| `TraceFieldDay()` | Performs field tracing for a day. |


## Usage

Download the position data first of all:
```python
RBSP.Pos.DownloadData(sc='a')
```

Now convert it to binary:
```python
RBSP.Pos.ConvertH5toBinary(sc='a')
```

Save the field line traces:
```python
RBSP.Pos.SaveFieldTraces(sc='a',Model='T96')
```

Read in position data for whole mission:
```python
posa = RBSP.Pos.GetPos(sc='a')
```

Get the velocity:
```python
vela = RBSP.Pos.GetVelocity(sc='a')
```

Get the field trace footprints:
```python
fpa = RBSP.Pos.ReadAllFieldTraces(sc='a',Model='T96')
```
