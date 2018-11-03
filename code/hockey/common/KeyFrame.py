"""
Keyframe enum and yaml handling.

"""
import enum
import yaml


@enum.unique
class KeyFrame(enum.Enum):
    NOT_KEYFRAME = "NOT_KEYFRAME"
    HIT_EXAMPLE = "HIT_EXAMPLE"
    NOT_HIT_EXAMPLE = "NOT_HIT_EXAMPLE"
    AMBIGUOUS_EXAMPLE = "AMBIGUOUS_EXAMPLE"


def __repr__(self):
    return "KeyFrame(%s)" % (self.value)


def keyframe_representer(dumper, kf):
    return dumper.represent_scalar(u"!KeyFrame", u"%s" % (kf.value))


yaml.add_representer(KeyFrame, keyframe_representer)


def keyframe_constructor(loader, node):
    kfstr = loader.construct_scalar(node)
    kf = KeyFrame.NOT_KEYFRAME
    if kfstr == "HIT_EXAMPLE":
        kf = KeyFrame.HIT_EXAMPLE
    elif kfstr == "NOT_HIT_EXAMPLE":
        kf = KeyFrame.NOT_HIT_EXAMPLE
    elif kfstr == "AMBIGUOUS_EXAMPLE":
        kf = KeyFrame.AMBIGUOUS_EXAMPLE
    else:
        raise ValueError("Unknown keyframe type: {:s}".format(kfstr))
    return kf


yaml.add_constructor(u"!KeyFrame", keyframe_constructor)
