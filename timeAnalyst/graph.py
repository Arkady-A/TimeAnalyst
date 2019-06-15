# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 16:21:00 2019

@author: ark4d
"""
# comment blocks comments what below

class MainGrapher():
    def __init__(self, style):
        self.style = style
        
    def _create_line(self, ax):
        ax.axhline(1.0, linestyle='--', alpha=0.3, color='green')
    
    def _apply_style(self, ax):
        ax.grid = self.style['grid']['alpha']
        y_lim = self.style['y']['lim']
        ax.set_ylim(*y_lim)
        
        ax.set_yticks(self.style['y']['ticks'])
        ax.xaxis.set_tick_params(rotation=self.style['ticks_x']['rotation'])
        if self.style['spine']['remove']:
            for spine in ax.spines.items():
                spine[1].set_visible(False)
        for tick in ax.xaxis.get_major_ticks():
            tick.label.set_fontsize(self.style['ticks_x']['fontsize']) 
class DateTimeGrapher(MainGrapher):
    '''
    Class for creating graph with datetime
    '''
    def __init__(self, style, locator, formatter):
        '''
        Inizialization
        Parameters
        ---------
        style : dict-type object
            see README for more details
        locator : matplotlib.dates.Locator
            What will be used as a locator in the plot
        formatter : matplotlib.dates.Formatter
            Object that will format date
        '''
        super().__init__(style)
        self.locator = locator
        self.formatter = formatter
        
    def create_graph(self, ax, data, color):
        '''
        Applies style and creates plot on given axis. 
        
        Parameters
        ----------
        ax : matplotlib.axes
            axes on which the graph will be plotted
        data : pandas.DataFrame
            index - datetime
            values - values of interest
        color : str
            Hex of color or a standart mpl name (e.g. yellow, red, purple) 
        '''
        ax.plot(data.index, data.values, color=color)
        self._apply_style(ax)
        self._create_line(ax)
        if self.locator:
            ax.xaxis.set_major_locator(self.locator)
        if self.formatter:
            ax.xaxis.set_major_formatter(self.formatter)
        return ax

class BasicGrapher(MainGrapher):
    def __init__(self, style):
        '''
        Inizialization
        Parameters
        ---------
        style : dict-type object
            see README for more details
        '''
        super().__init__(style)
    
    def create_graph(self, ax, data, color, line=True):
        '''
        Applies style and creates plot on given axis. 
        
        Parameters
        ----------
        ax : matplotlib.axes
            axes on which the graph will be plotted
        data : pandas.DataFrame
            index - datetime
            values - values of interest
        color : str
            Hex of color or a standart mpl name (e.g. yellow, red, purple) 
        line : bool
            If true shows line at 1.0
        '''
        ax.plot(data.index, data.values, color=color)
        self._apply_style(ax)
        if line:
            self._create_line(ax)
        return ax

class PieCharter():
    pass
    # TODO: implement pie charter