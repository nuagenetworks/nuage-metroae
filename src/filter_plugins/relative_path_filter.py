import os


METROAE_ROOT = "/metroae/"
print("INSIDE FILTER")


def relative_path_to_absolute_path(string):
    print("INSIDE FUNCTION")
    if not os.path.isabs(string):
        string = METROAE_ROOT + string.lstrip("./")
        print("INSIDE CONDITION")
    return string


class FilterModule(object):
    ''' Query filter '''

    def filters(self):
        return {'relative_path_to_absolute_path': relative_path_to_absolute_path}
