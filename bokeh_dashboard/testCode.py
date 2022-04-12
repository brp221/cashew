from helperLibrary import *

# /api/v3/analyst-estimates/AAPL?limit=30

from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.transform import dodge, factor_cmap
from bokeh.palettes import Spectral6, Set3, Plasma6


#       <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<   VBAR  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
url = ("https://financialmodelingprep.com/api/v3/analyst-estimates/NVDA?limit=4&apikey=ce687b3fe0554890e65d6a5e48f601f9")
estimatedEarningsDF = pd.DataFrame.from_dict(get_jsonparsed_data(url))

# QUARTER : api/v3/income-statement/AAPL?period=quarter&limit=400&apikey=ce687b3fe0554890e65d6a5e48f601f9
incomeStatURL = ("https://financialmodelingprep.com/api/v3/income-statement/NVDA?limit=4&apikey=ce687b3fe0554890e65d6a5e48f601f9")
incomeStatementDF  = pd.DataFrame.from_dict(get_jsonparsed_data(incomeStatURL))


metrics = ['Revenue', 'Earnings', "EBITDA"]
years = ['2019', '2020', '2021', '2022']

data = {'metrics' : metrics,
        '2019'   : [incomeStatementDF.revenue[3],incomeStatementDF.netIncome[3], incomeStatementDF.ebitda[3]],
        '2020'   : [incomeStatementDF.revenue[2],incomeStatementDF.netIncome[2], incomeStatementDF.ebitda[2]],
        '2021'   : [incomeStatementDF.revenue[1],incomeStatementDF.netIncome[1], incomeStatementDF.ebitda[1]],
        '2022'   : [incomeStatementDF.revenue[0],incomeStatementDF.netIncome[0], incomeStatementDF.ebitda[0]]}


x = [ (metric, year) for metric in metrics for year in years ]
counts = sum(zip(data['2019'], data['2020'], data['2021'], data['2022']), ()) # like an hstack

source = ColumnDataSource(data=dict(x=x, counts=counts))

p = figure(x_range=FactorRange(*x), height=250, title="Fruit counts by year",
           toolbar_location=None, tools="")

p.vbar(x='x', top='counts', width=0.9, source=source, line_color="white",
       fill_color=factor_cmap('x', palette=Plasma6, factors=years, start=1, end=2))

p.y_range.start = 0
p.x_range.range_padding = 0.1
p.xaxis.major_label_orientation = 1
p.xgrid.grid_line_color = None

show(p)