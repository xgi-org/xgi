rm -rf docs/build
rm -rf docs/source/api/classes
rm -rf docs/source/api/algorithms
rm -rf docs/source/api/generators
rm -rf docs/source/api/linalg
rm -rf docs/source/api/readwrite
rm -rf docs/source/api/utils

sphinx-apidoc -o docs/source/api/classes xgi/classes
sphinx-apidoc -o docs/source/api/algorithms xgi/algorithms
sphinx-apidoc -o docs/source/api/linalg xgi/linalg
sphinx-apidoc -o docs/source/api/generators xgi/generators
sphinx-apidoc -o docs/source/api/readwrite xgi/readwrite
sphinx-apidoc -o docs/source/api/utils xgi/utils
sphinx-build -b html docs/source docs/build