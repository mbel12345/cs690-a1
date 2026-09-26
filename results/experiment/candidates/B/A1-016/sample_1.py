def flatten_one_level(items):
    result = []
    for sublist in items:
        result.extend(sublist)
    return result
