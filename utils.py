def print_types(obj: any, prefix: str = "") -> None:
    """
    Recursively print the type structure of a dict/list/primitive.
    Example:
        {"id": 123, "name": "Alice", "tags": ["x", "y"]}
    prints:
        id: int
        name: str
        tags: list[str]
    """
    if isinstance(obj, dict):
        for k, v in obj.items():
            t = type(v).__name__
            if isinstance(v, (dict, list)):
                print(f"{prefix}{k}: {t}")
                print_types(v, prefix + "  ")
            else:
                print(f"{prefix}{k}: {t}")
    elif isinstance(obj, list):
        print(f"{prefix}list[{len(obj)}]")  # show size
        if obj:  # inspect first element
            print_types(obj[0], prefix + "  ")
    else:
        print(f"{prefix}{obj}: {type(obj).__name__}")