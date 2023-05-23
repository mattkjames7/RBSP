# RBSP
Some tools for loading RBSP (Van Allen Probe) data. 

## Installation

Firstly, install the Python wheel package:
```python
pip3 install wheel --user
```


Clone this repo, build and install (swap x.x.x for the current version):
```bash
git clone git@github.com:mattkjames7/RBSP.git
cd RBSP

#build the wheel
python3 setup.py bdist_wheel

#install the package just built
pip3 install dist/RBSP-0.0.1-py3-none-any.whl --user
```

## Submodules

This is a list of submodules contained within this package.

- [ECT](doc/ECT.md)
- [EFW](doc/EFW.md)
- [EMFISIS](doc/EMFISIS.md)
- [Fields](doc/Fields.md)
- [Pos](doc/Pos.md)
- [RBSPICE](doc/RBSPICE.md)
- [RPS](doc/RPS.md)
- [VExB](doc/VExB.md)

