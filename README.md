# Time Analyst
Package that provides with means to create graphs of your "efficiency"

## Coefficient of efficiency 

Efficiency in terms of the package in it's current stage is how well you've spend your time of work in a day. It's being calculate by following formula ((TODO: add latex formula here)how many time you've spend working/how you expected to this time be spend working)

## How-To

You need a dataset with following structure (see work_sample.csv) for details:
* Date (yyyy-mm-dd) 
* start(hh-mm-ss) when a period of work started
*  end(hh-mm-ss) when the period of work ended
*   label(char) - how you work ended (default: p-planned d-distracted)
*   frate(float 0 to 5) - focus rate
*    task_id (optional)

Then you can use **example.py** as a skeleton for your needs.  


## Short-Term Plans

* Add pie chart showing which tasks you were performing
* Add setup.py