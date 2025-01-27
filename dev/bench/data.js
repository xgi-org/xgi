window.BENCHMARK_DATA = {
  "lastUpdate": 1737996676280,
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