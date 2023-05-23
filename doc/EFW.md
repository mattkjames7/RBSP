# EFW - Electric Field and Waves

The full documentation for this instrument can be found in Wygant et al., 2013.

## List of Functions

| Function Name           | Description                                                             |
| ----------------------- | ----------------------------------------------------------------------- |
| `DownloadData()`        | Download latest data files.                                             |
| `ReadCDF()`             | Read a downloaded CDF file.                                             |
| `DataAvailability()`    | Checks what dates have data.                                            |
| `DeleteDate()`          | Deletes data from a specific date.                                      |
| `RebuildDataIndex()`    | Scan the downloaded data and rebuild the index file.                    |
| `GetPotential()`		  | Get the spacecraft potential.											|
| `SavePotentials()`	  | Save spacecraft potentials for all dates.								|
| `ReadElectronDensity()` | Read the electron density calculated using UHR.							|

## Downloading Data

The data can be downloaded using the following data products, `L`:

| `L`                | Description |
| ------------------ | ----------- |
| `'l3'` | Spin-fit Electric field in modified-GSE (MGSE) coord, density, and other products |
| `'l2.spec'` | 8 second FFT power spectra |
| `'l2.e-spinfit-mgse'` | Spin-fit E12 Electric field in modified-GSE (MGSE) coordinates |
| `'l2.fbk'` | 8 sample/sec filterbank peak, average wave amplitude |
| `'l2.esvy_despun'` | 32 sample/sec despun electric field in modified-GSE (MGSE) coordinates |
| `'l2.vsvy-hires'` | 16 sample/sec single-ended V1-V6 probe potentials |
| `'l1.eb1'` | EB1 in UVW coordinates |
| `'l1.eb2'` | EB2 in UVW coordinates |
| `'l1.mscb1'` | MSCB1 in UVW coordinates | 
| `'l1.mscb2'` | MSCB2 in UVW coordinates | 
| `'l1.vb1'` | VB1 in UVW coordinates |
| `'l1.vb2'` | VB2 in UVW coordinates |

## Spacecraft Potentials

Spacecraft potentials need to be saved first using `SavePotentials()`, e.g.

```python
RBSP.EFW.SavePotentials(sc)
```

where `sc` can be `'a'` or `'b'`. This will save the potentials for every date found in the `l3` data.

Read the data using `GetPotential()`, e.g.:

```python
data = RBSP.EFW.GetPotential(Date,sc)
```

where `Date` may be a single date, a range of dates or a list of specific dates (e.g. `20140101`, `[20140101,20140104]` or `[20140101,20150101,20160101]`).

## Electron Density

The electron densities as measured using the upper hybrid resonance can be obtained using the `ReadElectronDensity()` function, which is a wrapper for the `ReadCDF()` function, e.g.:

```python
data = RBSP.EFW.ReadElectronDensity(Date,sc)
```

where `Date` is an integer date in the format YYYYMMDD. For this function to work, the `l4` data must be downloaded first.

