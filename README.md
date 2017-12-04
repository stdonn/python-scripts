# python-scripts

This repository is a set of python scripts with different aim, but mainly to simplify data transfers, modelling process or similar issues.  
It is devided in two parts: On part with scripts which requires ESRIs ArcGIS and one part which run in a terminal or command line.

**ATTENTION**  
The scripts are not tested in detail, they are developed until they work for the current purpose. I highly recommened to use this scripts only if you are familiar with python scripting to solve and recognize errors or failures for yourself.

## Usage

Scripts in the ArcGIS-Scripts folder have to be used with ESRIs ArcGIS. For some script a toolbox item is available, some have to be run in the arcgis console. The scripts ArcGIS scripts were used with python 2.7 and ESRIs ArcGIS 10.5. 

Script inside the cmd-Scripts folder have to be run in a command line or terminal. Most of the scripts should work with python 2.7 and python 3.5.

Hence ESRIs ArcGIS is only working on Windows platforms, the associated scripts also work only on Windows, whereas the most of the commandline scripts should work on all platforms where python works.

## ArcGIS-Scripts

Currently nothing in here, but this will follow soon...

## cmd-Scripts

**Split_GOCAD_PLines.py**

Splits an SKUA-GOCAD Ascii file with multiple PLine objects (curves) inside in multiple files each containing one PLine object. The output files will be saved in the subdirectory out/ inside the input file containing folder.

```
python3 Split_GOCAD_PLines.py <InputFile.ts>
``` 

**Split_GOCAD_TSurfs.py**

Splits an SKUA-GOCAD Ascii file with multiple TSurf objects (surfaces) inside in multiple files each containing one TSurf object. The output files will be saved in the subdirectory out/ inside the input file containing folder.

```
python3 Split_GOCAD_TSurfs.py <InputFile.ts>
``` 

## Built With

* [Python 2 and Python 3](http://www.python.org/)
* [ESRI ArcGIS](https://www.esri.com/)

## Authors

* Stephan Donndorf - [stdonn](https://github.com/stdonn)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
