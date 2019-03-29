"""
Point class and related yaml handlers.

"""
import yaml


class Point:
    def __init__(self, x_0=0, y_0=0):
        self._x = x_0
        self._y = y_0

    @classmethod
    def fromlist(cls, coords):
        assert len(coords) == 2
        return cls(coords[0], coords[1])

    def __repr__(self):
        return "Point(%s, %s)" % (self._x, self._y)

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def as_tuple(self):
        return (self._x, self._y)


def point_representer(dumper, coords):
    return dumper.represent_scalar(u"!Point", u"x%s y%s" % (coords.x, coords.y))


yaml.add_representer(Point, point_representer)


def point_constructor(loader, node):
    value = loader.construct_scalar(node)
    # "x10 y20" => (10, 20).
    try:
        x, y = (int(p[1:]) for p in value.split(" "))
    except ValueError:
        x, y = (float(p[1:]) for p in value.split(" "))
    return Point(x, y)


yaml.add_constructor(u"!Point", point_constructor)
