import xgi


def test_dual_dict(dict5):
    dual = xgi.dual_dict(dict5)
    assert dual[0] == [0]
    assert dual[1] == [0]
    assert dual[2] == [0]
    assert dual[3] == [0]
    assert dual[4] == [1]
    assert dual[5] == [2]
    assert dual[6] == [2, 3]
    assert dual[7] == [3]
    assert dual[8] == [3]


def test_powerset():

    edge = [1, 2, 3, 4]

    PS = xgi.powerset(edge)
    PS1 = xgi.powerset(edge, include_empty=True)
    PS2 = xgi.powerset(edge, include_empty=True, include_full=True)

    out = [
        (1,),
        (2,),
        (3,),
        (4,),
        (1, 2),
        (1, 3),
        (1, 4),
        (2, 3),
        (2, 4),
        (3, 4),
        (1, 2, 3),
        (1, 2, 4),
        (1, 3, 4),
        (2, 3, 4),
    ]

    assert list(PS) == out
    assert list(PS1) == [()] + out
    assert list(PS2) == [()] + out + [tuple(edge)]
