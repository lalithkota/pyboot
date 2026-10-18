# Pyboot
[![Pre-commit Status](https://github.com/lalithkota/pyboot/actions/workflows/pre-commit.yml/badge.svg?branch=develop)](https://github.com/lalithkota/pyboot/actions/workflows/pre-commit.yml?query=branch%3Adevelop)
[![Build Status](https://github.com/lalithkota/pyboot/actions/workflows/test.yml/badge.svg?branch=develop)](https://github.com/lalithkota/pyboot/actions/workflows/test.yml?query=branch%3Adevelop)
[![codecov](https://codecov.io/gh/lalithkota/pyboot/branch/develop/graph/badge.svg)](https://codecov.io/gh/lalithkota/pyboot)

Pyboot is a collection of python libraries/packages that are used to bootstrap python applications of different types like API backends, database elements, background job runners etc.<br>
Pyboot allows developers to write modular python application, that are easily extensible by implementors, and easily packagable into a larger app.<br>
Pyboot goes with a fully object-oriented IOC approach to application development.

## Available Python Modules

addon | summary
----- | -------
[pyboot-core](pyboot-core/) | Library implementing core IOC elements
[pyboot-db](pyboot-db/) | Library implementing basic DB elements
[pyboot-fastapi](pyboot-fastapi/) | Library implementing basic FastAPI elements
[pyboot-fastapi-auth](pyboot-fastapi-auth/) | API Auth Library

## Documentation

Refer to [docs](https://lalithkota.github.io/pyboot/docs)

## Acknowledgments & Licensing

A few modules in this project are derived from [OpenG2P/openg2p-fastapi-common](https://github.com/OpenG2P/openg2p-fastapi-common) under the MPL 2.0 license. To maintain consistency and avoid mixed-license complexity within this codebase, all modules in this repository are distributed under the [**Mozilla Public License 2.0 (MPL 2.0)**](LICENSE).
