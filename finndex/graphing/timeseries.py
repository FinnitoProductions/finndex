import datetime

import matplotlib
import numpy as np
from matplotlib import cm
from matplotlib import pyplot as plt

from finndex.util import dateutil


'''
Represents an easily modifiable time series. 

The data is provided in 'data', where each key (string) represents the type of value stored (like 'price' or 'sentiment')
and the corresponding value is a dictionary where the key is date and the value is the corresponding value on that day.

dateFormat (string) represents the format of all the incoming x-values. graphDateFormat (string) represents the format in which the given
dates will be displayed on the x-axis. 

If seeking to modify an existing graph, existingGraph represents the TimeSeries which was already produced by this function.
'''
class TimeSeries:
    def __init__(self, title, data, colors=['tab:red', 'tab:blue', 'tab:green'], dataDateFormat=dateutil.DESIRED_DATE_FORMAT, graphedDateFormat = "%Y", yMin=None, yMax=None):
        self.title = title
        self.data = data
        self.dataDateFormat = dataDateFormat
        self.graphedDateFormat = graphedDateFormat
        self.yMin = yMin
        self.yMax = yMax
        self.colors=colors

        self.fig = None
        self.axes = []
        
        self.plotTimeSeries()
    
    def plotTimeSeries(self):
        if self.fig == None: # generating the graph for the first time
            self.fig, baseAxis = plt.subplots()
            firstExecution = True
            print('hello')
        else:
            baseAxis = self.axes[0]
            firstExecution = False
        
        for idx, (valueType, valDict) in enumerate(self.data.items()):
            dates = [date for date in valDict]
            values = [val for val in valDict.values()]

            formattedDates = []
            for date in dates:
                if not isinstance(date, datetime.datetime):
                    formattedDates += [datetime.datetime.strptime(date, self.dataDateFormat)]
                else:
                    formattedDates += [date]
                
            dates = matplotlib.dates.date2num(formattedDates)

            if not firstExecution:
                desiredAxes = self.axes[idx]
            else:
                if idx == 0:
                    desiredAxes = baseAxis
                else:
                    desiredAxes = baseAxis.twinx()
                self.axes += [desiredAxes]
                
                
            desiredAxes.set_ylabel(valueType, color=self.colors[idx])
            desiredAxes.plot(formattedDates, values, color = self.colors[idx])
            desiredAxes.set_title(self.title)
            desiredAxes.xaxis.set_major_formatter(matplotlib.dates.DateFormatter(self.graphedDateFormat))
            
            if self.yMin != None:
                desiredAxes.set_ylim(ymin=self.yMin)
            if self.yMax != None:
                desiredAxes.set_ylim(ymax=self.yMax)
            
        self.fig.tight_layout()
        plt.show()
