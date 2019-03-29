"""
Rectangle class and related yaml handlers.

"""
import yaml


class Rect:
    def __init__(self, xmin_0=0, xmax_0=0, ymin_0=0, ymax_0=0):
        self._xmin = xmin_0
        self._xmax = xmax_0
        self._ymin = ymin_0
        self._ymax = ymax_0

    def __repr__(self):
        return "Rect(%s-%s, %s-%s)" % (self._xmin, self._xmax, self._ymin, self._ymax)

    @property
    def xmin(self):
        return self._xmin

    @property
    def xmax(self):
        return self._xmax

    @property
    def ymin(self):
        return self._ymin

    @property
    def ymax(self):
        return self._ymax

def rect_representer(dumper, coords):
    return dumper.represent_scalar(u"!Rect", u"x%s-%s y%s-%s" % (
        coords.xmin, coords.xmax, coords.ymin, coords.ymax
        ))


yaml.add_representer(Rect, rect_representer)


def rect_constructor(loader, node):
    value = loader.construct_scalar(node)
    x, y = value.split(" ")
    try:
        xmin, xmax = [int(v) for v in x[1:].split("-")]
        ymin, ymax = [int(v) for v in y[1:].split("-")]
    except ValueError:
        xmin, xmax = [float(v) for v in x[1:].split("-")]
        ymin, ymax = [float(v) for v in y[1:].split("-")]
    return Rect(xmin, xmax, ymin, ymax)


yaml.add_constructor(u"!Rect", rect_constructor)
