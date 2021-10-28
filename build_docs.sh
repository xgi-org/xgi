rm -rf docs/build
rm -rf docs/source/api/classes
rm -rf docs/source/api/algorithms
rm -rf docs/source/api/generators
rm -rf docs/source/api/linalg
rm -rf docs/source/api/readwrite
rm -rf docs/source/api/utils

sphinx-apidoc -o docs/source/api/classes hypergraph/classes
sphinx-apidoc -o docs/source/api/algorithms hypergraph/algorithms
sphinx-apidoc -o docs/source/api/linalg hypergraph/linalg
sphinx-apidoc -o docs/source/api/generators hypergraph/generators
sphinx-apidoc -o docs/source/api/readwrite hypergraph/readwrite
sphinx-apidoc -o docs/source/api/utils hypergraph/utils
sphinx-build -b html docs/source docs/build