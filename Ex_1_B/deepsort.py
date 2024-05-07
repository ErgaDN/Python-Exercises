def deep_sorted(x: any) -> str:
    """
    Sorts a nested structure (dict, list, set, tuple) recursively and returns a string representation.

    :param x: The input nested structure.
    :return: A string representation of the sorted nested structure.

    >>> deep_sorted({'b': 2, 'a': 1})
    '{"a":1, "b":2}'

    >>> deep_sorted([3, 1, [4, 2]])
    '[1, 3, [2, 4]]'

    >>> deep_sorted((3, 1, {2, 4}))
    '(1, 3, {2, 4})'

    >>> deep_sorted(42)
    '42'

    >>> deep_sorted("Hello")
    'Hello'

    >>> x = {"a": 5, "c": 6, "b": [1, 3, 2, 4]}
    >>> deep_sorted(x)
    '{"a":5, "b":[1, 2, 3, 4], "c":6}'

    >>> x = {"a": {"b": {"c": [{"d": [3, 2, 1]}, 9, 8]}, "e": 7}}
    >>> deep_sorted(x)
    '{"a":{"b":{"c":[8, 9, {"d":[1, 2, 3]}]}, "e":7}}'

    >>> x = {"b": [2, 4, 1], "a": 5, "c": 6}
    >>> deep_sorted(x)
    '{"a":5, "b":[1, 2, 4], "c":6}'

    >>> x = {'a': 6, 'b': [0, 3, [6, 2], 7, 6], 'c': 66}
    >>> deep_sorted(x)
    '{"a":6, "b":[0, 3, 6, 7, [2, 6]], "c":66}'

    >>> x = {'a': 6, 'c': 7}
    >>> deep_sorted(x)
    '{"a":6, "c":7}'

    >>> x = [5, {'b': 4, 'f': 7, 'a': 9}, (8, 9)]
    >>> deep_sorted(x)
    '[(8, 9), 5, {"a":9, "b":4, "f":7}]'

    >>> x = [1, [3, 2], {7, 6}, (5, 4), 8, '9']
    >>> deep_sorted(x)
    '[(4, 5), 1, 8, 9, [2, 3], {6, 7}]'

    >>> x = (9, (8, (7, (6, (5, (4, (3, (2, 1))))))))
    >>> deep_sorted(x)
    '((((((((1, 2), 3), 4), 5), 6), 7), 8), 9)'

    >>> x = [3, 1, 7]
    >>> deep_sorted(x)
    '[1, 3, 7]'

    >>> x = [10, {'a': 2, 'b': (3, 4, [2, 5]), 'c': [8, 9]}, (6, 7), '1']
    >>> deep_sorted(x)
    '[(6, 7), 1, 10, {"a":2, "b":(3, 4, [2, 5]), "c":[8, 9]}]'

    >>> x = [7, 3, 1, [7, 3, 1, [7, 3, 1, [7, 3, 1, [7, 3, 1]]]]]
    >>> deep_sorted(x)
    '[1, 3, 7, [1, 3, 7, [1, 3, 7, [1, 3, 7, [1, 3, 7]]]]]'

    >>> x = {"a": (1, [3, 2], {"b": [5, 4, {"d": (7, 8), "c": 6}]}), "e": [10, 9]}
    >>> deep_sorted(x)
    '{"a":(1, [2, 3], {"b":[4, 5, {"c":6, "d":(7, 8)}]}), "e":[10, 9]}'
    """

    if isinstance(x, dict):
        sorted_items = sorted((str(k), deep_sorted(v)) for k, v in x.items())
        result = "{" + ", ".join(f'"{k}":{v}' for k, v in sorted_items) + "}"
    elif isinstance(x, (list, set, tuple)):
        start = "[" if isinstance(x, list) else "{" if isinstance(x, set) else "("
        end = "]" if isinstance(x, list) else "}" if isinstance(x, set) else ")"
        sorted_values = sorted((deep_sorted(v) for v in x))
        # print(f"sorted_values = {sorted_values}")
        result = start + ", ".join(sorted_values) + end
    else:
        result = str(x)
    return result


if __name__ == '__main__':
    x = eval(input())
    print(deep_sorted(x))
