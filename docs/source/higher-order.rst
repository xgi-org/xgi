:orphan:

***********************************
What are higher-order interactions?
***********************************

Our world is highly interconnected, and examples of these connections include friends connecting on Facebook or meeting up for coffee; academic articles written by several authors; trains, busses, and planes traveling between cities; and even molecules held together by chemical bonds. Network science can describe each of these examples as a collection of *nodes* (The entities in the system, whether they be people, transit stations, or atoms) and *edges* (The connections between these entities, whether they be friendships, train routes connecting two cities, or a paper that co-authors wrote together). Traditional network science, however, assumes that only two of these entities may interact or associate at once, forming a *pairwise interaction*. The collection of these interactions is known as a *pairwise network*. This is often not the case in the physical world. Emails are often sent to more than one recipient, papers may be written by more than two authors, and friends may interaction not only one-to-one but in group settings as well. These group interactions are also known as *higher-order interactions*. For example, consider a group of friends. A higher-order network wouldn't just describe who is friends with whom individually, but also how sub-groups form and interact with one another. For example, the dynamics can change when three or more friends are together rather than just two.

A *higher-order network* is formed by the collection of these higher-order interactions. A higher-order interaction is represented most typically by a *hypergraph* or a *simplicial complex*. A hypergraph is a higher-order interaction network where each interaction is a set (a unique collection) listing the entities that participate in that interaction, also known as a *hyperedge*. A simplicial complex is a special type of hypergraph where, if an interaction occurs, it implies that every every possible sub-interaction also occurs. E.g., if authors 1, 2, and 3 wrote a paper together, then authors 1 and 2, 2 and 3, and 1 and 3 must have also co-authored a paper together (and 1, 2, 3 must all have sole-authored papers).

Why higher-order interactions?
==============================

Higher-order interactions can reveal more nuanced and sophisticated patterns of connection and can naturally encode different scales of interaction which are inaccessible to pairwise network representations. Higher-order networks can be helpful for describing social networks, ecological communities, co-authorship or citation networks, email, protein interactions, and many more examples. Higher-order networks can also exhibit rich dynamical behavior for simple models of contagion, synchronization, and opinion formation.


Academic References
===================

* `The Why, How, and When of Representations for Complex Systems
  <https://doi.org/10.1137/20M1355896>`_, Torres, L., Blevins, A.S., Bassett, D. and Eliassi-Rad, T., 2021. SIAM Review, 63(3), pp.435-485.

* `Networks beyond pairwise interactions: Structure and dynamics
  <https://doi.org/10.1016/j.physrep.2020.05.004>`_, Battiston, F., Cencetti, G., Iacopini, I., Latora, V., Lucas, M., Patania, A., Young, J.G. and Petri, G., 2020. Physics reports, 874, pp.1-92.

* `What are higher-order networks? <https://arxiv.org/abs/2104.11329>`_, Bick, C., Gross, E., Harrington, H.A. and Schaub, M.T., 2023. SIAM Review, 65(3), pp.686-731.

* `From networks to optimal higher-order models of complex systems
  <https://www.nature.com/articles/s41567-019-0459-y>`_, Lambiotte, R., Rosvall, M. and Scholtes, I., 2019. Nature physics, 15(4), pp.313-320.