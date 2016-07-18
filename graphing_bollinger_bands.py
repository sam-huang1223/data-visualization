''' Github version 1.0.0
This script automatically pulls stock data from Yahoo Finance to create a graph displaying
the stock price data and its bollinger bands (moving volatility based on moving mean and
standard deviation) over n number of years. The user may specify the type (bollinger bands
or only stock price) and aesthetics of the graph (either clean with dashed lines,
or more PowerPoint-professional style)
* Bollinger bands are generally used as approximate measures of divergence from the mean.
As you will see in the resulting graph, the stock price rarely ever moves past the upper or lower
bollinger band - algorithmic traders can use bollinger bands to generate buy/sell signals from
stock prices that approach their bollinger bands

All axes labels and text positionings are dynamically determined

Finance professionals can use this script to quickly create beautiful bollinger band graphs to
assist with technical analysis, while business professionals can use the graph code
(e.g. clean_style function) to automate the process of creating professional visuals for presentations

Author: Sam Huang
Colors and designs inspired by:
http://www.randalolson.com/2014/06/28/how-to-make-beautiful-data-visualizations-in-python-with-matplotlib/ '''
import pandas as pd
import matplotlib.pyplot as plt
import yahoo_finance
from matplotlib.dates import date2num
from math import ceil,floor
# user inputs
symbols = ['SPY']
start_year = 2010
years = 5
selection = 'bollinger_bands'      # choose from 'line', 'bollinger_bands'
style = 'clean'                    # choose from 'clean', 'professional'
notes = 'Data source: Yahoo Finance \nNote: Data was processed using pandas and plotted using matplotlib'

def line_plot(symbols,adj_close,start_year,years,title,notes,style):
    '''plots a simple line graph showing adjusted close prices'''
    # get tableau color set in list form
    tableau_colors = get_tableau_colors()
    title = title + 'Adjusted Close (' + str(start_year) + '-' + str(start_year + years) + ')'
    # sets up graph style based on user input
    if style == 'clean':
        Xmin,Xmax,Xincrement,Ymin,Ymax,Yincrement = clean_style(adj_close,symbols[0],title,years,notes)
    elif style == 'professional':
        Xmin,Xmax,Xincrement,Ymin,Ymax,Yincrement = professional_style(adj_close,symbols[0],title,years,notes)

    # Limit the range of the plot to avoid unnecessary whitespace
    plt.ylim(Ymin - 1, Ymax)
        # - 1 to enable the lowest dotted line to show up
    plt.xlim(date2num(Xmin), date2num(Xmax))
    # plot adjusted close prices for each stock
    for rank, column in enumerate(symbols):
        # avoid using the light colors in tableau color set (light colors are odd)
        color_rank = rank*2
        # plot the line using the dates as the x-values and adjusted close prices as the y-values
        plt.plot(adj_close.index, adj_close.ix[:,rank], lw=2, color=tableau_colors[color_rank])
        # plot the line label beside the line
        plt.text(date2num(Xmax) + Xincrement * 0.2, adj_close.ix[-1,rank], column, fontsize=24, color=tableau_colors[color_rank])
    plt.savefig('graphs/' + title + '.pdf', bbox_inches='tight')

def bollinger_bands(symbols,adj_close,start_year,years,title,notes,style):
    '''plots a graph showing adjusted close prices and the upper and lower bollinger bands'''
    tableau_colors = get_tableau_colors()
    title = title + 'Bollinger Bands (' + str(start_year) + '-' + str(start_year + years) + ')'
    # calculates the rolling mean and standard deviation (user can adjust window)
    rm = adj_close.rolling(window = 30,center=False).mean()
    rstd = adj_close.rolling(window = 30,center=False).std()

    # this script uses 3 standard deviations as the boundary (user can adjust based on preferences)
    upper_band = rm + rstd * 3
    # drops not a number values to clean data
    upper_band.dropna(inplace=True)
    lower_band = rm - rstd * 3
    lower_band.dropna(inplace=True)

    if style == 'clean':
        Xmin,Xmax,Xincrement,Ymin,Ymax,Yincrement = clean_style(adj_close,symbols[0],title,years,notes)
    elif style == 'professional':
        Xmin,Xmax,Xincrement,Ymin,Ymax,Yincrement = professional_style(adj_close,symbols[0],title,years,notes)

    plt.ylim(floor(lower_band[symbols[0]].min()), ceil(upper_band[symbols[0]].max()) + 1)
        # + 1 to enable the highest dotted line to show up
    plt.xlim(date2num(Xmin), date2num(Xmax))
    # plot the adjusted close prices and the line label
    plt.plot(adj_close.index, adj_close.ix[:,0], lw=1.5, color=tableau_colors[0])
    plt.text(date2num(Xmax) + Xincrement * 0.1, adj_close.ix[-1,0], (adj_close.columns.values)[0], fontsize=24, color=tableau_colors[0])
    # plot the upper and lower bollinger bands
    plt.plot(upper_band.index, upper_band.ix[:,0], lw=1.5, color=tableau_colors[14])
    plt.plot(lower_band.index, lower_band.ix[:,0], lw=1.5, color=tableau_colors[14])
    plt.savefig('graphs/' + title + '.pdf', bbox_inches='tight')

def clean_style(adj_close,symbol,title,years,notes,Xmin=0,Xmax=0,Xincrement=0,Ymin=0,Ymax=0,Yincrement=0):
    '''Sets up the aesthetics of the plot to have a clean look'''
    # adjusts the size of the plot
    plt.figure(figsize=(12, 9))        # user can adjust to fit preferences (1.33 ratio is optimal)
    # create new instance of plot
    ax = plt.subplot(111)              # maintain at 111
    # remove the graph borders for clean look
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    # remove tick lines on x and y axes
    ax.tick_params(axis="both", which="both", bottom="off", top="off", left="off", right="off")

    # shift x-axis labels downwards to prevent conflict with y-axis labels
    ax.tick_params(axis='x', pad=20)
    # shift y-axis labels downwards to prevent conflict with x-axis labels
    ax.tick_params(axis='y', pad=20)

    # dynamically determines minimum and maximum boundaries
    # finds the minimum of the column's minimum value then rounds down to nearest 10
    Ymin = floor(adj_close[symbol].min()/10)*10
    # finds the maximum of the column's maximum value then rounds up to nearest 10
    Ymax = ceil(adj_close[symbol].max()/10)*10
    Ymultiple = 10
    Yincrement = ceil(int(((Ymax-Ymin)/Ymultiple))/Ymultiple)*Ymultiple
    # range from Ymin to Ymax (inclusive of Ymax)
    Yrange = range(Ymin, Ymax + Yincrement, Yincrement)
    # format and enlarge y-axis ticks to increase readability
    plt.yticks(Yrange, ['${}'.format(y) for y in Yrange], fontsize = 20)

    Xmin = adj_close.index[0]
    Xmax = adj_close.index[-1]
    Xticks = years
    Xincrement = int((date2num(adj_close.index[-1]) - date2num(adj_close.index[0]))/Xticks)
    # format and enlarge x-axis
    plt.xticks(range(int(date2num(Xmin)),int(date2num(Xmax)),Xincrement),
               ['{}'.format(x) for x in range(adj_close.index[0].year,adj_close.index[-1].year + 2,ceil(years/Xticks))],
                fontsize = 20)
                # + 1 to account for the fact that 12-31-2014 should be represented as 2015
                # another + 1 to ensure that the range includes the Xmax

    # Provide tick lines across the plot to improve clarity
    for y in Yrange:
        plt.plot((date2num(Xmin), date2num(Xmax)),(y,y),"--", lw=0.5, color="black", alpha=0.33)
    # add title of the graph at the top
    plt.text((date2num(Xmin) + date2num(Xmax))/2, Ymax + Yincrement ** (((Ymax - Ymin)/Yincrement + 1)/9),
            title, fontsize=25, ha='center')
            # Yincrement ** (((Ymax - Ymin)/Yincrement + 1)/9) is a weighting algorithm
            # that attempts to keep the title in the same relative position by producing
            # returns based on the number of y labels (more y-labels -> lower distance
            # between -> greater weighting. Less y labels -> higher distance between -> lower weighting)

    # add notes section at the bottom
    plt.text(date2num(Xmin) - Xincrement * ((date2num(Xmax)-date2num(Xmin))/Xincrement)/20,
             Ymin - Yincrement * (((Ymax - Ymin)/Yincrement + 1)/5), notes, fontsize=16)
            # Xincrement * ((date2num(Xmax)-date2num(Xmin))/Xincrement)/20 is a weighting algorithm
            # that attempts to keep the notes in the same relative position by producing
            # returns based on the number of x labels (more x-labels -> lower distance
            # between -> greater weighting. Less x labels -> higher distance between -> lower weighting)

            # Yincrement * (((Ymax - Ymin)/Yincrement + 1)/5) is a weighting algorithm
            # that attempts to keep the notes in the same relative position by producing
            # returns based on the number of y labels (more y-labels -> lower distance
            # between -> greater weighting. Less y labels -> higher distance between -> lower weighting)
    return Xmin,Xmax,Xincrement,Ymin,Ymax,Yincrement

def professional_style(adj_close,symbol,title,years,notes,Xmin=0,Xmax=0,Xincrement=0,Ymin=0,Ymax=0,Yincrement=0):
    '''Sets up the aesthetics of the plot to have a professional look'''
    plt.figure(figsize=(12, 9))
    ax = plt.subplot(111)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(axis="both", which="both", top="off", right="off")
    ax.tick_params(axis='x', pad=20)
    ax.tick_params(axis='y', pad=20)

    Ymin = floor(adj_close[symbol].min()/10)*10
    Ymax = ceil(adj_close[symbol].max()/10)*10

    Ymultiple = 10
    Yincrement = ceil(int(((Ymax-Ymin)/Ymultiple))/Ymultiple)*Ymultiple
    Yrange = range(Ymin, Ymax + Yincrement, Yincrement)

    plt.yticks(Yrange, ['${}'.format(y) for y in Yrange], fontsize = 20)

    Xmin = adj_close.index[0]
    Xmax = adj_close.index[-1]
    Xticks = years
    Xincrement = int((date2num(adj_close.index[-1]) - date2num(adj_close.index[0]))/Xticks)
    plt.xticks(range(int(date2num(Xmin)),int(date2num(Xmax)),Xincrement),
               ['{}'.format(x) for x in range(adj_close.index[0].year,adj_close.index[-1].year + 2,ceil(years/Xticks))],
                fontsize = 20)

    plt.text((date2num(Xmin) + date2num(Xmax))/2, Ymax + Yincrement ** (((Ymax - Ymin)/Yincrement + 1)/9),
            title, fontsize=25, ha='center')
    plt.text(date2num(Xmin) - Xincrement * ((date2num(Xmax)-date2num(Xmin))/Xincrement)/20,
             Ymin - Yincrement * (((Ymax - Ymin)/Yincrement + 1)/5), notes, fontsize=16)
    return Xmin,Xmax,Xincrement,Ymin,Ymax,Yincrement

def get_data(symbols, dates):
    """Read stock data (adjusted close) for given symbols from Yahoo Finance"""
    # create dataframe with the dates as the row index instead of numbers
    df = pd.DataFrame(index=dates)
    for symbol in symbols:
        # get stock data from Yahoo finance
        yahoo = yahoo_finance.Share(symbol)
        start_date = str(dates[0])[:str(dates[0]).find(' ')]
        end_date = str(dates[-1])[:str(dates[0]).find(' ')]
        # read stock data into temp dataframe
        df_temp = pd.DataFrame(data = yahoo.get_historical(start_date,end_date), dtype = 'float32')
        # converts dates to datetime index objects
        df_temp['Date'] = pd.to_datetime(df_temp['Date'])
        # use date column as the index
        df_temp.set_index(keys = ['Date'], drop = True, inplace = True)
        # only use the adjusted close column
        df_temp.drop(['Close','High','Low','Open','Symbol','Volume'], axis = 1, inplace = True)
        # change name of adjusted close column to stock ticker (rename before joining to ensure non-conflict)
        df_temp.columns = [symbol]
        # join with main dataframes on the date index
        df = df.join(df_temp, how='left')
        # drop not a number values to clean data
        df.dropna(subset=["SPY"], inplace = True)
    # returns a dataframe containing clean data with each stock's adjusted close taking up 1 column
    return df

def get_tableau_colors():
    '''prepares the tableau colors for use with matplotlib.pyplot'''
    tableau_colors = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
                      (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
                      (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
                      (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
                      (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]
    # Scale the RGB values to the [0, 1] range, which is the format accepted by matplotlib
    for i in range(len(tableau_colors)):
        r, g, b = tableau_colors[i]
        tableau_colors[i] = (r / 255, g / 255, b / 255)
    return tableau_colors

# convert start and end dates into a range of dates
dates = pd.date_range(str(start_year) + '-01-01',str(start_year + years - 1) + '-12-31')
# reads adjusted close prices between dates into a pandas dataframe
adj_close = get_data(symbols,dates)
# creates the first part of the title
title = ''
for header in adj_close.columns.values:
    title = header + ' ' + title

# executes the appropriate functions based on user input
if selection == 'line':
    line_plot(symbols,adj_close,start_year,years,title,notes,style)
elif selection == 'bollinger_bands':
    bollinger_bands(symbols,adj_close,start_year,years,title,notes,style)
