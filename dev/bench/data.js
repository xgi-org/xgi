window.BENCHMARK_DATA = {
  "lastUpdate": 1755447222630,
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
      }
    ]
  }
}