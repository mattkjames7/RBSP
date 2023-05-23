# EMFISIS - Electric and Magnetic Field Instrument Suite and Integrated Science

The details of this instrument can be found in Kletzing et al., 2013.

## List of Functions

| Function Name           | Description                                                             |
| ----------------------- | ----------------------------------------------------------------------- |
| `DownloadData()`        | Download latest data files.                                             |
| `ReadCDF()`             | Read a downloaded CDF file.                                             |
| `DataAvailability()`    | Checks what dates have data.                                            |
| `DeleteDate()`          | Deletes data from a specific date.                                      |
| `RebuildDataIndex()`    | Scan the downloaded data and rebuild the index file.                    |
| `GetMag()`			  | Get the magnetometer data. 												|
| `ReadElectronDensity()` | Get the UHR electron density.											|


## Downloading Data

The data can be downloaded using the following data levels and products, `L` and `Prod`:

| `L`      | `Prod`  | Description |
| ---------|-------- | ----------- |
| `'l4'` |	`None`	|	densities |
| `'l3'` |	`'1sec-***'` |	1-second resolution magnetic fields |
| `'l3'`	 |	`'4sec-***'`	| 4-second resolution magnetic fields |
| `'l3'`	 |	`'hires-***'`	| High resolution magnetic fields |
| `'l2'`	|	`'HFR-spectra'` | |
| `'l2'`	|	`'HFR-spectra-merged'` | |
| `'l2'`	|	`'HFR-spectra-burst'` | |
| `'l2'`	|	`'HFR-waveform'` |  |
| `'l2'`	|	`'WFR-spectral-matrix'` | | 
| `'l2'`	|	`'WFR-spectral-matrix-burst'` |  |
| `'l2'`	|	`'WFR-spectral-matrix-burst-diagonal'` |  |
| `'l2'`	|	`'WFR-spectral-matrix-diagonal-merged'` |  |
| `'l2'`	|	`'WFR-spectral-matrix-diagonal'` |  |
| `'l2'`	|	`'WFR-waveform'` |  |
| `'l2'`	|	`'WFR-waveform-continuous-burst'` |  |

Note that `***` in the above table should be replaces with the coordinate system to be used, e.g. `gsm`, `gse`, etc.

## Mag Data

Magnetometer data can be obtained using `GetMag()` once it has been downloaded, e.g.:

```python
data = RBSP.EMFISIS.GetMag(Date,sc,ut=[ut0,ut1],Coord='GSE',Res='1sec')
```

where `Date` may be a range or a single date; `ut` will limit the start and end times (in hours); `Coord` can be one of the following strings `'GSE'|'GSM'|'SM'|'GEO'|'GEI'`; and Res may be `'1sec'|'4sec'|'hires'`.

## Electron Densities

Electron densities may be read from the `l4` data using the `ReadElectronDensity()` function, e.g.:
```python
data = RBSP.EMFISIS.ReadElectronDensity(Date,sc)
```
