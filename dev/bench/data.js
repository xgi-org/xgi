window.BENCHMARK_DATA = {
  "lastUpdate": 1746360095417,
  "repoUrl": "https://github.com/xgi-org/xgi",
  "entries": {
    "XGI Benchmarks": [
      {
        "commit": {
          "author": {
            "email": "nicholas.landry.91@gmail.com",
            "name": "Nicholas Landry",
            "username": "nwlandry"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "429ea3283c999482af9e2bb9d3954bd61513ffd4",
          "message": "Update tensor.py\n\nFix #674",
          "timestamp": "2025-05-04T08:00:38-04:00",
          "tree_id": "f611797ef60919c7957a2dfdef4a291d88b47f41",
          "url": "https://github.com/xgi-org/xgi/commit/429ea3283c999482af9e2bb9d3954bd61513ffd4"
        },
        "date": 1746360093622,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/algorithms.py::test_connected",
            "value": 93.87386216065892,
            "unit": "iter/sec",
            "range": "stddev: 0.00016985512413491676",
            "extra": "mean: 10.65259250001418 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/algorithms.py::test_clustering_coefficient",
            "value": 60.731885294058266,
            "unit": "iter/sec",
            "range": "stddev: 0.0003905085403583234",
            "extra": "mean: 16.465815200007228 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgelist",
            "value": 28.435295326250227,
            "unit": "iter/sec",
            "range": "stddev: 0.0423436892225592",
            "extra": "mean: 35.16756159999659 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgedict",
            "value": 28.13843291856048,
            "unit": "iter/sec",
            "range": "stddev: 0.03887888565058615",
            "extra": "mean: 35.53858179999736 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_df",
            "value": 22.61368490750987,
            "unit": "iter/sec",
            "range": "stddev: 0.03367136723391091",
            "extra": "mean: 44.22101059999761 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_memberships",
            "value": 1234.6331386368213,
            "unit": "iter/sec",
            "range": "stddev: 0.00002264693474575265",
            "extra": "mean: 809.9572000020316 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_members",
            "value": 134.65467270570596,
            "unit": "iter/sec",
            "range": "stddev: 0.0006264229470696664",
            "extra": "mean: 7.426403999997433 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_attributes",
            "value": 15194.958919442584,
            "unit": "iter/sec",
            "range": "stddev: 0.0000027628951831139724",
            "extra": "mean: 65.81130000427038 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_attributes",
            "value": 263.8267232516791,
            "unit": "iter/sec",
            "range": "stddev: 0.00006254630970429469",
            "extra": "mean: 3.7903665999976965 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_degree",
            "value": 10729.015120682592,
            "unit": "iter/sec",
            "range": "stddev: 0.000011559221206338634",
            "extra": "mean: 93.20519998823329 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_nodestats_degree",
            "value": 9612.861239300244,
            "unit": "iter/sec",
            "range": "stddev: 0.000004255693128848501",
            "extra": "mean: 104.02730000009797 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_size",
            "value": 250.16306879647243,
            "unit": "iter/sec",
            "range": "stddev: 0.0001274705804792684",
            "extra": "mean: 3.9973925999987614 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_isolates",
            "value": 8597.225159413876,
            "unit": "iter/sec",
            "range": "stddev: 0.000005504108387653416",
            "extra": "mean: 116.31660000261945 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_singletons",
            "value": 188.77888135191645,
            "unit": "iter/sec",
            "range": "stddev: 0.00011605756051870501",
            "extra": "mean: 5.297202699998138 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_copy",
            "value": 11.75181751200504,
            "unit": "iter/sec",
            "range": "stddev: 0.05933538322191495",
            "extra": "mean: 85.09322060000102 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_dual",
            "value": 11.746244310170416,
            "unit": "iter/sec",
            "range": "stddev: 0.0653541273942137",
            "extra": "mean: 85.13359450000166 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_erdos_renyi",
            "value": 50.23337723796676,
            "unit": "iter/sec",
            "range": "stddev: 0.0010982570920064928",
            "extra": "mean: 19.907082800003195 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_fast_erdos_renyi",
            "value": 34.27189898947603,
            "unit": "iter/sec",
            "range": "stddev: 0.002192068326892624",
            "extra": "mean: 29.178423999996994 msec\nrounds: 10"
          }
        ]
      }
    ]
  }
}