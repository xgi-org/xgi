window.BENCHMARK_DATA = {
  "lastUpdate": 1732722766582,
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
            "email": "nicholas.landry.91@gmail.com",
            "name": "Nicholas Landry",
            "username": "nwlandry"
          },
          "distinct": true,
          "id": "a9c77e41ca65c5e5f1bc8e26e19e6a84604f8fb9",
          "message": "fix filepath",
          "timestamp": "2024-11-24T17:12:48-05:00",
          "tree_id": "2b02c7e7df0788890df8989a8c880a3d018d6cdb",
          "url": "https://github.com/xgi-org/xgi/commit/a9c77e41ca65c5e5f1bc8e26e19e6a84604f8fb9"
        },
        "date": 1732486432762,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/core.py::test_construct_from_edgelist",
            "value": 20.580113092208133,
            "unit": "iter/sec",
            "range": "stddev: 0.048336137203109794",
            "extra": "mean: 48.590597899999466 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgedict",
            "value": 36.58853665194456,
            "unit": "iter/sec",
            "range": "stddev: 0.0006728024576353108",
            "extra": "mean: 27.330964599997287 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_df",
            "value": 19.532958981309505,
            "unit": "iter/sec",
            "range": "stddev: 0.032778676406075874",
            "extra": "mean: 51.195520400000305 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_memberships",
            "value": 1114.1343766431821,
            "unit": "iter/sec",
            "range": "stddev: 0.0001448175660616618",
            "extra": "mean: 897.557799996207 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_members",
            "value": 48.62219031870955,
            "unit": "iter/sec",
            "range": "stddev: 0.037878147975698585",
            "extra": "mean: 20.566741100003583 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_attributes",
            "value": 12718.552426598237,
            "unit": "iter/sec",
            "range": "stddev: 0.000005305626298380904",
            "extra": "mean: 78.62529999158596 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_attributes",
            "value": 225.46954483639777,
            "unit": "iter/sec",
            "range": "stddev: 0.00007244383276464813",
            "extra": "mean: 4.4351888000022655 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_degree",
            "value": 10627.760560577382,
            "unit": "iter/sec",
            "range": "stddev: 0.000004928701833156152",
            "extra": "mean: 94.09320000202115 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_nodestats_degree",
            "value": 9284.654508179154,
            "unit": "iter/sec",
            "range": "stddev: 0.0000043083294642210265",
            "extra": "mean: 107.70460000628646 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_size",
            "value": 244.52905964998385,
            "unit": "iter/sec",
            "range": "stddev: 0.00008746664573124768",
            "extra": "mean: 4.08949350000114 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_isolates",
            "value": 8503.987094210906,
            "unit": "iter/sec",
            "range": "stddev: 0.000004266138105069425",
            "extra": "mean: 117.59190000191211 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_singletons",
            "value": 187.3340243959503,
            "unit": "iter/sec",
            "range": "stddev: 0.00011485338898010783",
            "extra": "mean: 5.338058600003137 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_copy",
            "value": 12.281298550084468,
            "unit": "iter/sec",
            "range": "stddev: 0.04496261710571643",
            "extra": "mean: 81.424614499997 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_dual",
            "value": 10.60323548802993,
            "unit": "iter/sec",
            "range": "stddev: 0.06391991868746723",
            "extra": "mean: 94.31083569999998 msec\nrounds: 10"
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
          "id": "60bb6799649be52d2cc5cc3173f22f1d049202d5",
          "message": "update",
          "timestamp": "2024-11-24T17:21:08-05:00",
          "tree_id": "471e24faaa0d33dcbb9210fa8181bb3fb32451f5",
          "url": "https://github.com/xgi-org/xgi/commit/60bb6799649be52d2cc5cc3173f22f1d049202d5"
        },
        "date": 1732487064990,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/core.py::test_construct_from_edgelist",
            "value": 25.7342034510147,
            "unit": "iter/sec",
            "range": "stddev: 0.03770966362325038",
            "extra": "mean: 38.858789700000216 msec\nrounds: 100"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgedict",
            "value": 24.308225305997464,
            "unit": "iter/sec",
            "range": "stddev: 0.03821804354536747",
            "extra": "mean: 41.1383384599975 msec\nrounds: 100"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_df",
            "value": 20.726033517878996,
            "unit": "iter/sec",
            "range": "stddev: 0.02659419560901577",
            "extra": "mean: 48.248498640001 msec\nrounds: 100"
          },
          {
            "name": "benchmarks/core.py::test_node_memberships",
            "value": 1263.1363017555707,
            "unit": "iter/sec",
            "range": "stddev: 0.000042030199425375033",
            "extra": "mean: 791.6801999991208 usec\nrounds: 100"
          },
          {
            "name": "benchmarks/core.py::test_edge_members",
            "value": 67.35283938870829,
            "unit": "iter/sec",
            "range": "stddev: 0.027562038779780897",
            "extra": "mean: 14.847184009998102 msec\nrounds: 100"
          },
          {
            "name": "benchmarks/core.py::test_node_attributes",
            "value": 13299.68159219077,
            "unit": "iter/sec",
            "range": "stddev: 0.000004558205668727357",
            "extra": "mean: 75.18977000074756 usec\nrounds: 100"
          },
          {
            "name": "benchmarks/core.py::test_edge_attributes",
            "value": 231.5094121273792,
            "unit": "iter/sec",
            "range": "stddev: 0.0001242361609786864",
            "extra": "mean: 4.319478810000987 msec\nrounds: 100"
          },
          {
            "name": "benchmarks/core.py::test_degree",
            "value": 10857.29411460062,
            "unit": "iter/sec",
            "range": "stddev: 0.0000071479240978061495",
            "extra": "mean: 92.10398000135456 usec\nrounds: 100"
          },
          {
            "name": "benchmarks/core.py::test_nodestats_degree",
            "value": 9644.905445298073,
            "unit": "iter/sec",
            "range": "stddev: 0.000007661843140323563",
            "extra": "mean: 103.68167999899924 usec\nrounds: 100"
          },
          {
            "name": "benchmarks/core.py::test_edge_size",
            "value": 258.49310369873774,
            "unit": "iter/sec",
            "range": "stddev: 0.0002800744818155445",
            "extra": "mean: 3.868575159999068 msec\nrounds: 100"
          },
          {
            "name": "benchmarks/core.py::test_isolates",
            "value": 8493.111407244665,
            "unit": "iter/sec",
            "range": "stddev: 0.00000668349495631835",
            "extra": "mean: 117.7424799993787 usec\nrounds: 100"
          },
          {
            "name": "benchmarks/core.py::test_singletons",
            "value": 192.98064439070106,
            "unit": "iter/sec",
            "range": "stddev: 0.00022813097843320831",
            "extra": "mean: 5.181866829998967 msec\nrounds: 100"
          },
          {
            "name": "benchmarks/core.py::test_copy",
            "value": 12.80768880026752,
            "unit": "iter/sec",
            "range": "stddev: 0.03962380542504712",
            "extra": "mean: 78.07809945999878 msec\nrounds: 100"
          },
          {
            "name": "benchmarks/core.py::test_dual",
            "value": 13.007486449721082,
            "unit": "iter/sec",
            "range": "stddev: 0.04473471458958939",
            "extra": "mean: 76.8788038999989 msec\nrounds: 100"
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
          "id": "71b897f9395dea85bac449f81aaec866694ae1b0",
          "message": "fix iterations",
          "timestamp": "2024-11-24T18:42:53-05:00",
          "tree_id": "f8b4518c0a36fa3e23fad901a571a61f1d69f345",
          "url": "https://github.com/xgi-org/xgi/commit/71b897f9395dea85bac449f81aaec866694ae1b0"
        },
        "date": 1732491843998,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/algorithms.py::test_connected",
            "value": 92.23766121817006,
            "unit": "iter/sec",
            "range": "stddev: 0.00015448424147658773",
            "extra": "mean: 10.841558500000303 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/algorithms.py::test_clustering_coefficient",
            "value": 56.800834649645914,
            "unit": "iter/sec",
            "range": "stddev: 0.00040275855308559053",
            "extra": "mean: 17.605375099998355 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgelist",
            "value": 19.96773649079654,
            "unit": "iter/sec",
            "range": "stddev: 0.05246381300469888",
            "extra": "mean: 50.08078910000222 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgedict",
            "value": 36.5385924449952,
            "unit": "iter/sec",
            "range": "stddev: 0.000608732922034258",
            "extra": "mean: 27.368323000000316 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_df",
            "value": 20.180950270697924,
            "unit": "iter/sec",
            "range": "stddev: 0.03138025041200466",
            "extra": "mean: 49.55168049999941 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_memberships",
            "value": 1275.8242781696467,
            "unit": "iter/sec",
            "range": "stddev: 0.00002325155676281878",
            "extra": "mean: 783.8070000005359 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_members",
            "value": 119.8984397867633,
            "unit": "iter/sec",
            "range": "stddev: 0.0005727181484078093",
            "extra": "mean: 8.340392100001282 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_attributes",
            "value": 13999.955199635115,
            "unit": "iter/sec",
            "range": "stddev: 0.000003764670406816324",
            "extra": "mean: 71.4288000025931 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_attributes",
            "value": 234.11846834645945,
            "unit": "iter/sec",
            "range": "stddev: 0.000056508410083019674",
            "extra": "mean: 4.271341799999107 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_degree",
            "value": 11145.898699826887,
            "unit": "iter/sec",
            "range": "stddev: 0.000006307138131506437",
            "extra": "mean: 89.71909999644367 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_nodestats_degree",
            "value": 10186.100047659114,
            "unit": "iter/sec",
            "range": "stddev: 0.0000036204724955588704",
            "extra": "mean: 98.17300000207752 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_size",
            "value": 266.63496199198687,
            "unit": "iter/sec",
            "range": "stddev: 0.00019995406235429262",
            "extra": "mean: 3.750445900001864 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_isolates",
            "value": 7999.270466434904,
            "unit": "iter/sec",
            "range": "stddev: 0.00001203358529176826",
            "extra": "mean: 125.0114000015401 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_singletons",
            "value": 185.2959372531518,
            "unit": "iter/sec",
            "range": "stddev: 0.00045870380997684073",
            "extra": "mean: 5.396772400000316 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_copy",
            "value": 9.951700545942318,
            "unit": "iter/sec",
            "range": "stddev: 0.06622935553861015",
            "extra": "mean: 100.48533870000114 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_dual",
            "value": 10.235818969621151,
            "unit": "iter/sec",
            "range": "stddev: 0.07080257275813118",
            "extra": "mean: 97.69613969999824 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_erdos_renyi",
            "value": 30.844487427403482,
            "unit": "iter/sec",
            "range": "stddev: 0.0012947020100274567",
            "extra": "mean: 32.4207040999994 msec\nrounds: 10"
          }
        ]
      }
    ],
    "Python Benchmark with pytest-benchmark": [
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
          "id": "be8039e7fcdeabf77f1f8d3dba37f1a1e366d8da",
          "message": "Modify changelog generator (#626)\n\n* modify changelog generator\r\n\r\n* Changed the formatting of the changelog generator.\r\n\r\n* update\r\n\r\n* Update HOW_TO_CONTRIBUTE.md\r\n\r\n* Update check-urls.yml\r\n\r\n* remove unused dependency",
          "timestamp": "2024-11-26T14:09:39-05:00",
          "tree_id": "82366c5a589a7661b863f28fd860fc5f0569adb3",
          "url": "https://github.com/xgi-org/xgi/commit/be8039e7fcdeabf77f1f8d3dba37f1a1e366d8da"
        },
        "date": 1732722763282,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/algorithms.py::test_connected",
            "value": 91.50512953508559,
            "unit": "iter/sec",
            "range": "stddev: 0.00021251527630285276",
            "extra": "mean: 10.928349099998513 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/algorithms.py::test_clustering_coefficient",
            "value": 57.44556210083509,
            "unit": "iter/sec",
            "range": "stddev: 0.00036858183914411",
            "extra": "mean: 17.407785099999273 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgelist",
            "value": 20.253986325281836,
            "unit": "iter/sec",
            "range": "stddev: 0.050445329220540666",
            "extra": "mean: 49.372996700000726 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgedict",
            "value": 36.460942265666766,
            "unit": "iter/sec",
            "range": "stddev: 0.00032022659907138105",
            "extra": "mean: 27.426608800004715 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_df",
            "value": 20.23170907022532,
            "unit": "iter/sec",
            "range": "stddev: 0.029990868787670932",
            "extra": "mean: 49.427361599998676 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_memberships",
            "value": 1293.2406321192216,
            "unit": "iter/sec",
            "range": "stddev: 0.000013528577437488455",
            "extra": "mean: 773.2513000007657 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_members",
            "value": 119.37603816121816,
            "unit": "iter/sec",
            "range": "stddev: 0.0005606722295711288",
            "extra": "mean: 8.376890499997103 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_attributes",
            "value": 13184.923830595184,
            "unit": "iter/sec",
            "range": "stddev: 0.0000033705551059319125",
            "extra": "mean: 75.84420000057435 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_attributes",
            "value": 231.74731496387682,
            "unit": "iter/sec",
            "range": "stddev: 0.00006497615594572562",
            "extra": "mean: 4.315044600002693 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_degree",
            "value": 10752.873167927415,
            "unit": "iter/sec",
            "range": "stddev: 0.000009399630716875031",
            "extra": "mean: 92.9983999981232 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_nodestats_degree",
            "value": 10186.017042578962,
            "unit": "iter/sec",
            "range": "stddev: 0.000005830485444734796",
            "extra": "mean: 98.17380000640696 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_size",
            "value": 260.7945607018073,
            "unit": "iter/sec",
            "range": "stddev: 0.0002627370806488222",
            "extra": "mean: 3.8344357999989143 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_isolates",
            "value": 8817.377994133934,
            "unit": "iter/sec",
            "range": "stddev: 0.000008451186898689532",
            "extra": "mean: 113.41239999751451 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_singletons",
            "value": 176.2140837590171,
            "unit": "iter/sec",
            "range": "stddev: 0.0004784791640199272",
            "extra": "mean: 5.674915300002681 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_copy",
            "value": 10.64208488088802,
            "unit": "iter/sec",
            "range": "stddev: 0.06167937430842019",
            "extra": "mean: 93.96654990000002 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_dual",
            "value": 10.523377186242078,
            "unit": "iter/sec",
            "range": "stddev: 0.06682000865930143",
            "extra": "mean: 95.02652829999931 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_erdos_renyi",
            "value": 31.069288493308285,
            "unit": "iter/sec",
            "range": "stddev: 0.002561211250297945",
            "extra": "mean: 32.18612490000794 msec\nrounds: 10"
          }
        ]
      }
    ]
  }
}