def flatten_dict(d, parent_key='', sep='_'):
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

nested_dict = {
    'name': 'mathstral:7b-v0.1-q8_0',
    'model': 'mathstral:7b-v0.1-q8_0',
    'modified_at': '2024-07-18T22:40:07.22967415+07:00',
    'size': 7702576371,
    'digest': '939f2d6f06c5d2c256b49ad599021751d34aa72a1f71dc76b7a7ecdb1c2078ad',
    'details': {
        'parent_model': '',
        'format': 'gguf',
        'family': 'llama',
        'families': ['llama'],
        'parameter_size': '7.2B',
        'quantization_level': 'Q8_0'
    },
    'expires_at': '0001-01-01T00:00:00Z'
}

print(flatten_dict(nested_dict))
print(ensure_str_str_dict(nested_dict))
