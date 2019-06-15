# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 16:38:56 2019

@author: ark4d
"""
# comment blocks comments what below
from timeAnalyst import collect
from timeAnalyst import process
from timeAnalyst import graph

import numpy as np
import matplotlib.pyplot as plt


from matplotlib.dates import DayLocator, YearLocator, MonthLocator,\
WeekdayLocator, DateFormatter

work = collect.load_data_csv('work.csv')

# change cred if you want to connect your database
cred = {'host':"localhost",
  'user':"test",
  'passwd':"test",
    'database':'redmine'}

default_style={
       'grid':{'alpha':0.3},
       'spine':{'remove':True},
       'y':{'lim':[0,1.5],'ticks':np.arange(0, 1.5, 0.1)},
       'ticks_x':{'rotation':45,'fontsize':8},
       }
# how many datapoints will be shown
default_amount={
        'days_l':100, # 200 will allow to see more patters
        'days_s':30,
        'weeks':25,
        'month':20,
        'years':10,
        }

# gets tasks id's 
ids = [dig for dig in set(work.task_id.values) if str(dig).isdigit()]
# collects data crom redmine give ids This is optional and have no use as for 
# 2019-06-15
redm_df = collect.load_data_redmine_mysql(cred, ids)
# calculates time
work_time_df = process.count_time_spread(work)
# calculates efficiency of time (README you can look what folmula is used)
eff_df = process.calculate_days_efficiency(work_time_df )

fig, axes = plt.subplots(2,2,figsize=(15,15))
axes= axes.ravel()

#left top graph
ax = axes[0]
day_graph = graph.DateTimeGrapher(default_style, DayLocator(),
                                  DateFormatter('%d-%m'))
#data=eff_df.iloc[-default_amount['days_s']:] will look up how much days or 
# month or e.t.c display
day_graph.create_graph(ax=ax, data=eff_df.iloc[-default_amount['days_s']:],
                       color='orange')
day_graph.create_graph(ax=ax,
                       data=eff_df.rolling(5).mean().iloc[-default_amount['days_s']:],
                       color='black')
#right top graph
ax = axes[1]
month_graph = graph.DateTimeGrapher(default_style, MonthLocator(range(1, 13)), 
                                    DateFormatter('%B-%y'))
month_eff_df = process.calculate_mean_month_efficiency(eff_df)
month_graph.create_graph(ax=ax, data=month_eff_df.iloc[-default_amount['month']:],
                         color='orange')
#left bottom graph
ax = axes[2]
year_graph = graph.DateTimeGrapher(default_style, YearLocator(),
                                   DateFormatter('%Y'))
year_eff_df = process.calculate_mean_year_efficiency(eff_df)
year_graph.create_graph(ax=ax, data=year_eff_df.iloc[-default_amount['years']:], 
                        color='orange')

#right bottom graph
ax = axes[3]
week_graph = graph.BasicGrapher(default_style)
week_eff_df = process.calculate_mean_week_efficiency(eff_df)
week_graph.create_graph(ax=ax, data=week_eff_df.iloc[-default_amount['weeks']:], 
                        color='orange')

# latest graph
f = plt.figure(figsize=(15,10))
ax = f.gca()
day_graph = graph.DateTimeGrapher(default_style, DayLocator(),
                                  DateFormatter('%d-%m'))
day_graph.create_graph(ax=ax, data=eff_df.iloc[-default_amount['days_l']:],
                       color='orange')
day_graph.create_graph(ax=ax,
                       data=eff_df.rolling(10).mean().iloc[-default_amount['days_l']:],
                       color='black')

for ind,aax in enumerate([axes[1],ax]):
    aax.get_figure().savefig('example_pics/pic{}.png'.format(ind)
            )
graph