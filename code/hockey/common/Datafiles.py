"""
General information for all sessions.

"""
_basedir = "/Users/lemonad/Pictures/Hockey/Shots/"
_files = {
    "20180901": {
        "training": [
            "IMG_0388",  # Blurry
            "IMG_0389",  # Blurry
            "IMG_0391",  # Blurry
            "IMG_0393",  # Blurry
        ],
        "testing": ["IMG_0392"],  # Blurry
    },
    "20180903": {
        "training": [
            "IMG_0420",  # Blurry
            "IMG_0421",  # Blurry
            "IMG_0422",  # Blurry
            "IMG_0423",  # Blurry
            "IMG_0424",  # Blurry
            "IMG_0426",  # Blurry
            "IMG_0427",
        ],
        "testing": ["IMG_0425"],
    },
    "20180908": {
        "training": [
            "IMG_0452",
            "IMG_0453",
            "IMG_0455",
            "IMG_0456",
            "IMG_0457",
            "IMG_0458",
            "IMG_0459",
            "IMG_0460",
            "IMG_0461",
        ],
        "testing": ["IMG_0454"],
    },
    "20180909": {
        "training": [
            "IMG_0462",
            "IMG_0463",
            "IMG_0465",
            "IMG_0466",
            "IMG_0467",
            "IMG_0468",
            "IMG_0469",
        ],
        "testing": ["IMG_0464"],
    },
    "20180913": {
        "training": [
            "IMG_0513",
            "IMG_0514",
            "IMG_0515",
            "IMG_0518",
            "IMG_0519",
            "IMG_0520",
            "IMG_0521",
            "IMG_0522",
            "IMG_0523",
        ],
        "testing": ["IMG_0517"],
    },
    "20180916": {
        "training": [
            "IMG_0550",
            "IMG_0551",
            "IMG_0552",
            "IMG_0553",
            "IMG_0554",
            "IMG_0557",
            "IMG_0558",
            "IMG_0559",
        ],
        "testing": ["IMG_0555"],
    },
    "20180917 skymning": {
        "prefix": "20180917",
        "training": ["IMG_0565", "IMG_0566", "IMG_0570"],
        "testing": ["IMG_0568_60fps"],
    },
    "20181001": {
        "training": [
            "IMG_0074",
            "IMG_0075",
            "IMG_0076",
            "IMG_0077",
            "IMG_0078",
            "IMG_0081",
            "IMG_0082",
            "IMG_0083",
            "IMG_0084",
            "IMG_0085",
            "IMG_0086",
            "IMG_0087",
            "IMG_0088",
            "IMG_0089",
            "IMG_0091",
            "IMG_0092",
        ],
        "testing": ["IMG_0090"],
    },
    "20181014": {
        "training": [
            "IMG_0234",
            "IMG_0235",
            "IMG_0236",
            "IMG_0237",
            "IMG_0238",
            "IMG_0239",
            "IMG_0240",
            "IMG_0241",
            "IMG_0242",
            "IMG_0243",
            "IMG_0245",
        ],
        "testing": ["IMG_0244"],
    },
    "20181024 Kent": {
        "prefix": "20181024",
        "training": [
            "IMG_0346",
            "IMG_0347",
            "IMG_0348",
            "IMG_0349",
            "IMG_0350",
            "IMG_0351",
        ],
        "testing": ["IMG_0345"],
    },
}


def get_session_names():
    return list(_files.keys())


def get_all_paths_no_ext(training=False, testing=False, session_name=None):
    paths = []
    for sname, data in _files.items():
        if session_name is not None and session_name is not sname:
            continue

        if training:
            for name in data["training"]:
                name = "{:s}{:s}/{:s}".format(_basedir, sname, name)
                paths.append(name)
        if testing:
            for name in data["testing"]:
                name = "{:s}{:s}/{:s}".format(_basedir, sname, name)
                paths.append(name)
    return paths


def get_paths(extension, session_name, training=False, testing=False):
    paths_no_ext = get_all_paths_no_ext(training, testing, session_name)
    paths = []
    for p in paths_no_ext:
        paths.append(p + "." + extension)
    return paths


def get_all_paths(extension, training=False, testing=False):
    return get_paths(extension, None, training, testing)


def get_prefix_for_session(session_name):
    if "prefix" not in _files[session_name]:
        return session_name
    return _files[session_name]["prefix"]


def get_round_names_for_session(session_name, training=False, testing=False):
    round_names = []
    if training:
        round_names.extend(_files[session_name]["training"])
    if testing:
        round_names.extend(_files[session_name]["testing"])
    return round_names
