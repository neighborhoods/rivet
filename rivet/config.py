_options = {
    'verbose': True
}


def set_option(opt, val):
    valid_options = _options.keys()
    if opt not in valid_options:
        raise ValueError('\'{}\' is not a valid rivet option .')
    else:
        _options[opt] = val


def get_option(opt):
    return _options.get(opt)
