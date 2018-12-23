from master import Master, init
from mpi4py import MPI


class TestCase:
    def __init__(self):
        self.app = init()

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



def prettyprint(test):
    try:
        test()
    except:
        print(test.__name__, ': FAIL')
    finally:
        print(test.__name__, ': OK')

def main():
    test = TestCase()
    prettyprint(test.test_int)
    prettyprint(test.test_list)
    prettyprint(test.test_modif_int)
    prettyprint(test.test_modif_list)
    prettyprint(test.test_int_free)
    prettyprint(test.test_list_free)
    test.app.terminate_slaves()

if __name__ == '__main__':
    main()
