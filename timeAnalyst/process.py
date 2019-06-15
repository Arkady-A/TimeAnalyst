#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 16:24:14 2019

@author: ark4d
"""
# comment blocks comments what below 

import pandas as pd
from . import const 

def count_time_spread(df):
    '''
    Calculate how much time was spend on work and idle between work periods.
    '''
    if not set(['date', 'start', 'end']).issubset(
            df.columns):
        raise IndexError('''['date', 'start', 'end'] should be in columns''')
    sav = [df.end.copy(), df.start.copy()] 
    df.end = pd.to_datetime(df.end, format='%H:%M:%S') 
    df.start =  pd.to_datetime(df.start, format='%H:%M:%S') 
    
    # calculates in munites how many time was spent in work
    def time_spread_day(group):
        group.loc[:, 'working_time'] = (group.end-group.start).astype('timedelta64[m]')
        not_working_time=[]
        for ind in range(0,group.shape[0]):
            if ind+1 == group.shape[0]:
                not_working_time.append(0)
            else:
                not_working_time.append(
                        (group.iloc[ind+1].start-group.iloc[ind].end).seconds/60
                )
        group.loc[:,'not_working_after_time']=not_working_time
        group.loc[:,]
        return group
    
    grps = df.groupby('date')
    work_time_df = grps.apply(time_spread_day)
    work_time_df.end,work_time_df.start=sav
    return work_time_df

def count_data_planned_time(row):
    raise NotImplementedError('This function will be implemented in future')

def calculate_days_efficiency(work_df):
    '''
    Calculate Coefficient of day efficiency in terms of time spending (see docs)
    for the formula
    
    Parameters
    ----------
    time : float
    time spend on work in a day
    
    Returns
    -------
    float 
        Coefficient of efficiency
    '''
    work_df.date = pd.to_datetime(work_df.date)
    work_df.frate = work_df.frate.fillna(4.5)
    # maps 
    work_df.loc[:,'label_c'] = work_df.label.map(const.eff_c)
    work_df.loc[:,'frate_c'] = work_df.frate/5
    def day_eff_calc(day):
        ove = (day.loc[:,'label_c']*day.loc[:,'frate_c']*day.loc[:,'working_time']).sum()
        div = (const.stndr_p)*const.exp_focus*const.exp_label_coef
        return ove/div

    grps = work_df.groupby('date')
    return grps.apply(day_eff_calc)
    

def calculate_mean_week_efficiency(days_eff_df):
    '''
    Calculates mean efficiency for every week 
    Parameters 
    ----------
    days_eff_df : pandas.DataFrame
        index - date, values - list of floats
    
    Returns 
    -------
    pandas.DataFrame
        index - string *week*w-*year*, values - mean eff by corres. week
    '''
    #group by year and week
    grps = days_eff_df.groupby([days_eff_df.index.year, days_eff_df.index.week])
    #aggregate by mean
    result = grps.agg('mean')
    #sort by year, week
    result.sort_index(ascending=True)
    #conver multiindex to list of strings object *week*w-*year*
    func = lambda x: '{1}w-{0}'.format(*x)
    result.index = list(map(func, result.index))
    return result

def calculate_mean_month_efficiency(days_eff_df):
    '''
    Calculates mean efficiency for every month 
    Parameters 
    ----------
    days_eff_df : pandas.DataFrame
        index - date, values - list of floats
    
    Returns 
    -------
    pandas.DataFrame
        index - datetime, values - mean eff by corres. month
    '''
    #group by month, year
    grps = days_eff_df.groupby([days_eff_df.index.month,days_eff_df.index.year])
    #aggregate by mean
    result = grps.agg('mean')
    #convert multiindex to list of pandas.DateTime by mapping a function
    func = lambda x: pd.to_datetime('{}-{}'.format(*x),format='%m-%Y')
    result.index = list(map(func, result.index))
    return result.sort_index(ascending=True)

def calculate_mean_year_efficiency(days_eff_df):
    '''
    Calculates mean efficiency for every year 
    Parameters 
    ----------
    days_eff_df : pandas.DataFrame
        index - date, values - list of floats
    
    Returns 
    -------
    pandas.DataFrame
        index - datetime, values - mean eff by corres. year
    '''
    #group by year
    grps = days_eff_df.groupby([days_eff_df.index.year])
    #aggregate by mean
    result = grps.agg('mean')
    #convert multiindex to list of pandas.DateTime by mapping a function
    func = lambda x: pd.to_datetime('{}'.format(x),format='%Y')
    result.index = list(map(func, result.index))
    return result.sort_index(ascending=True)








