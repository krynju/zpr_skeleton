# info

This project contains:

1. Python bindings for C++ code (using [`pybind11`](http://pybind11.readthedocs.io/en/stable/index.html) and built with [CMake](http://cmake.org))
2. Unit tests for C++ code (using [`catch`](http://catch-lib.net))
3. Unit tests for Python code (using `unittest`)
4. A `setuptools` setup.py script for building, installation, and testing


## clone and prepare the environment

Main dependencies: Python3.7

On windows run from *Developer Command Prompt for VS 2017* for cl.exe environment variables or just run it from Powershell

When cloning remember about `--recursive flag`

`git clone --recursive https://github.com/krynju/zpr_skeleton`

Create a python3.7 venv and activate it

`python3.7 -m venv venv`

shell `source venv/bin/activate`

cmd `bin/Scripts/activate`


Install other requirements 

`pip -r install requirements.txt`


Build the frontend (requires nodejs and npm)

`python setup.py site` -- necessary to build the frontend


## run

Run all tests

`python setup.py test`

Install and run

`python setup.py site` -- necessary to build the frontend

`python setup.py install`

`python -m distribution`




