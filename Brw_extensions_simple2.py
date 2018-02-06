def duplicate(n):
    try:
        return 2*int(n)
    except IndexError:
        return -1