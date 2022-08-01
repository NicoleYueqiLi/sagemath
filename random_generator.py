def createRandomList(num, start=-9223372036854775800, end=9223372036854775807, allow_repeat=True, sort=False):
    """
    Random generate an array for create intervals
    
    INPUT:
    
    - ``num``: the amount of numbers 
    - ``start``, ``end``: range of random generated interval
    - ``allow_repeat``: boolean, if repeated boundaries are allowed
    - ``sort``: boolean, if the list number are sorted
    
    OUTPUT:
    
    A list numbers.

    EXAMPLES::
    
        createRandomList(1000, allow_repeat=True, sort=Fase)
        createRandomList(1000)
    """
    if not allow_repeat:
        arr = set()
        while len(arr) < num:
            arr.add(random.randint(start, end))
        arr = list(arr)
    else:
        arr = []
        for _ in range(num):
            arr.append(random.randint(start, end))
    if sort:
        arr.sort()

    return arr


def createRandomInterval(num, allow_repeat=False, disjoint=False, sort=False):
    """
    Create number of ranndome interval
    
    INPUT:

    - ``num``: number of interval in each realset
    - ``allow_repeat``: boolean, if repeated boundaries are allowed
    - ``disjoint``: boolean, if generated intervals are forced to be disjointed
    - ``sort``: boolean, if the interval are sorted
    
    OUTPUT:
    
    A list of interval
    
    EXAMPLES::
    
    createRandomInterval(1000)
    """
    arr = createRandomList(2*num, allow_repeat=allow_repeat, sort=disjoint)
    interval = []
    while len(arr) > 0:
        a = arr.pop(0)
        b = arr.pop(0)
        if a > b:
            a, b = b, a
        interval.append([a, b])
    if not sort:
        random.shuffle(interval)
    else:
        interval.sort()
    return interval

def create_test_file(num_of_example, num_of_interval, file_name,  allow_repeat=False, disjoint=False, sort=False):
    """
    Write number of randome gernrated realset into a file
    
    INPUT:
    
    - ``num_of_exampl``e: number of realsets
    - ``num_of_interval``: number of interval in each realset
    - ``file_name``: the loacation of those realsets will be stored at
    - ``num``: number of interval in each realset
    - ``allow_repeat``: boolean, if repeated boundaries are allowed
    - ``disjoint``: boolean, if generated intervals are forced to be disjointed
    - ``sort``: boolean, if the interval are sorted
    
    OUTPUT:
    
    A file contain number of realsets in the current directory
    
    EXAMPLES::
    create_test_file(1000, 1000, 'test.txt', True, True, False)
    """
    with open(file_name, 'w') as fp:
        for i in range(num_of_example):
            fp.write("%s\n" % createRandomInterval(num_of_interval,  allow_repeat=allow_repeat, disjoint=disjoint, sort=sort))



