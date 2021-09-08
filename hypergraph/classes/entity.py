from hypergraph.utils.utilities import HypergraphCounter
from exception import HypergraphError
from collections import defaultdict

__all__ = ["Entity", "EntitySet"]


class Entity():
    def __init__(self, uid, elements={}, entity=None, **props):
        self._uid = uid

        if entity is not None:
            if isinstance(entity, Entity):
                if uid == entity.uid:
                    HypergraphError("The new entity will be indistinguishable from the original with the same uid. Use a different uid.")
                self._elements = entity.elements
                self.__dict__.update(entity.properties)
        else:
            try:
                self._elements = set(elements)
            except:
                HypergraphError("elements cannot be cast to a set")

        self.__dict__.update(props)

    @property
    def properties(self):
        """Dictionary of properties of entity"""
        temp = self.__dict__.copy()
        del temp["_elements"]
        del temp["_uid"]
        return temp

    @property
    def uid(self):
        """String identifier for entity"""
        return self._uid

    @property
    def elements(self):
        """
        Dictionary of elements belonging to entity.
        """
        return self._elements

    @property
    def is_empty(self):
        """Boolean indicating if entity.elements is empty"""
        return len(self) == 0

    def __len__(self):
        """Returns the number of elements in entity"""
        return len(self._elements)

    def __str__(self):
        """Return the entity uid."""
        return f"{self.uid}"

    def __repr__(self):
        """Returns a string resembling the constructor for entity without any
        children"""
        return f"Entity({self._uid},{list(self._elements)},{self.properties})"

    def __contains__(self, item):
        """
        Defines containment for Entities.
        Parameters
        ----------
        item : hashable or Entity
        Returns
        -------
        Boolean
        Depends on the `Honor System`_ . Allows for uids to be used as shorthand for their entity.
        This is done for performance reasons, but will fail if uids are
        not unique to their entities.
        Is not transitive.
        """
        if isinstance(item, Entity):
            return item.uid in self._elements
        else:
            return item in self._elements

    def __getitem__(self, item):
        """
        Returns Entity element by uid. Use :func:`E[uid]`.
        Parameters
        ----------
        item : hashable or Entity
        Returns
        -------
        Entity or None
        If item not in entity, returns None.
        """
        if isinstance(item, Entity):
            return self._elements.get(item.uid, "")
        else:
            return self._elements.get(item, "")

    def __iter__(self):
        """Returns iterator on element ids."""
        return iter(self._elements)

    def __call__(self):
        """Returns an iterator on element ids"""
        for e in self._elements:
            yield e

    def __setattr__(self, k, v):
        """Sets entity property.
        Parameters
        ----------
        k : hashable, property key
        v : hashable, property value
            Will not set uid or change elements or memberships.
        Returns
        -------
        None
        """
        if k == "uid":
            HypergraphError(
                "Cannot reassign uid to Entity once it"
                " has been created. Create a clone instead."
            )
        elif k == "elements":
            HypergraphError("To add elements to Entity use self.add().")
        else:
            self.__dict__[k] = v
 
    def size(self):
        """
        Returns the number of elements in entity
        """
        return len(self)

    def clone(self, newuid):
        """
        Returns shallow copy of entity with newuid. Entity's elements will
        belong to two distinct Entities.
        Parameters
        ----------
        newuid : hashable
            Name of the new entity
        Returns
        -------
        clone : Entity
        """
        return Entity(newuid, entity=self)

    def add_element(self, item):
        if isinstance(item, Entity):
            # if item is an Entity, descendents will be compared to avoid collisions
            self._elements.add(item.uid)
        else:
            self._elements.add(item)

        return self

    def remove_element(self, item):
        """
        Removes item from entity and reference to entity from
        item.memberships
        Parameters
        ----------
        item : Hashable or Entity
        Returns
        -------
        self : Entity
        """
        if isinstance(item, Entity):
            self._elements.discard(item.uid)
        else:
            self._elements.discard(item)

        return self


class EntitySet():
    def __init__(self, elements=dict(), entityset=None, uid=""):

        if entityset is not None:
            self._elements = entityset.elements
            self._uid = entityset.uid
        else:
            self._count = HypergraphCounter()
            self._elements = dict()
            self._uid = uid
            self.add_elements_from(elements)

    def __len__(self):
        """Returns the number of elements in entity"""
        return len(self._elements)

    def __str__(self):
        """Return the entity uid."""
        return f"{self.uid}"

    def __repr__(self):
        """Returns a string resembling the constructor for entity without any
        children"""
        return f"Entity({self._uid},{list(self.uidset)})"

    def __contains__(self, item):
        """
        Defines containment for Entities.
        Parameters
        ----------
        item : hashable or Entity
        Returns
        -------
        Boolean
        Depends on the `Honor System`_ . Allows for uids to be used as shorthand for their entity.
        This is done for performance reasons, but will fail if uids are
        not unique to their entities.
        Is not transitive.
        """
        if isinstance(item, Entity):
            return item.uid in self._elements
        else:
            return item in self._elements

    def __getitem__(self, item):
        """
        Returns Entity element by uid. Use :func:`E[uid]`.
        Parameters
        ----------
        item : hashable or Entity
        Returns
        -------
        Entity or None
        If item not in entity, returns None.
        """
        if isinstance(item, Entity):
            return self._elements.get(item.uid)
        else:
            return self._elements.get(item)

    def __iter__(self):
        """Returns iterator on element ids."""
        return iter(self.elements)

    def __call__(self):
        """Returns an iterator on elements"""
        for e in self.elements.values():
            yield e

    @property
    def uidset(self):
        """
        Set of uids of elements of entity.
        """
        return frozenset(self._elements.keys())

    @property
    def elements(self):
        return self._elements

    @property
    def children(self):
        children = set()
        for uid in self.uidset:
            children.union(self._elements[uid])
        return list(children)

    def dual(self):
        incidence_dict = defaultdict(set)
        for uid in self.uidset:
            for child_uid in self._elements[uid]:
                incidence_dict[child_uid].add(uid)
        return EntitySet(incidence_dict)

    
    def add(self, *args):
        """
        Adds unpacked args to entity elements. Depends on add_element()
        Parameters
        ----------
        args : One or more entities or hashables
        Returns
        -------
        self : Entity
        Note
        ----
        Adding an element to an object in a hypergraph will not add the
        element to the hypergraph and will cause an error. Use :func:`Hypergraph.add_edge <classes.hypergraph.Hypergraph.add_edge>`
        or :func:`Hypergraph.add_node_to_edge <classes.hypergraph.Hypergraph.add_node_to_edge>` instead.
        """
        self.add_elements_from(*args)

    def add_elements_from(self, item_set):
        """
        Similar to :func:`add()` it allows for adding from an interable.
        Parameters
        ----------
        arg_set : Iterable of hashables or entities
        Returns
        -------
        self : Entity
        """
        if isinstance(item_set, list):
            for item in item_set:
                self.add_element(item)
        if isinstance(item_set, dict):
            for uid, item in item_set.items():
                self.add_element(item, uid)

    def add_element(self, item, uid=None):
        if isinstance(item, Entity):
            if item in self:
                # item is already an element so only the properties will be updated
                self._elements[item.uid].__dict__.update(item.properties)
            else:
                # if item's uid doesn't appear in complete_registry
                # then it is added as something new
                self._elements[item.uid] = item
        else:
            if uid is None:
                uid = self._count()
            if uid not in self._elements:
                self._elements[uid] = Entity(uid, elements=item)

    def remove(self, *args):
        """
        Removes args from entitie's elements if they belong.
        Does nothing with args not in entity.
        Parameters
        ----------
        args : One or more hashables or entities
        Returns
        -------
        self : Entity
        """
        for item in args:
            self.remove_element(item)

    def remove_elements_from(self, item_set):
        """
        Similar to :func:`remove()`. Removes elements in arg_set.
        Parameters
        ----------
        arg_set : Iterable of hashables or entities
        Returns
        -------
        self : Entity
        """
        for item in item_set:
            self.remove_element(item)

    def remove_element(self, item):
        """
        Removes item from entity and reference to entity from
        item.memberships
        Parameters
        ----------
        item : Hashable or Entity
        Returns
        -------
        self : Entity
        """
        if isinstance(item, Entity):
            del self._elements[item.uid]
        else:
            del self._elements[item]

    def clone(self, newuid):
        """
        Returns shallow copy of entityset with newuid. Entityset's
        elements will belong to two distinct entitysets.
        Parameters
        ----------
        newuid : hashable
            Name of the new entityset
        Returns
        -------
        clone : EntitySet
        """
        return EntitySet(elements=self.elements, uid=newuid)


    def collapse_identical_elements(self, newuid, return_equivalence_classes=False):
        """
        Returns a deduped copy of the entityset, using representatives of equivalence classes as element keys.
        Two elements of an EntitySet are collapsed if they share the same children.
        Parameters
        ----------
        newuid : hashable
        return_equivalence_classes : boolean, default=False
            If True, return a dictionary of equivalence classes keyed by new edge names
        Returns
        -------
         : EntitySet
        eq_classes : dict
            if return_equivalence_classes = True
        Notes
        -----
        Treats elements of the entityset as equal if they have the same uidsets. Using this
        as an equivalence relation, the entityset's uidset is partitioned into equivalence classes.
        The equivalent elements are identified using a single entity by using the
        frozenset of uids associated to these elements as the uid for the new element
        and dropping the properties.
        If use_reps is set to True a representative element of the equivalence class is
        used as identifier instead of the frozenset.
        Example: ::
            >>> E = EntitySet('E',elements=[Entity('E1', ['a','b']),Entity('E2',['a','b'])])
            >>> E.incidence_dict
            {'E1': {'a', 'b'}, 'E2': {'a', 'b'}}
            >>> E.collapse_identical_elements('_',).incidence_dict
            {'E2': {'a', 'b'}}
        """

        shared_children = defaultdict(set)
        for e in self.__call__():
            shared_children[frozenset(e.uidset)].add(e.uid)
        new_entity_dict = {
            f"{next(iter(v))}:{len(v)}": set(k) for k, v in shared_children.items()
        }
        if return_equivalence_classes:
            eq_classes = {
                f"{next(iter(v))}:{len(v)}": v for k, v in shared_children.items()
            }
            return EntitySet(newuid, new_entity_dict), dict(eq_classes)
        else:
            return EntitySet(newuid, new_entity_dict)