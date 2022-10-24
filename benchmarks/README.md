# Benchmarking with asv

## Install asv
Make sure that asv is installed by installing the requirements file with
```
pip install -r requirements/benchmarks.txt
```

or installing python in edit mode
```
pip install -e .["all"]
```

*All the following commands need to be run from the `benchmarks` directory.*

## Run benchmarks
Run the following commands, where ID1 is the latest commit hash on the main branch and ID2 is the latest commit hash on your development branch:
```
asv run ID1
asv run ID2
asv compare ID1 ID2
```

This will compare the most up-to-date version of XGI with your most recent changes.

*When you run these commands for the first time, you will need to create a machine profile for the computer on which you are running the benchmarks.*

## Visualize
First, run benchmarks on each release by running the following command:
```
asv run HASHFILE:releasehashes.txt
```
where `releasehashes.txt` contains the commit hashes of every release v0.4 and after. You can also run
```
asv run v0.4..main
```
to benchmark all the commits on main since v0.4. After the benchmarks have been run, we display a webpage with our results by running the following commands:
```
asv publish
asv preview
```

This will generate a website on your local machine for viewing.