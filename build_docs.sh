rm -rf docs/build
rm -rf docs/source/classes
rm -rf docs/source/algorithms
rm -rf docs/source/generators
rm -rf docs/source/linalg
rm -rf docs/source/readwrite
rm -rf docs/source/utils

sphinx-apidoc -o docs/source/classes hypergraph/classes
sphinx-apidoc -o docs/source/algorithms hypergraph/algorithms
sphinx-apidoc -o docs/source/linalg hypergraph/linalg
sphinx-apidoc -o docs/source/generators hypergraph/generators
sphinx-apidoc -o docs/source/readwrite hypergraph/readwrite
sphinx-apidoc -o docs/source/utils hypergraph/utils
sphinx-build -b html docs/source docs/build