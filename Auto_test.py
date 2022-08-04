from time import process_time

def load_test_file(input_file_name):
    """
    Load input File.
    
    INPUT: 
    
    - ``input_file_name``: testing file name
    
    OUTPUT:
    
    list.
    
    EXAMPLES::
    
    load_test_file('difference_test.txt')
    """
    with open(input_file_name, 'r') as rd:
        lines = rd.readlines()
        return lines

    


def timing_test():
    """
    Testing union, intersection, difference, symmetric_difference, and is_disjoint cpu time
    
    INPUT: 
    
    - ``input_file_name``: testing file name
    
    OUTPUT:
    
    file
    
    EXAMPLES::
    
        timing_test('difference_test.txt', 'difference_res.txt')
    """
    test_file = ["test_union.txt", "intersection_test.txt","test_difference.txt","test_symmetric_difference.txt","test_is_disjoint.txt"]
    test_contents = {"union": 0, 
                     "intersection": 0, 
                     "difference": 0,
                     "symmetric_difference":0,
                     "is_disjoint":0}
    total_time = 0
    for test_name in test_contents:
        for test in test_file:
            test = load_test_file(test)
            s1, s2 = None, RealSet(*eval(test[0]))
            for i in range(len(test)-1):
            s1, s2 = s2, RealSet(*eval(test[i + 1])
                output_dir = "res_" + test_name + ".txt"
                tim = test_inner(test_name)
                print(tim, end='\r')
                test_contents[test_name] += tim
                with open(output_dir, 'a') as fp:
                    fp.write("%s\n" % tim)
     for test_name in test_contents:
        output_dir = test_name + "_res.txt"
        with open(output_dir, 'a') as fp:
            fp.write("Average: {avg:.6f}".format(avg=test_contents[test_name] / (len(test) - 1)))
        print("{test} Average Time: {avg:.6f}".format(test=test_name, avg=test_contents[test_name] / (len(test) - 1)))
    print("done") 
        
    def test_inner(s1, s2):
        if test_name == "union":
            start = process_time()
            s1.union(s2)
            end = process_time()
        elif test_name == "difference":
            start = process_time()
            s1.difference(s2)
            end = process_time()
        elif test_name == "intersection":
            start = process_time()
            s1.intersection(s2)
            end = process_time()
        elif test_name == "symmetric_difference":
            start = process_time()
            s1.symmetric_difference(s2)
            end = process_time()
        elif test_name == "is_disjoint":
            start = process_time()
            s1.is_disjoint(s2)
            end = process_time()
        else:
            raise ValueError("Invalid testing name: " + test_name)
        return end-start
#     s1, s2 = None, RealSet(*eval(test[0]))
#     for i in range(len(test)-1):
#         s1, s2 = s2, RealSet(*eval(test[i + 1]))
#         for test_name in test_contents:
#             output_dir = "res_" + test_name + ".txt"
#             tim = test_inner(s1, s2, test_name)
#             print(tim, end='\r')
#             test_contents[test_name] += tim
#             with open(output_dir, 'a') as fp:
#                 fp.write("%s\n" % tim)
    
#     for test_name in test_contents:
#         output_dir = test_name + "_res.txt"
#         with open(output_dir, 'a') as fp:
#             fp.write("Average: {avg:.6f}".format(avg=test_contents[test_name] / (len(test) - 1)))
#         print("{test} Average Time: {avg:.6f}".format(test=test_name, avg=test_contents[test_name] / (len(test) - 1)))
#     print("done") 
    
