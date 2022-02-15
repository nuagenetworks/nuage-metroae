import os

METROAE_ROOT = "/metroae/"

def relative_path_to_absolute_path(string):
    if not os.path.isabs(string):
        string = METROAE_ROOT + string.lstrip("./")
    return string

class FilterModule(object):
    ''' Query filter '''

    def filters(self):
        return {'relative_path_to_absolute_path': relative_path_to_absolute_path}