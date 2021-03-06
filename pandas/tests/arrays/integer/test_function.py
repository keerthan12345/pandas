import numpy as np
import pytest

import pandas as pd
import pandas._testing as tm
from pandas.core.arrays import integer_array


@pytest.mark.parametrize("ufunc", [np.abs, np.sign])
# np.sign emits a warning with nans, <https://github.com/numpy/numpy/issues/15127>
@pytest.mark.filterwarnings("ignore:invalid value encountered in sign")
def test_ufuncs_single_int(ufunc):
    a = integer_array([1, 2, -3, np.nan])
    result = ufunc(a)
    expected = integer_array(ufunc(a.astype(float)))
    tm.assert_extension_array_equal(result, expected)

    s = pd.Series(a)
    result = ufunc(s)
    expected = pd.Series(integer_array(ufunc(a.astype(float))))
    tm.assert_series_equal(result, expected)


@pytest.mark.parametrize("ufunc", [np.log, np.exp, np.sin, np.cos, np.sqrt])
def test_ufuncs_single_float(ufunc):
    a = integer_array([1, 2, -3, np.nan])
    with np.errstate(invalid="ignore"):
        result = ufunc(a)
        expected = ufunc(a.astype(float))
    tm.assert_numpy_array_equal(result, expected)

    s = pd.Series(a)
    with np.errstate(invalid="ignore"):
        result = ufunc(s)
        expected = ufunc(s.astype(float))
    tm.assert_series_equal(result, expected)


@pytest.mark.parametrize("ufunc", [np.add, np.subtract])
def test_ufuncs_binary_int(ufunc):
    # two IntegerArrays
    a = integer_array([1, 2, -3, np.nan])
    result = ufunc(a, a)
    expected = integer_array(ufunc(a.astype(float), a.astype(float)))
    tm.assert_extension_array_equal(result, expected)

    # IntegerArray with numpy array
    arr = np.array([1, 2, 3, 4])
    result = ufunc(a, arr)
    expected = integer_array(ufunc(a.astype(float), arr))
    tm.assert_extension_array_equal(result, expected)

    result = ufunc(arr, a)
    expected = integer_array(ufunc(arr, a.astype(float)))
    tm.assert_extension_array_equal(result, expected)

    # IntegerArray with scalar
    result = ufunc(a, 1)
    expected = integer_array(ufunc(a.astype(float), 1))
    tm.assert_extension_array_equal(result, expected)

    result = ufunc(1, a)
    expected = integer_array(ufunc(1, a.astype(float)))
    tm.assert_extension_array_equal(result, expected)


@pytest.mark.parametrize("values", [[0, 1], [0, None]])
def test_ufunc_reduce_raises(values):
    a = integer_array(values)
    msg = r"The 'reduce' method is not supported."
    with pytest.raises(NotImplementedError, match=msg):
        np.add.reduce(a)


@pytest.mark.parametrize(
    "pandasmethname, kwargs",
    [
        ("var", {"ddof": 0}),
        ("var", {"ddof": 1}),
        ("kurtosis", {}),
        ("skew", {}),
        ("sem", {}),
    ],
)
def test_stat_method(pandasmethname, kwargs):
    s = pd.Series(data=[1, 2, 3, 4, 5, 6, np.nan, np.nan], dtype="Int64")
    pandasmeth = getattr(s, pandasmethname)
    result = pandasmeth(**kwargs)
    s2 = pd.Series(data=[1, 2, 3, 4, 5, 6], dtype="Int64")
    pandasmeth = getattr(s2, pandasmethname)
    expected = pandasmeth(**kwargs)
    assert expected == result


def test_value_counts_na():
    arr = pd.array([1, 2, 1, pd.NA], dtype="Int64")
    result = arr.value_counts(dropna=False)
    expected = pd.Series([2, 1, 1], index=[1, 2, pd.NA], dtype="Int64")
    tm.assert_series_equal(result, expected)

    result = arr.value_counts(dropna=True)
    expected = pd.Series([2, 1], index=[1, 2], dtype="Int64")
    tm.assert_series_equal(result, expected)


# TODO(jreback) - these need testing / are broken

# shift

# set_index (destroys type)
