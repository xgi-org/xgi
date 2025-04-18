window.BENCHMARK_DATA = {
  "lastUpdate": 1744985321347,
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
          "id": "ade37fb034f308f2a06789b0ffa447789f996db1",
          "message": "fix syntax error",
          "timestamp": "2024-12-02T18:39:55-05:00",
          "tree_id": "61abb61633952e7989abd7a1d9f1f3c1c5074880",
          "url": "https://github.com/xgi-org/xgi/commit/ade37fb034f308f2a06789b0ffa447789f996db1"
        },
        "date": 1733182900633,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/algorithms.py::test_connected",
            "value": 90.67354247767133,
            "unit": "iter/sec",
            "range": "stddev: 0.00010948006320670888",
            "extra": "mean: 11.028575399998886 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/algorithms.py::test_clustering_coefficient",
            "value": 56.66627948486963,
            "unit": "iter/sec",
            "range": "stddev: 0.00111645565947214",
            "extra": "mean: 17.647179399999402 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgelist",
            "value": 19.968585740411235,
            "unit": "iter/sec",
            "range": "stddev: 0.05141806114954402",
            "extra": "mean: 50.0786591999983 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgedict",
            "value": 35.85804008473057,
            "unit": "iter/sec",
            "range": "stddev: 0.0004890896044718541",
            "extra": "mean: 27.887748399997747 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_df",
            "value": 19.738234611743678,
            "unit": "iter/sec",
            "range": "stddev: 0.03092689628698586",
            "extra": "mean: 50.66309219999994 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_memberships",
            "value": 1274.2775356077866,
            "unit": "iter/sec",
            "range": "stddev: 0.000018542018401796288",
            "extra": "mean: 784.7584000003849 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_members",
            "value": 118.7249557126253,
            "unit": "iter/sec",
            "range": "stddev: 0.0005415036294183851",
            "extra": "mean: 8.422828999999865 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_attributes",
            "value": 13413.546341372548,
            "unit": "iter/sec",
            "range": "stddev: 0.0000032588621480755636",
            "extra": "mean: 74.55149999486821 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_attributes",
            "value": 227.84086400174024,
            "unit": "iter/sec",
            "range": "stddev: 0.00014505376051092634",
            "extra": "mean: 4.389028299999609 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_degree",
            "value": 10535.798007445383,
            "unit": "iter/sec",
            "range": "stddev: 0.0000069930346799349515",
            "extra": "mean: 94.91450000211898 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_nodestats_degree",
            "value": 9208.849336033189,
            "unit": "iter/sec",
            "range": "stddev: 0.000008614414668051977",
            "extra": "mean: 108.59119999793165 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_size",
            "value": 254.9764909126118,
            "unit": "iter/sec",
            "range": "stddev: 0.00017615410390433065",
            "extra": "mean: 3.9219301999992244 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_isolates",
            "value": 8466.411205853285,
            "unit": "iter/sec",
            "range": "stddev: 0.000007542297680097357",
            "extra": "mean: 118.11380001347516 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_singletons",
            "value": 189.5960027703423,
            "unit": "iter/sec",
            "range": "stddev: 0.000189387692537369",
            "extra": "mean: 5.2743727999967405 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_copy",
            "value": 10.653184519055372,
            "unit": "iter/sec",
            "range": "stddev: 0.0615543725148747",
            "extra": "mean: 93.86864540000204 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_dual",
            "value": 10.569125051460395,
            "unit": "iter/sec",
            "range": "stddev: 0.06475647148697551",
            "extra": "mean: 94.6152112999954 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_erdos_renyi",
            "value": 40.31546366533193,
            "unit": "iter/sec",
            "range": "stddev: 0.001047120543829645",
            "extra": "mean: 24.804377999996063 msec\nrounds: 10"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "97421170+willcollins10@users.noreply.github.com",
            "name": "Will Collins",
            "username": "willcollins10"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "e4b3c3bf003ff697db616b69aa75ca240a693f0d",
          "message": "Add metadata attributes to ashist() for improved plotting (#635)\n\n* test: Add simple benchmark test\r\n\r\n* test: Add pedantic benchmark test to understand workflow\r\n\r\n* Attempting to change results from data.js\r\n\r\n* Reverted benchmarks.yml back to normal\r\n\r\n* Added pull_request to benchmark.yml workflow to understand what happens when a pull request is made\r\n\r\n* Added two branches for each fix and added ashist function to add-metadata-attributes branch\r\n\r\n* Added unittests to add-metadata-attributes\r\n\r\n* Changed benhmark.yml and core.py back to normal",
          "timestamp": "2024-12-10T10:26:29-05:00",
          "tree_id": "2872ae66cb5d455804bc8c5a06d35c2f078a06ce",
          "url": "https://github.com/xgi-org/xgi/commit/e4b3c3bf003ff697db616b69aa75ca240a693f0d"
        },
        "date": 1733844460428,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/algorithms.py::test_connected",
            "value": 88.16390806056522,
            "unit": "iter/sec",
            "range": "stddev: 0.0002082254185061371",
            "extra": "mean: 11.34250990000396 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/algorithms.py::test_clustering_coefficient",
            "value": 57.37884847754879,
            "unit": "iter/sec",
            "range": "stddev: 0.0002630558347809407",
            "extra": "mean: 17.428024899999173 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgelist",
            "value": 19.326056202214875,
            "unit": "iter/sec",
            "range": "stddev: 0.05366145838688594",
            "extra": "mean: 51.74361439999302 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgedict",
            "value": 34.70591526231726,
            "unit": "iter/sec",
            "range": "stddev: 0.0015917824073934299",
            "extra": "mean: 28.813531999998077 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_df",
            "value": 20.103124081170066,
            "unit": "iter/sec",
            "range": "stddev: 0.03243989818987664",
            "extra": "mean: 49.74351229999456 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_memberships",
            "value": 1244.3904434355256,
            "unit": "iter/sec",
            "range": "stddev: 0.000020663143575010945",
            "extra": "mean: 803.6062999963178 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_members",
            "value": 116.19024637724074,
            "unit": "iter/sec",
            "range": "stddev: 0.0005865940871705771",
            "extra": "mean: 8.606574399999545 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_attributes",
            "value": 12802.064717704103,
            "unit": "iter/sec",
            "range": "stddev: 0.000005313581884136515",
            "extra": "mean: 78.11239999568897 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_attributes",
            "value": 217.3813756903169,
            "unit": "iter/sec",
            "range": "stddev: 0.00024224507572507647",
            "extra": "mean: 4.600210099988544 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_degree",
            "value": 9705.468158514026,
            "unit": "iter/sec",
            "range": "stddev: 0.000011414155689809506",
            "extra": "mean: 103.03469999257686 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_nodestats_degree",
            "value": 8815.465853383212,
            "unit": "iter/sec",
            "range": "stddev: 0.000009321846764480271",
            "extra": "mean: 113.43699999883938 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_size",
            "value": 260.37376601986506,
            "unit": "iter/sec",
            "range": "stddev: 0.0001607751153301305",
            "extra": "mean: 3.840632700007518 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_isolates",
            "value": 8531.8335503909,
            "unit": "iter/sec",
            "range": "stddev: 0.000007656044107387636",
            "extra": "mean: 117.20810000497295 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_singletons",
            "value": 190.30503194257807,
            "unit": "iter/sec",
            "range": "stddev: 0.0002384073968408701",
            "extra": "mean: 5.25472180000861 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_copy",
            "value": 10.233553734847174,
            "unit": "iter/sec",
            "range": "stddev: 0.06474882084057107",
            "extra": "mean: 97.71776509999768 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_dual",
            "value": 10.276499062437225,
            "unit": "iter/sec",
            "range": "stddev: 0.06874853134030573",
            "extra": "mean: 97.30940410000244 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_erdos_renyi",
            "value": 39.38877041753337,
            "unit": "iter/sec",
            "range": "stddev: 0.0012246776742394973",
            "extra": "mean: 25.387946600000078 msec\nrounds: 10"
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
          "id": "943b64a12e209a9f6604672924d297aca78d0116",
          "message": "Fix issue with load_xgi_data HIF (#637)",
          "timestamp": "2024-12-10T10:28:17-05:00",
          "tree_id": "b335399fa7739f44067eee0f6d8af2d9b9433599",
          "url": "https://github.com/xgi-org/xgi/commit/943b64a12e209a9f6604672924d297aca78d0116"
        },
        "date": 1733844564893,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/algorithms.py::test_connected",
            "value": 88.00654543401401,
            "unit": "iter/sec",
            "range": "stddev: 0.0002959567153032041",
            "extra": "mean: 11.362791199999833 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/algorithms.py::test_clustering_coefficient",
            "value": 56.70296332976113,
            "unit": "iter/sec",
            "range": "stddev: 0.0003134076169702502",
            "extra": "mean: 17.63576259999695 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgelist",
            "value": 19.212745680151276,
            "unit": "iter/sec",
            "range": "stddev: 0.0547711259365941",
            "extra": "mean: 52.04878140000062 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgedict",
            "value": 35.28823410206005,
            "unit": "iter/sec",
            "range": "stddev: 0.0005459288457003986",
            "extra": "mean: 28.33805730000023 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_df",
            "value": 20.123244974834318,
            "unit": "iter/sec",
            "range": "stddev: 0.031786690577760006",
            "extra": "mean: 49.69377460000004 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_memberships",
            "value": 1179.8747350589917,
            "unit": "iter/sec",
            "range": "stddev: 0.000036086464136019724",
            "extra": "mean: 847.5476000000981 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_members",
            "value": 114.32510483730398,
            "unit": "iter/sec",
            "range": "stddev: 0.0005983537459936224",
            "extra": "mean: 8.74698519999697 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_attributes",
            "value": 12156.384594017029,
            "unit": "iter/sec",
            "range": "stddev: 0.0000059989707293722546",
            "extra": "mean: 82.26129999968634 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_attributes",
            "value": 222.9346917724107,
            "unit": "iter/sec",
            "range": "stddev: 0.00020283252907937345",
            "extra": "mean: 4.485618600001828 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_degree",
            "value": 10196.423909589445,
            "unit": "iter/sec",
            "range": "stddev: 0.000007316945997602739",
            "extra": "mean: 98.07360000593235 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_nodestats_degree",
            "value": 8420.400271990187,
            "unit": "iter/sec",
            "range": "stddev: 0.000007761924702298439",
            "extra": "mean: 118.7592000022164 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_size",
            "value": 223.15438270973567,
            "unit": "iter/sec",
            "range": "stddev: 0.00013542302266081135",
            "extra": "mean: 4.481202599998824 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_isolates",
            "value": 7538.447969354458,
            "unit": "iter/sec",
            "range": "stddev: 0.000004541731412798777",
            "extra": "mean: 132.65329999825326 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_singletons",
            "value": 173.0137959990204,
            "unit": "iter/sec",
            "range": "stddev: 0.00013433214667637078",
            "extra": "mean: 5.77988589999876 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_copy",
            "value": 10.183578161861666,
            "unit": "iter/sec",
            "range": "stddev: 0.06557731935739788",
            "extra": "mean: 98.19731179999991 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_dual",
            "value": 10.155578207708292,
            "unit": "iter/sec",
            "range": "stddev: 0.06936763129338827",
            "extra": "mean: 98.46805169999868 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_erdos_renyi",
            "value": 39.74656066650797,
            "unit": "iter/sec",
            "range": "stddev: 0.0011288365580202596",
            "extra": "mean: 25.159409600001936 msec\nrounds: 10"
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
          "id": "a549885b59a021c680b2c3aed1410488763a79ba",
          "message": "Update using-xgi.rst (#638)",
          "timestamp": "2024-12-13T15:17:40-05:00",
          "tree_id": "e1a831cf5df5a2450a7ec7dc3e57be0cd60bb0ca",
          "url": "https://github.com/xgi-org/xgi/commit/a549885b59a021c680b2c3aed1410488763a79ba"
        },
        "date": 1734121221334,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/algorithms.py::test_connected",
            "value": 90.01149059689672,
            "unit": "iter/sec",
            "range": "stddev: 0.0001430146969484794",
            "extra": "mean: 11.109692699994866 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/algorithms.py::test_clustering_coefficient",
            "value": 57.907481090015246,
            "unit": "iter/sec",
            "range": "stddev: 0.0002714653066650613",
            "extra": "mean: 17.26892590001512 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgelist",
            "value": 19.968435414898213,
            "unit": "iter/sec",
            "range": "stddev: 0.051064768781202884",
            "extra": "mean: 50.07903619999752 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgedict",
            "value": 35.81267117985934,
            "unit": "iter/sec",
            "range": "stddev: 0.0003758378461342889",
            "extra": "mean: 27.923077700006615 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_df",
            "value": 20.405574380932794,
            "unit": "iter/sec",
            "range": "stddev: 0.03106414053791275",
            "extra": "mean: 49.006216700001914 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_memberships",
            "value": 1224.4482146593339,
            "unit": "iter/sec",
            "range": "stddev: 0.00003957366123791363",
            "extra": "mean: 816.6943999981413 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_members",
            "value": 116.5218117993949,
            "unit": "iter/sec",
            "range": "stddev: 0.0006044159358872707",
            "extra": "mean: 8.582084200008921 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_attributes",
            "value": 13285.717323853745,
            "unit": "iter/sec",
            "range": "stddev: 0.000004340601412124837",
            "extra": "mean: 75.26879999204539 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_attributes",
            "value": 226.09956855275095,
            "unit": "iter/sec",
            "range": "stddev: 0.00005619143071507336",
            "extra": "mean: 4.422830199990813 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_degree",
            "value": 10696.399804327948,
            "unit": "iter/sec",
            "range": "stddev: 0.000007206317290144345",
            "extra": "mean: 93.48940001245865 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_nodestats_degree",
            "value": 9855.129595102637,
            "unit": "iter/sec",
            "range": "stddev: 0.000006198287226768396",
            "extra": "mean: 101.4699999984714 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_size",
            "value": 250.45937379950084,
            "unit": "iter/sec",
            "range": "stddev: 0.00023711239394873064",
            "extra": "mean: 3.9926634999915227 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_isolates",
            "value": 8227.831959192054,
            "unit": "iter/sec",
            "range": "stddev: 0.000013742663450867518",
            "extra": "mean: 121.53869998314804 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_singletons",
            "value": 183.5867497512674,
            "unit": "iter/sec",
            "range": "stddev: 0.00019142027342091287",
            "extra": "mean: 5.447016199997279 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_copy",
            "value": 10.48145985244519,
            "unit": "iter/sec",
            "range": "stddev: 0.06097930929470572",
            "extra": "mean: 95.40655730000367 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_dual",
            "value": 10.744108008257506,
            "unit": "iter/sec",
            "range": "stddev: 0.06467352398164236",
            "extra": "mean: 93.07426909999776 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_erdos_renyi",
            "value": 39.85521588479591,
            "unit": "iter/sec",
            "range": "stddev: 0.0017333983498968217",
            "extra": "mean: 25.090818799992576 msec\nrounds: 10"
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
          "id": "ddc5cbb73ac1da6e9f164b46434f21fb43a326e0",
          "message": "Improve changelog generator (#639)\n\n* format with isort and black\r\n\r\n* associate issues with PRs",
          "timestamp": "2024-12-20T13:18:55-05:00",
          "tree_id": "0ef5e10492bf932bfa9a53e7996fde9a917ae3a8",
          "url": "https://github.com/xgi-org/xgi/commit/ddc5cbb73ac1da6e9f164b46434f21fb43a326e0"
        },
        "date": 1734718804501,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/algorithms.py::test_connected",
            "value": 90.6459810604257,
            "unit": "iter/sec",
            "range": "stddev: 0.0006879585634238404",
            "extra": "mean: 11.031928699998161 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/algorithms.py::test_clustering_coefficient",
            "value": 59.90111129199528,
            "unit": "iter/sec",
            "range": "stddev: 0.00037563806573235665",
            "extra": "mean: 16.694181100002936 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgelist",
            "value": 20.592943664758256,
            "unit": "iter/sec",
            "range": "stddev: 0.055112650035053945",
            "extra": "mean: 48.56032319999741 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgedict",
            "value": 40.659420829887935,
            "unit": "iter/sec",
            "range": "stddev: 0.000548467722877444",
            "extra": "mean: 24.594546100000514 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_df",
            "value": 21.654428478739717,
            "unit": "iter/sec",
            "range": "stddev: 0.03420178191989865",
            "extra": "mean: 46.17993040000101 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_memberships",
            "value": 1033.2726182320132,
            "unit": "iter/sec",
            "range": "stddev: 0.0001573063396742263",
            "extra": "mean: 967.7988000021287 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_members",
            "value": 130.8271320400953,
            "unit": "iter/sec",
            "range": "stddev: 0.0005833365026021968",
            "extra": "mean: 7.643674399997735 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_attributes",
            "value": 11990.68084265124,
            "unit": "iter/sec",
            "range": "stddev: 0.000006427011131777534",
            "extra": "mean: 83.39810000137504 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_attributes",
            "value": 253.08741335539906,
            "unit": "iter/sec",
            "range": "stddev: 0.0003503147061626486",
            "extra": "mean: 3.9512040000019515 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_degree",
            "value": 8812.27302896715,
            "unit": "iter/sec",
            "range": "stddev: 0.000009840756558127338",
            "extra": "mean: 113.47809999904257 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_nodestats_degree",
            "value": 8039.903649905054,
            "unit": "iter/sec",
            "range": "stddev: 0.000007421545017271623",
            "extra": "mean: 124.37959999829219 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_size",
            "value": 213.74182074178387,
            "unit": "iter/sec",
            "range": "stddev: 0.0002339026308563718",
            "extra": "mean: 4.678541599999164 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_isolates",
            "value": 7510.230812020581,
            "unit": "iter/sec",
            "range": "stddev: 0.000006636366493941812",
            "extra": "mean: 133.15169999827958 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_singletons",
            "value": 171.591005357279,
            "unit": "iter/sec",
            "range": "stddev: 0.00012893308173216628",
            "extra": "mean: 5.82781130000285 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_copy",
            "value": 11.108059566698621,
            "unit": "iter/sec",
            "range": "stddev: 0.06481413291291695",
            "extra": "mean: 90.02472429999813 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_dual",
            "value": 11.182822963849473,
            "unit": "iter/sec",
            "range": "stddev: 0.07143943902737891",
            "extra": "mean: 89.42285890000079 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_erdos_renyi",
            "value": 51.520063937632436,
            "unit": "iter/sec",
            "range": "stddev: 0.0016120100594188935",
            "extra": "mean: 19.409913800001277 msec\nrounds: 10"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "maximelucas@users.noreply.github.com",
            "name": "Maxime Lucas",
            "username": "maximelucas"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "b4f9f38a46dd308f42f45b4f5026e1f40add2459",
          "message": "feat: added seed to shuffle-hypedges (#645)",
          "timestamp": "2025-01-14T14:29:01+01:00",
          "tree_id": "7ad575797eef563d3162527a11bdd156d49c6d61",
          "url": "https://github.com/xgi-org/xgi/commit/b4f9f38a46dd308f42f45b4f5026e1f40add2459"
        },
        "date": 1736861505938,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/algorithms.py::test_connected",
            "value": 87.43346903187309,
            "unit": "iter/sec",
            "range": "stddev: 0.0005430309823494733",
            "extra": "mean: 11.437267799993833 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/algorithms.py::test_clustering_coefficient",
            "value": 60.177747132070564,
            "unit": "iter/sec",
            "range": "stddev: 0.00038996888942768827",
            "extra": "mean: 16.617438299996934 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgelist",
            "value": 27.258243679288544,
            "unit": "iter/sec",
            "range": "stddev: 0.04489417346735151",
            "extra": "mean: 36.686149400000545 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgedict",
            "value": 25.655617767011137,
            "unit": "iter/sec",
            "range": "stddev: 0.044803460785936895",
            "extra": "mean: 38.97781799999507 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_df",
            "value": 20.701025017671565,
            "unit": "iter/sec",
            "range": "stddev: 0.04018466742696344",
            "extra": "mean: 48.30678669999884 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_memberships",
            "value": 1095.1655014106022,
            "unit": "iter/sec",
            "range": "stddev: 0.00006397278346867732",
            "extra": "mean: 913.1039999999757 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_members",
            "value": 129.8607411071254,
            "unit": "iter/sec",
            "range": "stddev: 0.0006210069503102892",
            "extra": "mean: 7.700556700004313 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_attributes",
            "value": 12341.199614983689,
            "unit": "iter/sec",
            "range": "stddev: 0.000009931760598095821",
            "extra": "mean: 81.02939999332648 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_attributes",
            "value": 242.5689311162117,
            "unit": "iter/sec",
            "range": "stddev: 0.0004003738386893474",
            "extra": "mean: 4.122539500002631 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_degree",
            "value": 8908.582795821816,
            "unit": "iter/sec",
            "range": "stddev: 0.000009890610561272304",
            "extra": "mean: 112.25130000127592 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_nodestats_degree",
            "value": 7971.519355969202,
            "unit": "iter/sec",
            "range": "stddev: 0.000004208316343049581",
            "extra": "mean: 125.44659999491614 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_size",
            "value": 216.05418258667166,
            "unit": "iter/sec",
            "range": "stddev: 0.00012367504715968475",
            "extra": "mean: 4.628468599995017 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_isolates",
            "value": 7307.105209756569,
            "unit": "iter/sec",
            "range": "stddev: 0.000008514653951073259",
            "extra": "mean: 136.85310000255413 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_singletons",
            "value": 167.64721848279493,
            "unit": "iter/sec",
            "range": "stddev: 0.00013378294849417867",
            "extra": "mean: 5.964906600001996 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_copy",
            "value": 10.831511656306624,
            "unit": "iter/sec",
            "range": "stddev: 0.06789073174770376",
            "extra": "mean: 92.3232168999931 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_dual",
            "value": 11.0644758330328,
            "unit": "iter/sec",
            "range": "stddev: 0.07253058411924952",
            "extra": "mean: 90.379337899995 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_erdos_renyi",
            "value": 51.70787678444528,
            "unit": "iter/sec",
            "range": "stddev: 0.0012551501937860163",
            "extra": "mean: 19.33941330000266 msec\nrounds: 10"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "martingonzalezcoll@gmail.com",
            "name": "Martin Coll",
            "username": "colltoaction"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "55ecf682270566cd56b4d217eb900977aec63b0b",
          "message": "Support DiHypergraph in from_bipartite_graph (#633)\n\n* Support DiHypergraph in from_bipartite_graph\n\n* PR feedback\n\n* Add the ability to check bipartiteness of directed and undirected\n\n* format with black .\n\n* PR feedback\n\n* fix additional PR comments\n\n* fixed small bugs\n\n---------\n\nCo-authored-by: Nicholas Landry <nicholas.landry.91@gmail.com>",
          "timestamp": "2025-01-18T11:45:24-05:00",
          "tree_id": "e48acd2a76ae294067f27766ff481079fc906fce",
          "url": "https://github.com/xgi-org/xgi/commit/55ecf682270566cd56b4d217eb900977aec63b0b"
        },
        "date": 1737218784487,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/algorithms.py::test_connected",
            "value": 99.92700232552156,
            "unit": "iter/sec",
            "range": "stddev: 0.0003964284205985289",
            "extra": "mean: 10.007305100000963 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/algorithms.py::test_clustering_coefficient",
            "value": 62.43707942343004,
            "unit": "iter/sec",
            "range": "stddev: 0.00032012536255182996",
            "extra": "mean: 16.016123900003265 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgelist",
            "value": 29.995380051576138,
            "unit": "iter/sec",
            "range": "stddev: 0.03856349008804685",
            "extra": "mean: 33.338467399997285 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgedict",
            "value": 28.686854145241934,
            "unit": "iter/sec",
            "range": "stddev: 0.03688860776581055",
            "extra": "mean: 34.85917259999951 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_df",
            "value": 23.226653322366722,
            "unit": "iter/sec",
            "range": "stddev: 0.03190241548103688",
            "extra": "mean: 43.05398569999852 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_memberships",
            "value": 1291.5062669672197,
            "unit": "iter/sec",
            "range": "stddev: 0.000035740248661505856",
            "extra": "mean: 774.2897000014182 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_members",
            "value": 138.72996793020505,
            "unit": "iter/sec",
            "range": "stddev: 0.0005214572038085597",
            "extra": "mean: 7.208247900000231 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_attributes",
            "value": 16247.5344362667,
            "unit": "iter/sec",
            "range": "stddev: 0.000005714766773528954",
            "extra": "mean: 61.547800001449104 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_attributes",
            "value": 268.7057708621267,
            "unit": "iter/sec",
            "range": "stddev: 0.00006992344555761489",
            "extra": "mean: 3.7215427000006684 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_degree",
            "value": 12119.126162995966,
            "unit": "iter/sec",
            "range": "stddev: 0.000004013549877634857",
            "extra": "mean: 82.5141999968082 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_nodestats_degree",
            "value": 10692.728410225756,
            "unit": "iter/sec",
            "range": "stddev: 0.0000061490283635995574",
            "extra": "mean: 93.52149999841686 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_size",
            "value": 283.3851673141584,
            "unit": "iter/sec",
            "range": "stddev: 0.00009121976603437357",
            "extra": "mean: 3.5287662000015985 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_isolates",
            "value": 9441.916633765919,
            "unit": "iter/sec",
            "range": "stddev: 0.0000074321533612596",
            "extra": "mean: 105.91069999748015 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_singletons",
            "value": 207.2422976224093,
            "unit": "iter/sec",
            "range": "stddev: 0.0001648381680068364",
            "extra": "mean: 4.825269799999887 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_copy",
            "value": 12.564608252213251,
            "unit": "iter/sec",
            "range": "stddev: 0.0570996551084096",
            "extra": "mean: 79.5886333999988 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_dual",
            "value": 12.764502624843887,
            "unit": "iter/sec",
            "range": "stddev: 0.058830062459537896",
            "extra": "mean: 78.34226129999564 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_erdos_renyi",
            "value": 52.366283637320386,
            "unit": "iter/sec",
            "range": "stddev: 0.0014221813245608049",
            "extra": "mean: 19.096256800001754 msec\nrounds: 10"
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
          "id": "b86da86cfa7608d14b2043f00411c5235bc4d47e",
          "message": "Update changelog and up-version",
          "timestamp": "2025-01-19T12:14:32-05:00",
          "tree_id": "da24b6994f47c62edee5895de6771e80b15f7efb",
          "url": "https://github.com/xgi-org/xgi/commit/b86da86cfa7608d14b2043f00411c5235bc4d47e"
        },
        "date": 1737307014817,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/algorithms.py::test_connected",
            "value": 94.79057718730732,
            "unit": "iter/sec",
            "range": "stddev: 0.0003842906861217604",
            "extra": "mean: 10.549571799990076 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/algorithms.py::test_clustering_coefficient",
            "value": 61.40996279745164,
            "unit": "iter/sec",
            "range": "stddev: 0.00030323981960319414",
            "extra": "mean: 16.284002699990197 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgelist",
            "value": 28.133167357398282,
            "unit": "iter/sec",
            "range": "stddev: 0.04249706760433676",
            "extra": "mean: 35.5452334000006 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgedict",
            "value": 27.6669231796213,
            "unit": "iter/sec",
            "range": "stddev: 0.03899483009370033",
            "extra": "mean: 36.144243200001824 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_df",
            "value": 21.22451732714673,
            "unit": "iter/sec",
            "range": "stddev: 0.03330619614665878",
            "extra": "mean: 47.11532350000596 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_memberships",
            "value": 1226.1898455846388,
            "unit": "iter/sec",
            "range": "stddev: 0.000024385270260990238",
            "extra": "mean: 815.5343999959541 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_members",
            "value": 132.5479461045234,
            "unit": "iter/sec",
            "range": "stddev: 0.0006286672880682078",
            "extra": "mean: 7.544439800005875 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_attributes",
            "value": 12915.174425441202,
            "unit": "iter/sec",
            "range": "stddev: 0.000006436896528134353",
            "extra": "mean: 77.42830000267986 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_attributes",
            "value": 254.31512365023835,
            "unit": "iter/sec",
            "range": "stddev: 0.00007764160114330672",
            "extra": "mean: 3.9321294999950847 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_degree",
            "value": 10043.478217219312,
            "unit": "iter/sec",
            "range": "stddev: 0.00001584871886208454",
            "extra": "mean: 99.56709999983104 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_nodestats_degree",
            "value": 8534.658822928379,
            "unit": "iter/sec",
            "range": "stddev: 0.000005261640833470191",
            "extra": "mean: 117.16929999749937 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_size",
            "value": 247.8675643598994,
            "unit": "iter/sec",
            "range": "stddev: 0.00019008444865957746",
            "extra": "mean: 4.034412500007534 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_isolates",
            "value": 8445.353914830675,
            "unit": "iter/sec",
            "range": "stddev: 0.000006224334497293726",
            "extra": "mean: 118.4083000055125 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_singletons",
            "value": 179.46090088942495,
            "unit": "iter/sec",
            "range": "stddev: 0.00021702328182346617",
            "extra": "mean: 5.572244399999704 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_copy",
            "value": 11.68479704704048,
            "unit": "iter/sec",
            "range": "stddev: 0.06113461819907601",
            "extra": "mean: 85.58128960000033 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_dual",
            "value": 11.76711257527932,
            "unit": "iter/sec",
            "range": "stddev: 0.06604750699179084",
            "extra": "mean: 84.9826151999963 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_erdos_renyi",
            "value": 51.61667503940121,
            "unit": "iter/sec",
            "range": "stddev: 0.00120275273547175",
            "extra": "mean: 19.37358420000237 msec\nrounds: 10"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "maximelucas@users.noreply.github.com",
            "name": "Maxime Lucas",
            "username": "maximelucas"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "29880f91b3f39a6a2a2c8cb29fbc2ff1a8b46d46",
          "message": "Fix sparse diag by upgrading SciPy and Numpy (#650)\n\n* updated scipy requirement\r\n\r\n* added test\r\n\r\n* dropped python 3.9 support",
          "timestamp": "2025-01-27T17:17:19+01:00",
          "tree_id": "4d127233b075f87568038e05ec8312179526c693",
          "url": "https://github.com/xgi-org/xgi/commit/29880f91b3f39a6a2a2c8cb29fbc2ff1a8b46d46"
        },
        "date": 1737994707087,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/algorithms.py::test_connected",
            "value": 92.06770098958863,
            "unit": "iter/sec",
            "range": "stddev: 0.0005943070485416864",
            "extra": "mean: 10.861572400000341 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/algorithms.py::test_clustering_coefficient",
            "value": 60.20498267391519,
            "unit": "iter/sec",
            "range": "stddev: 0.00038396953434016094",
            "extra": "mean: 16.609920900006614 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgelist",
            "value": 26.668727199203165,
            "unit": "iter/sec",
            "range": "stddev: 0.04775593551950689",
            "extra": "mean: 37.49710260000256 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgedict",
            "value": 26.885128987470306,
            "unit": "iter/sec",
            "range": "stddev: 0.041546366137309075",
            "extra": "mean: 37.19528369999807 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_df",
            "value": 21.300915952167436,
            "unit": "iter/sec",
            "range": "stddev: 0.03735603435401352",
            "extra": "mean: 46.94633799999792 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_memberships",
            "value": 1035.4344299752079,
            "unit": "iter/sec",
            "range": "stddev: 0.00004295150514721064",
            "extra": "mean: 965.7782000005 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_members",
            "value": 130.51523276569787,
            "unit": "iter/sec",
            "range": "stddev: 0.0009102402112278705",
            "extra": "mean: 7.6619408999960115 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_attributes",
            "value": 13238.9659837066,
            "unit": "iter/sec",
            "range": "stddev: 0.0000054995380499974566",
            "extra": "mean: 75.53460000053747 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_attributes",
            "value": 245.52363156362307,
            "unit": "iter/sec",
            "range": "stddev: 0.0005833405758373741",
            "extra": "mean: 4.0729276999996955 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_degree",
            "value": 8869.439193978582,
            "unit": "iter/sec",
            "range": "stddev: 0.000010249821222155763",
            "extra": "mean: 112.74670000318565 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_nodestats_degree",
            "value": 9431.648841079172,
            "unit": "iter/sec",
            "range": "stddev: 0.000012728187406376893",
            "extra": "mean: 106.02599999742779 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_size",
            "value": 246.34715211050926,
            "unit": "iter/sec",
            "range": "stddev: 0.00031646470694440105",
            "extra": "mean: 4.059312200010368 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_isolates",
            "value": 7169.990435092223,
            "unit": "iter/sec",
            "range": "stddev: 0.000011486048408596054",
            "extra": "mean: 139.4702000027337 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_singletons",
            "value": 170.57776171914378,
            "unit": "iter/sec",
            "range": "stddev: 0.00009902852203399978",
            "extra": "mean: 5.8624289000022145 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_copy",
            "value": 11.224147417045613,
            "unit": "iter/sec",
            "range": "stddev: 0.06604103130212538",
            "extra": "mean: 89.09362669999723 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_dual",
            "value": 11.056801062547997,
            "unit": "iter/sec",
            "range": "stddev: 0.0750730838238104",
            "extra": "mean: 90.44207219999976 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_erdos_renyi",
            "value": 50.22918799933586,
            "unit": "iter/sec",
            "range": "stddev: 0.001467657429192255",
            "extra": "mean: 19.90874309999242 msec\nrounds: 10"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "maxime.lucas.work@gmail.com",
            "name": "Maxime Lucas",
            "username": "maximelucas"
          },
          "committer": {
            "email": "maxime.lucas.work@gmail.com",
            "name": "Maxime Lucas",
            "username": "maximelucas"
          },
          "distinct": true,
          "id": "d02990af09d2e4acdd446fcdfafca169cdbaa3c6",
          "message": "updated python version in readme",
          "timestamp": "2025-01-27T17:49:57+01:00",
          "tree_id": "09c84e604de6dc1a9f21276f8cf090e62296183a",
          "url": "https://github.com/xgi-org/xgi/commit/d02990af09d2e4acdd446fcdfafca169cdbaa3c6"
        },
        "date": 1737996673955,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/algorithms.py::test_connected",
            "value": 92.2035712121405,
            "unit": "iter/sec",
            "range": "stddev: 0.00020501200324371389",
            "extra": "mean: 10.845566899998005 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/algorithms.py::test_clustering_coefficient",
            "value": 61.006557936556156,
            "unit": "iter/sec",
            "range": "stddev: 0.00026990283123685575",
            "extra": "mean: 16.391680399998165 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgelist",
            "value": 27.005291781443166,
            "unit": "iter/sec",
            "range": "stddev: 0.04657447969915951",
            "extra": "mean: 37.029779499999904 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgedict",
            "value": 26.989947434838072,
            "unit": "iter/sec",
            "range": "stddev: 0.042147180934977706",
            "extra": "mean: 37.05083169999881 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_df",
            "value": 21.864944462363333,
            "unit": "iter/sec",
            "range": "stddev: 0.03668304502540582",
            "extra": "mean: 45.735309399999835 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_memberships",
            "value": 1141.9272877833341,
            "unit": "iter/sec",
            "range": "stddev: 0.000018619032405055573",
            "extra": "mean: 875.7124999974053 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_members",
            "value": 135.3616097419339,
            "unit": "iter/sec",
            "range": "stddev: 0.0006315758243731164",
            "extra": "mean: 7.38761899999929 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_attributes",
            "value": 14186.771686448415,
            "unit": "iter/sec",
            "range": "stddev: 0.0000036662282099331354",
            "extra": "mean: 70.48820000079559 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_attributes",
            "value": 262.18484398565704,
            "unit": "iter/sec",
            "range": "stddev: 0.00025166067353000305",
            "extra": "mean: 3.814102999999136 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_degree",
            "value": 9259.928031818776,
            "unit": "iter/sec",
            "range": "stddev: 0.000018470410568862878",
            "extra": "mean: 107.99220000023979 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_nodestats_degree",
            "value": 8494.213741653242,
            "unit": "iter/sec",
            "range": "stddev: 0.000009785583442911677",
            "extra": "mean: 117.7271999992513 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_size",
            "value": 229.86697988634438,
            "unit": "iter/sec",
            "range": "stddev: 0.0001387946387291166",
            "extra": "mean: 4.3503421000025355 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_isolates",
            "value": 7859.225551757687,
            "unit": "iter/sec",
            "range": "stddev: 0.000009892334397171624",
            "extra": "mean: 127.23900000253252 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_singletons",
            "value": 177.25497486462973,
            "unit": "iter/sec",
            "range": "stddev: 0.00012112592972697973",
            "extra": "mean: 5.641590600002644 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_copy",
            "value": 10.804953626505858,
            "unit": "iter/sec",
            "range": "stddev: 0.06862272715151106",
            "extra": "mean: 92.55014270000004 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_dual",
            "value": 11.292999613525328,
            "unit": "iter/sec",
            "range": "stddev: 0.07206229819806134",
            "extra": "mean: 88.55043249999994 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_erdos_renyi",
            "value": 51.823935909872866,
            "unit": "iter/sec",
            "range": "stddev: 0.0014035518693882422",
            "extra": "mean: 19.2961029000017 msec\nrounds: 10"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "maxime.lucas.work@gmail.com",
            "name": "Maxime Lucas",
            "username": "maximelucas"
          },
          "committer": {
            "email": "maxime.lucas.work@gmail.com",
            "name": "Maxime Lucas",
            "username": "maximelucas"
          },
          "distinct": true,
          "id": "e564995ffde1bbfdac5c09b4ef6e8431acad52f2",
          "message": "updated python version in readme",
          "timestamp": "2025-01-27T17:51:07+01:00",
          "tree_id": "3b7351345785aebeded3799716393c5dfc6d147c",
          "url": "https://github.com/xgi-org/xgi/commit/e564995ffde1bbfdac5c09b4ef6e8431acad52f2"
        },
        "date": 1737996807271,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/algorithms.py::test_connected",
            "value": 95.2589133931459,
            "unit": "iter/sec",
            "range": "stddev: 0.00023986525497569564",
            "extra": "mean: 10.497705300005578 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/algorithms.py::test_clustering_coefficient",
            "value": 60.248759899750674,
            "unit": "iter/sec",
            "range": "stddev: 0.0003473388512569516",
            "extra": "mean: 16.597852000006696 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgelist",
            "value": 28.728275268866927,
            "unit": "iter/sec",
            "range": "stddev: 0.04092160352723755",
            "extra": "mean: 34.80891179999617 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgedict",
            "value": 25.551725439923004,
            "unit": "iter/sec",
            "range": "stddev: 0.04748700665186702",
            "extra": "mean: 39.136300300000926 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_df",
            "value": 21.98410872545271,
            "unit": "iter/sec",
            "range": "stddev: 0.03658719311688382",
            "extra": "mean: 45.487402399999155 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_memberships",
            "value": 1143.1722664571719,
            "unit": "iter/sec",
            "range": "stddev: 0.00004245694745826006",
            "extra": "mean: 874.7588000005635 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_members",
            "value": 131.50647518807665,
            "unit": "iter/sec",
            "range": "stddev: 0.0005843716100897215",
            "extra": "mean: 7.604188300004466 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_attributes",
            "value": 14450.324120263229,
            "unit": "iter/sec",
            "range": "stddev: 0.000006941549605490569",
            "extra": "mean: 69.20260000242706 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_attributes",
            "value": 259.6963407043142,
            "unit": "iter/sec",
            "range": "stddev: 0.00007221375628019268",
            "extra": "mean: 3.850651100003688 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_degree",
            "value": 10206.247855995427,
            "unit": "iter/sec",
            "range": "stddev: 0.00001380495613448345",
            "extra": "mean: 97.97920000664817 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_nodestats_degree",
            "value": 9879.421659259788,
            "unit": "iter/sec",
            "range": "stddev: 0.000009564787979730973",
            "extra": "mean: 101.22049999381488 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_size",
            "value": 259.09450873818275,
            "unit": "iter/sec",
            "range": "stddev: 0.00030411650510374057",
            "extra": "mean: 3.859595499997681 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_isolates",
            "value": 8769.191375484907,
            "unit": "iter/sec",
            "range": "stddev: 0.000006144139598266334",
            "extra": "mean: 114.03559999791923 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_singletons",
            "value": 192.89287364406206,
            "unit": "iter/sec",
            "range": "stddev: 0.00019533910649844152",
            "extra": "mean: 5.18422470000246 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_copy",
            "value": 12.120815293065592,
            "unit": "iter/sec",
            "range": "stddev: 0.05911678992829488",
            "extra": "mean: 82.50270099999852 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_dual",
            "value": 11.973730564303418,
            "unit": "iter/sec",
            "range": "stddev: 0.0643350925216188",
            "extra": "mean: 83.51616019999994 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_erdos_renyi",
            "value": 52.71643993019012,
            "unit": "iter/sec",
            "range": "stddev: 0.0007172809765750839",
            "extra": "mean: 18.969414499997583 msec\nrounds: 10"
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
          "id": "d14e3e5ff7d49769812f28abfd6371e59ea1d631",
          "message": "Fix/normalized hypergraph laplacian (#648)\n\n* fix: rewrite `normalized_hypergraph_laplacian`\r\n\r\nFixes the implementation of `normalized_hypergraph_laplacian` to prevent\r\nnegative eigenvalues. Rewrites core matrix calculations in full\r\ndefinition.\r\n\r\n* test: add unit tests for updated laplacian\r\n\r\nAdds a proprty test for eigenvalue sign.\r\nAdds error tests for new `weights` variable.\r\n\r\n* doc: update `normalized_hypergraph_laplacian` doc\r\n\r\nUpdated 'Raises' portion of function docstring to include type and\r\nlength error catches on `weights` parameter.\r\n\r\n* test: added issue #657 m.w.e. as test\r\n\r\n* fix(test): fix typo in unit test\r\n\r\n* Update xgi/linalg/laplacian_matrix.py\r\n\r\nImplement suggestion - Edge weight matrix\r\n\r\nCo-authored-by: Maxime Lucas <maximelucas@users.noreply.github.com>\r\n\r\n* test: add sqrt(d) eigenvector, true_L tests\r\n\r\n* feat: update weighted argument for laplacian\r\n\r\n* doc: update normalized_hypergraph_laplacian args\r\n\r\n* Update xgi/linalg/laplacian_matrix.py\r\n\r\nFix docstring typo\r\n\r\nCo-authored-by: Maxime Lucas <maximelucas@users.noreply.github.com>\r\n\r\n* Update xgi/linalg/laplacian_matrix.py\r\n\r\nCo-authored-by: Maxime Lucas <maximelucas@users.noreply.github.com>\r\n\r\n* Update xgi/linalg/laplacian_matrix.py\r\n\r\nCo-authored-by: Maxime Lucas <maximelucas@users.noreply.github.com>\r\n\r\n* Update xgi/linalg/laplacian_matrix.py\r\n\r\nCo-authored-by: Maxime Lucas <maximelucas@users.noreply.github.com>\r\n\r\n* Update xgi/linalg/laplacian_matrix.py\r\n\r\nCo-authored-by: Maxime Lucas <maximelucas@users.noreply.github.com>\r\n\r\n* Update xgi/linalg/laplacian_matrix.py\r\n\r\nCo-authored-by: Maxime Lucas <maximelucas@users.noreply.github.com>\r\n\r\n* Update xgi/linalg/laplacian_matrix.py\r\n\r\nCo-authored-by: Maxime Lucas <maximelucas@users.noreply.github.com>\r\n\r\n* Update xgi/linalg/laplacian_matrix.py\r\n\r\nCo-authored-by: Maxime Lucas <maximelucas@users.noreply.github.com>\r\n\r\n* Update xgi/linalg/laplacian_matrix.py\r\n\r\nCo-authored-by: Maxime Lucas <maximelucas@users.noreply.github.com>\r\n\r\n* Update xgi/linalg/laplacian_matrix.py\r\n\r\nImplement suggestion - Edge weight matrix\r\n\r\nCo-authored-by: Maxime Lucas <maximelucas@users.noreply.github.com>\r\n\r\n* feat: update weighted argument for laplacian\r\n\r\n* doc: update normalized_hypergraph_laplacian args\r\n\r\n* Update xgi/linalg/laplacian_matrix.py\r\n\r\nFix docstring typo\r\n\r\nCo-authored-by: Maxime Lucas <maximelucas@users.noreply.github.com>\r\n\r\nUpdate xgi/linalg/laplacian_matrix.py\r\n\r\nCo-authored-by: Maxime Lucas <maximelucas@users.noreply.github.com>\r\n\r\nUpdate xgi/linalg/laplacian_matrix.py\r\n\r\nCo-authored-by: Maxime Lucas <maximelucas@users.noreply.github.com>\r\n\r\nUpdate xgi/linalg/laplacian_matrix.py\r\n\r\nCo-authored-by: Maxime Lucas <maximelucas@users.noreply.github.com>\r\n\r\nUpdate xgi/linalg/laplacian_matrix.py\r\n\r\nCo-authored-by: Maxime Lucas <maximelucas@users.noreply.github.com>\r\n\r\nUpdate xgi/linalg/laplacian_matrix.py\r\n\r\nCo-authored-by: Maxime Lucas <maximelucas@users.noreply.github.com>\r\n\r\nUpdate xgi/linalg/laplacian_matrix.py\r\n\r\nCo-authored-by: Maxime Lucas <maximelucas@users.noreply.github.com>\r\n\r\nUpdate xgi/linalg/laplacian_matrix.py\r\n\r\nCo-authored-by: Maxime Lucas <maximelucas@users.noreply.github.com>\r\n\r\nUpdate xgi/linalg/laplacian_matrix.py\r\n\r\nCo-authored-by: Maxime Lucas <maximelucas@users.noreply.github.com>\r\n\r\n* test: separated #647 m.w.e. into new test\r\n\r\nAdd the minimum(?) working example of issue #647 as new `test_`\r\nfunction.\r\nTidied `test_normalized_hypergraph_laplacian` and added L2 and L3\r\ncomparison.\r\n\r\n* feat: update scipy sparse array to modern use\r\n\r\n* chore: update diags_array scipy use in 'laplacian'\r\n\r\n* Update xgi/linalg/laplacian_matrix.py\r\n\r\nCo-authored-by: Maxime Lucas <maximelucas@users.noreply.github.com>\r\n\r\n---------\r\n\r\nCo-authored-by: Maxime Lucas <maximelucas@users.noreply.github.com>",
          "timestamp": "2025-01-30T11:16:39-05:00",
          "tree_id": "0ef687a480689d93dc8eaf152b5df80717829ac3",
          "url": "https://github.com/xgi-org/xgi/commit/d14e3e5ff7d49769812f28abfd6371e59ea1d631"
        },
        "date": 1738253858247,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/algorithms.py::test_connected",
            "value": 90.93204794460615,
            "unit": "iter/sec",
            "range": "stddev: 0.0002849675714012341",
            "extra": "mean: 10.997222899996473 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/algorithms.py::test_clustering_coefficient",
            "value": 59.05819157756282,
            "unit": "iter/sec",
            "range": "stddev: 0.0003433937502239907",
            "extra": "mean: 16.93245210000498 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgelist",
            "value": 27.421187325898817,
            "unit": "iter/sec",
            "range": "stddev: 0.045660267657570225",
            "extra": "mean: 36.46815099999401 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgedict",
            "value": 27.611626960114396,
            "unit": "iter/sec",
            "range": "stddev: 0.04133231028174423",
            "extra": "mean: 36.21662720000245 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_df",
            "value": 20.238855204698098,
            "unit": "iter/sec",
            "range": "stddev: 0.04268805485303625",
            "extra": "mean: 49.40990930000169 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_memberships",
            "value": 956.1782549496878,
            "unit": "iter/sec",
            "range": "stddev: 0.00022589851773273067",
            "extra": "mean: 1.0458301000085157 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_members",
            "value": 125.32343943209284,
            "unit": "iter/sec",
            "range": "stddev: 0.0006455674148642409",
            "extra": "mean: 7.979353300001435 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_attributes",
            "value": 13344.720828686834,
            "unit": "iter/sec",
            "range": "stddev: 0.0000065849632910491825",
            "extra": "mean: 74.93599999861544 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_attributes",
            "value": 250.95215639826526,
            "unit": "iter/sec",
            "range": "stddev: 0.00017145416095638635",
            "extra": "mean: 3.9848232999958095 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_degree",
            "value": 8182.1878676937895,
            "unit": "iter/sec",
            "range": "stddev: 0.000011820583801474767",
            "extra": "mean: 122.21670000371886 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_nodestats_degree",
            "value": 7902.258544675305,
            "unit": "iter/sec",
            "range": "stddev: 0.000009122046586848662",
            "extra": "mean: 126.54609999742661 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_size",
            "value": 210.95408181490745,
            "unit": "iter/sec",
            "range": "stddev: 0.00020854674210992648",
            "extra": "mean: 4.740368099999159 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_isolates",
            "value": 7124.785632673542,
            "unit": "iter/sec",
            "range": "stddev: 0.000011642477395433723",
            "extra": "mean: 140.35510000667273 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_singletons",
            "value": 181.94833773466436,
            "unit": "iter/sec",
            "range": "stddev: 0.00021706696625134746",
            "extra": "mean: 5.496065599996314 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_copy",
            "value": 11.595594262308628,
            "unit": "iter/sec",
            "range": "stddev: 0.06424001304661707",
            "extra": "mean: 86.23965080000175 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_dual",
            "value": 10.68520401965807,
            "unit": "iter/sec",
            "range": "stddev: 0.068207662894218",
            "extra": "mean: 93.58735669999874 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_erdos_renyi",
            "value": 42.95632619147527,
            "unit": "iter/sec",
            "range": "stddev: 0.0013472198482219256",
            "extra": "mean: 23.27945819999968 msec\nrounds: 10"
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
          "id": "1a728ee54dc67d2040a251779c54b915a3a1ef64",
          "message": "Fix `fast_random_hypergraph` (#655)\n\n* Fix `fast_random_hypergraph` fencepost errors\n\n* changed all samples to geometric to be consistent\n\n* Update random.py\n\n* fix errors\n\n* changed the sampler to custom code\n\n* Document p\n\n* Update test_random.py\n\n* update docs\n\n* fix failing tests\n\n* format with black\n\n* Fix error\n\n* switched from floor to ceil a la Numpy\n\n* add missing tests",
          "timestamp": "2025-02-07T07:03:28-05:00",
          "tree_id": "a194320a54eaa226d8cc245d10af2554da3bff93",
          "url": "https://github.com/xgi-org/xgi/commit/1a728ee54dc67d2040a251779c54b915a3a1ef64"
        },
        "date": 1738929863224,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/algorithms.py::test_connected",
            "value": 98.12419316152253,
            "unit": "iter/sec",
            "range": "stddev: 0.00016476444494413072",
            "extra": "mean: 10.191166600003498 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/algorithms.py::test_clustering_coefficient",
            "value": 61.60786080325902,
            "unit": "iter/sec",
            "range": "stddev: 0.00029319900178408184",
            "extra": "mean: 16.23169489999725 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgelist",
            "value": 27.814300890795735,
            "unit": "iter/sec",
            "range": "stddev: 0.04439282732100158",
            "extra": "mean: 35.9527282000073 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgedict",
            "value": 27.813975426224346,
            "unit": "iter/sec",
            "range": "stddev: 0.03997315913576679",
            "extra": "mean: 35.95314890000054 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_df",
            "value": 22.415451282592215,
            "unit": "iter/sec",
            "range": "stddev: 0.034668479510748716",
            "extra": "mean: 44.61208419999991 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_memberships",
            "value": 1202.916205695879,
            "unit": "iter/sec",
            "range": "stddev: 0.00003480888810718311",
            "extra": "mean: 831.3131000022622 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_members",
            "value": 134.1086116410887,
            "unit": "iter/sec",
            "range": "stddev: 0.0006659212022956137",
            "extra": "mean: 7.456642699995086 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_attributes",
            "value": 15123.8110797165,
            "unit": "iter/sec",
            "range": "stddev: 0.000003041212133697023",
            "extra": "mean: 66.12089999862292 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_attributes",
            "value": 266.317769083177,
            "unit": "iter/sec",
            "range": "stddev: 0.00008966351372975585",
            "extra": "mean: 3.7549128000080145 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_degree",
            "value": 10597.553660786734,
            "unit": "iter/sec",
            "range": "stddev: 0.000015216202495407696",
            "extra": "mean: 94.36139999934312 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_nodestats_degree",
            "value": 8876.690343576265,
            "unit": "iter/sec",
            "range": "stddev: 0.000011634081263190612",
            "extra": "mean: 112.65460000231542 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_size",
            "value": 246.82181128779936,
            "unit": "iter/sec",
            "range": "stddev: 0.0003403339463914888",
            "extra": "mean: 4.051505800003952 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_isolates",
            "value": 8338.586642977509,
            "unit": "iter/sec",
            "range": "stddev: 0.000006157936139051242",
            "extra": "mean: 119.9243999991495 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_singletons",
            "value": 187.22009425771208,
            "unit": "iter/sec",
            "range": "stddev: 0.00027000745024063346",
            "extra": "mean: 5.341307000003326 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_copy",
            "value": 11.683657409307164,
            "unit": "iter/sec",
            "range": "stddev: 0.06187567295769493",
            "extra": "mean: 85.58963729999505 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_dual",
            "value": 11.673882349770967,
            "unit": "iter/sec",
            "range": "stddev: 0.07028019830047433",
            "extra": "mean: 85.66130529999896 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_erdos_renyi",
            "value": 52.90056607521,
            "unit": "iter/sec",
            "range": "stddev: 0.001174766981903563",
            "extra": "mean: 18.90338939999765 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_fast_erdos_renyi",
            "value": 34.25350064953312,
            "unit": "iter/sec",
            "range": "stddev: 0.001078013146487571",
            "extra": "mean: 29.194096400001968 msec\nrounds: 10"
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
          "id": "32cf609bb237d429695f9d802a26e8da5264e62e",
          "message": "update changelog and up-version",
          "timestamp": "2025-02-07T10:53:13-05:00",
          "tree_id": "f887d25f4839381f9decb23247e88de402de0d00",
          "url": "https://github.com/xgi-org/xgi/commit/32cf609bb237d429695f9d802a26e8da5264e62e"
        },
        "date": 1738943658082,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/algorithms.py::test_connected",
            "value": 91.26736676527722,
            "unit": "iter/sec",
            "range": "stddev: 0.0004351762129461531",
            "extra": "mean: 10.956818799996881 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/algorithms.py::test_clustering_coefficient",
            "value": 59.73823458305826,
            "unit": "iter/sec",
            "range": "stddev: 0.0004378609760600209",
            "extra": "mean: 16.739697900004558 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgelist",
            "value": 26.276789117533916,
            "unit": "iter/sec",
            "range": "stddev: 0.04891893916840574",
            "extra": "mean: 38.056400099992516 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgedict",
            "value": 25.713634417312107,
            "unit": "iter/sec",
            "range": "stddev: 0.04607716193796295",
            "extra": "mean: 38.88987390000125 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_df",
            "value": 20.70687197966383,
            "unit": "iter/sec",
            "range": "stddev: 0.04240776495687119",
            "extra": "mean: 48.293146400001774 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_memberships",
            "value": 1056.6743036039672,
            "unit": "iter/sec",
            "range": "stddev: 0.00006253754680191198",
            "extra": "mean: 946.3654000001043 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_members",
            "value": 130.3004105936614,
            "unit": "iter/sec",
            "range": "stddev: 0.0007454006387149884",
            "extra": "mean: 7.674572899992427 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_attributes",
            "value": 12123.269402955979,
            "unit": "iter/sec",
            "range": "stddev: 0.000007848584311707982",
            "extra": "mean: 82.4860000022909 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_attributes",
            "value": 256.23851090536607,
            "unit": "iter/sec",
            "range": "stddev: 0.00017289259476679415",
            "extra": "mean: 3.9026140000061105 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_degree",
            "value": 8376.6896837266,
            "unit": "iter/sec",
            "range": "stddev: 0.000015902599665788655",
            "extra": "mean: 119.37889998989704 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_nodestats_degree",
            "value": 7520.318019377923,
            "unit": "iter/sec",
            "range": "stddev: 0.000005874848446090599",
            "extra": "mean: 132.97309999700246 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_size",
            "value": 217.86177210876545,
            "unit": "iter/sec",
            "range": "stddev: 0.00008780345977960786",
            "extra": "mean: 4.590066399995862 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_isolates",
            "value": 7063.788125823934,
            "unit": "iter/sec",
            "range": "stddev: 0.000009964128935653922",
            "extra": "mean: 141.56710000179373 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_singletons",
            "value": 170.9915268567925,
            "unit": "iter/sec",
            "range": "stddev: 0.00021440012066809973",
            "extra": "mean: 5.84824300000264 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_copy",
            "value": 10.442018615243098,
            "unit": "iter/sec",
            "range": "stddev: 0.07468760340057415",
            "extra": "mean: 95.7669237000033 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_dual",
            "value": 10.58083015324854,
            "unit": "iter/sec",
            "range": "stddev: 0.0800913985461834",
            "extra": "mean: 94.51054269999588 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_erdos_renyi",
            "value": 51.90405833782798,
            "unit": "iter/sec",
            "range": "stddev: 0.001683382275084498",
            "extra": "mean: 19.266316200003075 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_fast_erdos_renyi",
            "value": 33.40396177934787,
            "unit": "iter/sec",
            "range": "stddev: 0.0015275296395004015",
            "extra": "mean: 29.936568799999463 msec\nrounds: 10"
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
          "id": "27db0f6d65f974a9e6def13ef546e925a996c80e",
          "message": "Update README.md",
          "timestamp": "2025-02-08T13:56:22-05:00",
          "tree_id": "fe9baf1a69bff5a1f57bd9c1445ebabe747a1a79",
          "url": "https://github.com/xgi-org/xgi/commit/27db0f6d65f974a9e6def13ef546e925a996c80e"
        },
        "date": 1739041037405,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/algorithms.py::test_connected",
            "value": 97.98182715375219,
            "unit": "iter/sec",
            "range": "stddev: 0.00019312675109245798",
            "extra": "mean: 10.205974199999446 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/algorithms.py::test_clustering_coefficient",
            "value": 61.87824354148966,
            "unit": "iter/sec",
            "range": "stddev: 0.0004121669144743913",
            "extra": "mean: 16.16076900000394 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgelist",
            "value": 28.75708587895788,
            "unit": "iter/sec",
            "range": "stddev: 0.04178652621553713",
            "extra": "mean: 34.7740381000051 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgedict",
            "value": 28.54981285555575,
            "unit": "iter/sec",
            "range": "stddev: 0.03832925856302725",
            "extra": "mean: 35.02649929999109 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_df",
            "value": 22.801960653036243,
            "unit": "iter/sec",
            "range": "stddev: 0.03290423463422165",
            "extra": "mean: 43.85587780000151 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_memberships",
            "value": 1287.2279186405228,
            "unit": "iter/sec",
            "range": "stddev: 0.000021093366509929813",
            "extra": "mean: 776.8631999965692 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_members",
            "value": 137.16034657625656,
            "unit": "iter/sec",
            "range": "stddev: 0.0006020235620315553",
            "extra": "mean: 7.290736899997796 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_attributes",
            "value": 16104.95275833422,
            "unit": "iter/sec",
            "range": "stddev: 0.0000027785417799817504",
            "extra": "mean: 62.09269999146727 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_attributes",
            "value": 270.16569424144666,
            "unit": "iter/sec",
            "range": "stddev: 0.00004261540612412252",
            "extra": "mean: 3.701432199997612 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_degree",
            "value": 11962.080205732052,
            "unit": "iter/sec",
            "range": "stddev: 0.000014922380467412431",
            "extra": "mean: 83.5975000001099 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_nodestats_degree",
            "value": 10871.857761492012,
            "unit": "iter/sec",
            "range": "stddev: 0.000003063921024923083",
            "extra": "mean: 91.98059999846464 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_size",
            "value": 282.1899349905957,
            "unit": "iter/sec",
            "range": "stddev: 0.00007347799999947429",
            "extra": "mean: 3.543712499998719 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_isolates",
            "value": 9442.950884816559,
            "unit": "iter/sec",
            "range": "stddev: 0.000004771034388416748",
            "extra": "mean: 105.89909999509928 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_singletons",
            "value": 202.9366186930531,
            "unit": "iter/sec",
            "range": "stddev: 0.00014512986848523658",
            "extra": "mean: 4.927646900003424 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_copy",
            "value": 11.757550458461543,
            "unit": "iter/sec",
            "range": "stddev: 0.05994463254044284",
            "extra": "mean: 85.05172940000705 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_dual",
            "value": 12.053701719401882,
            "unit": "iter/sec",
            "range": "stddev: 0.06592661769896406",
            "extra": "mean: 82.96206619999396 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_erdos_renyi",
            "value": 52.39847303304512,
            "unit": "iter/sec",
            "range": "stddev: 0.0010689698630362364",
            "extra": "mean: 19.08452559999887 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_fast_erdos_renyi",
            "value": 34.115551412748516,
            "unit": "iter/sec",
            "range": "stddev: 0.0018298102269305617",
            "extra": "mean: 29.312145299996928 msec\nrounds: 10"
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
          "id": "d2594135c238627b69e61d5592c41dab0cd966c0",
          "message": "Update README.md",
          "timestamp": "2025-02-08T14:02:05-05:00",
          "tree_id": "cc8e5134a3d5279631f04cd4861e529a8fbd0ecf",
          "url": "https://github.com/xgi-org/xgi/commit/d2594135c238627b69e61d5592c41dab0cd966c0"
        },
        "date": 1739041378947,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/algorithms.py::test_connected",
            "value": 93.50094649603538,
            "unit": "iter/sec",
            "range": "stddev: 0.0003185931258548558",
            "extra": "mean: 10.695078900002386 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/algorithms.py::test_clustering_coefficient",
            "value": 61.58130696964586,
            "unit": "iter/sec",
            "range": "stddev: 0.000494254152572845",
            "extra": "mean: 16.238693999997622 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgelist",
            "value": 27.808174275115377,
            "unit": "iter/sec",
            "range": "stddev: 0.04551305454942865",
            "extra": "mean: 35.96064920000401 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgedict",
            "value": 27.392491653940453,
            "unit": "iter/sec",
            "range": "stddev: 0.040844975192554256",
            "extra": "mean: 36.50635409999836 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_df",
            "value": 21.69353891611671,
            "unit": "iter/sec",
            "range": "stddev: 0.03562595958941312",
            "extra": "mean: 46.0966744000018 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_memberships",
            "value": 1123.537056446183,
            "unit": "iter/sec",
            "range": "stddev: 0.000030956807098565294",
            "extra": "mean: 890.0462999974934 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_members",
            "value": 131.37321173305617,
            "unit": "iter/sec",
            "range": "stddev: 0.000567559862573969",
            "extra": "mean: 7.611901900000362 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_attributes",
            "value": 13060.832131285904,
            "unit": "iter/sec",
            "range": "stddev: 0.000007913938490814931",
            "extra": "mean: 76.5648000026431 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_attributes",
            "value": 252.07254042716016,
            "unit": "iter/sec",
            "range": "stddev: 0.0002959971429776606",
            "extra": "mean: 3.9671120000036812 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_degree",
            "value": 9183.166521296,
            "unit": "iter/sec",
            "range": "stddev: 0.000007806445519439204",
            "extra": "mean: 108.89489999783564 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_nodestats_degree",
            "value": 7996.033967104151,
            "unit": "iter/sec",
            "range": "stddev: 0.000007056038544021023",
            "extra": "mean: 125.06200000075296 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_size",
            "value": 228.92876675408218,
            "unit": "iter/sec",
            "range": "stddev: 0.00014365667018505416",
            "extra": "mean: 4.368170999995868 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_isolates",
            "value": 7837.32226864535,
            "unit": "iter/sec",
            "range": "stddev: 0.000006447524643882677",
            "extra": "mean: 127.59460000779654 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_singletons",
            "value": 168.7538707918949,
            "unit": "iter/sec",
            "range": "stddev: 0.00048664560212580935",
            "extra": "mean: 5.925790000000575 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_copy",
            "value": 11.246305321602188,
            "unit": "iter/sec",
            "range": "stddev: 0.06573592808727491",
            "extra": "mean: 88.91809099999932 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_dual",
            "value": 11.591956599121,
            "unit": "iter/sec",
            "range": "stddev: 0.06751318135038079",
            "extra": "mean: 86.26671359999989 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_erdos_renyi",
            "value": 53.629407707167715,
            "unit": "iter/sec",
            "range": "stddev: 0.0009449034554334675",
            "extra": "mean: 18.646486000000095 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_fast_erdos_renyi",
            "value": 33.99838411120446,
            "unit": "iter/sec",
            "range": "stddev: 0.0013249001842095371",
            "extra": "mean: 29.413162599996667 msec\nrounds: 10"
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
          "id": "be93e74bd8e32b0da44b9ed27821d9ed3373d528",
          "message": "Merge branch 'main' of https://github.com/xgi-org/xgi",
          "timestamp": "2025-02-09T09:51:43-05:00",
          "tree_id": "a48b8022088fa825209d13379847a0c66b5a7239",
          "url": "https://github.com/xgi-org/xgi/commit/be93e74bd8e32b0da44b9ed27821d9ed3373d528"
        },
        "date": 1739112759411,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/algorithms.py::test_connected",
            "value": 98.6204896869,
            "unit": "iter/sec",
            "range": "stddev: 0.00026456542140609706",
            "extra": "mean: 10.139880699992432 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/algorithms.py::test_clustering_coefficient",
            "value": 61.44142492198839,
            "unit": "iter/sec",
            "range": "stddev: 0.00036191159382476055",
            "extra": "mean: 16.275664200003348 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgelist",
            "value": 27.64499472138171,
            "unit": "iter/sec",
            "range": "stddev: 0.045531634140730595",
            "extra": "mean: 36.172913400000084 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgedict",
            "value": 28.335073338236345,
            "unit": "iter/sec",
            "range": "stddev: 0.03823599932872479",
            "extra": "mean: 35.291950300003805 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_df",
            "value": 22.9622366844243,
            "unit": "iter/sec",
            "range": "stddev: 0.03325925112565539",
            "extra": "mean: 43.54976450000265 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_memberships",
            "value": 1256.0106389107546,
            "unit": "iter/sec",
            "range": "stddev: 0.000022099393829769414",
            "extra": "mean: 796.1716000011165 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_members",
            "value": 136.21057468347797,
            "unit": "iter/sec",
            "range": "stddev: 0.000591332625540181",
            "extra": "mean: 7.341573899998366 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_attributes",
            "value": 13974.30683855479,
            "unit": "iter/sec",
            "range": "stddev: 0.000002967834917588263",
            "extra": "mean: 71.55990000455859 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_attributes",
            "value": 256.88185196993214,
            "unit": "iter/sec",
            "range": "stddev: 0.00017926659143535555",
            "extra": "mean: 3.8928402000038886 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_degree",
            "value": 9054.296806572323,
            "unit": "iter/sec",
            "range": "stddev: 0.000009276839585032882",
            "extra": "mean: 110.44480000634849 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_nodestats_degree",
            "value": 9054.141047414847,
            "unit": "iter/sec",
            "range": "stddev: 0.000013373004319214815",
            "extra": "mean: 110.44669999762391 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_size",
            "value": 262.55847374125364,
            "unit": "iter/sec",
            "range": "stddev: 0.0001710637835198998",
            "extra": "mean: 3.8086754000005385 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_isolates",
            "value": 8722.15234789137,
            "unit": "iter/sec",
            "range": "stddev: 0.000007419096498378163",
            "extra": "mean: 114.65060000261929 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_singletons",
            "value": 194.53587252183698,
            "unit": "iter/sec",
            "range": "stddev: 0.00019260232577766434",
            "extra": "mean: 5.140440100001342 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_copy",
            "value": 11.955122431033454,
            "unit": "iter/sec",
            "range": "stddev: 0.05974384035205233",
            "extra": "mean: 83.64615300000366 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_dual",
            "value": 12.018847105095643,
            "unit": "iter/sec",
            "range": "stddev: 0.06655020660351643",
            "extra": "mean: 83.20265590000133 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_erdos_renyi",
            "value": 52.68610823749986,
            "unit": "iter/sec",
            "range": "stddev: 0.001195986754110067",
            "extra": "mean: 18.98033530000305 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_fast_erdos_renyi",
            "value": 34.100044647866035,
            "unit": "iter/sec",
            "range": "stddev: 0.0017921171544183787",
            "extra": "mean: 29.325474800003803 msec\nrounds: 10"
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
          "id": "03c67c9604a9aa910e2889bd836cc82106474a65",
          "message": "final fix",
          "timestamp": "2025-02-09T09:58:29-05:00",
          "tree_id": "3927b0f4117c3b5351704dcaf808b1b5a88b57e3",
          "url": "https://github.com/xgi-org/xgi/commit/03c67c9604a9aa910e2889bd836cc82106474a65"
        },
        "date": 1739113162688,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/algorithms.py::test_connected",
            "value": 100.87881283963848,
            "unit": "iter/sec",
            "range": "stddev: 0.00018827427079466994",
            "extra": "mean: 9.912884299993152 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/algorithms.py::test_clustering_coefficient",
            "value": 62.20096729469923,
            "unit": "iter/sec",
            "range": "stddev: 0.0003687272753745415",
            "extra": "mean: 16.07692040000188 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgelist",
            "value": 28.837711550638833,
            "unit": "iter/sec",
            "range": "stddev: 0.041354176566051594",
            "extra": "mean: 34.676815400001715 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgedict",
            "value": 28.13931315836558,
            "unit": "iter/sec",
            "range": "stddev: 0.038580366716833965",
            "extra": "mean: 35.537470100001656 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_df",
            "value": 23.052790706295518,
            "unit": "iter/sec",
            "range": "stddev: 0.032980487632111505",
            "extra": "mean: 43.378695999999195 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_memberships",
            "value": 1280.6673403794593,
            "unit": "iter/sec",
            "range": "stddev: 0.000018967801944936703",
            "extra": "mean: 780.8429000021988 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_members",
            "value": 137.4128496789264,
            "unit": "iter/sec",
            "range": "stddev: 0.0005803251121659747",
            "extra": "mean: 7.277339800000959 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_attributes",
            "value": 15960.265322357678,
            "unit": "iter/sec",
            "range": "stddev: 0.000002315433690165441",
            "extra": "mean: 62.655600004291045 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_attributes",
            "value": 265.7706439736926,
            "unit": "iter/sec",
            "range": "stddev: 0.00006865129568012321",
            "extra": "mean: 3.762642800003846 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_degree",
            "value": 11107.19890914469,
            "unit": "iter/sec",
            "range": "stddev: 0.000014920736626564387",
            "extra": "mean: 90.03169999743932 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_nodestats_degree",
            "value": 10419.60803563009,
            "unit": "iter/sec",
            "range": "stddev: 0.000005200783029677823",
            "extra": "mean: 95.97289999589975 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_size",
            "value": 266.194345617087,
            "unit": "iter/sec",
            "range": "stddev: 0.0003052759428941787",
            "extra": "mean: 3.7566537999964567 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_isolates",
            "value": 7206.667031797324,
            "unit": "iter/sec",
            "range": "stddev: 0.000029615384917721696",
            "extra": "mean: 138.76040000013745 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_singletons",
            "value": 182.09814944557084,
            "unit": "iter/sec",
            "range": "stddev: 0.0004918413348004035",
            "extra": "mean: 5.491544000005888 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_copy",
            "value": 12.232112022062653,
            "unit": "iter/sec",
            "range": "stddev: 0.05906769158296043",
            "extra": "mean: 81.75203090000593 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_dual",
            "value": 12.079421320632806,
            "unit": "iter/sec",
            "range": "stddev: 0.06710849047723",
            "extra": "mean: 82.78542270000173 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_erdos_renyi",
            "value": 53.23835979064264,
            "unit": "iter/sec",
            "range": "stddev: 0.0007969262967602498",
            "extra": "mean: 18.783448700006034 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_fast_erdos_renyi",
            "value": 33.82084205739205,
            "unit": "iter/sec",
            "range": "stddev: 0.0013328187934342167",
            "extra": "mean: 29.567566599999395 msec\nrounds: 10"
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
          "id": "18de14b6f8924aac80ec917553eeb05d50bc6185",
          "message": "update literature",
          "timestamp": "2025-02-09T10:33:10-05:00",
          "tree_id": "c1ac66a9005ac7d35dc769d290adb03cd73178a9",
          "url": "https://github.com/xgi-org/xgi/commit/18de14b6f8924aac80ec917553eeb05d50bc6185"
        },
        "date": 1739115249066,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/algorithms.py::test_connected",
            "value": 94.80879289735273,
            "unit": "iter/sec",
            "range": "stddev: 0.00028319574666127234",
            "extra": "mean: 10.547544900003913 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/algorithms.py::test_clustering_coefficient",
            "value": 60.053512604139385,
            "unit": "iter/sec",
            "range": "stddev: 0.0005112335671104021",
            "extra": "mean: 16.651815299994155 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgelist",
            "value": 27.757446142416793,
            "unit": "iter/sec",
            "range": "stddev: 0.044396886699954806",
            "extra": "mean: 36.02636909999717 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgedict",
            "value": 27.369516357628076,
            "unit": "iter/sec",
            "range": "stddev: 0.04180909977122623",
            "extra": "mean: 36.53699930000016 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_df",
            "value": 22.72483538538249,
            "unit": "iter/sec",
            "range": "stddev: 0.0343390222619023",
            "extra": "mean: 44.004719200000864 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_memberships",
            "value": 1203.47616871282,
            "unit": "iter/sec",
            "range": "stddev: 0.000022639427620578187",
            "extra": "mean: 830.9262999944167 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_members",
            "value": 134.95765305516204,
            "unit": "iter/sec",
            "range": "stddev: 0.0005721887725935308",
            "extra": "mean: 7.409731699996769 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_attributes",
            "value": 14834.264183825495,
            "unit": "iter/sec",
            "range": "stddev: 0.000004013726700158012",
            "extra": "mean: 67.41149999811569 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_attributes",
            "value": 248.78362842549495,
            "unit": "iter/sec",
            "range": "stddev: 0.0006500566885909838",
            "extra": "mean: 4.019557099994131 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_degree",
            "value": 9287.198247815613,
            "unit": "iter/sec",
            "range": "stddev: 0.00001248363065870816",
            "extra": "mean: 107.67509999425329 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_nodestats_degree",
            "value": 8707.410964395804,
            "unit": "iter/sec",
            "range": "stddev: 0.000006455215980998054",
            "extra": "mean: 114.84470000198144 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_size",
            "value": 227.9016321858477,
            "unit": "iter/sec",
            "range": "stddev: 0.00017908147516754454",
            "extra": "mean: 4.387858000001188 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_isolates",
            "value": 7682.881387997299,
            "unit": "iter/sec",
            "range": "stddev: 0.00000976746680051185",
            "extra": "mean: 130.15949999726217 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_singletons",
            "value": 171.0396750984543,
            "unit": "iter/sec",
            "range": "stddev: 0.0006439226139897624",
            "extra": "mean: 5.846596700001783 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_copy",
            "value": 11.664503950989111,
            "unit": "iter/sec",
            "range": "stddev: 0.062114663430674455",
            "extra": "mean: 85.73017800000002 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_dual",
            "value": 11.621701825812256,
            "unit": "iter/sec",
            "range": "stddev: 0.0682187529444252",
            "extra": "mean: 86.04591780000419 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_erdos_renyi",
            "value": 52.89299505907338,
            "unit": "iter/sec",
            "range": "stddev: 0.001241513369747093",
            "extra": "mean: 18.90609520000055 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_fast_erdos_renyi",
            "value": 33.79132541398914,
            "unit": "iter/sec",
            "range": "stddev: 0.0012189154298549822",
            "extra": "mean: 29.593393799996193 msec\nrounds: 10"
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
          "id": "ee0908e17f6d667307e0f9096344aa6b5856dd34",
          "message": "Added Zulip as a sponsor and added ref data (#662)\n\n* Update date and add Zulip\n\n* update refs to specify xgi vs. xgi-data\n\n* updated reference list\n\n* updated logos\n\n* resize logos\n\n* updated landing page\n\n* moved support to a new file\n\n* update logo sizes\n\n* transparent background",
          "timestamp": "2025-02-13T08:27:01-05:00",
          "tree_id": "209e9817bcac10c1d567221a9cfc9828ed49cb49",
          "url": "https://github.com/xgi-org/xgi/commit/ee0908e17f6d667307e0f9096344aa6b5856dd34"
        },
        "date": 1739453282017,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/algorithms.py::test_connected",
            "value": 97.57109635016089,
            "unit": "iter/sec",
            "range": "stddev: 0.00016780906735709597",
            "extra": "mean: 10.248936800005026 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/algorithms.py::test_clustering_coefficient",
            "value": 61.50203114146873,
            "unit": "iter/sec",
            "range": "stddev: 0.0003241218356716562",
            "extra": "mean: 16.25962560000289 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgelist",
            "value": 27.98101547420018,
            "unit": "iter/sec",
            "range": "stddev: 0.04441179136383015",
            "extra": "mean: 35.73851709999758 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgedict",
            "value": 27.727378338334084,
            "unit": "iter/sec",
            "range": "stddev: 0.04066100677050473",
            "extra": "mean: 36.06543640000268 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_df",
            "value": 22.862416471959758,
            "unit": "iter/sec",
            "range": "stddev: 0.03374588150110158",
            "extra": "mean: 43.739908300003094 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_memberships",
            "value": 1319.044041296269,
            "unit": "iter/sec",
            "range": "stddev: 0.000021845645424253",
            "extra": "mean: 758.1248000008145 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_members",
            "value": 136.24186462369238,
            "unit": "iter/sec",
            "range": "stddev: 0.0005760993004856506",
            "extra": "mean: 7.339887799994926 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_attributes",
            "value": 16116.86662415439,
            "unit": "iter/sec",
            "range": "stddev: 0.0000036162757059892518",
            "extra": "mean: 62.04679999655127 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_attributes",
            "value": 263.0407516146448,
            "unit": "iter/sec",
            "range": "stddev: 0.00014628826250707752",
            "extra": "mean: 3.8016923000014913 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_degree",
            "value": 11723.865451942313,
            "unit": "iter/sec",
            "range": "stddev: 0.000014610839526468967",
            "extra": "mean: 85.29610000209686 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_nodestats_degree",
            "value": 10743.515751085597,
            "unit": "iter/sec",
            "range": "stddev: 0.0000022118769978741404",
            "extra": "mean: 93.07939999985138 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_size",
            "value": 276.36289952979604,
            "unit": "iter/sec",
            "range": "stddev: 0.00017081771852735635",
            "extra": "mean: 3.6184307000013405 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_isolates",
            "value": 9342.782000796788,
            "unit": "iter/sec",
            "range": "stddev: 0.000004872807365994642",
            "extra": "mean: 107.03449999311943 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_singletons",
            "value": 202.62763053472955,
            "unit": "iter/sec",
            "range": "stddev: 0.00008538463700931664",
            "extra": "mean: 4.9351610999991635 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_copy",
            "value": 12.190866803496313,
            "unit": "iter/sec",
            "range": "stddev: 0.06024142569673307",
            "extra": "mean: 82.02862159999995 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_dual",
            "value": 12.093741151538348,
            "unit": "iter/sec",
            "range": "stddev: 0.06454782800126906",
            "extra": "mean: 82.68739900000242 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_erdos_renyi",
            "value": 51.65841462237262,
            "unit": "iter/sec",
            "range": "stddev: 0.0006421241605162777",
            "extra": "mean: 19.357930499998588 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_fast_erdos_renyi",
            "value": 32.783559273198996,
            "unit": "iter/sec",
            "range": "stddev: 0.0013789609769714866",
            "extra": "mean: 30.503094299999134 msec\nrounds: 10"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "maximelucas@users.noreply.github.com",
            "name": "Maxime Lucas",
            "username": "maximelucas"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "a365243d13fb56412b90c06980f2b73467092491",
          "message": "Add adjacency tensor function (#664)\n\n* feat: added adj tensor\r\n\r\n* test: added + fix support for empty hypergraph\r\n\r\n* fix: test\r\n\r\n* docs: added new function\r\n\r\n* style: isort + black\r\n\r\n* review changes\r\n\r\n* review: added normalized option\r\n\r\n* fix: dtype\r\n\r\n* fix: coldict",
          "timestamp": "2025-02-13T15:16:29+01:00",
          "tree_id": "8846df7b3d712919c508ccb1b5367568454a41cb",
          "url": "https://github.com/xgi-org/xgi/commit/a365243d13fb56412b90c06980f2b73467092491"
        },
        "date": 1739456250373,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/algorithms.py::test_connected",
            "value": 89.19198784091573,
            "unit": "iter/sec",
            "range": "stddev: 0.0005035386456682",
            "extra": "mean: 11.211769400000549 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/algorithms.py::test_clustering_coefficient",
            "value": 60.87051310359314,
            "unit": "iter/sec",
            "range": "stddev: 0.00034380055932295623",
            "extra": "mean: 16.428315600003884 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgelist",
            "value": 27.419101503902798,
            "unit": "iter/sec",
            "range": "stddev: 0.04529739157555914",
            "extra": "mean: 36.470925199998305 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgedict",
            "value": 26.63502844345289,
            "unit": "iter/sec",
            "range": "stddev: 0.04364758373885502",
            "extra": "mean: 37.544544100001076 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_df",
            "value": 21.27051825979191,
            "unit": "iter/sec",
            "range": "stddev: 0.038783242364370696",
            "extra": "mean: 47.01342900000327 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_memberships",
            "value": 1042.1860227004306,
            "unit": "iter/sec",
            "range": "stddev: 0.0001722387096711351",
            "extra": "mean: 959.5216000008122 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_members",
            "value": 129.140686250913,
            "unit": "iter/sec",
            "range": "stddev: 0.0006184038048264257",
            "extra": "mean: 7.7434930000066515 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_attributes",
            "value": 12757.59172376312,
            "unit": "iter/sec",
            "range": "stddev: 0.000007098965612012466",
            "extra": "mean: 78.38470000081088 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_attributes",
            "value": 243.81050462428718,
            "unit": "iter/sec",
            "range": "stddev: 0.0002218521697160708",
            "extra": "mean: 4.101546000001122 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_degree",
            "value": 8978.353190645721,
            "unit": "iter/sec",
            "range": "stddev: 0.000012491450608712207",
            "extra": "mean: 111.37899999766887 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_nodestats_degree",
            "value": 8156.1478186816075,
            "unit": "iter/sec",
            "range": "stddev: 0.000005846852133775142",
            "extra": "mean: 122.60690000118757 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_size",
            "value": 223.62557707684678,
            "unit": "iter/sec",
            "range": "stddev: 0.00018516106561370228",
            "extra": "mean: 4.471760400002722 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_isolates",
            "value": 7453.314302853977,
            "unit": "iter/sec",
            "range": "stddev: 0.000005858760136487615",
            "extra": "mean: 134.1684999943027 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_singletons",
            "value": 172.87920777642907,
            "unit": "iter/sec",
            "range": "stddev: 0.00009851305791909619",
            "extra": "mean: 5.784385599991992 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_copy",
            "value": 10.994670525869116,
            "unit": "iter/sec",
            "range": "stddev: 0.0671732295982246",
            "extra": "mean: 90.95315750000168 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_dual",
            "value": 11.091135926014799,
            "unit": "iter/sec",
            "range": "stddev: 0.07249706974412097",
            "extra": "mean: 90.16209039999694 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_erdos_renyi",
            "value": 52.09039700820356,
            "unit": "iter/sec",
            "range": "stddev: 0.0013386455147398422",
            "extra": "mean: 19.19739640000273 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_fast_erdos_renyi",
            "value": 29.223267155014298,
            "unit": "iter/sec",
            "range": "stddev: 0.004819810668391021",
            "extra": "mean: 34.21930869999983 msec\nrounds: 10"
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
          "id": "1c44e11570a6d36dd5f3905fbec8834a7d0611f0",
          "message": "Update contributors and adjacency tensor (#666)\n\n* Update contribute.rst\n\n* Update hypergraph_matrix.py\n\n* fix failing tests",
          "timestamp": "2025-02-14T23:11:36-05:00",
          "tree_id": "572241392a3a73fc7e7059c092141f666c4ac127",
          "url": "https://github.com/xgi-org/xgi/commit/1c44e11570a6d36dd5f3905fbec8834a7d0611f0"
        },
        "date": 1739592747802,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/algorithms.py::test_connected",
            "value": 98.81012648072544,
            "unit": "iter/sec",
            "range": "stddev: 0.00020122022402674537",
            "extra": "mean: 10.120420199999103 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/algorithms.py::test_clustering_coefficient",
            "value": 61.90032397576511,
            "unit": "iter/sec",
            "range": "stddev: 0.0003355747620437435",
            "extra": "mean: 16.155004300001963 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgelist",
            "value": 29.356082606444684,
            "unit": "iter/sec",
            "range": "stddev: 0.04076924764241054",
            "extra": "mean: 34.06449059999801 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgedict",
            "value": 28.838228823582472,
            "unit": "iter/sec",
            "range": "stddev: 0.03645258252397498",
            "extra": "mean: 34.67619339999999 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_df",
            "value": 22.98704731144995,
            "unit": "iter/sec",
            "range": "stddev: 0.032675919169292515",
            "extra": "mean: 43.502759900002275 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_memberships",
            "value": 1263.0184043301924,
            "unit": "iter/sec",
            "range": "stddev: 0.00005274293966399109",
            "extra": "mean: 791.7540999969219 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_members",
            "value": 136.78054034195907,
            "unit": "iter/sec",
            "range": "stddev: 0.0005666592542450741",
            "extra": "mean: 7.310981499999514 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_attributes",
            "value": 14516.4006294708,
            "unit": "iter/sec",
            "range": "stddev: 0.000006612165154431796",
            "extra": "mean: 68.88759999981175 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_attributes",
            "value": 253.93731069935689,
            "unit": "iter/sec",
            "range": "stddev: 0.0005792057566403583",
            "extra": "mean: 3.9379797999984594 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_degree",
            "value": 11065.44769690895,
            "unit": "iter/sec",
            "range": "stddev: 0.000006601672990045342",
            "extra": "mean: 90.37140000032196 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_nodestats_degree",
            "value": 9549.867018034145,
            "unit": "iter/sec",
            "range": "stddev: 0.000006093788827859879",
            "extra": "mean: 104.71350000074153 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_size",
            "value": 248.23702067927258,
            "unit": "iter/sec",
            "range": "stddev: 0.00014102984893980637",
            "extra": "mean: 4.028407999997796 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_isolates",
            "value": 8871.42204451002,
            "unit": "iter/sec",
            "range": "stddev: 0.0000033937464791624943",
            "extra": "mean: 112.7215000011006 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_singletons",
            "value": 190.6718670256704,
            "unit": "iter/sec",
            "range": "stddev: 0.00025903192352986733",
            "extra": "mean: 5.244612200002052 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_copy",
            "value": 12.155104131762128,
            "unit": "iter/sec",
            "range": "stddev: 0.058423653076859455",
            "extra": "mean: 82.26996570000011 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_dual",
            "value": 12.367700344096473,
            "unit": "iter/sec",
            "range": "stddev: 0.05971098797681553",
            "extra": "mean: 80.85577530000023 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_erdos_renyi",
            "value": 52.94730708355309,
            "unit": "iter/sec",
            "range": "stddev: 0.0010525292349286273",
            "extra": "mean: 18.886701799998207 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_fast_erdos_renyi",
            "value": 33.613528762301264,
            "unit": "iter/sec",
            "range": "stddev: 0.001023184183657177",
            "extra": "mean: 29.74992619999881 msec\nrounds: 10"
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
          "id": "41e8c679aa22c325b51de8cd33984fc39dd6ca44",
          "message": "Add `mode` to `stats` module (#667)\n\n* Added `mode` as a `stats` function\n\n* add unit tests\n\n* format with isort and black\n\n* updated docs",
          "timestamp": "2025-02-18T13:28:39-05:00",
          "tree_id": "62b41d3ace71e7a05b3e9ec16763a468ac4e9858",
          "url": "https://github.com/xgi-org/xgi/commit/41e8c679aa22c325b51de8cd33984fc39dd6ca44"
        },
        "date": 1739903380743,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/algorithms.py::test_connected",
            "value": 99.64805602044363,
            "unit": "iter/sec",
            "range": "stddev: 0.00022582487271672594",
            "extra": "mean: 10.035318699993923 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/algorithms.py::test_clustering_coefficient",
            "value": 61.96989172980919,
            "unit": "iter/sec",
            "range": "stddev: 0.0004137402294996441",
            "extra": "mean: 16.136868599997456 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgelist",
            "value": 29.37872694490094,
            "unit": "iter/sec",
            "range": "stddev: 0.0403907213496607",
            "extra": "mean: 34.0382346000041 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgedict",
            "value": 28.827363837780435,
            "unit": "iter/sec",
            "range": "stddev: 0.03663532419392319",
            "extra": "mean: 34.68926280000062 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_df",
            "value": 22.734368898842494,
            "unit": "iter/sec",
            "range": "stddev: 0.03248205798697236",
            "extra": "mean: 43.986266099997806 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_memberships",
            "value": 1281.3038548161499,
            "unit": "iter/sec",
            "range": "stddev: 0.000025278148179648904",
            "extra": "mean: 780.4549999917754 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_members",
            "value": 137.38900737081318,
            "unit": "iter/sec",
            "range": "stddev: 0.0005611971137556304",
            "extra": "mean: 7.278602700003489 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_attributes",
            "value": 15177.523907606686,
            "unit": "iter/sec",
            "range": "stddev: 0.000005858484491425836",
            "extra": "mean: 65.88690000342012 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_attributes",
            "value": 261.2321668226678,
            "unit": "iter/sec",
            "range": "stddev: 0.00007619476148810426",
            "extra": "mean: 3.828012500002842 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_degree",
            "value": 11490.053060542754,
            "unit": "iter/sec",
            "range": "stddev: 0.000007801245854949064",
            "extra": "mean: 87.03180000395605 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_nodestats_degree",
            "value": 10280.630366808115,
            "unit": "iter/sec",
            "range": "stddev: 0.000005592373660690847",
            "extra": "mean: 97.27030000306058 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_size",
            "value": 267.5957448211109,
            "unit": "iter/sec",
            "range": "stddev: 0.0001963424334332633",
            "extra": "mean: 3.7369801999972196 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_isolates",
            "value": 9202.883079374324,
            "unit": "iter/sec",
            "range": "stddev: 0.000005268939583318502",
            "extra": "mean: 108.66159999807223 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_singletons",
            "value": 197.41701551078685,
            "unit": "iter/sec",
            "range": "stddev: 0.00022464294951357223",
            "extra": "mean: 5.06541949999928 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_copy",
            "value": 12.15057642662712,
            "unit": "iter/sec",
            "range": "stddev: 0.058353858756416147",
            "extra": "mean: 82.30062219999468 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_dual",
            "value": 12.269285849027874,
            "unit": "iter/sec",
            "range": "stddev: 0.061726576559385085",
            "extra": "mean: 81.50433630000009 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_erdos_renyi",
            "value": 51.23182176491718,
            "unit": "iter/sec",
            "range": "stddev: 0.0009875799120787957",
            "extra": "mean: 19.519118499994192 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_fast_erdos_renyi",
            "value": 32.88187267473432,
            "unit": "iter/sec",
            "range": "stddev: 0.001458245933394205",
            "extra": "mean: 30.41189319999944 msec\nrounds: 10"
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
          "id": "6764dcf3eb643bde3f95654fc6b4ec6ac753a48e",
          "message": "Feature/spectral clustering (#665)\n\n* feat: add kmeans skeleton\n\nAdd module boilerplate.\nAdd `_kmeans` function with naive signature.\nAdd test class and trivial clustering test case.\n\n* feat: add spectral clustering skeleton\n\nAdd `spectral_clustering` function.\nAdd test class and test overabundant cluster exception.\n\n* refactor: rename `commdetect` to `communities`\n\n* refactor: change `_kmeans` return type to dict\n\n* test(kmeans): add simple unit tests\n\n* test(kmeans): add perfectly separable unit tests\n\n* feat(kmeans): implement kmeans\n\n* refactor(kmeans): add numpy rng, fix seed\n\nAdd `numpy.random.default_rng` to `_kmeans` for random number sampling.\nFixes bug with test cases where clusters could get merged from rare random conditions.\n\n* test(spectral): add spectral clustering test\n\nAdd perfectly separable `spectral_clustering` test.\n\n* fix(spectral): fix node indexing in cluster return\n\n* test(spectral): add spectral clustering test\n\n* doc: Add `spectral_clustering` docstring\n\n* refactor(kmeans): move kwargs to `_kmeans`\n\n* doc: update `_kmeans` docstring\n\n* refactor: propogate kmean kwargs\n\n* fix(kmeans): fix centroid updating\n\n* test(spectral): add sbm test\n\n* test: fix test seeds\n\n* chore: pylint + isort\n\n* Apply suggestions from code review\n\nCo-authored-by: Thomas Robiglio <83019028+thomasrobiglio@users.noreply.github.com>\n\n* doc: expand spectral clustering docstring\n\n* doc: add api reference for communities module\n\nAdd communities section-level API documentation.\nAdd communites.spectral function-level API documentation.\n\n* doc: update spectral docs\n\nAdd communities module to API reference docs.\nRemove _kmeans from doc source.\nRemove auto-generated examples.\nAdd auto-generated examples to .gitignore.\n\n* refactor(spectral): refactor function signature\n\nAdd `_kmeans` kwargs explicitly to `spectral_clustering` arguments.\n\n---------\n\nCo-authored-by: Thomas Robiglio <83019028+thomasrobiglio@users.noreply.github.com>",
          "timestamp": "2025-03-14T11:51:18-04:00",
          "tree_id": "5dd4a924d6e3b9599a18608ee406d264c12f6896",
          "url": "https://github.com/xgi-org/xgi/commit/6764dcf3eb643bde3f95654fc6b4ec6ac753a48e"
        },
        "date": 1741967534646,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/algorithms.py::test_connected",
            "value": 94.42327097020168,
            "unit": "iter/sec",
            "range": "stddev: 0.0003131648266162609",
            "extra": "mean: 10.59060959999556 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/algorithms.py::test_clustering_coefficient",
            "value": 61.49473594296819,
            "unit": "iter/sec",
            "range": "stddev: 0.00035225081531166646",
            "extra": "mean: 16.261554500005104 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgelist",
            "value": 27.489069926584925,
            "unit": "iter/sec",
            "range": "stddev: 0.0461102739648425",
            "extra": "mean: 36.378095100005226 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgedict",
            "value": 27.394858532951652,
            "unit": "iter/sec",
            "range": "stddev: 0.04191438907974974",
            "extra": "mean: 36.503199999998515 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_df",
            "value": 21.65791185286202,
            "unit": "iter/sec",
            "range": "stddev: 0.03746593626982887",
            "extra": "mean: 46.172502999999665 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_memberships",
            "value": 1231.8056151576413,
            "unit": "iter/sec",
            "range": "stddev: 0.000027637855952717728",
            "extra": "mean: 811.8164000023853 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_members",
            "value": 132.1427587909258,
            "unit": "iter/sec",
            "range": "stddev: 0.0006338035590389037",
            "extra": "mean: 7.567573199997923 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_attributes",
            "value": 13793.483958157296,
            "unit": "iter/sec",
            "range": "stddev: 0.000007649066361939431",
            "extra": "mean: 72.49800000010964 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_attributes",
            "value": 253.30312980576272,
            "unit": "iter/sec",
            "range": "stddev: 0.00011952931232347973",
            "extra": "mean: 3.947839100001715 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_degree",
            "value": 10142.337565082034,
            "unit": "iter/sec",
            "range": "stddev: 0.000014454823757378762",
            "extra": "mean: 98.59660000302028 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_nodestats_degree",
            "value": 9219.31741992131,
            "unit": "iter/sec",
            "range": "stddev: 0.000006773097719902455",
            "extra": "mean: 108.46790000300643 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_size",
            "value": 246.811668356963,
            "unit": "iter/sec",
            "range": "stddev: 0.00023405007305577792",
            "extra": "mean: 4.051672300005293 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_isolates",
            "value": 8331.847487637195,
            "unit": "iter/sec",
            "range": "stddev: 0.000008714302650879356",
            "extra": "mean: 120.021399993675 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_singletons",
            "value": 182.1364006027554,
            "unit": "iter/sec",
            "range": "stddev: 0.0002457234381678739",
            "extra": "mean: 5.490390699995373 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_copy",
            "value": 11.33430389355336,
            "unit": "iter/sec",
            "range": "stddev: 0.06681455693078353",
            "extra": "mean: 88.22773850000374 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_dual",
            "value": 11.54509467047494,
            "unit": "iter/sec",
            "range": "stddev: 0.07039695195800846",
            "extra": "mean: 86.61687309999877 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_erdos_renyi",
            "value": 52.85264319449277,
            "unit": "iter/sec",
            "range": "stddev: 0.0014929593665745661",
            "extra": "mean: 18.92052960000683 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_fast_erdos_renyi",
            "value": 33.10887743761748,
            "unit": "iter/sec",
            "range": "stddev: 0.001157315560864136",
            "extra": "mean: 30.203379799999652 msec\nrounds: 10"
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
          "id": "eb8a69d91425e0ed527adb2943fddcae3aa82bea",
          "message": "Added a recipe for community detection (#668)\n\n* Added a recipe for community detection\n\n* Update recipes.ipynb\n\n* Update using-xgi.rst\n\n* Update recipes.ipynb\n\n* Update recipes.ipynb",
          "timestamp": "2025-03-27T14:27:11-04:00",
          "tree_id": "e72039806ab2b133e621337e70e829a5bdc0fba2",
          "url": "https://github.com/xgi-org/xgi/commit/eb8a69d91425e0ed527adb2943fddcae3aa82bea"
        },
        "date": 1743100090385,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/algorithms.py::test_connected",
            "value": 88.66320674462771,
            "unit": "iter/sec",
            "range": "stddev: 0.0002853467608712213",
            "extra": "mean: 11.278635599998665 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/algorithms.py::test_clustering_coefficient",
            "value": 60.01472569319224,
            "unit": "iter/sec",
            "range": "stddev: 0.0003270807241586573",
            "extra": "mean: 16.662577200006012 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgelist",
            "value": 26.690634928010514,
            "unit": "iter/sec",
            "range": "stddev: 0.04760984414822775",
            "extra": "mean: 37.46632489999513 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgedict",
            "value": 26.03852861711825,
            "unit": "iter/sec",
            "range": "stddev: 0.04409056888775485",
            "extra": "mean: 38.404627799997115 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_df",
            "value": 19.501018279795087,
            "unit": "iter/sec",
            "range": "stddev: 0.045412179042913926",
            "extra": "mean: 51.27937350000309 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_memberships",
            "value": 1127.4159254968517,
            "unit": "iter/sec",
            "range": "stddev: 0.000024887599511208103",
            "extra": "mean: 886.9840999977896 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_members",
            "value": 127.34410086299151,
            "unit": "iter/sec",
            "range": "stddev: 0.0007508724888851633",
            "extra": "mean: 7.852739099990912 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_attributes",
            "value": 11855.44888194117,
            "unit": "iter/sec",
            "range": "stddev: 0.00000846109705082476",
            "extra": "mean: 84.34940000654478 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_attributes",
            "value": 240.8184417033217,
            "unit": "iter/sec",
            "range": "stddev: 0.0004400872747993424",
            "extra": "mean: 4.15250589999232 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_degree",
            "value": 9110.314059835606,
            "unit": "iter/sec",
            "range": "stddev: 0.000013711086239791824",
            "extra": "mean: 109.76570000025276 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_nodestats_degree",
            "value": 8193.114997587638,
            "unit": "iter/sec",
            "range": "stddev: 0.00000456170760133997",
            "extra": "mean: 122.05370000231142 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_size",
            "value": 215.40514714022652,
            "unit": "iter/sec",
            "range": "stddev: 0.00017607266094213267",
            "extra": "mean: 4.64241460000494 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_isolates",
            "value": 7217.9548070181945,
            "unit": "iter/sec",
            "range": "stddev: 0.000007300468612281113",
            "extra": "mean: 138.54339999852527 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_singletons",
            "value": 168.11890296829216,
            "unit": "iter/sec",
            "range": "stddev: 0.0002413992241719869",
            "extra": "mean: 5.948171100001787 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_copy",
            "value": 11.024454914429876,
            "unit": "iter/sec",
            "range": "stddev: 0.06576248537294052",
            "extra": "mean: 90.70743250000532 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_dual",
            "value": 10.93991002799213,
            "unit": "iter/sec",
            "range": "stddev: 0.07437318438164817",
            "extra": "mean: 91.40842999999848 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_erdos_renyi",
            "value": 53.46956208551482,
            "unit": "iter/sec",
            "range": "stddev: 0.0015073809831656485",
            "extra": "mean: 18.702229100000523 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_fast_erdos_renyi",
            "value": 35.56026367124928,
            "unit": "iter/sec",
            "range": "stddev: 0.0012585585601353159",
            "extra": "mean: 28.1212762999985 msec\nrounds: 10"
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
          "id": "4fbe28591eac2031849cd58e0e57de354fc88aaf",
          "message": "Updated changelog and up-versioned",
          "timestamp": "2025-03-27T15:02:55-04:00",
          "tree_id": "539ad8ae522d45392ae8026d8e751a297320efb0",
          "url": "https://github.com/xgi-org/xgi/commit/4fbe28591eac2031849cd58e0e57de354fc88aaf"
        },
        "date": 1743102252937,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/algorithms.py::test_connected",
            "value": 97.18099979677712,
            "unit": "iter/sec",
            "range": "stddev: 0.00044955644569912674",
            "extra": "mean: 10.290077299998757 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/algorithms.py::test_clustering_coefficient",
            "value": 62.0076403458035,
            "unit": "iter/sec",
            "range": "stddev: 0.00037380146973154234",
            "extra": "mean: 16.12704490000283 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgelist",
            "value": 28.747397799928766,
            "unit": "iter/sec",
            "range": "stddev: 0.04240490650954672",
            "extra": "mean: 34.78575719999526 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgedict",
            "value": 27.71763935462748,
            "unit": "iter/sec",
            "range": "stddev: 0.04068399812277393",
            "extra": "mean: 36.078108499995665 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_df",
            "value": 22.433256955272913,
            "unit": "iter/sec",
            "range": "stddev: 0.03570248216144362",
            "extra": "mean: 44.57667479999827 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_memberships",
            "value": 1240.9078680552338,
            "unit": "iter/sec",
            "range": "stddev: 0.00004733098721337969",
            "extra": "mean: 805.8615999971153 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_members",
            "value": 138.49086613974004,
            "unit": "iter/sec",
            "range": "stddev: 0.0005746235623166419",
            "extra": "mean: 7.220692799992889 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_attributes",
            "value": 14958.863125374763,
            "unit": "iter/sec",
            "range": "stddev: 0.000004920173728938286",
            "extra": "mean: 66.8500000045924 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_attributes",
            "value": 266.8976363227425,
            "unit": "iter/sec",
            "range": "stddev: 0.00012358067006104062",
            "extra": "mean: 3.7467547999966655 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_degree",
            "value": 10347.071829755054,
            "unit": "iter/sec",
            "range": "stddev: 0.000026128959469224423",
            "extra": "mean: 96.64570000609274 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_nodestats_degree",
            "value": 9161.939105978572,
            "unit": "iter/sec",
            "range": "stddev: 0.00000960760004446925",
            "extra": "mean: 109.14720000130274 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_size",
            "value": 265.80672873725496,
            "unit": "iter/sec",
            "range": "stddev: 0.00020304157467432117",
            "extra": "mean: 3.762132000008478 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_isolates",
            "value": 8973.100439827898,
            "unit": "iter/sec",
            "range": "stddev: 0.000010774263808911618",
            "extra": "mean: 111.44419999595812 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_singletons",
            "value": 188.49915034956112,
            "unit": "iter/sec",
            "range": "stddev: 0.0003172226217227458",
            "extra": "mean: 5.3050636999984135 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_copy",
            "value": 11.84620936368662,
            "unit": "iter/sec",
            "range": "stddev: 0.06617422391945503",
            "extra": "mean: 84.41518880000558 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_dual",
            "value": 11.341871106765531,
            "unit": "iter/sec",
            "range": "stddev: 0.0771752406925212",
            "extra": "mean: 88.16887360000862 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_erdos_renyi",
            "value": 53.95695341235731,
            "unit": "iter/sec",
            "range": "stddev: 0.001390719303318382",
            "extra": "mean: 18.53329249999831 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_fast_erdos_renyi",
            "value": 36.265443915811055,
            "unit": "iter/sec",
            "range": "stddev: 0.0013376624266685806",
            "extra": "mean: 27.574459100003423 msec\nrounds: 10"
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
          "id": "b72e272a6635f6ba5fdb471e4f16e125576b083b",
          "message": "Update using-xgi.rst",
          "timestamp": "2025-03-28T13:41:12-04:00",
          "tree_id": "4bcf1f62f8955afa39cc13f91c72c7459e9eeb8a",
          "url": "https://github.com/xgi-org/xgi/commit/b72e272a6635f6ba5fdb471e4f16e125576b083b"
        },
        "date": 1743183726057,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/algorithms.py::test_connected",
            "value": 98.45001865821733,
            "unit": "iter/sec",
            "range": "stddev: 0.00023716120478220611",
            "extra": "mean: 10.157438400003116 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/algorithms.py::test_clustering_coefficient",
            "value": 60.73208446627531,
            "unit": "iter/sec",
            "range": "stddev: 0.0009827986239631394",
            "extra": "mean: 16.46576120000134 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgelist",
            "value": 29.17864952345297,
            "unit": "iter/sec",
            "range": "stddev: 0.04045759587144027",
            "extra": "mean: 34.27163410000276 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgedict",
            "value": 28.69727118910895,
            "unit": "iter/sec",
            "range": "stddev: 0.0387350766325051",
            "extra": "mean: 34.84651880000058 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_df",
            "value": 22.893077558468267,
            "unit": "iter/sec",
            "range": "stddev: 0.03344760019566825",
            "extra": "mean: 43.681326700004774 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_memberships",
            "value": 1250.2345752672954,
            "unit": "iter/sec",
            "range": "stddev: 0.00005017621323530019",
            "extra": "mean: 799.8498999967296 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_members",
            "value": 138.81924789945765,
            "unit": "iter/sec",
            "range": "stddev: 0.0005709666255788344",
            "extra": "mean: 7.203612000003545 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_attributes",
            "value": 14179.911886943255,
            "unit": "iter/sec",
            "range": "stddev: 0.000004728914889361166",
            "extra": "mean: 70.52229999544579 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_attributes",
            "value": 261.8497416632322,
            "unit": "iter/sec",
            "range": "stddev: 0.00014108547966284142",
            "extra": "mean: 3.8189840999962144 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_degree",
            "value": 10403.640441718679,
            "unit": "iter/sec",
            "range": "stddev: 0.000014308994851242386",
            "extra": "mean: 96.12020000133725 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_nodestats_degree",
            "value": 8638.637168878353,
            "unit": "iter/sec",
            "range": "stddev: 0.0000055980569981484195",
            "extra": "mean: 115.75899999627381 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_size",
            "value": 238.29533809471263,
            "unit": "iter/sec",
            "range": "stddev: 0.00018666918605672738",
            "extra": "mean: 4.196473200002515 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_isolates",
            "value": 8100.885183674254,
            "unit": "iter/sec",
            "range": "stddev: 0.000010764600291996121",
            "extra": "mean: 123.44330000075844 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_singletons",
            "value": 185.69375222961645,
            "unit": "iter/sec",
            "range": "stddev: 0.0002414516753206637",
            "extra": "mean: 5.3852108000029375 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_copy",
            "value": 11.771477168390767,
            "unit": "iter/sec",
            "range": "stddev: 0.06274605442305944",
            "extra": "mean: 84.95110560000398 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_dual",
            "value": 11.692854242218955,
            "unit": "iter/sec",
            "range": "stddev: 0.06836093815814195",
            "extra": "mean: 85.52231810000137 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_erdos_renyi",
            "value": 53.87366551092221,
            "unit": "iter/sec",
            "range": "stddev: 0.0012113910530624817",
            "extra": "mean: 18.561944699999344 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_fast_erdos_renyi",
            "value": 36.0421593066676,
            "unit": "iter/sec",
            "range": "stddev: 0.0013311314313527636",
            "extra": "mean: 27.745285500000705 msec\nrounds: 10"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "maximelucas@users.noreply.github.com",
            "name": "Maxime Lucas",
            "username": "maximelucas"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "c55afe7b8b64d6e27970936c23b22f342c4f1dd3",
          "message": "added 2 gallery examples (#669)\n\n* added 2 gallery examples\n\n* fix: minor changes\n\n* docs: added comment",
          "timestamp": "2025-03-31T13:51:07+02:00",
          "tree_id": "000bfd4d417a6cb37d840efb412fa5b5c3ca180b",
          "url": "https://github.com/xgi-org/xgi/commit/c55afe7b8b64d6e27970936c23b22f342c4f1dd3"
        },
        "date": 1743421919416,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/algorithms.py::test_connected",
            "value": 99.75388720947555,
            "unit": "iter/sec",
            "range": "stddev: 0.00017647052871285997",
            "extra": "mean: 10.024672000000123 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/algorithms.py::test_clustering_coefficient",
            "value": 62.035337102222584,
            "unit": "iter/sec",
            "range": "stddev: 0.0004882467459113133",
            "extra": "mean: 16.119844700000385 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgelist",
            "value": 28.796435360682217,
            "unit": "iter/sec",
            "range": "stddev: 0.040749213713759336",
            "extra": "mean: 34.72652039999957 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgedict",
            "value": 28.65623736089858,
            "unit": "iter/sec",
            "range": "stddev: 0.038121188185397545",
            "extra": "mean: 34.89641669999912 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_df",
            "value": 22.79462862720951,
            "unit": "iter/sec",
            "range": "stddev: 0.03264935263376398",
            "extra": "mean: 43.86998429999949 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_memberships",
            "value": 1289.4992977365253,
            "unit": "iter/sec",
            "range": "stddev: 0.000021971429899399774",
            "extra": "mean: 775.4948000012973 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_members",
            "value": 140.17237726131776,
            "unit": "iter/sec",
            "range": "stddev: 0.0005836436699190594",
            "extra": "mean: 7.13407319999817 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_attributes",
            "value": 15691.788174310628,
            "unit": "iter/sec",
            "range": "stddev: 0.0000037037843766464882",
            "extra": "mean: 63.72759999635491 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_attributes",
            "value": 268.105945174112,
            "unit": "iter/sec",
            "range": "stddev: 0.00006985719695010525",
            "extra": "mean: 3.729868800002123 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_degree",
            "value": 11223.117826612019,
            "unit": "iter/sec",
            "range": "stddev: 0.000018759372118898986",
            "extra": "mean: 89.10180000327728 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_nodestats_degree",
            "value": 10121.580423850191,
            "unit": "iter/sec",
            "range": "stddev: 0.000009722605600640307",
            "extra": "mean: 98.79880000198682 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_size",
            "value": 280.13184237093725,
            "unit": "iter/sec",
            "range": "stddev: 0.00009139443402197255",
            "extra": "mean: 3.5697476999985156 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_isolates",
            "value": 9280.78552565165,
            "unit": "iter/sec",
            "range": "stddev: 0.000004360300906305884",
            "extra": "mean: 107.74950000040917 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_singletons",
            "value": 176.5278850331881,
            "unit": "iter/sec",
            "range": "stddev: 0.00024219782192982218",
            "extra": "mean: 5.6648273999996945 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_copy",
            "value": 11.78848797800015,
            "unit": "iter/sec",
            "range": "stddev: 0.0627724733642785",
            "extra": "mean: 84.82852099999718 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_dual",
            "value": 12.21860381303547,
            "unit": "iter/sec",
            "range": "stddev: 0.06377413496146583",
            "extra": "mean: 81.84241139999529 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_erdos_renyi",
            "value": 53.68700067363744,
            "unit": "iter/sec",
            "range": "stddev: 0.0007126505567335434",
            "extra": "mean: 18.626482900003793 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_fast_erdos_renyi",
            "value": 36.1551068546176,
            "unit": "iter/sec",
            "range": "stddev: 0.0013011476840518433",
            "extra": "mean: 27.65860999999461 msec\nrounds: 10"
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
          "id": "80b06e2f1ec2614d592da26e48c022c30f034339",
          "message": "Update using-xgi.rst",
          "timestamp": "2025-04-08T13:41:36-04:00",
          "tree_id": "d3f3cc451d7205e64369929ff109ffa8a0f6e925",
          "url": "https://github.com/xgi-org/xgi/commit/80b06e2f1ec2614d592da26e48c022c30f034339"
        },
        "date": 1744134157876,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/algorithms.py::test_connected",
            "value": 86.34638168759228,
            "unit": "iter/sec",
            "range": "stddev: 0.0008282529056116039",
            "extra": "mean: 11.581261200012705 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/algorithms.py::test_clustering_coefficient",
            "value": 60.14637389964492,
            "unit": "iter/sec",
            "range": "stddev: 0.0003785282866232668",
            "extra": "mean: 16.626106199993274 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgelist",
            "value": 25.84756284532083,
            "unit": "iter/sec",
            "range": "stddev: 0.05052058139223851",
            "extra": "mean: 38.68836709999641 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgedict",
            "value": 26.690026489593954,
            "unit": "iter/sec",
            "range": "stddev: 0.04321238858935405",
            "extra": "mean: 37.46717899998657 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_df",
            "value": 20.980761296492567,
            "unit": "iter/sec",
            "range": "stddev: 0.03910893632036669",
            "extra": "mean: 47.66271279999614 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_memberships",
            "value": 1094.2696926188432,
            "unit": "iter/sec",
            "range": "stddev: 0.0000194833748870399",
            "extra": "mean: 913.8514999960989 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_members",
            "value": 127.32472020650955,
            "unit": "iter/sec",
            "range": "stddev: 0.0006790758455519532",
            "extra": "mean: 7.853934399997797 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_attributes",
            "value": 12629.212631520206,
            "unit": "iter/sec",
            "range": "stddev: 0.000003974934571578046",
            "extra": "mean: 79.18150000136848 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_attributes",
            "value": 234.83031947798042,
            "unit": "iter/sec",
            "range": "stddev: 0.00021349486994721604",
            "extra": "mean: 4.258393899999646 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_degree",
            "value": 8492.778165637339,
            "unit": "iter/sec",
            "range": "stddev: 0.000012196281264403445",
            "extra": "mean: 117.7471000062269 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_nodestats_degree",
            "value": 7546.993240358427,
            "unit": "iter/sec",
            "range": "stddev: 0.000006032108040616381",
            "extra": "mean: 132.5030999964838 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_size",
            "value": 215.97283234544045,
            "unit": "iter/sec",
            "range": "stddev: 0.00007107614312444763",
            "extra": "mean: 4.630212000000711 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_isolates",
            "value": 7060.11262285966,
            "unit": "iter/sec",
            "range": "stddev: 0.00001427373738227551",
            "extra": "mean: 141.64080000114154 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_singletons",
            "value": 164.94345565126187,
            "unit": "iter/sec",
            "range": "stddev: 0.0006801597849375898",
            "extra": "mean: 6.06268370000862 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_copy",
            "value": 10.823036618281398,
            "unit": "iter/sec",
            "range": "stddev: 0.07026214895308681",
            "extra": "mean: 92.39551109998843 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_dual",
            "value": 10.94594709512156,
            "unit": "iter/sec",
            "range": "stddev: 0.07406574351703092",
            "extra": "mean: 91.3580151000076 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_erdos_renyi",
            "value": 53.532002729400006,
            "unit": "iter/sec",
            "range": "stddev: 0.0015789479511466831",
            "extra": "mean: 18.680414499993958 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_fast_erdos_renyi",
            "value": 36.15169854273344,
            "unit": "iter/sec",
            "range": "stddev: 0.0009863189194258429",
            "extra": "mean: 27.66121759999578 msec\nrounds: 10"
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
          "id": "b33de0d0c6be88476ee3534ccf2bb3e5830fce7d",
          "message": "Update references",
          "timestamp": "2025-04-18T10:07:45-04:00",
          "tree_id": "fc0e9e56e337ee94ed8abdbc1940d768d056cf4e",
          "url": "https://github.com/xgi-org/xgi/commit/b33de0d0c6be88476ee3534ccf2bb3e5830fce7d"
        },
        "date": 1744985318896,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/algorithms.py::test_connected",
            "value": 96.25130893361386,
            "unit": "iter/sec",
            "range": "stddev: 0.00013776310427291471",
            "extra": "mean: 10.389469099996518 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/algorithms.py::test_clustering_coefficient",
            "value": 61.279110618521564,
            "unit": "iter/sec",
            "range": "stddev: 0.00030243691730863395",
            "extra": "mean: 16.318774699999494 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgelist",
            "value": 28.729123799043034,
            "unit": "iter/sec",
            "range": "stddev: 0.040923281369003923",
            "extra": "mean: 34.807883700000275 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgedict",
            "value": 28.509569322471567,
            "unit": "iter/sec",
            "range": "stddev: 0.037623892372052825",
            "extra": "mean: 35.07594200000028 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_df",
            "value": 22.529404595983845,
            "unit": "iter/sec",
            "range": "stddev: 0.033936826801494145",
            "extra": "mean: 44.3864370999961 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_memberships",
            "value": 1245.1020797041006,
            "unit": "iter/sec",
            "range": "stddev: 0.000018864171623100928",
            "extra": "mean: 803.146999993487 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_members",
            "value": 135.6966110368953,
            "unit": "iter/sec",
            "range": "stddev: 0.0005821489553105779",
            "extra": "mean: 7.369380799997316 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_attributes",
            "value": 14408.370687568353,
            "unit": "iter/sec",
            "range": "stddev: 0.0000035047330719616415",
            "extra": "mean: 69.40409999742769 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_attributes",
            "value": 255.37562498402298,
            "unit": "iter/sec",
            "range": "stddev: 0.00024165135449149397",
            "extra": "mean: 3.9158004999990226 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_degree",
            "value": 10202.696980488927,
            "unit": "iter/sec",
            "range": "stddev: 0.000017886602139923325",
            "extra": "mean: 98.01330000414055 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_nodestats_degree",
            "value": 9868.482730831289,
            "unit": "iter/sec",
            "range": "stddev: 0.000004673885465697343",
            "extra": "mean: 101.33269999812455 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_size",
            "value": 257.3889813120077,
            "unit": "iter/sec",
            "range": "stddev: 0.00013216762734111914",
            "extra": "mean: 3.8851701999931265 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_isolates",
            "value": 8677.934096473102,
            "unit": "iter/sec",
            "range": "stddev: 0.000009266459158677336",
            "extra": "mean: 115.2347999976655 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_singletons",
            "value": 189.29044627663856,
            "unit": "iter/sec",
            "range": "stddev: 0.00015071038723017428",
            "extra": "mean: 5.2828867999949125 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_copy",
            "value": 11.924513982030529,
            "unit": "iter/sec",
            "range": "stddev: 0.0581304538830698",
            "extra": "mean: 83.86086019999937 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_dual",
            "value": 11.70344995643754,
            "unit": "iter/sec",
            "range": "stddev: 0.06870680606093005",
            "extra": "mean: 85.44489049999697 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_erdos_renyi",
            "value": 48.22361421077268,
            "unit": "iter/sec",
            "range": "stddev: 0.0012442964075409743",
            "extra": "mean: 20.736728600002152 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_fast_erdos_renyi",
            "value": 33.91430171361006,
            "unit": "iter/sec",
            "range": "stddev: 0.0016849633194511986",
            "extra": "mean: 29.486085499991077 msec\nrounds: 10"
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
          "id": "c3569948dafd7e39efae8347c1c0c2ded180c3cc",
          "message": "Integrate HIF with more of XGI (#613)\n\n* move hif functionality to convert\r\n\r\n* format with isort and black\r\n\r\n* add docs\r\n\r\n* add collection handling\r\n\r\n* add warning\r\n\r\n* add docstrings\r\n\r\n* added HIF to `load_xgi_data`\r\n\r\n* added more close to tests\r\n\r\n* Update xgi_data.py\r\n\r\n* Update xgi_data.py\r\n\r\n* remove other changes\r\n\r\n* added unit tests\r\n\r\n* Update xgi_data.py\r\n\r\n* Update HOW_TO_CONTRIBUTE.md\r\n\r\n* response to review\r\n\r\n* Response to review\r\n\r\n* Update docs.txt\r\n\r\n* Update release.txt",
          "timestamp": "2024-12-02T16:21:39-05:00",
          "tree_id": "c065879a4c02bc1d7016e06ea7d20c4d5d30b319",
          "url": "https://github.com/xgi-org/xgi/commit/c3569948dafd7e39efae8347c1c0c2ded180c3cc"
        },
        "date": 1733174876220,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/algorithms.py::test_connected",
            "value": 84.7107039666093,
            "unit": "iter/sec",
            "range": "stddev: 0.0021422348075570727",
            "extra": "mean: 11.804883600001403 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/algorithms.py::test_clustering_coefficient",
            "value": 51.96739623763352,
            "unit": "iter/sec",
            "range": "stddev: 0.0013726666389160267",
            "extra": "mean: 19.242834400000675 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgelist",
            "value": 19.47743817509476,
            "unit": "iter/sec",
            "range": "stddev: 0.05325011854793626",
            "extra": "mean: 51.34145420000209 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_edgedict",
            "value": 35.74876079780611,
            "unit": "iter/sec",
            "range": "stddev: 0.0004541957195242786",
            "extra": "mean: 27.97299759999987 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_construct_from_df",
            "value": 20.047008028654385,
            "unit": "iter/sec",
            "range": "stddev: 0.030763794125184214",
            "extra": "mean: 49.882755500004805 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_memberships",
            "value": 1257.2938760942845,
            "unit": "iter/sec",
            "range": "stddev: 0.00001555074951672886",
            "extra": "mean: 795.3590000028044 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_members",
            "value": 114.72968275561176,
            "unit": "iter/sec",
            "range": "stddev: 0.0007066067333557977",
            "extra": "mean: 8.71614020000493 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_node_attributes",
            "value": 13518.665219931454,
            "unit": "iter/sec",
            "range": "stddev: 0.00000148755524347939",
            "extra": "mean: 73.97180000623393 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_attributes",
            "value": 232.51027486117326,
            "unit": "iter/sec",
            "range": "stddev: 0.00007011409839004795",
            "extra": "mean: 4.300885200007087 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_degree",
            "value": 10817.710755929134,
            "unit": "iter/sec",
            "range": "stddev: 0.000005977132920896104",
            "extra": "mean: 92.44100000103117 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_nodestats_degree",
            "value": 9613.36026431445,
            "unit": "iter/sec",
            "range": "stddev: 0.00000638399057823358",
            "extra": "mean: 104.0218999918352 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_edge_size",
            "value": 224.04974119295818,
            "unit": "iter/sec",
            "range": "stddev: 0.000095546846281856",
            "extra": "mean: 4.463294600009249 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_isolates",
            "value": 7297.741276020338,
            "unit": "iter/sec",
            "range": "stddev: 0.000008298729047935285",
            "extra": "mean: 137.0287000014514 usec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_singletons",
            "value": 159.71538973094727,
            "unit": "iter/sec",
            "range": "stddev: 0.0007485163075350578",
            "extra": "mean: 6.261137399999939 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_copy",
            "value": 9.787473699883556,
            "unit": "iter/sec",
            "range": "stddev: 0.0687294509248274",
            "extra": "mean: 102.17141120000122 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/core.py::test_dual",
            "value": 9.785901023772807,
            "unit": "iter/sec",
            "range": "stddev: 0.07139927470695101",
            "extra": "mean: 102.18783099999769 msec\nrounds: 10"
          },
          {
            "name": "benchmarks/generators.py::test_erdos_renyi",
            "value": 30.272798510402954,
            "unit": "iter/sec",
            "range": "stddev: 0.0016330891622332012",
            "extra": "mean: 33.032955299998434 msec\nrounds: 10"
          }
        ]
      }
    ]
  }
}