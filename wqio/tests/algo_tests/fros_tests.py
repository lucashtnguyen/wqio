import sys
import nose.tools as ntools

import numpy
import numpy.testing as npt
from numpy.testing import dec
import pandas.util.testing as pdtest
from wqio import testing

import pandas

from wqio.algo import fros
from statsmodels.compat.python import StringIO


@ntools.nottest
def load_basic_data():
    df = (
        testing
            .getTestROSData()
            .assign(conc=lambda df: df['res'])
            .assign(censored=lambda df: df['qual'] == 'ND')
    )
    return df


@ntools.nottest
def load_intermediate_data():
    df = pandas.DataFrame([
        {'censored': True, 'conc': 5.0, 'det_limit_index': 1, 'rank': 1},
        {'censored': True, 'conc': 5.0, 'det_limit_index': 1, 'rank': 2},
        {'censored': True, 'conc': 5.5, 'det_limit_index': 2, 'rank': 1},
        {'censored': True, 'conc': 5.75, 'det_limit_index': 3, 'rank': 1},
        {'censored': True, 'conc': 9.5, 'det_limit_index': 4, 'rank': 1},
        {'censored': True, 'conc': 9.5, 'det_limit_index': 4, 'rank': 2},
        {'censored': True, 'conc': 11.0, 'det_limit_index': 5, 'rank': 1},
        {'censored': False, 'conc': 2.0, 'det_limit_index': 0, 'rank': 1},
        {'censored': False, 'conc': 4.2, 'det_limit_index': 0, 'rank': 2},
        {'censored': False, 'conc': 4.62, 'det_limit_index': 0, 'rank': 3},
        {'censored': False, 'conc': 5.57, 'det_limit_index': 2, 'rank': 1},
        {'censored': False, 'conc': 5.66, 'det_limit_index': 2, 'rank': 2},
        {'censored': False, 'conc': 5.86, 'det_limit_index': 3, 'rank': 1},
        {'censored': False, 'conc': 6.65, 'det_limit_index': 3, 'rank': 2},
        {'censored': False, 'conc': 6.78, 'det_limit_index': 3, 'rank': 3},
        {'censored': False, 'conc': 6.79, 'det_limit_index': 3, 'rank': 4},
        {'censored': False, 'conc': 7.5, 'det_limit_index': 3, 'rank': 5},
        {'censored': False, 'conc': 7.5, 'det_limit_index': 3, 'rank': 6},
        {'censored': False, 'conc': 7.5, 'det_limit_index': 3, 'rank': 7},
        {'censored': False, 'conc': 8.63, 'det_limit_index': 3, 'rank': 8},
        {'censored': False, 'conc': 8.71, 'det_limit_index': 3, 'rank': 9},
        {'censored': False, 'conc': 8.99, 'det_limit_index': 3, 'rank': 10},
        {'censored': False, 'conc': 9.85, 'det_limit_index': 4, 'rank': 1},
        {'censored': False, 'conc': 10.82, 'det_limit_index': 4, 'rank': 2},
        {'censored': False, 'conc': 11.25, 'det_limit_index': 5, 'rank': 1},
        {'censored': False, 'conc': 11.25, 'det_limit_index': 5, 'rank': 2},
        {'censored': False, 'conc': 12.2, 'det_limit_index': 5, 'rank': 3},
        {'censored': False, 'conc': 14.92, 'det_limit_index': 5, 'rank': 4},
        {'censored': False, 'conc': 16.77, 'det_limit_index': 5, 'rank': 5},
        {'censored': False, 'conc': 17.81, 'det_limit_index': 5, 'rank': 6},
        {'censored': False, 'conc': 19.16, 'det_limit_index': 5, 'rank': 7},
        {'censored': False, 'conc': 19.19, 'det_limit_index': 5, 'rank': 8},
        {'censored': False, 'conc': 19.64, 'det_limit_index': 5, 'rank': 9},
        {'censored': False, 'conc': 20.18, 'det_limit_index': 5, 'rank': 10},
        {'censored': False, 'conc': 22.97, 'det_limit_index': 5, 'rank': 11}
    ])

    return df


@ntools.nottest
def load_basic_cohn():
    cohn = pandas.DataFrame([
        {'DL': 2.0, 'lower': 2.0, 'ncen_equal': 0.0, 'nobs_below': 0.0,
         'nuncen_above': 3.0, 'prob_exceedance': 1.0, 'upper': 5.0},
        {'DL': 5.0, 'lower': 5.0, 'ncen_equal': 2.0, 'nobs_below': 5.0,
         'nuncen_above': 0.0, 'prob_exceedance': 0.77757437070938218, 'upper': 5.5},
        {'DL': 5.5, 'lower': 5.5, 'ncen_equal': 1.0, 'nobs_below': 6.0,
         'nuncen_above': 2.0, 'prob_exceedance': 0.77757437070938218, 'upper': 5.75},
        {'DL': 5.75, 'lower': 5.75, 'ncen_equal': 1.0, 'nobs_below': 9.0,
         'nuncen_above': 10.0, 'prob_exceedance': 0.7034324942791762, 'upper': 9.5},
        {'DL': 9.5, 'lower': 9.5, 'ncen_equal': 2.0, 'nobs_below': 21.0,
         'nuncen_above': 2.0, 'prob_exceedance': 0.37391304347826088, 'upper': 11.0},
        {'DL': 11.0, 'lower': 11.0, 'ncen_equal': 1.0, 'nobs_below': 24.0,
         'nuncen_above': 11.0, 'prob_exceedance': 0.31428571428571428, 'upper': numpy.inf},
        {'DL': numpy.nan, 'lower': numpy.nan, 'ncen_equal': numpy.nan, 'nobs_below': numpy.nan,
         'nuncen_above': numpy.nan, 'prob_exceedance': 0.0, 'upper': numpy.nan}
    ])
    return cohn


class Test__ros_sort(object):
    def setup(self):
        self.df = load_basic_data()

        self.expected_baseline = pandas.DataFrame([
            {'censored': True,  'conc': 5.0},   {'censored': True,  'conc': 5.0},
            {'censored': True,  'conc': 5.5},   {'censored': True,  'conc': 5.75},
            {'censored': True,  'conc': 9.5},   {'censored': True,  'conc': 9.5},
            {'censored': True,  'conc': 11.0},  {'censored': False, 'conc': 2.0},
            {'censored': False, 'conc': 4.2},   {'censored': False, 'conc': 4.62},
            {'censored': False, 'conc': 5.57},  {'censored': False, 'conc': 5.66},
            {'censored': False, 'conc': 5.86},  {'censored': False, 'conc': 6.65},
            {'censored': False, 'conc': 6.78},  {'censored': False, 'conc': 6.79},
            {'censored': False, 'conc': 7.5},   {'censored': False, 'conc': 7.5},
            {'censored': False, 'conc': 7.5},   {'censored': False, 'conc': 8.63},
            {'censored': False, 'conc': 8.71},  {'censored': False, 'conc': 8.99},
            {'censored': False, 'conc': 9.85},  {'censored': False, 'conc': 10.82},
            {'censored': False, 'conc': 11.25}, {'censored': False, 'conc': 11.25},
            {'censored': False, 'conc': 12.2},  {'censored': False, 'conc': 14.92},
            {'censored': False, 'conc': 16.77}, {'censored': False, 'conc': 17.81},
            {'censored': False, 'conc': 19.16}, {'censored': False, 'conc': 19.19},
            {'censored': False, 'conc': 19.64}, {'censored': False, 'conc': 20.18},
            {'censored': False, 'conc': 22.97},
        ])[['conc', 'censored']]

        self.expected_with_warning = self.expected_baseline.iloc[:-1]

    def test_baseline(self):
        result = fros._ros_sort(self.df, result='conc', censorship='censored')
        pdtest.assert_frame_equal(result, self.expected_baseline)

    def test_censored_greater_than_max(self):
        df = self.df.copy()
        max_row = df['conc'].argmax()
        df.loc[max_row, 'censored'] = True
        result = fros._ros_sort(df, result='conc', censorship='censored')
        pdtest.assert_frame_equal(result, self.expected_with_warning)


class Test_cohn_numbers(object):
    def setup(self):
        self.df = load_basic_data()
        self.final_cols = ['DL', 'lower', 'upper', 'nuncen_above', 'nobs_below',
                           'ncen_equal', 'prob_exceedance']

        self.expected_baseline = pandas.DataFrame([
            {'DL': 2.0, 'lower': 2.0, 'ncen_equal': 0.0, 'nobs_below': 0.0,
             'nuncen_above': 3.0, 'prob_exceedance': 1.0, 'upper': 5.0},
            {'DL': 5.0, 'lower': 5.0, 'ncen_equal': 2.0, 'nobs_below': 5.0,
             'nuncen_above': 0.0, 'prob_exceedance': 0.77757437070938218, 'upper': 5.5},
            {'DL': 5.5, 'lower': 5.5, 'ncen_equal': 1.0, 'nobs_below': 6.0,
             'nuncen_above': 2.0, 'prob_exceedance': 0.77757437070938218, 'upper': 5.75},
            {'DL': 5.75, 'lower': 5.75, 'ncen_equal': 1.0, 'nobs_below': 9.0,
             'nuncen_above': 10.0, 'prob_exceedance': 0.7034324942791762, 'upper': 9.5},
            {'DL': 9.5, 'lower': 9.5, 'ncen_equal': 2.0, 'nobs_below': 21.0,
             'nuncen_above': 2.0, 'prob_exceedance': 0.37391304347826088, 'upper': 11.0},
            {'DL': 11.0, 'lower': 11.0, 'ncen_equal': 1.0, 'nobs_below': 24.0,
             'nuncen_above': 11.0, 'prob_exceedance': 0.31428571428571428, 'upper': numpy.inf},
            {'DL': numpy.nan, 'lower': numpy.nan, 'ncen_equal': numpy.nan, 'nobs_below': numpy.nan,
             'nuncen_above': numpy.nan, 'prob_exceedance': 0.0, 'upper': numpy.nan}
        ])[self.final_cols]


    def test_baseline(self):
        result = fros.cohn_numbers(self.df, result='conc', censorship='censored')
        pdtest.assert_frame_equal(result, self.expected_baseline)

    def test_no_NDs(self):
        result = fros.cohn_numbers(self.df.assign(qual=False), result='conc', censorship='qual')
        ntools.assert_tuple_equal(result.shape, (0, 7))


class Test__detection_limit_index(object):
    def setup(self):
        self.cohn = load_basic_cohn()
        self.empty_cohn = pandas.DataFrame(numpy.empty((0, 7)))

    def test_empty(self):
        ntools.assert_equal(fros._detection_limit_index(None, self.empty_cohn), 0)

    def test_populated(self):
         ntools.assert_equal(fros._detection_limit_index(3.5, self.cohn), 0)
         ntools.assert_equal(fros._detection_limit_index(6.0, self.cohn), 3)
         ntools.assert_equal(fros._detection_limit_index(12.0, self.cohn), 5)

    @ntools.raises(IndexError)
    def test_out_of_bounds(self):
        fros._detection_limit_index(0, self.cohn)


def test__ros_group_rank():
    df = pandas.DataFrame({
        'params': list('AABCCCDE') + list('DCBA'),
        'values': list(range(12))
    })

    result = fros._ros_group_rank(df, ['params'])
    expected = pandas.Series([1, 2, 1, 1, 2, 3, 1, 1, 2, 4, 2, 3], name='rank')
    pdtest.assert_series_equal(result, expected)


class Test__ros_plot_pos(object):
    def setup(self):
        self.cohn = load_basic_cohn()

    def test_uncensored_1(self):
        row = {'censored': False, 'det_limit_index': 2, 'rank': 1}
        result = fros._ros_plot_pos(row, self.cohn, censorship='censored')
        ntools.assert_equal(result, 0.24713958810068648)

    def test_uncensored_2(self):
        row = {'censored': False, 'det_limit_index': 2, 'rank': 12}
        result = fros._ros_plot_pos(row, self.cohn, censorship='censored')
        ntools.assert_equal(result, 0.51899313501144173)

    def test_censored_1(self):
        row = {'censored': True, 'det_limit_index': 5, 'rank': 4}
        result = fros._ros_plot_pos(row, self.cohn, censorship='censored')
        ntools.assert_equal(result, 1.3714285714285714)

    def test_censored_2(self):
        row = {'censored': True, 'det_limit_index': 4, 'rank': 2}
        result = fros._ros_plot_pos(row, self.cohn, censorship='censored')
        ntools.assert_equal(result, 0.41739130434782606)


def test__norm_plot_pos():
    result = fros._norm_plot_pos([1, 2, 3, 4])
    expected = numpy.array([ 0.159104,  0.385452,  0.614548,  0.840896])
    npt.assert_array_almost_equal(result, expected)


class Test__substitute_NDs(object):
    def test_censored(self):
        row = {'censored': True, 'value': 10}
        result = fros._substitute_NDs(row, fraction=0.75, result='value', censorship='censored')
        ntools.assert_equal(result, 7.5)

    def test_uncensored(self):
        row = {'censored': False, 'value': 10}
        result = fros._substitute_NDs(row, fraction=0.75, result='value', censorship='censored')
        ntools.assert_equal(result, 10)


class Test__select_final(object):
    def test_censored(self):
        row = {'censored': True, 'value': 10, 'est': 0.75}
        result = fros._select_final(row, estimated='est', result='value', censorship='censored')
        ntools.assert_equal(result, 0.75)

    def test_uncensored(self):
        row = {'censored': False, 'value': 10, 'est': 0.75}
        result = fros._select_final(row, estimated='est', result='value', censorship='censored')
        ntools.assert_equal(result, 10)


def test_plotting_positions():
    df = load_intermediate_data()
    cohn = load_basic_cohn()

    results = fros.plotting_positions(df, cohn, censorship='censored')
    expected = numpy.array([
        0.07414188,  0.11121281,  0.14828375,  0.14828375,  0.20869565,
        0.34285714,  0.4173913 ,  0.05560641,  0.11121281,  0.16681922,
        0.24713959,  0.27185355,  0.32652382,  0.35648013,  0.38643645,
        0.41639276,  0.44634907,  0.47630539,  0.5062617 ,  0.53621802,
        0.56617433,  0.59613064,  0.64596273,  0.66583851,  0.71190476,
        0.73809524,  0.76428571,  0.79047619,  0.81666667,  0.84285714,
        0.86904762,  0.8952381 ,  0.92142857,  0.94761905,  0.97380952
    ])
    npt.assert_array_almost_equal(results, expected)
