# Visualizing Stock Prices and Bollinger Bands

Please excuse any improper formatting or non-adherence to Github etiquette. I'm formally a commerce student specializing in finance. This is my first interaction with Github as a very new, but very passionate programmer.

The graphing_bollinger_bands script automatically pulls stock data from Yahoo Finance to create 
a graph displaying the stock price data and its bollinger bands (moving volatility based on moving 
mean and standard deviation) over n number of years. The user may specify the type (bollinger bands
or only stock price) and aesthetics of the graph (either beautifully clean with dashed lines, or 
more PowerPoint-professional style)
* Bollinger bands are generally used as approximate measures of maximum divergence from the mean.
As you will see in the resulting graph, the stock price rarely ever moves past the upper or lower
bollinger band - algorithmic traders can use bollinger bands to generate buy/sell signals from
stock prices that approach their bollinger bands

Finance professionals can use this script to quickly create beautiful bollinger band graphs to
assist with technical analysis, while business professionals can use the graph code
(e.g. clean_style function) to automate the process of creating professional visuals for presentations
