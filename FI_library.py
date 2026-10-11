# -*- coding: utf-8 -*-
"""
Created on Mon Nov 17 12:36:38 2025

@author: User
"""

import QuantLib as ql
import pandas as pd
import numpy as np

def get_schedule_dataframe(settlement_date,
                       maturity_date,
                       tenor,
                       day_count=ql.Actual360(),
                       calendar=ql.TARGET(),
                       day_rolling=ql.ModifiedFollowing,
                       end_of_month=False):

    termination_day_rolling = day_rolling

    # Compute the coupon schedule
    schedule = ql.Schedule(settlement_date,
                           maturity_date,
                           tenor,
                           calendar,
                           day_rolling,
                           termination_day_rolling,
                           ql.DateGeneration.Backward,
                           end_of_month)
    
    cpn_date = [d for d in schedule]
    start_date = cpn_date[:-1]
    pay_date = cpn_date[1:]
    
    # Find the previous coupon date:
    # Create a new unadjusted schedule to compute the next 
    # unadjusted coupon date, then move backward by one tenor 
    # period and adjust for business-day day_rolling and end-of-month.
    
    schedule_no_adj = ql.MakeSchedule(settlement_date,
                           maturity_date,
                           tenor)
    
    neg_tenor = ql.Period(-tenor.length(), tenor.units())
    previous_coupon_date = calendar.advance(schedule_no_adj[1], 
                                            neg_tenor, day_rolling, 
                                            end_of_month)   
    
    start_date[0] = previous_coupon_date
    print(previous_coupon_date)
    
    day_count_time = ql.ActualActual(ql.ActualActual.ISDA)

    # Compute accrual factors (year_frac) and payment times (in years)
    
    # np.vectorize creates a "vectorized wrapper" for a function that normally works on one element.
    # So we can apply QuantLib's .yearFraction() to arrays directly (like MATLAB arrayfun).
    vf_year_frac = np.vectorize(lambda s, p: day_count.yearFraction(s, p))
    vf_time = np.vectorize(lambda p: day_count_time.yearFraction(settlement_date, p))
    
    # If the data come from: np.vectorize(...) calls, QuantLib methods, 
    # lists of mixed types (dates, None, floats, etc.), then it's safer to always specify dtype=float.
    # Using dtype=float tells NumPy: “Convert whatever this array-like object contains 
    # into a proper numeric array of floats.”
    # It guarantees that the result is a numeric NumPy array rather than an object array.
    
    year_frac = np.array(vf_year_frac(start_date, pay_date), dtype=float)   # element-wise yearFraction(start, end)
    pay_time = np.array(vf_time(pay_date), dtype=float)                     # element-wise time to payment
    
    
    # Construct a dataframe table with all information related to dates and conventions
    
    table = pd.DataFrame({"Start Date": start_date,
                          "Pay Date": pay_date,
                          "YearFrac": year_frac,
                          "Pay Time": pay_time})
        
    table.index = np.arange(1, len(table) + 1)
    table.style.format({"Discount Curve": "{:.6f}"})    

    return table