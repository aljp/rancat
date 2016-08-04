import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
from rancat import RanCat

class TestRanCat:
    def test_init_without_seed(self):
        r = RanCat()
        assert len(r.files) == 0
        assert not hasattr(r.seed, '__call__')
        assert hasattr(r._conversion, '__call__')

    def test_init_with_seed(self):
        seed_value = 123
        r = RanCat(seed=seed_value)
        assert len(r.files) == 0
        assert not hasattr(r.seed, '__call__')
        assert r.seed == seed_value
        assert hasattr(r._conversion, '__call__')

    def test_load(self):
        datafile = 'examples/data/colors.txt'
        seed_value = 123
        r = RanCat(seed=seed_value)
        r.load(datafile)
        assert len(r.files) == 1

    def test_next(self):
        datafile = 'examples/data/colors.txt'
        seed_value = 123
        r = RanCat(seed=seed_value)
        r.load(datafile)
        value = r.next()
        assert isinstance(value, str)

    def test_open_all(self):
        pass

    def test_default_conversion(self):
        raw_string = 'S\'tr ing   '
        correct_string = 'Str_ing'
        r = RanCat()
        processed_string = r._conversion(raw_string)
        assert processed_string == correct_string

    def test_set_conversion(self):
        raw_string = 'string'
        correct_string = raw_string.upper()
        r = RanCat()
        r.set_conversion(str.upper)
        processed_string = r._conversion(raw_string)
        assert processed_string == correct_string

    def test_iterable(self):
        datafile = 'examples/data/colors.txt'
        seed_value = 123
        r = RanCat(seed=seed_value)
        r.load(datafile)
        i = []
        for x in r:
            i.append(x)
            break
        assert i != []
        
