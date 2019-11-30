def sub_dict(d, keys):
    return {key: value for key, value in d.items() if key in keys}
