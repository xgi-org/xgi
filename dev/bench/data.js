window.BENCHMARK_DATA = {
  "lastUpdate": 1745602490661,
  "repoUrl": "https://github.com/xgi-org/xgi",
  "entries": {
    "XGI Benchmarks": [
      {
        "commit": {
          "author": {
            "name": "Nicholas Landry",
            "username": "nwlandry",
            "email": "nicholas.landry.91@gmail.com"
          },
          "committer": {
            "name": "GitHub",
            "username": "web-flow",
            "email": "noreply@github.com"
          },
          "id": "a18bb9116087e03eea48bb0e335688042444559f",
          "message": "Improved the hypergraph equality method (#671)\n\n* Improved the hypergraph equality method\n\n* added unit tests\n\n* add docstring\n\n* response to review\n\n* added docstring",
          "timestamp": "2025-04-25T17:04:37Z",
          "url": "https://github.com/xgi-org/xgi/commit/a18bb9116087e03eea48bb0e335688042444559f"
        },
        "date": 1745602487939,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/algorithms.py::test_connected",
            "value": 89.57922140441754,
            "unit": "iter/sec",
            "range": "stddev: 0.00035250850852660057",
            "extra": "mean: 11.16330310000535 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/algorithms.py::test_clustering_coefficient",
            "value": 59.123420791258994,
            "unit": "iter/sec",
            "range": "stddev: 0.0005627319281012768",
            "extra": "mean: 16.91377100000011 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgelist",
            "value": 26.94404671813005,
            "unit": "iter/sec",
            "range": "stddev: 0.04688798842118254",
            "extra": "mean: 37.1139499000023 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgedict",
            "value": 26.957981516176414,
            "unit": "iter/sec",
            "range": "stddev: 0.0421882739331835",
            "extra": "mean: 37.09476539999628 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_df",
            "value": 20.726050545986837,
            "unit": "iter/sec",
            "range": "stddev: 0.039323479225585885",
            "extra": "mean: 48.248459000001276 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_memberships",
            "value": 1087.3163998276207,
            "unit": "iter/sec",
            "range": "stddev: 0.00006577392817714073",
            "extra": "mean: 919.695500002149 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_members",
            "value": 129.41647302936838,
            "unit": "iter/sec",
            "range": "stddev: 0.000653004327642498",
            "extra": "mean: 7.72699160000343 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_attributes",
            "value": 11892.854891727937,
            "unit": "iter/sec",
            "range": "stddev: 0.000008159786641728164",
            "extra": "mean: 84.08409999987043 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_attributes",
            "value": 255.33007923646943,
            "unit": "iter/sec",
            "range": "stddev: 0.0001451963393148609",
            "extra": "mean: 3.9164990000017497 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_degree",
            "value": 9198.455763313978,
            "unit": "iter/sec",
            "range": "stddev: 0.000015300747752773958",
            "extra": "mean: 108.71389999920211 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_nodestats_degree",
            "value": 7698.590926935556,
            "unit": "iter/sec",
            "range": "stddev: 0.000012421127482462453",
            "extra": "mean: 129.89389999944478 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_size",
            "value": 222.21983706258987,
            "unit": "iter/sec",
            "range": "stddev: 0.00017192397187015048",
            "extra": "mean: 4.5000483000009694 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_isolates",
            "value": 7144.005286729974,
            "unit": "iter/sec",
            "range": "stddev: 0.000009958401199901624",
            "extra": "mean: 139.97749999674625 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_singletons",
            "value": 169.2482525752262,
            "unit": "iter/sec",
            "range": "stddev: 0.00014737818740296702",
            "extra": "mean: 5.90848050000119 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_copy",
            "value": 10.632930719573237,
            "unit": "iter/sec",
            "range": "stddev: 0.07042400199862052",
            "extra": "mean: 94.0474481000038 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_dual",
            "value": 10.886197374563547,
            "unit": "iter/sec",
            "range": "stddev: 0.07434510015179605",
            "extra": "mean: 91.85944050000217 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_erdos_renyi",
            "value": 50.85644413318867,
            "unit": "iter/sec",
            "range": "stddev: 0.0012664560612214843",
            "extra": "mean: 19.663191500001176 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_fast_erdos_renyi",
            "value": 34.40796188126349,
            "unit": "iter/sec",
            "range": "stddev: 0.0019507159656520648",
            "extra": "mean: 29.06304079999984 msec\nrounds: 10"
          }
        ]
      }
    ]
  }
}