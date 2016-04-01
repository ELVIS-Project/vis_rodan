# VIS-Rodan
Wrappers for [VIS Framework](https://github.com/ELVIS-Project/vis-framework) to work in [Rodan](https://github.com/DDMAL/Rodan).

## Auto-generating wrappers
The files are split into scripts and wrappers. To auto-generate wrappers for resource distributors, the file in scripts/auto_distributor.py must be run.
auto_distributor.py reads from the resource_types.yaml file, which contains a list of all the different possible resources. From this, it creates a wrapper for each one. It first deletes the existing resource_distributors folder, and rebuilds it with the information in the yaml file, and the distributor template. 
Additionally, the wrappers are added to the folders __init__.py file so that they can be loaded when vis-rodan is started.