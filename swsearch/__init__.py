import pkg_resources


def get_current_version():
    _version = pkg_resources.get_distribution("swsearch").version

    if any((x not in '0123456789.' for x in _version)):
        raise Exception('Version {} invalid. It should only contain numbers and dots'.format(_version))
    return _version


version = get_current_version()
