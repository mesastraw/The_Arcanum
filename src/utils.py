def convert_to_int(num: int|None) -> int:
    '''Converts a int|None object to an int if its a None object it returns 0'''
    if num is None:
        return 0
    else:
        return int(num)

def convert_to_bytes(val: bytes|None) -> bytes:
    '''Converts bytes|None object to byte
    Returns 0 charecters in bytes to indicate error'''

    if val is None:
        return b'0'
    else:
        return bytes(val)
