def string_to_integer_list(string_list):
    if string_list is None:
        return None

    if string_list.strip() == "":
        return []

    try:
        return [int(x) for x in string_list.split(",")]
    except TypeError:
        return None
