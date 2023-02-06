---
title: 'XGI: A Python package for research on higher-order interactions'
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

date: 03/12/2023
bibliography: references.bib

---

# Summary
The Comple**X** **G**roup **I**nteractions (XGI) library provides data structures and algorithms for modeling, analyzing, and visualizing complex networks with group (i.e., higher-order) interactions. It includes both hypergraphs and simplicial complexes. XGI provides multiple methods to build them, standard and advanced algorithms to analyze their structure, flexible visualization functions. and simulation capabilities for dynamical processes. The library is accompanied by a collection of datasets including group interactions. XGI is implemented in pure Python and interoperates with the rest of the Python scientific stack (Numpy, Scipy, Pandas, Matplotlib, NetworkX). XGI is designed and developed by network scientists with the needs of network scientists in mind.

# Statement of need
The field of network science bridges across many different disciplines, bringing together theorists, computational scientists, social scientists, and many others. To facilitate cross-disciplinary collaboration, a common tool kit is crucial. Existing packages like NetworkX [@hagberg_exploring_2008], graph-tool [@peixoto_graph-tool_2014], and igraph [@igraph] have been successful in facilitating collaboration for traditional networks, restricted to pairwise interactions. However, the rapidly growing subfield of higher-order network science, that goes beyond pairwise to model group interactions of any number of units, requires a different approach. 
Higher-order interaction networks promotes rich dynamical behavior [@iacopini_simplicial_2019;@skardal_abrupt_2019;@neuhauser_multibody_2020;@hickok_bounded-confidence_2022], and can model some empirical interaction patterns more accurately than pairwise networks [@chodrow_configuration_2020]. We anticipate that this field will have lasting impacts on various research areas such as infectious diseases, dynamical systems, and behavioral science. To support the higher-order network science community, we have developed the Comple**X** **G**roup **I**nteractions (XGI)---an open-source solution in Python.


# Related Software
There are several existing packages to represent and analyze higher-order networks: `HyperNetX` [@doecode_22160] and `Reticula` [@badie-modiri_reticula_2023] in Python, `SimpleHypergraphs.jl` [@spagnuolo_analyzing_2020]  and `HyperGraphs.jl` [@diaz_hypergraphsjl_2022] in Julia, and `hyperG` in R. XGI is a valuable addition to the network science practitioner’s toolbox for several reasons. First, XGI is implemented in pure Python, ensuring interoperability and easy installation across operating systems. Second, like several of the packages listed, XGI has a well-documented codebase and tutorials designed to make the learning process intuitive. Third, in contrast to existing packages, XGI contains a `stats` module enabling researchers to easily access established nodal and edge quantities, and even define custom quantities. Fourth, XGI offers data structures for hypergraphs and simplicial complexes, which allows users to explore a wider range of interaction models than comparable packages. Lastly, XGI integrates higher-order datasets with its interface, providing a standard format in which to store hypergraphs with attributes and a data repository with corresponding functions to load these datasets.

# Overview of the API
We provide an overview of the functionality of the XGI library.

## Core architecture: hypergraphs and simplicial complexes
The two core classes of the library are those representing hypergraphs and simplicial complexes. The data structure (seen in \autoref{fig:diagram}) employed by XGI for those two is a bipartite graph with entities represented by one node type and relationships among entities (i.e., hyperedges or simplices) represented by a second node type. 

![Illustration of the underlying data structure. The hypergraph is internally represented as a bipartite network stored as two dictionaries, where keys are the node or edge IDs and the values are sets specifying which edges (or nodes) that node (edge) is connected to. Unique identifiers allow for multi-edges, as can be seen for edge IDs 1 and 2. \label{fig:diagram}](Figures/fig1.pdf)



XGI provides several ways to create and manipulate hypergraphs and simplicial complexes. First, by adding or removing nodes or hyperedges (or simplices). Second, by converting between multiple formats for representing hypergraphs. For example, in contagion models, it is important to efficiently access nodal neighbors whereas when computing averages over hyperedges (e.g., assortativity or modularity) it may be better to represent a hypergraph by a list of hyperedges. Third, by using generative models, which are useful as null models to create datasets with characteristics to empirical ones.

### File I/O
Although there are many excellent collections of hypergraph datasets [@benson_data_2021;@peixoto_netzschleuder_2021;@clauset_colorado_2016], the format of each dataset and the information about how and why it was collected varies widely. With larger datasets becoming more widely available, it is important to close the gap between dataset creators and consumers [@gebru_datasheets_2021,bagrow_network_2022]. XGI does this in two ways: first, by implementing methods for importing and writing hypergraphs from several common formats and second, by implementing a standard for hypergraph data in JSON format. The XGI-DATA repository [@landry_xgi-data_2023] is a collection of openly available hypergraph datasets in this standard JSON format with documentation that describes each one extensively.

## Analyzing
For hypergraphs and simplicial complexes, XGI offers methods for easily getting common basic outputs, including the number of nodes or hyperedges, the nodes that are members of a particular edge, and, conversely, the edges to which a node belongs to, subsets of hypergraphs, attributes of nodes or hyperedges. Below, we detail the stats subpackage, as well as more complex measures and dynamic simulations available in XGI.

### Stats
The `stats` package provides a way to compute statistics of nodes and edges, such as degree centrality or edge order. The main benefit of the `stats` package is that any measure that can be conceived of as a node-to-quantity mapping has the same interface.  [MENTION MULTIPLE STATS? ADD CODE?]

### Algorithms
XGI has implemented important measures of assortativity, centrality, connectedness, and clustering, and it will continue to incorporate more higher-order metrics in the future.

### Dynamics
Currently, XGI provides functions to simulate two types of synchronization models on hypergraphs: one where oscillators are placed only on the nodes of the hypergraphs [@adhikari_synchronization_2022;@lucas_multiorder_2020], and one where oscillators can also be placed on simplices [@millan_explosive_2020;@arnaudon_connecting_2022]. In the future, the library could be extended to other landmark dynamical processes on higher-order networks such as spreading, diffusion, and socio-physics models.

## Visualizing
The `draw()` function in XGI allows the user to visualize both hypergraphs and simplicial complexes. \autoref{fig:viz} illustrates an example of a hypergraph visualization. XGI currently supports multiple layouts and allows users to control many of the drawing parameters. [MENTION NODESTATS IF WE CAN] An example is shown in \autoref{fig:viz} where nodes are colored and sized by the degree and centrality respectively.

![A visualization of the email-enron dataset [@landry_xgi-data_2023;@benson_data_2021] with hyperedges of sizes 2 and 3 (all isolated nodes removed). The nodes are colored by their degree and their size proportional to the Clique motif Eigenvector Centrality [@benson_three_2019]. \label{fig:viz}](Figures/fig_2.pdf)

# Projects using XGI
One of the goals of XGI was to provide a common language and framework on top of which many projects could be built. Even in its nascence, XGI has proved to be an invaluable resource for research projects [@zhang_higher-order_2022] on higher-order networks as well as other software projects [@landry_hypercontagion_2022]. We expect that as this library matures, it will become a more essential part of the higher-order network science community.

# Funding
N.W.L. acknowledges support from the National Science Foundation Grant 2121905, "HNDS-I: Using Hypergraphs to Study Spreading Processes in Complex Social Networks", and from the National Institutes of Health 1P20 GM125498-01 Centers of Biomedical Research Excellence Award. I.I. acknowledges support from the James S. McDonnell Foundation $21^{\text{st}}$ Century Science Initiative Understanding Dynamic and Multi-scale Systems - Postdoctoral Fellowship Award.

# Acknowledgements
We acknowledge contributions from Martina Contisciani, Tim LaRock, Marco Nurisso, Alexis Arnaudon, and Sabina Adhikari.

# References

