window.BENCHMARK_DATA = {
  "lastUpdate": 1748543474932,
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
      },
      {
        "commit": {
          "author": {
            "email": "nicholas.landry.91@gmail.com",
            "name": "Nicholas Landry",
            "username": "nwlandry"
          },
          "committer": {
            "email": "nicholas.landry.91@gmail.com",
            "name": "Nicholas Landry",
            "username": "nwlandry"
          },
          "distinct": true,
          "id": "2ff03712cd1c823a1cbf622718f17340a6839a85",
          "message": "Update references",
          "timestamp": "2025-05-29T10:08:59-04:00",
          "tree_id": "b8281a2f8d9fec1e591e9f623e760669a1cb17ce",
          "url": "https://github.com/xgi-org/xgi/commit/2ff03712cd1c823a1cbf622718f17340a6839a85"
        },
        "date": 1748527792389,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/algorithms.py::test_connected",
            "value": 94.46248446992185,
            "unit": "iter/sec",
            "range": "stddev: 0.0004516127312645748",
            "extra": "mean: 10.586213199997019 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/algorithms.py::test_clustering_coefficient",
            "value": 60.90415358655169,
            "unit": "iter/sec",
            "range": "stddev: 0.00033288909403114415",
            "extra": "mean: 16.4192413999956 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgelist",
            "value": 28.28595451510594,
            "unit": "iter/sec",
            "range": "stddev: 0.0417036170250321",
            "extra": "mean: 35.353235099984204 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgedict",
            "value": 28.031605444522167,
            "unit": "iter/sec",
            "range": "stddev: 0.03854769880952422",
            "extra": "mean: 35.67401810000206 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_df",
            "value": 22.504380342609416,
            "unit": "iter/sec",
            "range": "stddev: 0.033758574621877445",
            "extra": "mean: 44.43579359999603 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_memberships",
            "value": 1234.6582904107754,
            "unit": "iter/sec",
            "range": "stddev: 0.00002279129731020078",
            "extra": "mean: 809.9407000031533 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_members",
            "value": 132.94255136252858,
            "unit": "iter/sec",
            "range": "stddev: 0.0007090847009536687",
            "extra": "mean: 7.522046099995805 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_attributes",
            "value": 14537.482718176683,
            "unit": "iter/sec",
            "range": "stddev: 0.00000717177752382012",
            "extra": "mean: 68.78770000184886 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_attributes",
            "value": 247.37799731542137,
            "unit": "iter/sec",
            "range": "stddev: 0.0001837101226745333",
            "extra": "mean: 4.042396699998108 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_degree",
            "value": 10068.891353784125,
            "unit": "iter/sec",
            "range": "stddev: 0.000013483941272807978",
            "extra": "mean: 99.31580000852591 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_nodestats_degree",
            "value": 9243.673399201272,
            "unit": "iter/sec",
            "range": "stddev: 0.000009795228606897535",
            "extra": "mean: 108.18209999570172 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_size",
            "value": 247.76696308046337,
            "unit": "iter/sec",
            "range": "stddev: 0.00019772859700138324",
            "extra": "mean: 4.036050599995633 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_isolates",
            "value": 7566.219553274472,
            "unit": "iter/sec",
            "range": "stddev: 0.000007521307145325889",
            "extra": "mean: 132.16640000450752 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_singletons",
            "value": 177.30986256698628,
            "unit": "iter/sec",
            "range": "stddev: 0.00013443151714751742",
            "extra": "mean: 5.639844199993149 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_copy",
            "value": 11.381960207242352,
            "unit": "iter/sec",
            "range": "stddev: 0.061805740597029035",
            "extra": "mean: 87.858328599998 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_dual",
            "value": 11.646780272691624,
            "unit": "iter/sec",
            "range": "stddev: 0.06690492159524969",
            "extra": "mean: 85.86063930000591 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_erdos_renyi",
            "value": 51.318872704820116,
            "unit": "iter/sec",
            "range": "stddev: 0.0012283861450006065",
            "extra": "mean: 19.486008699993818 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_fast_erdos_renyi",
            "value": 33.37061865927394,
            "unit": "iter/sec",
            "range": "stddev: 0.0018330662320698969",
            "extra": "mean: 29.966480699994236 msec\nrounds: 10"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "nicholas.landry.91@gmail.com",
            "name": "Nicholas Landry",
            "username": "nwlandry"
          },
          "committer": {
            "email": "nicholas.landry.91@gmail.com",
            "name": "Nicholas Landry",
            "username": "nwlandry"
          },
          "distinct": true,
          "id": "1dd25d0b73507af53ffbe4631f4257f08c2f82aa",
          "message": "Fix affiliations",
          "timestamp": "2025-05-29T14:30:11-04:00",
          "tree_id": "27422f8a890778e42d47e398354d8362422f027a",
          "url": "https://github.com/xgi-org/xgi/commit/1dd25d0b73507af53ffbe4631f4257f08c2f82aa"
        },
        "date": 1748543472381,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/algorithms.py::test_connected",
            "value": 93.06056487654051,
            "unit": "iter/sec",
            "range": "stddev: 0.0012732765069088815",
            "extra": "mean: 10.745690199996716 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/algorithms.py::test_clustering_coefficient",
            "value": 60.5957339912588,
            "unit": "iter/sec",
            "range": "stddev: 0.0004070713553609541",
            "extra": "mean: 16.502811899997027 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgelist",
            "value": 28.938792569802764,
            "unit": "iter/sec",
            "range": "stddev: 0.04041960832852467",
            "extra": "mean: 34.55569189999608 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgedict",
            "value": 28.49554323007293,
            "unit": "iter/sec",
            "range": "stddev: 0.03755557656923393",
            "extra": "mean: 35.09320710000168 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_df",
            "value": 21.884074895015672,
            "unit": "iter/sec",
            "range": "stddev: 0.0358431313998302",
            "extra": "mean: 45.695328900001186 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_memberships",
            "value": 1167.5732678472027,
            "unit": "iter/sec",
            "range": "stddev: 0.000032240575509718775",
            "extra": "mean: 856.4773000017567 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_members",
            "value": 130.329634925762,
            "unit": "iter/sec",
            "range": "stddev: 0.000680751293284124",
            "extra": "mean: 7.672852000004582 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_attributes",
            "value": 13667.06483339168,
            "unit": "iter/sec",
            "range": "stddev: 0.00000787657026195858",
            "extra": "mean: 73.16860000230463 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_attributes",
            "value": 255.6544958342278,
            "unit": "iter/sec",
            "range": "stddev: 0.00005719002834191231",
            "extra": "mean: 3.911529099994482 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_degree",
            "value": 10670.855332222884,
            "unit": "iter/sec",
            "range": "stddev: 0.000015137649555487298",
            "extra": "mean: 93.71320000752803 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_nodestats_degree",
            "value": 9624.500127229176,
            "unit": "iter/sec",
            "range": "stddev: 0.000008164416775307307",
            "extra": "mean: 103.90150000318954 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_size",
            "value": 252.32173847645927,
            "unit": "iter/sec",
            "range": "stddev: 0.0002037866385260961",
            "extra": "mean: 3.96319400000209 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_isolates",
            "value": 8051.549238886052,
            "unit": "iter/sec",
            "range": "stddev: 0.000019724886976235518",
            "extra": "mean: 124.19969999939441 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_singletons",
            "value": 189.97334370026763,
            "unit": "iter/sec",
            "range": "stddev: 0.00020156073214158603",
            "extra": "mean: 5.263896400001045 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_copy",
            "value": 11.890812283265,
            "unit": "iter/sec",
            "range": "stddev: 0.06008766984073381",
            "extra": "mean: 84.09854400000825 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_dual",
            "value": 11.539610333300242,
            "unit": "iter/sec",
            "range": "stddev: 0.06887744962238526",
            "extra": "mean: 86.65803879999885 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_erdos_renyi",
            "value": 50.94052147017529,
            "unit": "iter/sec",
            "range": "stddev: 0.0015145598155313854",
            "extra": "mean: 19.630737399998566 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_fast_erdos_renyi",
            "value": 34.21781772754088,
            "unit": "iter/sec",
            "range": "stddev: 0.0011539937031183184",
            "extra": "mean: 29.22454049999601 msec\nrounds: 10"
          }
        ]
      }
    ]
  }
}