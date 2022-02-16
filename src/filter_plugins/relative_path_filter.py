import os


METROAE_ROOT = "/metroae/"
print("INSIDE FILTER")


def relative_path_to_absolute_path(string):
    print("INSIDE FUNCTION")
    if not os.path.isabs(string):
        print("PATH IS" + string)
        string = METROAE_ROOT + string.lstrip("./")
        print("PATH IS" + string)
        print("INSIDE CONDITION")
    return string


class FilterModule(object):
    ''' Query filter '''

    def filters(self):
        return {'relative_path_to_absolute_path': relative_path_to_absolute_path}
