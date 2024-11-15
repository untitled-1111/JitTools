from typing import Dict, Any, Callable, Optional, Set


def recursive_eq(a, b, type_checkers: Dict[Any, Callable[[Any, Any], Optional[bool]]] = None, visited=None,
                 exclude: Optional[Set[str]] = None):
    """
    Recursively compare two 'things', which could be objects, lists, etc.

    This comparison can be heavily customised via the arguments, and can safely handle
    loops in the object graph (if two objects refer to each other, it won't overflow
    the stack).

    This function, since it's designed to be used in comparing objects, raises an exception
    if there's a difference between the two objects.

    :param a: The first object to compare.
    :param b: The second object to compare.
    :param type_checkers: A mapping of types to comparison functions, used to set custom logic for comparing types. The
    function should return true or false to indicate a match or difference respectively, or None to fall through
    to the standard comparison logic.
    :param visited: A set of the things visited so far, on the 'a' side of the tree. This will be written into.
    :param exclude: A set of names to skip. This only does anything if we're comparing objects, and this only applies
    to the immediate objects - this won't be carried through recursion.
    """

    # Nones are always the same
    if a is None and b is None:
        return

    # Make sure both objects are of the same type, otherwise none of the later comparisons are necessarily fair
    assert type(a) == type(b)

    # Make sure we don't get stuck in infinite recursion, and note we use object identity rather than equals
    if visited is None:
        visited = set()
    if id(a) in visited:
        return
    visited.add(id(a))

    # If the user has set a custom comparison for this type, use that
    if type_checkers and type(a) in type_checkers:
        res = type_checkers[type(a)](a, b)
        if res is not None:
            assert res
            return

    # Special handling for lists
    if type(a) == list:
        for aa, bb in zip(a, b):
            recursive_eq(aa, bb, type_checkers=type_checkers, visited=visited)

        return

    # If the type has a custom equals method, use that to compare them
    if type(a).__eq__ != object.__eq__:
        if a != b:
            print(a)
            print(b)
            raise Exception("Mismatch")
        return

    # At this point we're going to do an object comparison. Make sure the keys are the
    # same, then compare each value and check they match too.

    assert a.__dict__.keys() == b.__dict__.keys()

    exclusions = {"_addr"}
    if exclude:
        exclusions.update(exclude)

    for name in a.__dict__.keys():
        if name in exclusions:
            continue

        va = a.__dict__[name]
        vb = b.__dict__[name]

        recursive_eq(va, vb, type_checkers=type_checkers, visited=visited)
