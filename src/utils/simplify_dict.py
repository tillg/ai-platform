def flatten_dict(d, parent_key="", sep="_"):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def ensure_str_str_dict(d):
    flat_dict = flatten_dict(d)
    new_dict = {}
    for entry in flat_dict:
        new_key = str(entry)
        new_val = str(flat_dict[entry])
        new_dict[new_key] = new_val
    return new_dict
