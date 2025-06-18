def convert_to_int(num: int | None) -> int:
    '''Converts a int|None object to an int if its a None object it returns 0'''
    if num is None:
        return 0
    else:
        return int(num)
