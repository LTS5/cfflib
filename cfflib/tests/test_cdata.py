from nose.tools import assert_true, assert_false, assert_equal, assert_almost_equal

from numpy.testing import assert_array_equal, assert_array_almost_equal

import cfflib as cf

def test_json():
    c = cf.CData()
    