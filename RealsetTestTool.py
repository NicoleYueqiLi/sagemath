import random
from sage.sets.real_set import RealSet
from sage.rings.infinity import infinity, minus_infinity
from time import process_time

 ###################   Generate testing file #####################
# g = RealsetTestTool(start=-10 ** 9, end=10 ** 9)
# my_case = []
# for _ in range(1000):
#     # g.num = random.choice(range(1, 101))
#     g.num = 1000
#     g.sort = random.choice([True, False])
#     g.disjoint = random.choice([True, False])
#     g.digit_type = random.choice(["Int", "Double"])
#     # g.boundary_type = {"cc": 0.25, "co": 0.25, "oc": 0.25, "oo": 0.25}
#     # g.interval_type = {"ff": 0.9, "fi": 0.05, "if": 0.05, "ii": 0}
#     g.interval_type = {"ff": 0.98, "fi": 0.01, "if": 0.01, "ii": 0}
#     my_case.append(g.create_random_interval())
# g.save_test_file(my_case, "test.txt")

 ###################   Load file and timing    #####################
# g = RealsetTestTool()
# interval_list = g.load_test_file("test.txt")
# functions = {"union": lambda x: x[0].union(x[1]),
#              "difference": lambda x: x[0].difference(x[1]),
#              "intersection": lambda x: x[0].intersection(x[1])}
# g.rolling_timing_test(functions, 2, "test.txt")



class RealsetTestTool:
    def __init__(self, num=10, start=-9223372036854775800, end=9223372036854775807, allow_repeat=True,
                 sort=False, digit_type="int", disjoint=False,
                 boundary_type={"cc": 0.25, "co": 0.25, "oc": 0.25, "oo": 0.25},
                 interval_type={"ff": 0.9, "fi": 0.05, "if": 0.05, "ii": 0}):
        self.num = num
        self.start = start
        self.end = end
        self.allow_repeat = allow_repeat
        self.sort = sort
        self.digit_type = digit_type
        self.disjoint = disjoint
        self.boundary_type = boundary_type
        self.interval_type = interval_type

    @property
    def digit_type(self):
        return self._digit_type

    @digit_type.setter
    def digit_type(self, value):
        self._digit_type = value
        if self.digit_type.lower() == "int":
            self._generator = lambda: random.randint(self.start, self.end)
        elif self.digit_type.lower() == "double":
            self._generator = lambda: random.uniform(self.start, self.end)
        else:
            raise ValueError("Invalid type: " + self._digit_type)

    @property
    def boundary_type(self):
        return self._boundary_type

    @boundary_type.setter
    def boundary_type(self, dic):
        if len(dic) != 4:
            raise ValueError("Invalid length of boundary_type. Should be 4, got " + str(len(dic)))
        elif "cc" not in dic or "co" not in dic or "oc" not in dic or "oo" not in dic:
            raise ValueError("Invalid key of boundary_type. Only support cc, co, oc, oo")
        elif abs(sum(dic[name] for name in dic) - 1) > 1e-6:
            raise ValueError(
                "Invalid sum of boundary_type. Should sum up to 1, got " + str(abs(sum(dic[name] for name in dic))))
        self._boundary_type = dic

    @property
    def interval_type(self):
        return self._interval_type

    @interval_type.setter
    def interval_type(self, dic):
        if len(dic) != 4:
            raise ValueError("Invalid length of boundary_type. Should be 4, got " + str(len(dic)))
        elif "ff" not in dic or "fi" not in dic or "if" not in dic or "ii" not in dic:
            raise ValueError("Invalid key of boundary_type. Only support ff, fi, if, ii")
        elif abs(sum(dic[name] for name in dic) - 1) > 1e-6:
            raise ValueError(
                "Invalid sum of boundary_type. Should sum up to 1, got " + str(abs(sum(dic[name] for name in dic))))
        self._interval_type = dic

    def _init_types(self):
        nums = [round(self.num * self.interval_type["ff"]),
                round(self.num * self.interval_type["fi"]),
                round(self.num * self.interval_type["if"]),
                round(self.num * self.interval_type["ii"])]
        id = 0
        while sum(nums) < self.num:
            nums[id] += 1
            id = (id + 1) % 4
        while sum(nums) > self.num:
            nums[id] -= 1
            id = (id + 1) % 4
        self._interval_type_indicator = [0] * nums[0] + [1] * nums[1] + [2] * nums[2] + [3] * nums[3]
        random.shuffle(self._interval_type_indicator)

        nums = [round(self.num * self.boundary_type["cc"]),
                round(self.num * self.boundary_type["co"]),
                round(self.num * self.boundary_type["oc"]),
                round(self.num * self.boundary_type["oo"])]
        id = 0
        while sum(nums) < self.num:
            nums[id] += 1
            id = (id + 1) % 4
        while sum(nums) > self.num:
            nums[id] -= 1
            id = (id + 1) % 4
        self._boundary_type_indicator = [0] * nums[0] + [1] * nums[1] + [2] * nums[2] + [3] * nums[3]
        random.shuffle(self._boundary_type_indicator)

    def _create_random_list(self):
        """
        Random generate an array for create intervals

        INPUT:

        - ``num``: the amount of numbers
        - ``start``, ``end``: range of random generated interval
        - ``allow_repeat``: boolean, if repeated boundaries are allowed
        - ``sort``: boolean, if the list number are sorted
        - ``digit_type``: string, "int" for integers; "double" for double precision.

        OUTPUT:

        A list numbers.

        EXAMPLES::

            createRandomList(1000, allow_repeat=True, sort=Fase)
            createRandomList(1000)
        """
        if not self.allow_repeat:
            arr = set()
            while len(arr) < 2 * self.num:
                arr.add(self._generator())
            arr = list(arr)
        else:
            arr = []
            for _ in range(2 * self.num):
                arr.append(self._generator())
        if self.disjoint:
            arr.sort(reverse=True)

        return arr

    def create_random_interval(self):
        """
        Create number of ranndome interval

        INPUT:

        - ``num``: number of interval in each realset
        - ``allow_repeat``: boolean, if repeated boundaries are allowed
        - ``disjoint``: boolean, if generated intervals are forced to be disjointed
        - ``sort``: boolean, if the interval are sorted
        - ``boundary_type``: string, c -> closed; o -> open; "mix" -> mixed type
        - ``interval_type``: string, "two_end" -> intervals with finite boundaries;
                                     "one_end" -> intervals with at least one infinity boundary;


        OUTPUT:

        A list of interval

        EXAMPLES::

        createRandomInterval(1000)
        """
        arr = self._create_random_list()
        self._init_types()
        intervals = []
        for id in range(self.num):
            a = arr.pop()
            b = arr.pop()
            if a > b:
                a, b = b, a
            boundary_type = self._boundary_type_indicator.pop()
            interval_type = self._interval_type_indicator.pop()
            c, d = int(boundary_type < 2), int(boundary_type % 2 == 0)
            if interval_type > 0:
                if interval_type == 1:
                    b, d = float('Inf'), 0
                elif interval_type == 2:
                    a, c = -float('Inf'), 0
                else:
                    a, b, c, d = -float('Inf'), float('Inf'), 0, 0

            intervals.append([a, b, c, d])

        if not self.sort:
            random.shuffle(intervals)
        else:
            intervals.sort()
        return intervals

    def create_two_realsets_with_fixed_intersection_num(self, output_num):
        if output_num > self.num:
            raise ValueError("Invalid output_num: should be smaller or equal than input num.")
        arr = set()
        while len(arr) < 4 * self.num:
            arr.add(self._generator())

        arr = list(arr)
        arr.sort(reverse=True)
        res1, res2 = [], []
        for _ in range(output_num):
            a = arr.pop()
            c = arr.pop()
            b = arr.pop()
            d = arr.pop()
            res1.append([a, b, None, None])
            res2.append([c, d, None, None])
        for _ in range(self.num - output_num):
            a = arr.pop()
            b = arr.pop()
            c = arr.pop()
            d = arr.pop()
            res1.append([a, b, None, None])
            res2.append([c, d, None, None])
        self._init_types()
        for interval in res1:
            boundary_type = self._boundary_type_indicator.pop()
            interval[2], interval[3] = int(boundary_type < 2), int(boundary_type % 2 == 0)
        self._init_types()
        for interval in res2:
            boundary_type = self._boundary_type_indicator.pop()
            interval[2], interval[3] = int(boundary_type < 2), int(boundary_type % 2 == 0)

        random.shuffle(res1)
        random.shuffle(res2)
        return res1, res2




    @staticmethod
    def save_test_file(intervals_list, output_dir):
        with open(output_dir, 'a') as fp:
            for intervals in intervals_list:
                row = ""
                for interval in intervals:
                    row += "{zero},{one},{two},{three};".format(zero=interval[0], one=interval[1], two=interval[2],
                                                                three=interval[3])

                row += "\n"
                fp.write(row)

    @staticmethod
    def load_test_file(file_dir):
        intervals_list = []
        with open(file_dir, 'r') as rd:
            for row in rd:
                intervals = []
                for interval in row[:-1].split(';')[:-1]:
                    a, b, c, d = interval.split(',')
                    a = float(a) if '.' in a or a[-1] == 'f' else int(a)
                    b = float(b) if '.' in b or b[-1] == 'f' else int(b)
                    intervals.append([a, b, int(c), int(d)])

                intervals_list.append(intervals)

        return intervals_list

    @staticmethod
    def list_to_realset(intervals):
        result = []
        for interval in intervals:
            a = minus_infinity if interval[0] == -float("Inf") else interval[0]
            b = infinity if interval[1] == float("Inf") else interval[1]
            result.append(
                RealSet.interval(lower=a, upper=b, lower_closed=(interval[2] == 1), upper_closed=(interval[3] == 1)))

        return RealSet(*result)

    def rolling_timing_test(self, func_info, num_input, test_file_dir):
        interval_lists = self.load_test_file(test_file_dir)
        curr_window = []
        function_dict = {name: 0 for name in func_info}
        for id, interval_list in enumerate(interval_lists):
            curr_window.append(self.list_to_realset(interval_list))
            if len(curr_window) < num_input:
                continue
            elif len(curr_window) > num_input:
                curr_window.pop(0)
            for func_name in function_dict:
                func = func_info[func_name]
                tim = 0 - process_time()
                func(curr_window)
                tim += process_time()
                function_dict[func_name] += tim
            print("Complete: {per:.2f} %".format(per=float(id/len(interval_lists)*100)), end='\r')
        print("")

        for name in function_dict:
            print("{func_name} executed {use_time} s in average.".format(func_name=name,
                                                                        use_time=function_dict[name] / len(
                                                                            interval_lists)))

