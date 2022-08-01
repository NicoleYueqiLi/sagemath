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


def timing_test(input_file_name, output_file_name):
    """
    Testing intersection cpu time
    INPUT: 
    
    - ``input_file_name``: testing file name
    - ``output_file_name``: output file name, where out stored
    
    OUTPUT:
    
    file
    
    EXAMPLES::
    
        timing_test('difference_test.txt', 'difference_res.txt')
    """
    test = load_test_file(input_file_name)
    total_time = 0
    with open(output_file_name, 'w') as fp:
        for i in range(len(test)-1):
            s1 = RealSet(*eval(test[i]))
            s2 = RealSet(*eval(test[i + 1]))
            start = process_time()
            s1.difference(s2)
            end = process_time()
            tim = end - start
            print(tim, end='\r')
            total_time += tim
            fp.write("%s\n" % tim)
        fp.write("%s\n" % "Average:")
        avg = total_time / (len(test) - 1)
        fp.write("%s\n" % avg)
    print("average", avg)
    print("done")
