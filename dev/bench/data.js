window.BENCHMARK_DATA = {
  "lastUpdate": 1778869556013,
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
          "id": "eecad09dc650ac1db24b7a75f23145678f272703",
          "message": "Updated XGI publications",
          "timestamp": "2025-06-20T09:47:39-04:00",
          "tree_id": "823a95d4cc1961d0220fa0e44225a1ebd0d0c96b",
          "url": "https://github.com/xgi-org/xgi/commit/eecad09dc650ac1db24b7a75f23145678f272703"
        },
        "date": 1750427315776,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/algorithms.py::test_connected",
            "value": 94.7192044920456,
            "unit": "iter/sec",
            "range": "stddev: 0.00022796732059308375",
            "extra": "mean: 10.557521100000145 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/algorithms.py::test_clustering_coefficient",
            "value": 60.70769964435908,
            "unit": "iter/sec",
            "range": "stddev: 0.0003617101287769824",
            "extra": "mean: 16.47237509999968 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgelist",
            "value": 28.12271126829526,
            "unit": "iter/sec",
            "range": "stddev: 0.044645487914681675",
            "extra": "mean: 35.558449200001974 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgedict",
            "value": 27.818011818264633,
            "unit": "iter/sec",
            "range": "stddev: 0.04008771300953",
            "extra": "mean: 35.94793210000091 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_df",
            "value": 22.394417025253155,
            "unit": "iter/sec",
            "range": "stddev: 0.03557504380321231",
            "extra": "mean: 44.65398670000411 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_memberships",
            "value": 1277.474484038978,
            "unit": "iter/sec",
            "range": "stddev: 0.000021455288739660213",
            "extra": "mean: 782.7945000030923 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_members",
            "value": 133.73997239412793,
            "unit": "iter/sec",
            "range": "stddev: 0.0006784591295482861",
            "extra": "mean: 7.47719610000388 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_attributes",
            "value": 15741.040984647407,
            "unit": "iter/sec",
            "range": "stddev: 0.0000028238232903408096",
            "extra": "mean: 63.52820000756764 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_attributes",
            "value": 267.0048657098407,
            "unit": "iter/sec",
            "range": "stddev: 0.00005415561488058124",
            "extra": "mean: 3.745250099998998 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_degree",
            "value": 11017.60834129396,
            "unit": "iter/sec",
            "range": "stddev: 0.000007644801518943918",
            "extra": "mean: 90.76380000294648 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_nodestats_degree",
            "value": 9863.89793625141,
            "unit": "iter/sec",
            "range": "stddev: 0.000008831182222488052",
            "extra": "mean: 101.37980000024527 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_size",
            "value": 269.1811850209928,
            "unit": "iter/sec",
            "range": "stddev: 0.00034904467353930464",
            "extra": "mean: 3.7149699000025294 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_isolates",
            "value": 8772.814801816488,
            "unit": "iter/sec",
            "range": "stddev: 0.000007544811391091233",
            "extra": "mean: 113.98849999579852 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_singletons",
            "value": 194.21155565726394,
            "unit": "iter/sec",
            "range": "stddev: 0.00020410075961105258",
            "extra": "mean: 5.14902420000567 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_copy",
            "value": 11.557491828905215,
            "unit": "iter/sec",
            "range": "stddev: 0.06374824593355978",
            "extra": "mean: 86.52396340000053 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_dual",
            "value": 14.690733527776148,
            "unit": "iter/sec",
            "range": "stddev: 0.04600998013171258",
            "extra": "mean: 68.07012039999734 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_erdos_renyi",
            "value": 47.67047725394467,
            "unit": "iter/sec",
            "range": "stddev: 0.001854914275435768",
            "extra": "mean: 20.97734399999638 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_fast_erdos_renyi",
            "value": 32.69112319231214,
            "unit": "iter/sec",
            "range": "stddev: 0.0016265779093584186",
            "extra": "mean: 30.589343600013308 msec\nrounds: 10"
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
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "f6d1c9d0c36f51461b197b0cfca7774e90f3b1b6",
          "message": "fix JSON error (#677)",
          "timestamp": "2025-07-31T15:24:02-04:00",
          "tree_id": "0736a79a3607819fd41f340d2a455b1d725001ac",
          "url": "https://github.com/xgi-org/xgi/commit/f6d1c9d0c36f51461b197b0cfca7774e90f3b1b6"
        },
        "date": 1753989897215,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/algorithms.py::test_connected",
            "value": 97.39296846336553,
            "unit": "iter/sec",
            "range": "stddev: 0.00022461943803751537",
            "extra": "mean: 10.267681700000253 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/algorithms.py::test_clustering_coefficient",
            "value": 59.562543967952706,
            "unit": "iter/sec",
            "range": "stddev: 0.0003968089059530765",
            "extra": "mean: 16.78907470000013 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgelist",
            "value": 28.85673094792054,
            "unit": "iter/sec",
            "range": "stddev: 0.04088120517044259",
            "extra": "mean: 34.653959999999984 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgedict",
            "value": 28.41782898784079,
            "unit": "iter/sec",
            "range": "stddev: 0.03806760372451175",
            "extra": "mean: 35.189176500001906 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_df",
            "value": 22.837209131630967,
            "unit": "iter/sec",
            "range": "stddev: 0.03337781913743808",
            "extra": "mean: 43.788187699999526 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_memberships",
            "value": 1322.2939419817976,
            "unit": "iter/sec",
            "range": "stddev: 0.000016292356110529715",
            "extra": "mean: 756.2614999969242 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_members",
            "value": 133.77514447647397,
            "unit": "iter/sec",
            "range": "stddev: 0.000492539121298106",
            "extra": "mean: 7.475230200000738 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_attributes",
            "value": 15998.950470504773,
            "unit": "iter/sec",
            "range": "stddev: 0.000003660260873111284",
            "extra": "mean: 62.504099993532236 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_attributes",
            "value": 257.54261184159236,
            "unit": "iter/sec",
            "range": "stddev: 0.0000579205075042037",
            "extra": "mean: 3.8828526000003194 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_degree",
            "value": 11717.450094610407,
            "unit": "iter/sec",
            "range": "stddev: 0.000009259042113283496",
            "extra": "mean: 85.34280000560557 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_nodestats_degree",
            "value": 10444.835081568173,
            "unit": "iter/sec",
            "range": "stddev: 0.00001527114281060923",
            "extra": "mean: 95.74109999732627 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_size",
            "value": 280.1629450098837,
            "unit": "iter/sec",
            "range": "stddev: 0.00009492857011580634",
            "extra": "mean: 3.569351400003029 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_isolates",
            "value": 9300.084909987963,
            "unit": "iter/sec",
            "range": "stddev: 0.000004333381499191115",
            "extra": "mean: 107.52589999754036 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_singletons",
            "value": 203.57160269800065,
            "unit": "iter/sec",
            "range": "stddev: 0.00011800452651319181",
            "extra": "mean: 4.9122764999964375 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_copy",
            "value": 12.218489185962422,
            "unit": "iter/sec",
            "range": "stddev: 0.05913576584714554",
            "extra": "mean: 81.84317920000126 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_dual",
            "value": 15.040086070682355,
            "unit": "iter/sec",
            "range": "stddev: 0.0452439111129816",
            "extra": "mean: 66.48898120000126 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_erdos_renyi",
            "value": 52.96385017022422,
            "unit": "iter/sec",
            "range": "stddev: 0.0006373816876644083",
            "extra": "mean: 18.88080260000038 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_fast_erdos_renyi",
            "value": 33.92273520370585,
            "unit": "iter/sec",
            "range": "stddev: 0.0019050902222388943",
            "extra": "mean: 29.478755000002366 msec\nrounds: 10"
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
          "id": "448637867092c9f8b4899b0f3562208a730bf914",
          "message": "Update using-xgi.rst",
          "timestamp": "2025-08-17T12:12:44-04:00",
          "tree_id": "8bdea31fd9fbb70508b2d9a9a30eda8216fb1d55",
          "url": "https://github.com/xgi-org/xgi/commit/448637867092c9f8b4899b0f3562208a730bf914"
        },
        "date": 1755447220433,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/algorithms.py::test_connected",
            "value": 95.92871345425135,
            "unit": "iter/sec",
            "range": "stddev: 0.0002365613295466765",
            "extra": "mean: 10.424407500022426 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/algorithms.py::test_clustering_coefficient",
            "value": 59.38565198599997,
            "unit": "iter/sec",
            "range": "stddev: 0.00035836483498946794",
            "extra": "mean: 16.839084299954266 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgelist",
            "value": 28.97117432469722,
            "unit": "iter/sec",
            "range": "stddev: 0.041578422299922",
            "extra": "mean: 34.517068200011636 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgedict",
            "value": 28.52577136282969,
            "unit": "iter/sec",
            "range": "stddev: 0.038899107822195716",
            "extra": "mean: 35.0560195999833 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_df",
            "value": 22.746642889505797,
            "unit": "iter/sec",
            "range": "stddev: 0.03353244148905112",
            "extra": "mean: 43.96253130000787 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_memberships",
            "value": 1278.5130790460769,
            "unit": "iter/sec",
            "range": "stddev: 0.000013262310303147026",
            "extra": "mean: 782.1586000090974 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_members",
            "value": 134.36239701674154,
            "unit": "iter/sec",
            "range": "stddev: 0.0005314228180826568",
            "extra": "mean: 7.4425585000199135 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_attributes",
            "value": 15718.673473715264,
            "unit": "iter/sec",
            "range": "stddev: 0.000003745678743556509",
            "extra": "mean: 63.6185999837835 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_attributes",
            "value": 255.29213576865965,
            "unit": "iter/sec",
            "range": "stddev: 0.0001102959222979567",
            "extra": "mean: 3.917081100007635 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_degree",
            "value": 11865.760273570795,
            "unit": "iter/sec",
            "range": "stddev: 0.000011293576068181083",
            "extra": "mean: 84.27610005128372 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_nodestats_degree",
            "value": 10107.064133611955,
            "unit": "iter/sec",
            "range": "stddev: 0.000008997544416003442",
            "extra": "mean: 98.94069996789767 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_size",
            "value": 264.6539977160749,
            "unit": "iter/sec",
            "range": "stddev: 0.00017047214751096892",
            "extra": "mean: 3.778518399985842 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_isolates",
            "value": 9373.222019455729,
            "unit": "iter/sec",
            "range": "stddev: 0.000003937461162807709",
            "extra": "mean: 106.6868999714643 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_singletons",
            "value": 199.62050146585514,
            "unit": "iter/sec",
            "range": "stddev: 0.00015821556855932846",
            "extra": "mean: 5.009505499970146 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_copy",
            "value": 12.232840108607897,
            "unit": "iter/sec",
            "range": "stddev: 0.058154535778780464",
            "extra": "mean: 81.74716509997779 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_dual",
            "value": 14.783199136631824,
            "unit": "iter/sec",
            "range": "stddev: 0.04413141119573306",
            "extra": "mean: 67.64435699997193 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_erdos_renyi",
            "value": 50.28952433505527,
            "unit": "iter/sec",
            "range": "stddev: 0.0008862414276022483",
            "extra": "mean: 19.884856999988187 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_fast_erdos_renyi",
            "value": 34.193478023563436,
            "unit": "iter/sec",
            "range": "stddev: 0.0015506970559957685",
            "extra": "mean: 29.24534319997747 msec\nrounds: 10"
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
          "id": "794a05201ec2d387b49b819ca87b580b8b01281a",
          "message": "Updated pubs",
          "timestamp": "2025-10-15T08:37:41-04:00",
          "tree_id": "5f28932bc7ead529b5a98acfe3b3d6e31cc06e97",
          "url": "https://github.com/xgi-org/xgi/commit/794a05201ec2d387b49b819ca87b580b8b01281a"
        },
        "date": 1760531942399,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/algorithms.py::test_connected",
            "value": 93.30498653200685,
            "unit": "iter/sec",
            "range": "stddev: 0.00024278815581948494",
            "extra": "mean: 10.717540799997494 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/algorithms.py::test_clustering_coefficient",
            "value": 59.23652682523546,
            "unit": "iter/sec",
            "range": "stddev: 0.00034417164619105704",
            "extra": "mean: 16.88147590000142 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgelist",
            "value": 28.41930296578182,
            "unit": "iter/sec",
            "range": "stddev: 0.04225838357264205",
            "extra": "mean: 35.187351399999045 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgedict",
            "value": 27.625146464728623,
            "unit": "iter/sec",
            "range": "stddev: 0.040603956885631794",
            "extra": "mean: 36.19890309999931 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_df",
            "value": 21.639184685724743,
            "unit": "iter/sec",
            "range": "stddev: 0.03681843705951795",
            "extra": "mean: 46.21246199999831 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_memberships",
            "value": 1236.8449174555285,
            "unit": "iter/sec",
            "range": "stddev: 0.000019564074920519463",
            "extra": "mean: 808.5088000015617 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_members",
            "value": 126.83462157990299,
            "unit": "iter/sec",
            "range": "stddev: 0.0021089734284801638",
            "extra": "mean: 7.884282599999893 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_attributes",
            "value": 13865.47164838576,
            "unit": "iter/sec",
            "range": "stddev: 0.00001913987275604224",
            "extra": "mean: 72.12159999738788 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_attributes",
            "value": 245.71433654230995,
            "unit": "iter/sec",
            "range": "stddev: 0.00038183329076213224",
            "extra": "mean: 4.069766599995717 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_degree",
            "value": 10341.0691430942,
            "unit": "iter/sec",
            "range": "stddev: 0.000018741821465418877",
            "extra": "mean: 96.70179999403672 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_nodestats_degree",
            "value": 9346.563081899632,
            "unit": "iter/sec",
            "range": "stddev: 0.000004882285339539105",
            "extra": "mean: 106.9911999991291 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_size",
            "value": 248.1285216415171,
            "unit": "iter/sec",
            "range": "stddev: 0.0001478554321568138",
            "extra": "mean: 4.0301695000010795 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_isolates",
            "value": 8381.30934485262,
            "unit": "iter/sec",
            "range": "stddev: 0.000007982961025670866",
            "extra": "mean: 119.3131000007952 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_singletons",
            "value": 179.0347417096097,
            "unit": "iter/sec",
            "range": "stddev: 0.0005410949648374066",
            "extra": "mean: 5.585508099997583 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_copy",
            "value": 11.70195948000868,
            "unit": "iter/sec",
            "range": "stddev: 0.06030028721188232",
            "extra": "mean: 85.45577360000038 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_dual",
            "value": 11.732908871105794,
            "unit": "iter/sec",
            "range": "stddev: 0.06644206437856405",
            "extra": "mean: 85.2303560000081 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_erdos_renyi",
            "value": 51.652727412009085,
            "unit": "iter/sec",
            "range": "stddev: 0.0012355520977047794",
            "extra": "mean: 19.360061899993752 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_fast_erdos_renyi",
            "value": 29.904720182263432,
            "unit": "iter/sec",
            "range": "stddev: 0.001258672837378565",
            "extra": "mean: 33.43953710000278 msec\nrounds: 10"
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
          "id": "2103af52ef4f73ddfce1eef89571403dd1fc97e8",
          "message": "Update using-xgi.rst",
          "timestamp": "2025-11-04T11:56:51-05:00",
          "tree_id": "2d1d5072797d198e98bd63c211c1723c0e0223a6",
          "url": "https://github.com/xgi-org/xgi/commit/2103af52ef4f73ddfce1eef89571403dd1fc97e8"
        },
        "date": 1762275469555,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/algorithms.py::test_connected",
            "value": 86.64836474128816,
            "unit": "iter/sec",
            "range": "stddev: 0.0017914828254880484",
            "extra": "mean: 11.540898700001634 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/algorithms.py::test_clustering_coefficient",
            "value": 58.92025116312529,
            "unit": "iter/sec",
            "range": "stddev: 0.00037977509407546514",
            "extra": "mean: 16.97209330000007 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgelist",
            "value": 28.236950038702098,
            "unit": "iter/sec",
            "range": "stddev: 0.04120085046693049",
            "extra": "mean: 35.4145896999988 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgedict",
            "value": 28.240502809274847,
            "unit": "iter/sec",
            "range": "stddev: 0.03899813321509426",
            "extra": "mean: 35.410134400000004 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_df",
            "value": 21.64565517867786,
            "unit": "iter/sec",
            "range": "stddev: 0.03832931049126539",
            "extra": "mean: 46.198647800000714 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_memberships",
            "value": 1155.992787990689,
            "unit": "iter/sec",
            "range": "stddev: 0.00003342541751712015",
            "extra": "mean: 865.0573000011264 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_members",
            "value": 131.7803215713739,
            "unit": "iter/sec",
            "range": "stddev: 0.0005567496179992776",
            "extra": "mean: 7.5883864000012125 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_attributes",
            "value": 13299.21641018063,
            "unit": "iter/sec",
            "range": "stddev: 0.00000726597866937881",
            "extra": "mean: 75.19239999993488 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_attributes",
            "value": 248.8897402024759,
            "unit": "iter/sec",
            "range": "stddev: 0.0002435014364468784",
            "extra": "mean: 4.017843399999066 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_degree",
            "value": 10239.564859583354,
            "unit": "iter/sec",
            "range": "stddev: 0.000009649512551995435",
            "extra": "mean: 97.66039999874465 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_nodestats_degree",
            "value": 8856.768342157318,
            "unit": "iter/sec",
            "range": "stddev: 0.000008764028044118117",
            "extra": "mean: 112.90800000267609 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_size",
            "value": 241.7933288930372,
            "unit": "iter/sec",
            "range": "stddev: 0.0005023179444620731",
            "extra": "mean: 4.135763400000059 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_isolates",
            "value": 7422.279456349168,
            "unit": "iter/sec",
            "range": "stddev: 0.00001084786970258211",
            "extra": "mean: 134.72949999808748 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_singletons",
            "value": 166.98300762539924,
            "unit": "iter/sec",
            "range": "stddev: 0.00044867518478352653",
            "extra": "mean: 5.988633300002277 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_copy",
            "value": 11.070951983156949,
            "unit": "iter/sec",
            "range": "stddev: 0.06587116138007511",
            "extra": "mean: 90.32646889999825 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_dual",
            "value": 13.665614555101861,
            "unit": "iter/sec",
            "range": "stddev: 0.05101941684768445",
            "extra": "mean: 73.17636509999943 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_erdos_renyi",
            "value": 48.1291976330934,
            "unit": "iter/sec",
            "range": "stddev: 0.001578351526788846",
            "extra": "mean: 20.777408499999694 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_fast_erdos_renyi",
            "value": 33.25391832083671,
            "unit": "iter/sec",
            "range": "stddev: 0.0009190472582099114",
            "extra": "mean: 30.071644199998104 msec\nrounds: 10"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "56703624+kaiser-dan@users.noreply.github.com",
            "name": "Daniel Kaiser",
            "username": "kaiser-dan"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "a962e0ed4dda402c7a2c15c4a666a060a3c85ebb",
          "message": "Merge pull request #682 from GavinAnderberg/patch-1\n\nUpdate hypergraph_matrix.py",
          "timestamp": "2026-02-26T10:22:15-05:00",
          "tree_id": "fc677a0fa6a98fe5c3697fef767e899db869386b",
          "url": "https://github.com/xgi-org/xgi/commit/a962e0ed4dda402c7a2c15c4a666a060a3c85ebb"
        },
        "date": 1772119403145,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/algorithms.py::test_connected",
            "value": 88.35013838367747,
            "unit": "iter/sec",
            "range": "stddev: 0.0004629432612229941",
            "extra": "mean: 11.318601400003558 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/algorithms.py::test_clustering_coefficient",
            "value": 63.756674335580264,
            "unit": "iter/sec",
            "range": "stddev: 0.000304189187154274",
            "extra": "mean: 15.684632399998577 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgelist",
            "value": 45.560640447018834,
            "unit": "iter/sec",
            "range": "stddev: 0.0009318300051915803",
            "extra": "mean: 21.94876959999874 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgedict",
            "value": 26.012953852717253,
            "unit": "iter/sec",
            "range": "stddev: 0.04570729968482383",
            "extra": "mean: 38.442385500005116 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_df",
            "value": 16.33495048580841,
            "unit": "iter/sec",
            "range": "stddev: 0.042495355928256304",
            "extra": "mean: 61.21842860000015 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_memberships",
            "value": 1082.814872554526,
            "unit": "iter/sec",
            "range": "stddev: 0.00009614860658083931",
            "extra": "mean: 923.5188999952015 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_members",
            "value": 45.95308250934464,
            "unit": "iter/sec",
            "range": "stddev: 0.04478806124171485",
            "extra": "mean: 21.761325799997167 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_attributes",
            "value": 12982.865213979472,
            "unit": "iter/sec",
            "range": "stddev: 0.00000555819265985313",
            "extra": "mean: 77.02460000302835 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_attributes",
            "value": 234.03500929711413,
            "unit": "iter/sec",
            "range": "stddev: 0.00041620859132510607",
            "extra": "mean: 4.27286499999866 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_degree",
            "value": 8669.76350617182,
            "unit": "iter/sec",
            "range": "stddev: 0.000012547551853684993",
            "extra": "mean: 115.34340000025622 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_nodestats_degree",
            "value": 7994.9088419081745,
            "unit": "iter/sec",
            "range": "stddev: 0.000010863277412307121",
            "extra": "mean: 125.07960000220919 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_size",
            "value": 221.01709947429566,
            "unit": "iter/sec",
            "range": "stddev: 0.0001921133155650457",
            "extra": "mean: 4.524536799996781 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_isolates",
            "value": 6530.590920505436,
            "unit": "iter/sec",
            "range": "stddev: 0.000017542556334897115",
            "extra": "mean: 153.12550000032843 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_singletons",
            "value": 162.05182239018282,
            "unit": "iter/sec",
            "range": "stddev: 0.0005305639980566682",
            "extra": "mean: 6.17086550000181 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_copy",
            "value": 12.895565291567486,
            "unit": "iter/sec",
            "range": "stddev: 0.05517268585551074",
            "extra": "mean: 77.54603829999667 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_dual",
            "value": 13.465596044415685,
            "unit": "iter/sec",
            "range": "stddev: 0.05408011439741986",
            "extra": "mean: 74.2633297999987 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_erdos_renyi",
            "value": 54.76482270990259,
            "unit": "iter/sec",
            "range": "stddev: 0.00019270356033395945",
            "extra": "mean: 18.259896599997205 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_fast_erdos_renyi",
            "value": 33.7622227264805,
            "unit": "iter/sec",
            "range": "stddev: 0.0019203461324878398",
            "extra": "mean: 29.618902999999364 msec\nrounds: 10"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "56703624+kaiser-dan@users.noreply.github.com",
            "name": "Daniel Kaiser",
            "username": "kaiser-dan"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "cc32ef677b8d69964615873ed9ff7fd970d01feb",
          "message": "Merge pull request #676 from xgi-org/speedup-imports\n\nSpeedup imports",
          "timestamp": "2026-02-26T10:26:48-05:00",
          "tree_id": "73308a30c017021963bb3c439963545798cdbc76",
          "url": "https://github.com/xgi-org/xgi/commit/cc32ef677b8d69964615873ed9ff7fd970d01feb"
        },
        "date": 1772119667444,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/algorithms.py::test_connected",
            "value": 92.1670649342681,
            "unit": "iter/sec",
            "range": "stddev: 0.00026665771088099687",
            "extra": "mean: 10.849862700013091 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/algorithms.py::test_clustering_coefficient",
            "value": 63.52031087350527,
            "unit": "iter/sec",
            "range": "stddev: 0.000568067440342237",
            "extra": "mean: 15.742995999994493 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgelist",
            "value": 28.854629505138032,
            "unit": "iter/sec",
            "range": "stddev: 0.04126443066359366",
            "extra": "mean: 34.6564838000063 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgedict",
            "value": 41.612293962727,
            "unit": "iter/sec",
            "range": "stddev: 0.0005142000787059516",
            "extra": "mean: 24.031359600019186 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_df",
            "value": 16.910537416172115,
            "unit": "iter/sec",
            "range": "stddev: 0.03653154910882297",
            "extra": "mean: 59.13472619998856 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_memberships",
            "value": 1138.9499587465507,
            "unit": "iter/sec",
            "range": "stddev: 0.000029644172029703345",
            "extra": "mean: 878.0017000049156 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_members",
            "value": 129.91157334900322,
            "unit": "iter/sec",
            "range": "stddev: 0.000569676091059222",
            "extra": "mean: 7.697543600011159 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_attributes",
            "value": 12459.692896150838,
            "unit": "iter/sec",
            "range": "stddev: 0.000009742836062662846",
            "extra": "mean: 80.25879998285745 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_attributes",
            "value": 249.03461730625548,
            "unit": "iter/sec",
            "range": "stddev: 0.00029168430942461707",
            "extra": "mean: 4.015505999996094 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_degree",
            "value": 10592.423662500909,
            "unit": "iter/sec",
            "range": "stddev: 0.000011958743004173859",
            "extra": "mean: 94.40710000490071 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_nodestats_degree",
            "value": 8664.287453153314,
            "unit": "iter/sec",
            "range": "stddev: 0.000009210633738774017",
            "extra": "mean: 115.41630000238001 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_size",
            "value": 226.454121357326,
            "unit": "iter/sec",
            "range": "stddev: 0.00017614278632188592",
            "extra": "mean: 4.415905500002282 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_isolates",
            "value": 7511.996659007351,
            "unit": "iter/sec",
            "range": "stddev: 0.000007492586211302815",
            "extra": "mean: 133.12039999391345 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_singletons",
            "value": 154.8828011142456,
            "unit": "iter/sec",
            "range": "stddev: 0.0011357482360260182",
            "extra": "mean: 6.456494799977008 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_copy",
            "value": 10.803650863475092,
            "unit": "iter/sec",
            "range": "stddev: 0.06762311969918099",
            "extra": "mean: 92.56130290000328 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_dual",
            "value": 11.537732393713757,
            "unit": "iter/sec",
            "range": "stddev: 0.06699173384609329",
            "extra": "mean: 86.67214369999101 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_erdos_renyi",
            "value": 53.82598491834077,
            "unit": "iter/sec",
            "range": "stddev: 0.0015412838100435002",
            "extra": "mean: 18.578387400009433 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_fast_erdos_renyi",
            "value": 32.86742152813564,
            "unit": "iter/sec",
            "range": "stddev: 0.0012249226354787307",
            "extra": "mean: 30.425264699999843 msec\nrounds: 10"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "56703624+kaiser-dan@users.noreply.github.com",
            "name": "Daniel Kaiser",
            "username": "kaiser-dan"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "c71268524fcc1b1baec0df86d681e6a4f77d36f4",
          "message": "Merge pull request #686 from xgi-org/fix-test-collection\n\nFix slow test collection and matplotlib GUI popups",
          "timestamp": "2026-03-01T17:52:02-05:00",
          "tree_id": "debdb060079da77a0ac1849ece6ced2fab3844c4",
          "url": "https://github.com/xgi-org/xgi/commit/c71268524fcc1b1baec0df86d681e6a4f77d36f4"
        },
        "date": 1772405579325,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/algorithms.py::test_connected",
            "value": 97.40817022523437,
            "unit": "iter/sec",
            "range": "stddev: 0.00009194800552431147",
            "extra": "mean: 10.26607929999841 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/algorithms.py::test_clustering_coefficient",
            "value": 64.54502021612727,
            "unit": "iter/sec",
            "range": "stddev: 0.0003117102040207927",
            "extra": "mean: 15.493062000004443 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgelist",
            "value": 29.292197230619276,
            "unit": "iter/sec",
            "range": "stddev: 0.04024476559488981",
            "extra": "mean: 34.13878420000174 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgedict",
            "value": 42.90690193000816,
            "unit": "iter/sec",
            "range": "stddev: 0.0006612711578905366",
            "extra": "mean: 23.306273700004 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_df",
            "value": 17.757293090743236,
            "unit": "iter/sec",
            "range": "stddev: 0.03366696253673715",
            "extra": "mean: 56.31488959999729 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_memberships",
            "value": 1269.9515742021867,
            "unit": "iter/sec",
            "range": "stddev: 0.000011089728180120255",
            "extra": "mean: 787.4316000027193 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_members",
            "value": 129.68118606615323,
            "unit": "iter/sec",
            "range": "stddev: 0.000589318584802235",
            "extra": "mean: 7.711218800002939 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_attributes",
            "value": 14440.078727808026,
            "unit": "iter/sec",
            "range": "stddev: 0.00000463963325085366",
            "extra": "mean: 69.25169999760783 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_attributes",
            "value": 244.98009451011018,
            "unit": "iter/sec",
            "range": "stddev: 0.0005817784901816937",
            "extra": "mean: 4.0819642999963435 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_degree",
            "value": 10262.251846252371,
            "unit": "iter/sec",
            "range": "stddev: 0.000010793689731421091",
            "extra": "mean: 97.44449999686822 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_nodestats_degree",
            "value": 8392.634288174271,
            "unit": "iter/sec",
            "range": "stddev: 0.000008332731174494046",
            "extra": "mean: 119.15210000381649 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_size",
            "value": 251.46373899151945,
            "unit": "iter/sec",
            "range": "stddev: 0.0003971023827776866",
            "extra": "mean: 3.976716500002908 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_isolates",
            "value": 8827.231656529188,
            "unit": "iter/sec",
            "range": "stddev: 0.000004907561257822254",
            "extra": "mean: 113.2858000005399 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_singletons",
            "value": 190.1986815427071,
            "unit": "iter/sec",
            "range": "stddev: 0.000301338980919822",
            "extra": "mean: 5.257660000000897 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_copy",
            "value": 11.451487359831885,
            "unit": "iter/sec",
            "range": "stddev: 0.06308425815450662",
            "extra": "mean: 87.32490099999382 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_dual",
            "value": 11.61224512316725,
            "unit": "iter/sec",
            "range": "stddev: 0.06846871169640889",
            "extra": "mean: 86.11599129998808 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_erdos_renyi",
            "value": 52.38854407972239,
            "unit": "iter/sec",
            "range": "stddev: 0.0011784162586563798",
            "extra": "mean: 19.088142599997582 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_fast_erdos_renyi",
            "value": 33.25062451072892,
            "unit": "iter/sec",
            "range": "stddev: 0.0013758222978400645",
            "extra": "mean: 30.074623100006193 msec\nrounds: 10"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "56703624+kaiser-dan@users.noreply.github.com",
            "name": "Daniel Kaiser",
            "username": "kaiser-dan"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "ab72705ad798d76d75e63dada67c5e54095c9bcc",
          "message": "Merge pull request #690 from xgi-org/dev\n\nPatch v0.10.1",
          "timestamp": "2026-03-02T11:24:23-05:00",
          "tree_id": "fbd21624c07e763913062a9d7d2fefeffd992bc6",
          "url": "https://github.com/xgi-org/xgi/commit/ab72705ad798d76d75e63dada67c5e54095c9bcc"
        },
        "date": 1772468723793,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/algorithms.py::test_connected",
            "value": 95.47861040430065,
            "unit": "iter/sec",
            "range": "stddev: 0.00019431974453266095",
            "extra": "mean: 10.473550000000387 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/algorithms.py::test_clustering_coefficient",
            "value": 63.66104253399423,
            "unit": "iter/sec",
            "range": "stddev: 0.0003315299942206604",
            "extra": "mean: 15.708193899997982 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgelist",
            "value": 28.445110904544737,
            "unit": "iter/sec",
            "range": "stddev: 0.04147436274340494",
            "extra": "mean: 35.15542629999828 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgedict",
            "value": 42.352486659545924,
            "unit": "iter/sec",
            "range": "stddev: 0.000549412160760233",
            "extra": "mean: 23.61136450000174 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_df",
            "value": 17.45957581356394,
            "unit": "iter/sec",
            "range": "stddev: 0.03472537733737153",
            "extra": "mean: 57.275160100002154 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_memberships",
            "value": 1187.7704776068786,
            "unit": "iter/sec",
            "range": "stddev: 0.0000654986665140517",
            "extra": "mean: 841.9135000011124 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_members",
            "value": 132.06036125194274,
            "unit": "iter/sec",
            "range": "stddev: 0.0006049949962175699",
            "extra": "mean: 7.572294899998155 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_attributes",
            "value": 13785.212603154334,
            "unit": "iter/sec",
            "range": "stddev: 0.000007433111015375919",
            "extra": "mean: 72.54149999624815 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_attributes",
            "value": 254.2925665985377,
            "unit": "iter/sec",
            "range": "stddev: 0.00013656635319751246",
            "extra": "mean: 3.932478299999787 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_degree",
            "value": 9976.555095452179,
            "unit": "iter/sec",
            "range": "stddev: 0.000008893705464717323",
            "extra": "mean: 100.23500000073682 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_nodestats_degree",
            "value": 9278.486344901501,
            "unit": "iter/sec",
            "range": "stddev: 0.000007773427914238576",
            "extra": "mean: 107.7761999994209 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_size",
            "value": 249.6644322779894,
            "unit": "iter/sec",
            "range": "stddev: 0.00020185022073096972",
            "extra": "mean: 4.0053763000031495 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_isolates",
            "value": 8243.370681196462,
            "unit": "iter/sec",
            "range": "stddev: 0.000006373232500510308",
            "extra": "mean: 121.30960000149571 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_singletons",
            "value": 185.88390557481364,
            "unit": "iter/sec",
            "range": "stddev: 0.00021061923090998392",
            "extra": "mean: 5.379701899998679 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_copy",
            "value": 11.344092387432047,
            "unit": "iter/sec",
            "range": "stddev: 0.06428057600615712",
            "extra": "mean: 88.15160929999877 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_dual",
            "value": 11.505642189742565,
            "unit": "iter/sec",
            "range": "stddev: 0.06884859901841679",
            "extra": "mean: 86.91387960000299 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_erdos_renyi",
            "value": 54.36260917125306,
            "unit": "iter/sec",
            "range": "stddev: 0.0011937730052799592",
            "extra": "mean: 18.39499640000355 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_fast_erdos_renyi",
            "value": 34.43640852102842,
            "unit": "iter/sec",
            "range": "stddev: 0.0013147055387996989",
            "extra": "mean: 29.03903290000045 msec\nrounds: 10"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "leo@leotrs.com",
            "name": "Leo Torres",
            "username": "leotrs"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "a833e8145f240b8fda54951b78e4f59949d67be3",
          "message": "fix: update ReadTheDocs OS from ubuntu-20.04 to ubuntu-24.04 (#703)\n\nubuntu-20.04 has been deprecated by ReadTheDocs, causing build failures.\n\nCloses #702\n\nCo-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>",
          "timestamp": "2026-04-02T09:29:10-04:00",
          "tree_id": "55275e470d9343fe84c9dd1d5b8fd855c0e3d5a8",
          "url": "https://github.com/xgi-org/xgi/commit/a833e8145f240b8fda54951b78e4f59949d67be3"
        },
        "date": 1775136611358,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/algorithms.py::test_connected",
            "value": 96.98135824335586,
            "unit": "iter/sec",
            "range": "stddev: 0.00023373822295600218",
            "extra": "mean: 10.311259999996025 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/algorithms.py::test_clustering_coefficient",
            "value": 64.85326307181973,
            "unit": "iter/sec",
            "range": "stddev: 0.000311417848168664",
            "extra": "mean: 15.419424600001719 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgelist",
            "value": 28.78353418814125,
            "unit": "iter/sec",
            "range": "stddev: 0.04299799444826994",
            "extra": "mean: 34.74208530000453 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgedict",
            "value": 28.096103429801985,
            "unit": "iter/sec",
            "range": "stddev: 0.03922781676630671",
            "extra": "mean: 35.592124100001854 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_df",
            "value": 17.752516971828083,
            "unit": "iter/sec",
            "range": "stddev: 0.035846981262341426",
            "extra": "mean: 56.33004049999926 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_memberships",
            "value": 1245.261933995209,
            "unit": "iter/sec",
            "range": "stddev: 0.00003132145683183031",
            "extra": "mean: 803.0439000023648 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_members",
            "value": 125.9052175953028,
            "unit": "iter/sec",
            "range": "stddev: 0.001324073113896468",
            "extra": "mean: 7.942482600000744 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_attributes",
            "value": 14948.889745854285,
            "unit": "iter/sec",
            "range": "stddev: 0.0000038686764956887605",
            "extra": "mean: 66.89460000046665 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_attributes",
            "value": 258.3111682978698,
            "unit": "iter/sec",
            "range": "stddev: 0.00008393171131337103",
            "extra": "mean: 3.8712998999983483 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_degree",
            "value": 9279.545376619822,
            "unit": "iter/sec",
            "range": "stddev: 0.00000777832181929213",
            "extra": "mean: 107.76389999875846 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_nodestats_degree",
            "value": 9190.416234104205,
            "unit": "iter/sec",
            "range": "stddev: 0.000008491934802012992",
            "extra": "mean: 108.80899999818894 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_size",
            "value": 257.28372145040674,
            "unit": "iter/sec",
            "range": "stddev: 0.00039406617784061137",
            "extra": "mean: 3.8867597000020737 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_isolates",
            "value": 9167.457359524598,
            "unit": "iter/sec",
            "range": "stddev: 0.000004241421254674178",
            "extra": "mean: 109.08150000403793 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_singletons",
            "value": 195.36644326969503,
            "unit": "iter/sec",
            "range": "stddev: 0.0002189055834107803",
            "extra": "mean: 5.118586300000061 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_copy",
            "value": 11.932943525515821,
            "unit": "iter/sec",
            "range": "stddev: 0.05969396472165869",
            "extra": "mean: 83.80162009999736 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_dual",
            "value": 12.01603864790613,
            "unit": "iter/sec",
            "range": "stddev: 0.06342505018258002",
            "extra": "mean: 83.22210249999955 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_erdos_renyi",
            "value": 52.96081402889879,
            "unit": "iter/sec",
            "range": "stddev: 0.0010644275291306516",
            "extra": "mean: 18.881884999998988 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_fast_erdos_renyi",
            "value": 33.82886543272868,
            "unit": "iter/sec",
            "range": "stddev: 0.001294815819782992",
            "extra": "mean: 29.56055389999932 msec\nrounds: 10"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "dleonardotn@gmail.com",
            "name": "Leo Torres",
            "username": "leotrs"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "50db7145afee387ef4df49aac802d6132b96f2ce",
          "message": "Merge pull request #699 from xgi-org/stats-discoverability\n\nfeat: make built-in stats discoverable in dir() and IDE autocomplete",
          "timestamp": "2026-04-03T14:57:33+02:00",
          "tree_id": "018f5203424a8d07d1142426804cd24fed17ec4f",
          "url": "https://github.com/xgi-org/xgi/commit/50db7145afee387ef4df49aac802d6132b96f2ce"
        },
        "date": 1775221115756,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/algorithms.py::test_connected",
            "value": 92.62621333508534,
            "unit": "iter/sec",
            "range": "stddev: 0.0001386080572445198",
            "extra": "mean: 10.796079899999711 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/algorithms.py::test_clustering_coefficient",
            "value": 63.09492002923249,
            "unit": "iter/sec",
            "range": "stddev: 0.00034260876767670334",
            "extra": "mean: 15.849136500001748 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgelist",
            "value": 26.418839633839525,
            "unit": "iter/sec",
            "range": "stddev: 0.05041109477291273",
            "extra": "mean: 37.851775999999404 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgedict",
            "value": 26.102540646420035,
            "unit": "iter/sec",
            "range": "stddev: 0.04413536244851166",
            "extra": "mean: 38.310446999999215 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_df",
            "value": 16.47060899213794,
            "unit": "iter/sec",
            "range": "stddev: 0.041674420673498566",
            "extra": "mean: 60.714209199996105 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_memberships",
            "value": 1145.896584435533,
            "unit": "iter/sec",
            "range": "stddev: 0.00006092408837436747",
            "extra": "mean: 872.6791000015055 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_members",
            "value": 125.10269367362429,
            "unit": "iter/sec",
            "range": "stddev: 0.0007533569882582077",
            "extra": "mean: 7.993433000002881 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_attributes",
            "value": 11784.656613206174,
            "unit": "iter/sec",
            "range": "stddev: 0.00001383769604105292",
            "extra": "mean: 84.85609999695498 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_attributes",
            "value": 244.37400336645757,
            "unit": "iter/sec",
            "range": "stddev: 0.0003804405280022941",
            "extra": "mean: 4.09208829999983 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_degree",
            "value": 8706.925750082124,
            "unit": "iter/sec",
            "range": "stddev: 0.000015187859479928717",
            "extra": "mean: 114.85109999824772 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_nodestats_degree",
            "value": 8087.506823748098,
            "unit": "iter/sec",
            "range": "stddev: 0.000008964360093821016",
            "extra": "mean: 123.64750000131151 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_size",
            "value": 228.30966827531412,
            "unit": "iter/sec",
            "range": "stddev: 0.00012777712861937696",
            "extra": "mean: 4.380015999997511 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_isolates",
            "value": 7243.516147664528,
            "unit": "iter/sec",
            "range": "stddev: 0.000010345971974351203",
            "extra": "mean: 138.0544999989297 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_singletons",
            "value": 175.0148915795283,
            "unit": "iter/sec",
            "range": "stddev: 0.00006585010891194548",
            "extra": "mean: 5.713799500001926 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_copy",
            "value": 10.92034789756032,
            "unit": "iter/sec",
            "range": "stddev: 0.0686325489109287",
            "extra": "mean: 91.57217420000023 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_dual",
            "value": 11.048225922670454,
            "unit": "iter/sec",
            "range": "stddev: 0.07316418452536533",
            "extra": "mean: 90.51226930000098 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_erdos_renyi",
            "value": 52.86582575183515,
            "unit": "iter/sec",
            "range": "stddev: 0.0014318847266099203",
            "extra": "mean: 18.915811599997312 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_fast_erdos_renyi",
            "value": 34.17354308694336,
            "unit": "iter/sec",
            "range": "stddev: 0.0011850505361516747",
            "extra": "mean: 29.26240329999814 msec\nrounds: 10"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "jbd7qp@virginia.edu",
            "name": "Rudra Dave",
            "username": "jbd7qp"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "47b49abdd5e582e81cd9f0ee876236f5dc362351",
          "message": "Update using-xgi.rst (#698)\n\n* Update using-xgi.rst\n\n* Fix issues with PR\n\n---------\n\nCo-authored-by: Nicholas Landry <nicholas.landry.91@gmail.com>",
          "timestamp": "2026-04-26T12:57:39-04:00",
          "tree_id": "1dabc9650d9ac88ff26e5cee8d81198fee68a1ca",
          "url": "https://github.com/xgi-org/xgi/commit/47b49abdd5e582e81cd9f0ee876236f5dc362351"
        },
        "date": 1777222717170,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/algorithms.py::test_connected",
            "value": 66.64380206675033,
            "unit": "iter/sec",
            "range": "stddev: 0.0012291949551064716",
            "extra": "mean: 15.005146300002536 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/algorithms.py::test_clustering_coefficient",
            "value": 61.748533087946036,
            "unit": "iter/sec",
            "range": "stddev: 0.00032176961187994777",
            "extra": "mean: 16.194716700002232 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgelist",
            "value": 22.899225352409786,
            "unit": "iter/sec",
            "range": "stddev: 0.06409866674566167",
            "extra": "mean: 43.6695995000008 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgedict",
            "value": 23.35612045197897,
            "unit": "iter/sec",
            "range": "stddev: 0.05696220388023025",
            "extra": "mean: 42.8153297999998 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_df",
            "value": 16.05066960127189,
            "unit": "iter/sec",
            "range": "stddev: 0.050633109347858536",
            "extra": "mean: 62.30269670000297 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_memberships",
            "value": 861.5792765341666,
            "unit": "iter/sec",
            "range": "stddev: 0.00008603598564959193",
            "extra": "mean: 1.1606593000038856 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_members",
            "value": 122.0095222087079,
            "unit": "iter/sec",
            "range": "stddev: 0.0011497166131917026",
            "extra": "mean: 8.196081600003424 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_attributes",
            "value": 10543.040381105113,
            "unit": "iter/sec",
            "range": "stddev: 0.000007810655885613065",
            "extra": "mean: 94.8492999981454 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_attributes",
            "value": 220.43161215030264,
            "unit": "iter/sec",
            "range": "stddev: 0.0010342626218270575",
            "extra": "mean: 4.536554400002046 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_degree",
            "value": 8298.830943870837,
            "unit": "iter/sec",
            "range": "stddev: 0.000009940072795723649",
            "extra": "mean: 120.49889999730112 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_nodestats_degree",
            "value": 7713.394927207032,
            "unit": "iter/sec",
            "range": "stddev: 0.000009717147956413875",
            "extra": "mean: 129.6446000026208 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_size",
            "value": 213.48944136740397,
            "unit": "iter/sec",
            "range": "stddev: 0.00018493704685189412",
            "extra": "mean: 4.684072399997774 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_isolates",
            "value": 7066.548514132167,
            "unit": "iter/sec",
            "range": "stddev: 0.000007940594014030306",
            "extra": "mean: 141.51179999686292 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_singletons",
            "value": 158.3557930675135,
            "unit": "iter/sec",
            "range": "stddev: 0.0002962805707696353",
            "extra": "mean: 6.31489369999656 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_copy",
            "value": 10.548768788319387,
            "unit": "iter/sec",
            "range": "stddev: 0.07839530615923204",
            "extra": "mean: 94.7977930000036 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_dual",
            "value": 10.431425177400383,
            "unit": "iter/sec",
            "range": "stddev: 0.08750607749943959",
            "extra": "mean: 95.86417800000078 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_erdos_renyi",
            "value": 60.097822788698835,
            "unit": "iter/sec",
            "range": "stddev: 0.001456190166667805",
            "extra": "mean: 16.639537899999368 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_fast_erdos_renyi",
            "value": 36.51471633442028,
            "unit": "iter/sec",
            "range": "stddev: 0.0016356117666304717",
            "extra": "mean: 27.38621850000129 msec\nrounds: 10"
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
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "53163bd96aa072bf133be9e46c0f11c24e9b0b80",
          "message": "Add missing link to paper",
          "timestamp": "2026-04-26T14:19:37-04:00",
          "tree_id": "3d9f30bc2ef704721d4b062fa26e6584e6fce722",
          "url": "https://github.com/xgi-org/xgi/commit/53163bd96aa072bf133be9e46c0f11c24e9b0b80"
        },
        "date": 1777227628691,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/algorithms.py::test_connected",
            "value": 96.25735427845503,
            "unit": "iter/sec",
            "range": "stddev: 0.000282046360539275",
            "extra": "mean: 10.388816599999018 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/algorithms.py::test_clustering_coefficient",
            "value": 64.61283443628744,
            "unit": "iter/sec",
            "range": "stddev: 0.00037891132393198996",
            "extra": "mean: 15.476801299996623 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgelist",
            "value": 28.769209240570063,
            "unit": "iter/sec",
            "range": "stddev: 0.04245085883952028",
            "extra": "mean: 34.75938429999701 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgedict",
            "value": 28.37903364259411,
            "unit": "iter/sec",
            "range": "stddev: 0.039986877490830734",
            "extra": "mean: 35.237281600001324 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_df",
            "value": 18.329314609716565,
            "unit": "iter/sec",
            "range": "stddev: 0.033127491227826794",
            "extra": "mean: 54.55741370001306 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_memberships",
            "value": 1183.434753688495,
            "unit": "iter/sec",
            "range": "stddev: 0.00015037760016007915",
            "extra": "mean: 844.9980000023061 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_members",
            "value": 137.53169366305306,
            "unit": "iter/sec",
            "range": "stddev: 0.0005888251431070734",
            "extra": "mean: 7.2710513000004084 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_attributes",
            "value": 15542.624092982102,
            "unit": "iter/sec",
            "range": "stddev: 0.000004238316568253118",
            "extra": "mean: 64.33919999722093 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_attributes",
            "value": 258.9757431664638,
            "unit": "iter/sec",
            "range": "stddev: 0.00006131997590064915",
            "extra": "mean: 3.861365500000602 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_degree",
            "value": 11177.155681839617,
            "unit": "iter/sec",
            "range": "stddev: 0.000012825558749013068",
            "extra": "mean: 89.46820000232947 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_nodestats_degree",
            "value": 9694.140183245589,
            "unit": "iter/sec",
            "range": "stddev: 0.000011361320889274469",
            "extra": "mean: 103.15509999827555 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_size",
            "value": 275.6056302809182,
            "unit": "iter/sec",
            "range": "stddev: 0.00015129464632240253",
            "extra": "mean: 3.628372900004706 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_isolates",
            "value": 8105.658884362225,
            "unit": "iter/sec",
            "range": "stddev: 0.00002309670000001525",
            "extra": "mean: 123.37060000504606 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_singletons",
            "value": 190.97536370041513,
            "unit": "iter/sec",
            "range": "stddev: 0.00031767707177935334",
            "extra": "mean: 5.236277500006281 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_copy",
            "value": 11.787446390340204,
            "unit": "iter/sec",
            "range": "stddev: 0.06283375089782074",
            "extra": "mean: 84.83601679999992 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_dual",
            "value": 11.451685746660475,
            "unit": "iter/sec",
            "range": "stddev: 0.06885582159109557",
            "extra": "mean: 87.32338819999654 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_erdos_renyi",
            "value": 51.28480014733296,
            "unit": "iter/sec",
            "range": "stddev: 0.0014702719709290284",
            "extra": "mean: 19.498954800002366 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_fast_erdos_renyi",
            "value": 32.685522831488164,
            "unit": "iter/sec",
            "range": "stddev: 0.0022725199843936406",
            "extra": "mean: 30.5945847999908 msec\nrounds: 10"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "dleonardotn@gmail.com",
            "name": "Leo Torres",
            "username": "leotrs"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "fa7de97664fb25b7d3336b01b2c31a2242f840ae",
          "message": "Merge pull request #708 from xgi-org/stats-docstring-forwarding\n\nfeat: forward stat function docstrings to stat objects",
          "timestamp": "2026-04-27T09:40:22+02:00",
          "tree_id": "667570389622a5fa9f08f05732fae9fee2c72a01",
          "url": "https://github.com/xgi-org/xgi/commit/fa7de97664fb25b7d3336b01b2c31a2242f840ae"
        },
        "date": 1777275682407,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/algorithms.py::test_connected",
            "value": 95.20518144677405,
            "unit": "iter/sec",
            "range": "stddev: 0.00043335977798058677",
            "extra": "mean: 10.503630000002318 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/algorithms.py::test_clustering_coefficient",
            "value": 63.46100587725808,
            "unit": "iter/sec",
            "range": "stddev: 0.0003523466473755242",
            "extra": "mean: 15.75770799999816 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgelist",
            "value": 28.4043387502463,
            "unit": "iter/sec",
            "range": "stddev: 0.04346683552495536",
            "extra": "mean: 35.205889099999865 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgedict",
            "value": 27.83151835235294,
            "unit": "iter/sec",
            "range": "stddev: 0.041482392683335305",
            "extra": "mean: 35.930486699999165 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_df",
            "value": 16.97212065435768,
            "unit": "iter/sec",
            "range": "stddev: 0.03572295265141721",
            "extra": "mean: 58.92015619999995 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_memberships",
            "value": 1201.2541573862568,
            "unit": "iter/sec",
            "range": "stddev: 0.00005960183727502313",
            "extra": "mean: 832.463300002928 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_members",
            "value": 136.10587719743276,
            "unit": "iter/sec",
            "range": "stddev: 0.0005856501849063392",
            "extra": "mean: 7.347221299998807 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_attributes",
            "value": 14827.951281878477,
            "unit": "iter/sec",
            "range": "stddev: 0.000009944783320100136",
            "extra": "mean: 67.4401999972929 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_attributes",
            "value": 259.62273493458275,
            "unit": "iter/sec",
            "range": "stddev: 0.00004815829583529198",
            "extra": "mean: 3.851742799997737 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_degree",
            "value": 9755.412302703151,
            "unit": "iter/sec",
            "range": "stddev: 0.000014644894111555845",
            "extra": "mean: 102.50720000044566 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_nodestats_degree",
            "value": 9319.647120896452,
            "unit": "iter/sec",
            "range": "stddev: 0.000012382577380077481",
            "extra": "mean: 107.30019999982687 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_size",
            "value": 249.62339941792303,
            "unit": "iter/sec",
            "range": "stddev: 0.0005129064530420028",
            "extra": "mean: 4.006034699999361 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_isolates",
            "value": 8236.038267895372,
            "unit": "iter/sec",
            "range": "stddev: 0.000014412029674078106",
            "extra": "mean: 121.41760000048407 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_singletons",
            "value": 185.5195635853013,
            "unit": "iter/sec",
            "range": "stddev: 0.00038203546250213335",
            "extra": "mean: 5.39026709999888 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_copy",
            "value": 11.442857109868967,
            "unit": "iter/sec",
            "range": "stddev: 0.06709660099193965",
            "extra": "mean: 87.3907618000004 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_dual",
            "value": 11.452976727203758,
            "unit": "iter/sec",
            "range": "stddev: 0.07226125293771617",
            "extra": "mean: 87.31354510000386 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_erdos_renyi",
            "value": 51.10238081443339,
            "unit": "iter/sec",
            "range": "stddev: 0.0013776720257794005",
            "extra": "mean: 19.568559900002924 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_fast_erdos_renyi",
            "value": 33.41587388341152,
            "unit": "iter/sec",
            "range": "stddev: 0.0016320608808190807",
            "extra": "mean: 29.9258970000011 msec\nrounds: 10"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "dleonardotn@gmail.com",
            "name": "Leo Torres",
            "username": "leotrs"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "285693d728310d9865289be9896b00488fe72942",
          "message": "Merge pull request #701 from xgi-org/docs-quick-wins\n\ndocs: introduce stats earlier, add cheat sheet, link quickstart",
          "timestamp": "2026-04-27T09:40:25+02:00",
          "tree_id": "cab4c699f7ac94a690be7b1e9bf8acaf0da60ebc",
          "url": "https://github.com/xgi-org/xgi/commit/285693d728310d9865289be9896b00488fe72942"
        },
        "date": 1777275690081,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/algorithms.py::test_connected",
            "value": 94.4347745859279,
            "unit": "iter/sec",
            "range": "stddev: 0.0002113912864262578",
            "extra": "mean: 10.58931949999078 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/algorithms.py::test_clustering_coefficient",
            "value": 63.74057768452442,
            "unit": "iter/sec",
            "range": "stddev: 0.00039581434069117045",
            "extra": "mean: 15.688593300006916 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgelist",
            "value": 28.227739232238438,
            "unit": "iter/sec",
            "range": "stddev: 0.04414285569064274",
            "extra": "mean: 35.42614559999606 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgedict",
            "value": 27.863214209722504,
            "unit": "iter/sec",
            "range": "stddev: 0.04081421374739969",
            "extra": "mean: 35.88961390000236 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_df",
            "value": 17.783374118670476,
            "unit": "iter/sec",
            "range": "stddev: 0.037088501053681056",
            "extra": "mean: 56.232298400004765 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_memberships",
            "value": 1182.7961822124582,
            "unit": "iter/sec",
            "range": "stddev: 0.000026453193974427692",
            "extra": "mean: 845.4542000038145 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_members",
            "value": 132.99156451792297,
            "unit": "iter/sec",
            "range": "stddev: 0.0006028573212479595",
            "extra": "mean: 7.519273900001622 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_attributes",
            "value": 13814.36804854415,
            "unit": "iter/sec",
            "range": "stddev: 0.000003674880200395887",
            "extra": "mean: 72.38839999672564 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_attributes",
            "value": 253.39417057075937,
            "unit": "iter/sec",
            "range": "stddev: 0.00020442766699303936",
            "extra": "mean: 3.9464207000008855 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_degree",
            "value": 9753.147828840229,
            "unit": "iter/sec",
            "range": "stddev: 0.000011592214069240816",
            "extra": "mean: 102.53099999602 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_nodestats_degree",
            "value": 8310.520953367322,
            "unit": "iter/sec",
            "range": "stddev: 0.00001748382312309325",
            "extra": "mean: 120.32939999926384 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_size",
            "value": 240.89165758009062,
            "unit": "iter/sec",
            "range": "stddev: 0.0003794379714367995",
            "extra": "mean: 4.151243799995541 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_isolates",
            "value": 8143.727009313875,
            "unit": "iter/sec",
            "range": "stddev: 0.0000054992418088871466",
            "extra": "mean: 122.79389999889645 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_singletons",
            "value": 180.4367059069754,
            "unit": "iter/sec",
            "range": "stddev: 0.00018963319028742178",
            "extra": "mean: 5.542109600003187 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_copy",
            "value": 11.416124434623566,
            "unit": "iter/sec",
            "range": "stddev: 0.06347843834297913",
            "extra": "mean: 87.59540120000224 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_dual",
            "value": 11.511859296418876,
            "unit": "iter/sec",
            "range": "stddev: 0.06812429875761578",
            "extra": "mean: 86.8669408000045 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_erdos_renyi",
            "value": 51.146921378049804,
            "unit": "iter/sec",
            "range": "stddev: 0.001326962358728392",
            "extra": "mean: 19.551518900004794 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_fast_erdos_renyi",
            "value": 33.4763439398832,
            "unit": "iter/sec",
            "range": "stddev: 0.0018673381586301217",
            "extra": "mean: 29.871840299998098 msec\nrounds: 10"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "dleonardotn@gmail.com",
            "name": "Leo Torres",
            "username": "leotrs"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "fbcda0cfc2fdbf333f0bdc51973e5ccd58504715",
          "message": "Merge pull request #700 from xgi-org/stats-type-stubs\n\nfeat: add type stubs for stats on view classes",
          "timestamp": "2026-04-27T09:40:28+02:00",
          "tree_id": "0736c2c3c7728022dd8323478102f02daa4b0110",
          "url": "https://github.com/xgi-org/xgi/commit/fbcda0cfc2fdbf333f0bdc51973e5ccd58504715"
        },
        "date": 1777275787956,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/algorithms.py::test_connected",
            "value": 89.37189512543335,
            "unit": "iter/sec",
            "range": "stddev: 0.0003118549004605132",
            "extra": "mean: 11.189199899996538 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/algorithms.py::test_clustering_coefficient",
            "value": 63.04716745217328,
            "unit": "iter/sec",
            "range": "stddev: 0.0003039789480355046",
            "extra": "mean: 15.861140799998452 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgelist",
            "value": 26.47702655260318,
            "unit": "iter/sec",
            "range": "stddev: 0.04594230355620649",
            "extra": "mean: 37.76859150000291 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgedict",
            "value": 26.373671701560575,
            "unit": "iter/sec",
            "range": "stddev: 0.044948427031218166",
            "extra": "mean: 37.91660150000382 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_df",
            "value": 15.97568817217729,
            "unit": "iter/sec",
            "range": "stddev: 0.04002771280419286",
            "extra": "mean: 62.595112600004654 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_memberships",
            "value": 1092.5105126846463,
            "unit": "iter/sec",
            "range": "stddev: 0.00003640542463922005",
            "extra": "mean: 915.3229999981249 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_members",
            "value": 124.16113015632754,
            "unit": "iter/sec",
            "range": "stddev: 0.0013236558573638203",
            "extra": "mean: 8.054050399999824 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_attributes",
            "value": 13677.982004124518,
            "unit": "iter/sec",
            "range": "stddev: 0.000007158467181772919",
            "extra": "mean: 73.1102000059991 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_attributes",
            "value": 257.8236323407123,
            "unit": "iter/sec",
            "range": "stddev: 0.00006141282372181485",
            "extra": "mean: 3.8786204000047064 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_degree",
            "value": 10667.63386471119,
            "unit": "iter/sec",
            "range": "stddev: 0.000013084615112999709",
            "extra": "mean: 93.74150000667214 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_nodestats_degree",
            "value": 10008.59738521298,
            "unit": "iter/sec",
            "range": "stddev: 0.000005107752000139404",
            "extra": "mean: 99.9140999994097 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_size",
            "value": 276.28960521679505,
            "unit": "iter/sec",
            "range": "stddev: 0.00013558573011811784",
            "extra": "mean: 3.619390600002248 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_isolates",
            "value": 8570.625381041891,
            "unit": "iter/sec",
            "range": "stddev: 0.000012073778277138739",
            "extra": "mean: 116.67760000477756 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_singletons",
            "value": 194.2559185359713,
            "unit": "iter/sec",
            "range": "stddev: 0.00021725901939854196",
            "extra": "mean: 5.147848299998259 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_copy",
            "value": 11.107332075859942,
            "unit": "iter/sec",
            "range": "stddev: 0.06790435872703712",
            "extra": "mean: 90.03062060000389 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_dual",
            "value": 10.448733808958929,
            "unit": "iter/sec",
            "range": "stddev: 0.07861976378508963",
            "extra": "mean: 95.705376199993 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_erdos_renyi",
            "value": 49.52966751549798,
            "unit": "iter/sec",
            "range": "stddev: 0.0017587548656781686",
            "extra": "mean: 20.18991950000668 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_fast_erdos_renyi",
            "value": 32.56471169954848,
            "unit": "iter/sec",
            "range": "stddev: 0.0017555580750061102",
            "extra": "mean: 30.708087000010664 msec\nrounds: 10"
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
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "b8164bca1ce6b8b5c613223c33365dc61e432f28",
          "message": "docs: automated the generation of the \"Using XGI\" page (#710)\n\n* docs: automated the generation of the \"Using XGI\" page\n\n* Response to review: added docs and fixed formatting\n\n* docs: change reverse-alphabetical to alphabetical\n\n* response to review\n\n* Update generate_using_xgi.py",
          "timestamp": "2026-04-29T17:57:15-04:00",
          "tree_id": "0b8b036be1548d4318351fad94f29b4d9ebf8c8b",
          "url": "https://github.com/xgi-org/xgi/commit/b8164bca1ce6b8b5c613223c33365dc61e432f28"
        },
        "date": 1777499898685,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/algorithms.py::test_connected",
            "value": 93.82187899382423,
            "unit": "iter/sec",
            "range": "stddev: 0.00029392878819118435",
            "extra": "mean: 10.658494700003018 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/algorithms.py::test_clustering_coefficient",
            "value": 63.82062259263848,
            "unit": "iter/sec",
            "range": "stddev: 0.00040934534538259495",
            "extra": "mean: 15.668916399999944 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgelist",
            "value": 28.16866296807394,
            "unit": "iter/sec",
            "range": "stddev: 0.04480088195203021",
            "extra": "mean: 35.50044250000042 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgedict",
            "value": 28.07019631888242,
            "unit": "iter/sec",
            "range": "stddev: 0.03989058056732139",
            "extra": "mean: 35.62497350000058 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_df",
            "value": 16.981689142160576,
            "unit": "iter/sec",
            "range": "stddev: 0.03499451612000799",
            "extra": "mean: 58.8869571000032 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_memberships",
            "value": 1251.051039255897,
            "unit": "iter/sec",
            "range": "stddev: 0.000013814509893588429",
            "extra": "mean: 799.3278999990139 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_members",
            "value": 136.57112328427138,
            "unit": "iter/sec",
            "range": "stddev: 0.0005487202580852464",
            "extra": "mean: 7.322192099998404 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_attributes",
            "value": 14936.609030944515,
            "unit": "iter/sec",
            "range": "stddev: 0.000004321024806961068",
            "extra": "mean: 66.94960000146466 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_attributes",
            "value": 260.423150117995,
            "unit": "iter/sec",
            "range": "stddev: 0.00012193203017496155",
            "extra": "mean: 3.8399044000001936 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_degree",
            "value": 9626.27897186824,
            "unit": "iter/sec",
            "range": "stddev: 0.000013904385279410327",
            "extra": "mean: 103.88229999591658 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_nodestats_degree",
            "value": 8862.498338266736,
            "unit": "iter/sec",
            "range": "stddev: 0.000006818624005664239",
            "extra": "mean: 112.83500000018876 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_size",
            "value": 264.4874522788777,
            "unit": "iter/sec",
            "range": "stddev: 0.00032344247589357244",
            "extra": "mean: 3.7808976999997412 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_isolates",
            "value": 7767.424663847781,
            "unit": "iter/sec",
            "range": "stddev: 0.000013686775081268475",
            "extra": "mean: 128.74279999834926 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_singletons",
            "value": 183.1940759139932,
            "unit": "iter/sec",
            "range": "stddev: 0.00022465662031197984",
            "extra": "mean: 5.458691799998405 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_copy",
            "value": 11.39311236501296,
            "unit": "iter/sec",
            "range": "stddev: 0.0647222156759197",
            "extra": "mean: 87.7723283999984 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_dual",
            "value": 11.642762518966256,
            "unit": "iter/sec",
            "range": "stddev: 0.06820279536083228",
            "extra": "mean: 85.89026859999791 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_erdos_renyi",
            "value": 51.43572355123449,
            "unit": "iter/sec",
            "range": "stddev: 0.0012279857077558984",
            "extra": "mean: 19.44174070000031 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_fast_erdos_renyi",
            "value": 32.551955859368015,
            "unit": "iter/sec",
            "range": "stddev: 0.001617496199757029",
            "extra": "mean: 30.72012029999769 msec\nrounds: 10"
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
          "id": "b7d0f92ecaa48cd4cd9fe350683a63dd8bccfa5c",
          "message": "small formatting fix to \"Projects using XGI\" page",
          "timestamp": "2026-04-29T18:06:10-04:00",
          "tree_id": "f0db6ffd400aa69dd129e851074a45eda16a006a",
          "url": "https://github.com/xgi-org/xgi/commit/b7d0f92ecaa48cd4cd9fe350683a63dd8bccfa5c"
        },
        "date": 1777500432424,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/algorithms.py::test_connected",
            "value": 87.88624665136973,
            "unit": "iter/sec",
            "range": "stddev: 0.0023711280300693083",
            "extra": "mean: 11.378344600001356 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/algorithms.py::test_clustering_coefficient",
            "value": 64.39537897212756,
            "unit": "iter/sec",
            "range": "stddev: 0.000357171750233152",
            "extra": "mean: 15.529064600005427 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgelist",
            "value": 26.673161972808554,
            "unit": "iter/sec",
            "range": "stddev: 0.048715374899470774",
            "extra": "mean: 37.490868200006844 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgedict",
            "value": 28.060992621531774,
            "unit": "iter/sec",
            "range": "stddev: 0.039613138686774046",
            "extra": "mean: 35.636658099994634 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_df",
            "value": 16.38655452132565,
            "unit": "iter/sec",
            "range": "stddev: 0.03629621139608163",
            "extra": "mean: 61.02564140000197 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_memberships",
            "value": 1235.3715027670466,
            "unit": "iter/sec",
            "range": "stddev: 0.000044578833347391615",
            "extra": "mean: 809.4731000028332 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_members",
            "value": 134.4606225074981,
            "unit": "iter/sec",
            "range": "stddev: 0.0006572518963572526",
            "extra": "mean: 7.437121600000296 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_attributes",
            "value": 14641.609992099353,
            "unit": "iter/sec",
            "range": "stddev: 0.000006630643454601054",
            "extra": "mean: 68.29849999689941 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_attributes",
            "value": 255.01461373989522,
            "unit": "iter/sec",
            "range": "stddev: 0.0002238797765144558",
            "extra": "mean: 3.9213439000008066 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_degree",
            "value": 9747.59575596605,
            "unit": "iter/sec",
            "range": "stddev: 0.0000217497293135164",
            "extra": "mean: 102.5893999951677 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_nodestats_degree",
            "value": 9380.44065546899,
            "unit": "iter/sec",
            "range": "stddev: 0.000009638769235081052",
            "extra": "mean: 106.60480000126427 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_size",
            "value": 238.07965521459616,
            "unit": "iter/sec",
            "range": "stddev: 0.0002609938589176776",
            "extra": "mean: 4.200274900006207 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_isolates",
            "value": 7900.335684821339,
            "unit": "iter/sec",
            "range": "stddev: 0.000011293234154966994",
            "extra": "mean: 126.57690000708044 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_singletons",
            "value": 183.71482696978043,
            "unit": "iter/sec",
            "range": "stddev: 0.0002765221865609854",
            "extra": "mean: 5.44321879999643 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_copy",
            "value": 11.160651594241727,
            "unit": "iter/sec",
            "range": "stddev: 0.06220656784343206",
            "extra": "mean: 89.60050329999945 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_dual",
            "value": 11.410622714651655,
            "unit": "iter/sec",
            "range": "stddev: 0.06991569109028985",
            "extra": "mean: 87.63763600000232 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_erdos_renyi",
            "value": 50.570963626310146,
            "unit": "iter/sec",
            "range": "stddev: 0.001337940113992258",
            "extra": "mean: 19.774193100005277 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_fast_erdos_renyi",
            "value": 32.50385203962902,
            "unit": "iter/sec",
            "range": "stddev: 0.001606984120751371",
            "extra": "mean: 30.765584300002047 msec\nrounds: 10"
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
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "03ebe7fdf7d12903324d6fa23f0e300988a828b6",
          "message": "Merge pull request #716 from xgi-org/dev\n\nv0.10.2",
          "timestamp": "2026-05-15T14:11:24-04:00",
          "tree_id": "7d72fde1f41a173991ce920f073d22732dd96f07",
          "url": "https://github.com/xgi-org/xgi/commit/03ebe7fdf7d12903324d6fa23f0e300988a828b6"
        },
        "date": 1778868746419,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/algorithms.py::test_connected",
            "value": 87.31470869268877,
            "unit": "iter/sec",
            "range": "stddev: 0.0005664257458270484",
            "extra": "mean: 11.452824099998793 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/algorithms.py::test_clustering_coefficient",
            "value": 68.02481659591099,
            "unit": "iter/sec",
            "range": "stddev: 0.00022204965741472955",
            "extra": "mean: 14.700517400000024 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgelist",
            "value": 27.80023751244029,
            "unit": "iter/sec",
            "range": "stddev: 0.046730216397673933",
            "extra": "mean: 35.97091570000117 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgedict",
            "value": 42.22425395010692,
            "unit": "iter/sec",
            "range": "stddev: 0.0020532574707368936",
            "extra": "mean: 23.683070900000303 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_df",
            "value": 22.251708158494882,
            "unit": "iter/sec",
            "range": "stddev: 0.0012800198899265286",
            "extra": "mean: 44.94037010000227 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_memberships",
            "value": 996.6980390670855,
            "unit": "iter/sec",
            "range": "stddev: 0.00003355733048891546",
            "extra": "mean: 1.0033128999992869 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_members",
            "value": 45.69201265968239,
            "unit": "iter/sec",
            "range": "stddev: 0.04509957771826192",
            "extra": "mean: 21.885663200001204 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_attributes",
            "value": 12212.398026569394,
            "unit": "iter/sec",
            "range": "stddev: 0.0000033525893499162547",
            "extra": "mean: 81.88399999937701 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_attributes",
            "value": 266.8017252574166,
            "unit": "iter/sec",
            "range": "stddev: 0.00011704083873511836",
            "extra": "mean: 3.74810169999904 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_degree",
            "value": 10682.824795477101,
            "unit": "iter/sec",
            "range": "stddev: 0.000006081870340732803",
            "extra": "mean: 93.60819999812975 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_nodestats_degree",
            "value": 8963.786303060711,
            "unit": "iter/sec",
            "range": "stddev: 0.000004091428086095426",
            "extra": "mean: 111.56000000340782 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_size",
            "value": 232.80321635319967,
            "unit": "iter/sec",
            "range": "stddev: 0.00017313061719415837",
            "extra": "mean: 4.295473300003039 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_isolates",
            "value": 7701.869860037135,
            "unit": "iter/sec",
            "range": "stddev: 0.000014982180883742963",
            "extra": "mean: 129.83859999877723 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_singletons",
            "value": 180.67298446368866,
            "unit": "iter/sec",
            "range": "stddev: 0.00022863064206404428",
            "extra": "mean: 5.534861799999646 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_copy",
            "value": 11.236257134746232,
            "unit": "iter/sec",
            "range": "stddev: 0.06714428277056728",
            "extra": "mean: 88.99760730000281 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_dual",
            "value": 11.218036322902133,
            "unit": "iter/sec",
            "range": "stddev: 0.07681744527067424",
            "extra": "mean: 89.1421610000009 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_erdos_renyi",
            "value": 11.681734070996185,
            "unit": "iter/sec",
            "range": "stddev: 0.0014298605556963542",
            "extra": "mean: 85.60372920000248 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_fast_erdos_renyi",
            "value": 36.500261887553364,
            "unit": "iter/sec",
            "range": "stddev: 0.0011654017023741757",
            "extra": "mean: 27.3970637000005 msec\nrounds: 10"
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
          "id": "a61d6700096c3b5e864f34ef58c415f7b5c072ff",
          "message": "Up-version and update changelog",
          "timestamp": "2026-05-15T14:24:52-04:00",
          "tree_id": "cc1a9e330d4e940c19d8996246a6f88168fd6b4b",
          "url": "https://github.com/xgi-org/xgi/commit/a61d6700096c3b5e864f34ef58c415f7b5c072ff"
        },
        "date": 1778869552839,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/algorithms.py::test_connected",
            "value": 81.2314472959121,
            "unit": "iter/sec",
            "range": "stddev: 0.0006352248755845789",
            "extra": "mean: 12.310503299998743 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/algorithms.py::test_clustering_coefficient",
            "value": 67.24583260765142,
            "unit": "iter/sec",
            "range": "stddev: 0.0002576530713927346",
            "extra": "mean: 14.870809999997192 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgelist",
            "value": 26.77449498342416,
            "unit": "iter/sec",
            "range": "stddev: 0.051075166188179796",
            "extra": "mean: 37.34897710000098 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgedict",
            "value": 42.42865850187684,
            "unit": "iter/sec",
            "range": "stddev: 0.0005153334631004663",
            "extra": "mean: 23.568975199999898 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_df",
            "value": 21.178516457840963,
            "unit": "iter/sec",
            "range": "stddev: 0.00133629593937905",
            "extra": "mean: 47.217660500000136 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_memberships",
            "value": 890.3606352342551,
            "unit": "iter/sec",
            "range": "stddev: 0.00004307159745346622",
            "extra": "mean: 1.12314039999859 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_members",
            "value": 41.88882597513547,
            "unit": "iter/sec",
            "range": "stddev: 0.04848114714134743",
            "extra": "mean: 23.87271489999705 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_attributes",
            "value": 11239.84480002807,
            "unit": "iter/sec",
            "range": "stddev: 0.000005814794746413098",
            "extra": "mean: 88.96920000154296 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_attributes",
            "value": 239.48261218527324,
            "unit": "iter/sec",
            "range": "stddev: 0.00033083621950915834",
            "extra": "mean: 4.175668500000995 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_degree",
            "value": 8268.802222694907,
            "unit": "iter/sec",
            "range": "stddev: 0.000006779105615446892",
            "extra": "mean: 120.93649999940226 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_nodestats_degree",
            "value": 8068.843371408668,
            "unit": "iter/sec",
            "range": "stddev: 0.00000767528416139897",
            "extra": "mean: 123.93350000365898 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_size",
            "value": 212.3858725929688,
            "unit": "iter/sec",
            "range": "stddev: 0.0003805213017135643",
            "extra": "mean: 4.708411100000376 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_isolates",
            "value": 7393.9504175922,
            "unit": "iter/sec",
            "range": "stddev: 0.000010084645657327262",
            "extra": "mean: 135.24570000100766 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_singletons",
            "value": 161.6688022846005,
            "unit": "iter/sec",
            "range": "stddev: 0.0005500270248412837",
            "extra": "mean: 6.185485299999982 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_copy",
            "value": 10.145116013373368,
            "unit": "iter/sec",
            "range": "stddev: 0.0838447074244712",
            "extra": "mean: 98.56959730000057 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_dual",
            "value": 10.383026720027711,
            "unit": "iter/sec",
            "range": "stddev: 0.08595981451863913",
            "extra": "mean: 96.3110302000004 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_erdos_renyi",
            "value": 11.399944500282308,
            "unit": "iter/sec",
            "range": "stddev: 0.004196287646059247",
            "extra": "mean: 87.71972529999914 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_fast_erdos_renyi",
            "value": 35.551443217418615,
            "unit": "iter/sec",
            "range": "stddev: 0.0011639407889912975",
            "extra": "mean: 28.128253299996686 msec\nrounds: 10"
          }
        ]
      }
    ]
  }
}