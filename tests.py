from master import Master, init
from mpi4py import MPI


class TestCase:
    def __init__(self, max_size):
        self.app = init(max_size)

    def test_int(self):
        value = 55555
        v = self.app.allocate(value)
        assert self.app.read(v) == value
        self.app.free(v)

    def test_list(self):
        value = [i for i in range(1, 5)]
        v = self.app.allocate(value)
        assert self.app.read(v) == value
        self.app.free(v)

    def test_modif_int(self):
        old_value = 1234
        new_value = 55555
        v = self.app.allocate(old_value)
        assert self.app.read(v) == old_value
        assert self.app.modify(v, new_value) == True
        assert self.app.read(v) == new_value
        self.app.free(v)

    def test_modif_list(self):
        old_value = [i for i in range(1,5)]
        new_value = old_value
        new_value[1] = 10
        v = self.app.allocate(old_value)
        assert self.app.read(v) == old_value
        assert self.app.modify(v, 10, 1) == True
        assert self.app.read(v) == new_value
        self.app.free(v)
    
    def test_modif_list_wrong_index(self):
        old_value = [i for i in range(1,5)]
        new_value = old_value
        new_value[1] = 10
        v = self.app.allocate(old_value)
        assert self.app.read(v) == old_value
        assert self.app.modify(v, 10, 100) == False
        assert self.app.read(v) == old_value
        self.app.free(v)


    def test_int_free(self):
        value = 55555
        v = self.app.allocate(value)
        assert self.app.read(v) == value
        self.app.free(v)
        assert self.app.read(v) == None


    def test_list_free(self):
        value = [i for i in range(1, 5)]
        v = self.app.allocate(value)
        assert self.app.read(v) == value
        self.app.free(v)
        assert self.app.read(v) == None

    def test_list_in_multiple_processes(self):
        value = [i for i in range(1, 200)]
        v = self.app.allocate(value)
        assert len(v[1]) >= 2
        assert self.app.read(v) == value
        self.app.free(v)

    def test_add_lots_of_int(self):
        res = []
        values = [i for i in range(1, 200)]
        for val in values:
            res.append(self.app.allocate(val))
        for i, r in enumerate(res):
            assert self.app.read(r) == values[i]
            self.app.free(r)

    def test_add_lots_of_list(self):
        res = []
        values = [[i for i in range(1, 5)] for j in range(1,10)]
        for val in values:
            res.append(self.app.allocate(val))
        for i, r in enumerate(res):
            assert self.app.read(r) == values[i]
            self.app.free(r)

    def test_big_list_modify(self):
        values = [i for i in range(1,300)]
        var = self.app.allocate(values)
        val = self.app.read(var)
        assert values == val
        for i, v in enumerate(val):
            assert self.app.modify(var, v*2, i) == True
        assert self.app.read(var) == [i*2 for i in range(1,300)]
        self.app.free(var)

    def test_list_small_max_size(self):
        value1 = [5,10]
        value2 = [100]
        value3 = [111]
        value4 = [1]

        v1 = self.app.allocate(value1)
        v2 = self.app.allocate(value2)
        v3 = self.app.allocate(value3)
        v4 = self.app.allocate(value4)

        assert self.app.read(v1) == value1
        assert self.app.read(v2) == value2
        assert self.app.read(v3) == value3
        assert self.app.read(v4) == value4



def prettyprint(test):
    try:
        test()
        print(test.__name__, ': OK')
    except:
        print(test.__name__, ': FAIL')

def main():
    test = TestCase(100)
    prettyprint(test.test_int)
    prettyprint(test.test_list)
    prettyprint(test.test_modif_int)
    prettyprint(test.test_modif_list)
    prettyprint(test.test_modif_list_wrong_index)
    prettyprint(test.test_int_free)
    prettyprint(test.test_list_free)
    prettyprint(test.test_list_in_multiple_processes)
    prettyprint(test.test_add_lots_of_int)
    prettyprint(test.test_add_lots_of_list)
    prettyprint(test.test_big_list_modify)
    test2 = TestCase(2)
    prettyprint(test2.test_list_small_max_size)
    test.app.terminate_slaves()
    test2.app.terminate_slaves()

if __name__ == '__main__':
    main()
