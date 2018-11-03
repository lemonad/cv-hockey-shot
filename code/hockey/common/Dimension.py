"""
Dimension class and related yaml handlers.

"""
import yaml


class Dimension:
    def __init__(self, width, height):
        self._width = width
        self._height = height

    def __repr__(self):
        return "Dimension(%s, %s)" % (self._width, self._height)

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def as_tuple(self):
        return (self._width, self._height)


def dimension_representer(dumper, size):
    return dumper.represent_scalar(
        u"!Dimension", u"w%s h%s" % (size.width, size.height)
    )


yaml.add_representer(Dimension, dimension_representer)


def dimension_constructor(loader, node):
    value = loader.construct_scalar(node)
    # "w10 h20" => (10, 20).
    w, h = (int(d[1:]) for d in value.split(" "))
    return Dimension(w, h)


yaml.add_constructor(u"!Dimension", dimension_constructor)
