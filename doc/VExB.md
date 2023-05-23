# VExB

This submodule uses electric and magnetic fields to determine $\mathbf{E} \times \mathbf{B}$ drift, $V_{E\times B}$.

## List of Functions

|	Function	| 	Description |
|:--------------|:--------------|
| `VExB()`		| Calculate drift velocity vector. |
| `SaveData()`	| Save velocity data for a single date. |
| `ReadData()`	| Read the velocity data in for a single date. |

## Usage

Given arrays of electric field components `Ex`, `Ey` and `Ez` and magnetic field components `Bx`, `By` and `Bz`, calculate the velocity vectors:
```python
Vx,Vy,Vz = RBSP.VExB(Ex,Ey,Ez,Bx,By,Bz)
```

Save the field vectors for a single date:
```python
RBSP.SaveData(20170101,'a')
```

Read those vectors back in from file:
```python
data = RBSP.ReadData(20170101,'a')
```



