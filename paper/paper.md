---
title: 'XGI: A Python package for higher-order interaction networks'
tags:
  - python
  - higher-order
  - hypergraph
  - simplicial complex
authors:
  - name: Nicholas W. Landry
    orcid: 0000-0003-1270-4980
    affiliation: "1, 2"
    email: nicholas.landry@uvm.edu
    corresponding: true
  - name: Maxime Lucas
    orcid: 0000-0001-8087-2981
    affiliation: 3
  - name: Iacopo Iacopini
    orcid: 0000-0001-8794-6410
    affiliation: 4
  - name: Giovanni Petri
    orcid: 0000-0003-1847-5031
    affiliation: 3
  - name: Alice Schwarze
    orcid: 0000-0002-9146-8068
    affiliation: 5
  - name: Alice Patania
    orcid: 0000-0002-3047-4376
    affiliation: "1, 2"
  - name: Leo Torres
    orcid: 0000-0002-2675-2775
    affiliation: 6
affiliations:
 - name: Vermont Complex Systems Center, University of Vermont, USA
   index: 1
 - name: Department of Mathematics and Statistics, University of Vermont, USA
   index: 2
 - name: CENTAI Institute, Italy
   index: 3
 - name: Department of Network and Data Science, Central European University, Austria
   index: 4
 - name: Department of Mathematics, Dartmouth College, USA
   index: 5
 - name: Max Planck Institute for Mathematics in the Sciences, Germany
   index: 6

date: 08 February 2023
bibliography: references.bib

---

# Summary
Comple**X** **G**roup **I**nteractions (XGI) is a library for higher-order networks, which model interactions of arbitrary size between entities in a complex system. This library provides methods for building hypergraphs and simplicial complexes; algorithms to analyze their structure, visualize them, and simulate dynamical processes on them; and a collection of higher-order datasets. XGI is implemented in pure Python and integrates with the rest of the Python scientific stack. XGI is designed and developed by network scientists with the needs of network scientists in mind.

# Statement of need
The field of network science bridges across many different disciplines, bringing together theorists, computational scientists, social scientists, and many others. To facilitate cross-disciplinary collaboration, a common tool kit is crucial. Existing packages like NetworkX [@hagberg_exploring_2008], graph-tool [@peixoto_graph-tool_2014], and igraph [@igraph] have been successful in facilitating collaboration for traditional networks, restricted to pairwise interactions. However, the rapidly growing subfield of higher-order network science [@battiston_networks_2020], which models interactions between any number of entities, requires a different approach. 
Higher-order interaction networks promotes rich dynamical behavior [@iacopini_simplicial_2019;@skardal_abrupt_2019;@neuhauser_multibody_2020;@hickok_bounded-confidence_2022], and can model some empirical interaction patterns more accurately than pairwise networks [@chodrow_configuration_2020]. We anticipate that this field will have lasting impacts on various research areas such as infectious diseases, dynamical systems, and behavioral science. To support the higher-order network science community, we have developed the Comple**X** **G**roup **I**nteractions (XGI)---an open-source solution in Python.


# Related Software
There are several existing packages to represent and analyze higher-order networks: `HyperNetX` [@doecode_22160] and `Reticula` [@badie-modiri_reticula_2023] in Python, `SimpleHypergraphs.jl` [@spagnuolo_analyzing_2020]  and `HyperGraphs.jl` [@diaz_hypergraphsjl_2022] in Julia, and `hyperG` in R. XGI is a valuable addition to the network science practitioner’s toolbox for several reasons. First, XGI is implemented in pure Python, ensuring interoperability and easy installation across operating systems. Second, like several of the packages listed, XGI has a well-documented codebase and tutorials designed to make the learning process intuitive. Third, in contrast to existing packages, XGI contains a `stats` module enabling researchers to easily access established nodal and edge quantities, and even define custom quantities. Fourth, XGI offers data structures for hypergraphs and simplicial complexes, which allows users to explore a wider range of interaction models than comparable packages. Lastly, XGI integrates higher-order datasets with its interface, providing a standard format in which to store hypergraphs with attributes and a data repository with corresponding functions to load these datasets.

# Overview

The two core classes of the library are those representing hypergraphs and simplicial complexes. The data structure (seen in \autoref{fig:diagram}) employed by XGI for both is a bipartite graph with entities represented by one node type and relationships among entities (i.e., hyperedges or simplices) represented by a second node type.

![A hypergraph is internally represented as a bipartite network stored as two dictionaries, where keys are node IDs and sets specify the edges to which they belong, and vice-versa. Unique identifiers allow for multi-edges, as can be seen for edge IDs 1 and 2. \label{fig:diagram}](Figures/fig1.pdf)

XGI provides several ways to create hypergraphs and simplicial complexes. First, by adding or removing nodes or hyperedges (or simplices). Second, by creating generative models, which can produce datasets with desired structural characteristics. Third, by loading existing datasets. XGI allows easy and unified access to many hypergraph datasets currently existing in diverse formats [@benson_data_2021;@peixoto_netzschleuder_2021;@clauset_colorado_2016] in three ways: first, by implementing a standard for hypergraph data in JSON format; second, by storing datasets in this format in a single repository, XGI-DATA [@landry_xgi-data_2023]; and third, by providing file I/O for common formats. Each dataset in XGI-DATA can be easily accessed through the library's API and the repository provides a description of it.

XGI provides many standard and state-of-the-art measures such as assortativity, centralities, connectedness, and clustering. A strength of XGI is its `stats` package: it provides a convenient and unified interface for computing statistics of nodes and edges, such as degree centrality or edge order. Any measure that is a node/edge-to-quantity mapping uses the same interface. Stats can be used to filter nodes and edges and multiple stats filters can be combined.
XGI provides convenient visualization functions, as illustrated in \autoref{fig:viz}. We support multiple layouts and allow users to control many of the drawing parameters. Finally, XGI provides functions to simulate synchronization models on hypergraphs and simplicial complexes [@adhikari_synchronization_2022;@lucas_multiorder_2020;@millan_explosive_2020;@arnaudon_connecting_2022].

![A visualization of the email-enron dataset [@landry_xgi-data_2023;@benson_data_2021] with hyperedges of sizes 2 and 3 (all isolated nodes removed). The nodes are colored by their degree and their size proportional to the Clique motif Eigenvector Centrality [@benson_three_2019]. \label{fig:viz}](Figures/fig2.pdf)

# Projects using XGI
XGI has proved to be an invaluable resource for research projects [@zhang_higher-order_2022] on higher-order networks as well as other software projects [@landry_hypercontagion_2022]. We expect that as this library matures, it will become a more essential part of the higher-order network science community.

# Funding
N.W.L. acknowledges support from the National Science Foundation Grant 2121905, "HNDS-I: Using Hypergraphs to Study Spreading Processes in Complex Social Networks", and from the National Institutes of Health 1P20 GM125498-01 Centers of Biomedical Research Excellence Award. I.I. acknowledges support from the James S. McDonnell Foundation $21^{\text{st}}$ Century Science Initiative Understanding Dynamic and Multi-scale Systems - Postdoctoral Fellowship Award.

# Acknowledgements
We acknowledge contributions from Martina Contisciani, Tim LaRock, Marco Nurisso, Alexis Arnaudon, and Sabina Adhikari.

# References

