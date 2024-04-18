# api auto

## Overview

This project is a pytest based framework using python's request pacakge designed for api testing. It follows a modular structure and includes packages for libs, tests and features.

## Project Structure

1. api_auto (root folder)
The root folder contains the entire project structure:
     
    - lib:
        - dataprovider:
            -  json test data under directories based on env e.g: live > user.json
            - has a data_provider singleton to parse static data
            - models to map the test data to. (User, Account)
            - handle between static and dynamic data
        - logger:
            - use for logging - currently only used for info logs
        - api_service_provider:
            - api_service : singleton wrapper for http requests & used for session management.
            - services : e.g account, user - children of api_service calling api_service
            - api_constants : paths etc stored.
        - utils:
            - constants - for overall project
            - helpers = wrapper and data generator methods

    -  features:
        -  Call Hierarchy: Tests > (Features) > lib 
        - Functionality wise 
        -  logic implementation for different features/ scenarios/ use cases

    -  tests:
        -  Test scripts for different scenarios
        - baseCase - parent of all tests. 
    - reports:
        - using pytest-html package, easy to setup as descried below.
    - conftest:
        -  update pytest run configuration for request session management
   

## Convention

- Tests can call features and lib (dataprovider, api_provider etc)
- Its better to move assertions outside of tests (WIP)

## Getting Started

Pre-requisite
```sh
python 3 or above
```
Clone the repo.

```sh
git clone git@github.com:sajManzoor/api_auto.git 
```

Create a python virtual environment:
```sh
python3 -m venv venv
source venv/bin/activate
```

Install all requirements:
```sh
pip install -r requirements.txt
```


Run all tests:
```sh
pytest path/to/tests
```

Run all tests and generate reports:
```sh
pytest tests --html=reports/test_run.html
```
