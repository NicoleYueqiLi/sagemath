import random

def createRandomSortedList(num, start=-9223372036854775800, end=9223372036854775807, sort):
    """
    Random generate two array for create intervals
    Input:
      - num: number of examples
      - start, end: range of randome generated interval
      - sort: sorted are optional
    """
    arr = []
    for _ in range(num):
          arr.append(random.randint(start, end))

#     for _ in range(num):
#         arr.append(random.uniform(1, end))
     if sort:
        arr.sort()

    return arr


def createRandomInterval(num,sort):
    """
    Create num of ranndome interval:
    Input:
    - num: number of interval in each realset
    """
  
    arr1 = createRandomSortedList(num, sort)
    arr2 = createRandomSortedList(num, sort)
    interval = []
    for a, b in zip(arr1, arr2):
        if a > b:
            a, b = b, a
        interval.append([a, b])
    if not sort:
        random.shuffle(interval)
    return interval


def create_test_file(num_of_example, num_of_interval, file_name, sort=Fasle):
    """
    write interval in to file:
    Input:
      - num_of_example: number of realsets
      - num_of_interval: number of interval in each realset
      - file_name: the loacation of those realsets will be stored at
      - sort: if the random interval need to be sorted or not
    """
    with open(file_name, 'w') as fp:
        for i in range(num_of_example):
            fp.write("%s\n" % createRandomInterval(num_of_interval, sort))



