import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))

import pytest
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

        # Test TypeError gets raised
        with pytest.raises(TypeError):
            r.set_conversion("hello")

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

    def test_unique_option(self):
        datafile = 'examples/data/colors.txt'
        seed_value = 123
        r = RanCat(seed=seed_value)
        r.set_unique(True)
        r.load(datafile)
        i = []
        for x in r:
            i.append(x)
        assert i != []
        assert len(i) == r._total_combinations

    def test_read_size_option(self):
        datafile = 'examples/data/colors.txt'
        seed_value = 123
        r = RanCat(seed=seed_value)
        r.set_read_size(2)
        r.load(datafile)
        r._refresh_all(r._read_size)
        assert len(r.files[datafile].current_lines) == 2

    def test_duplicate_file_allowed(self):
        datafile = 'examples/data/colors.txt'
        seed_value = 123
        r = RanCat(seed=seed_value)
        r.load(datafile).load(datafile).load(datafile)
        result = r.next()
        result = result.split('_')
        assert len(result) == 3

    def test_soft_reset(self):
        datafile = 'examples/data/colors.txt'
        seed_value = 123
        r = RanCat(seed=seed_value, unique=True)
        r.load(datafile).load(datafile)
        i = []
        for x in r:
            i.append(x)
        assert i != []
        assert len(i) == r._total_combinations

        r.soft_reset()
        i = []
        for x in r:
            i.append(x)
        assert i != []
        assert len(i) == r._total_combinations

    def test_hard_reset(self):
        datafile = 'examples/data/colors.txt'
        seed_value = 123
        r = RanCat(seed=seed_value, unique=True)
        r.load(datafile).load(datafile)
        i = []
        for x in r:
            i.append(x)
        assert i != []
        assert len(i) == r._total_combinations

        r.hard_reset()
        i = []
        for x in r:
            i.append(x)
        assert i == []
        assert len(r.files) == 0
        assert len(i) == r._total_combinations

    def test_command_chaining(self):
        datafile = 'examples/data/colors.txt'
        r = RanCat().load(datafile).set_unique(True).set_conversion(str.upper).set_read_size(100)
        assert isinstance(r, RanCat)

    def test_load_structure(self):
        datafile = 'examples/data/colors.txt'
        r = RanCat().load_structure(datafile, ['cat', 'dog'])
        phrase = r.next()
        assert phrase.endswith('cat') or phrase.endswith('dog')

def main():
    pass

if __name__ == "__main__": main()