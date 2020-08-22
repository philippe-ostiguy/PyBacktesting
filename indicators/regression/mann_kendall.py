# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 09:16:06 2015
@author: Michael Schramm
Modified on August 5th 2020
by : Philippe Ostiguy
"""

from __future__ import division
import numpy as np
from scipy.stats import norm
import data_manip.input_dataframe as idfm

class MannKendall(idfm.InputDataframe):
    """
    Mann-Kendall is a non-parametric test to determine if a trend is present over time (using monotonic function)

    """

    def __init__(self,alpha=0.00000000001,iteration=True,nb_data=200,date_debut='2006-10-20',
                 date_fin='2007-10-20',asset="MSFT"):
        self.alpha=alpha
        super().__init__()
        self.nb_data=nb_data #Nombre de données pour évaluer la trend (ou pas trend selon le cas)
        self.date_debut = date_debut  # date debut in_sample
        self.date_fin = date_fin  # date fin in sample
        self.asset = asset # De type csv et dans le répertoires (scope) du projet
        self.series=super().ordinal_date()
        self.sous_series=super().sous_series_()
        self.first_iteration=True
        self.nb_sign=0

    def mk(self):

        """
        I'm not the original writer of this function, it comes from github :

        https://github.com/mps9506/Mann-Kendall-Trend/blob/master/mk_test.py

        This function is derived from code originally posted by Sat Kumar Tomer
        (satkumartomer@gmail.com)
        See also: http://vsp.pnnl.gov/help/Vsample/Design_Trend_Mann_Kendall.htm

        The purpose of the Mann-Kendall (MK) test (Mann 1945, Kendall 1975, Gilbert
        1987) is to statistically assess if there is a monotonic upward or downward
        trend of the variable of interest over time. A monotonic upward (downward)
        trend means that the variable consistently increases (decreases) through
        time, but the trend may or may not be linear. The MK test can be used in
        place of a parametric linear regression analysis, which can be used to test
        if the slope of the estimated linear regression line is different from
        zero. The regression analysis requires that the residuals from the fitted
        regression line be normally distributed; an assumption not required by the
        MK test, that is, the MK test is a non-parametric (distribution-free) test.
        Hirsch, Slack and Smith (1982, page 107) indicate that the MK test is best
        viewed as an exploratory analysis and is most appropriately used to
        identify stations where changes are significant or of large magnitude and
        to quantify these findings.

        By default, it is a two-side test

        Input:
            x:   a vector of data
            alpha: significance level (0.01 default)
        Output:
            trend: tells the trend (increasing, decreasing or no trend)
            h: True (if trend is present) or False (if trend is absence)
            p: p value of the significance test
            z: normalized test statistics

            Return value : -1 if there is a negative trend (at the significance level)
                            +1 if there is positive trend (at the significance level)

        """
        sous_series_ = self.sous_series.loc[:,"Close"]
        n = len(sous_series_)

        # calculate positive and negative sign
        if self.first_iteration:
            for k in range(n-1):
                for j in range(k+1, n):
                    self.nb_sign += np.sign(sous_series_.values[j] - sous_series_.values[k])

        # if we iterate through time, we use previous calculation and add new value and substract old value
        else:
            for k in range(n-1):
                self.nb_sign += np.sign(sous_series_.values[n-1] - sous_series_.values[k])

            self.sous_series=self.sous_series_(point_data=self.point_data-1)
            sous_series_=self.sous_series.loc[:,"Close"]
            n = len(sous_series_)
            for k in range(n-1):
                self.nb_sign -= np.sign(sous_series_.values[k+1] - sous_series_.values[0])


        self.first_iteration = False

        # calculate the unique data
        unique_x, tp = np.unique(sous_series_.values, return_counts=True)
        g = len(unique_x)

        # calculate the var(s)
        if n == g:  # there is no tie
            var_s = (n*(n-1)*(2*n+5))/18
        else:  # there are some ties in data
            var_s = (n*(n-1)*(2*n+5) - np.sum(tp*(tp-1)*(2*tp+5)))/18

        if self.nb_sign  > 0:
            z = (self.nb_sign - 1)/np.sqrt(var_s)
        elif self.nb_sign < 0:
            z = (self.nb_sign  + 1)/np.sqrt(var_s)
        else: # self.nb_sign == 0:
            z = 0

        # calculate the p_value
        p = 2*(1-norm.cdf(abs(z)))  # two tail test
        h = abs(z) > norm.ppf(1-self.alpha/2)

        if (z < 0) and h:
            trend = -1
        elif (z > 0) and h:
            trend = 1
        else:
            trend = 0

        # return +1 if there a positive trend, -1 if there a negative trend and 0 if none.
        return trend


    def check_num_samples(beta, delta, std_dev, alpha=0.05, n=4, num_iter=1000,
                          tol=1e-6, num_cycles=10000, m=5):
        """
        This function is an implementation of the "Calculation of Number of Samples
        Required to Detect a Trend" section written by Sat Kumar Tomer
        (satkumartomer@gmail.com) which can be found at:
        http://vsp.pnnl.gov/help/Vsample/Design_Trend_Mann_Kendall.htm
        As stated on the webpage in the URL above the method uses a Monte-Carlo
        simulation to determine the required number of points in time, n, to take a
        measurement in order to detect a linear trend for specified small
        probabilities that the MK test will make decision errors. If a non-linear
        trend is actually present, then the value of n computed by VSP is only an
        approximation to the correct n. If non-detects are expected in the
        resulting data, then the value of n computed by VSP is only an
        approximation to the correct n, and this approximation will tend to be less
        accurate as the number of non-detects increases.
        Input:
            beta: probability of falsely accepting the null hypothesis
            delta: change per sample period, i.e., the change that occurs between
                   two adjacent sampling times
            std_dev: standard deviation of the sample points.
            alpha: significance level (0.05 default)
            n: initial number of sample points (4 default).
            num_iter: number of iterations of the Monte-Carlo simulation (1000
                      default).
            tol: tolerance level to decide if the predicted probability is close
                 enough to the required statistical power value (1e-6 default).
            num_cycles: Total number of cycles of the simulation. This is to ensure
                        that the simulation does finish regardless of convergence
                        or not (10000 default).
            m: if the tolerance is too small then the simulation could continue to
               cycle through the same sample numbers over and over. This parameter
               determines how many cycles to look back. If the same number of
               samples was been determined m cycles ago then the simulation will
               stop.
            Examples
            --------
               num_samples = check_num_samples(0.2, 1, 0.1)
        """
        # Initialize the parameters
        power = 1.0 - beta
        P_d = 0.0
        cycle_num = 0
        min_diff_P_d_and_power = abs(P_d - power)
        best_P_d = P_d
        max_n = n
        min_n = n
        max_n_cycle = 1
        min_n_cycle = 1
        # Print information for user
        print("Delta (gradient): {}".format(delta))
        print("Standard deviation: {}".format(std_dev))
        print("Statistical power: {}".format(power))

        # Compute an estimate of probability of detecting a trend if the estimate
        # Is not close enough to the specified statistical power value or if the
        # number of iterations exceeds the number of defined cycles.
        while abs(P_d - power) > tol and cycle_num < num_cycles:
            cycle_num += 1
            print("Cycle Number: {}".format(cycle_num))
            count_of_trend_detections = 0

            # Perform MK test for random sample.
            for i in xrange(num_iter):
                r = np.random.normal(loc=0.0, scale=std_dev, size=n)
                x = r + delta * np.arange(n)
                trend, h, p, z = mk_test(x, alpha)
                if h:
                    count_of_trend_detections += 1
            P_d = float(count_of_trend_detections) / num_iter

            # Determine if P_d is close to the power value.
            if abs(P_d - power) < tol:
                print("P_d: {}".format(P_d))
                print("{} samples are required".format(n))
                return n

            # Determine if the calculated probability is closest to the statistical
            # power.
            if min_diff_P_d_and_power > abs(P_d - power):
                min_diff_P_d_and_power = abs(P_d - power)
                best_P_d = P_d

            # Update max or min n.
            if n > max_n and abs(best_P_d - P_d) < tol:
                max_n = n
                max_n_cycle = cycle_num
            elif n < min_n and abs(best_P_d - P_d) < tol:
                min_n = n
                min_n_cycle = cycle_num

            # In case the tolerance is too small we'll stop the cycling when the
            # number of cycles, n, is cycling between the same values.
            elif (abs(max_n - n) == 0 and
                  cycle_num - max_n_cycle >= m or
                  abs(min_n - n) == 0 and
                  cycle_num - min_n_cycle >= m):
                print("Number of samples required has converged.")
                print("P_d: {}".format(P_d))
                print("Approximately {} samples are required".format(n))
                return n

            # Determine whether to increase or decrease the number of samples.
            if P_d < power:
                n += 1
                print("P_d: {}".format(P_d))
                print("Increasing n to {}".format(n))
                print("")
            else:
                n -= 1
                print("P_d: {}".format(P_d))
                print("Decreasing n to {}".format(n))
                print("")
                if n == 0:
                    raise ValueError("Number of samples = 0. This should not happen.")