#  read_json.py
#  Aug 18 (PJW)

import json
from model import Model


def read_json(filename):
    """Read an OpenIGEM model description stored as a JSON file.
   
    Args:
        filename (str): Name of file to read.

    Returns:
        Model: a new OpenIGEM Model object.
    """

    fh = open(filename, 'r')
    obj = json.load(fh)

    mod = Model(obj['name'])
    for v in obj['sets']:
        mod.newset(v['name'], v['elements'])
    for v in obj['pars']:
        mod.newvar(v['name'], v['sets'], v['header'], par=True)
    for v in obj['vars']:
        mod.newvar(v['name'], v['sets'], v['header'])

    return mod
