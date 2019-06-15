# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 16:23:43 2019

@author: ark4d
"""
import pandas as pd
import mysql.connector


def load_data_csv(filename):
    '''
    Loads neccessary data from filename
    '''
    work_time_df = pd.read_csv(filename)
    return work_time_df

def load_data_redmine_mysql(credentials, ids, additional_keys = True):
    '''
    Load data from redmine on mysql
    Parameters
    ----------
    credentials : dict
        dictionary containing host, user, passwd, database info
    ids : list of int
        indexes of what task should be loaded
    Key arguments
    -------------
    additional_keys = True:
        If true appends -,'not recorded' to 'issues.id' column and
        'Not categorized', 'No data' to 'subject' column of returning
        dataframe
        
    Returns
    -------
    pandas.DataFrame with results
    '''
    mydb = mysql.connector.connect(**credentials)
    # if connection not established the mysql connector will raise an exception
    
    columns = ['issues.id','subject','status_id','issue_statuses.name']
    query='SELECT {0} from issues LEFT JOIN issue_statuses \
        ON issues.status_id=issue_statuses.id where issues.id IN({1})'.format(
        ','.join(columns),','.join(ids)) # Where issues.id IN list of ids
    cursor = mydb.cursor()
    cursor.execute(query)
    rdm_df = pd.DataFrame(cursor.fetchall())
    cursor.close()
    mydb.close()
    rdm_df.columns=columns
    
    if additional_keys:
        additional_work_keys ={
                'issues.id':['-','not recorded'],
                'subject':['Not categorized','No data'],
        }
        rdm_df=rdm_df.append(pd.DataFrame(additional_work_keys))
        
    rdm_df.set_index('issues.id',inplace=True)

    return rdm_df 
