# For Python 3.0 and later
from urllib.request import urlopen
import certifi
import json

from bokeh.models import TableColumn, FactorRange
from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.transform import dodge, factor_cmap
from bokeh.palettes import Spectral6, Set3, Plasma6



def get_jsonparsed_data(url):
    response = urlopen(url, cafile=certifi.where())
    data = response.read().decode("utf-8")
    return json.loads(data)

def column_formatter(df):
    columns=[]
    for i in df.columns:
        columns.append(TableColumn(field=i, title=i))
    return columns


def earningsBarChart(df):
    metrics = ['Revenue', 'Earnings', "EBITDA"]
    years = ['2019', '2020', '2021', '2022']

    data = {'metrics' : metrics,
            '2019'   : [df.revenue[3],df.netIncome[3], df.ebitda[3]],
            '2020'   : [df.revenue[2],df.netIncome[2], df.ebitda[2]],
            '2021'   : [df.revenue[1],df.netIncome[1], df.ebitda[1]],
            '2022'   : [df.revenue[0],df.netIncome[0], df.ebitda[0]]}


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
    return p
