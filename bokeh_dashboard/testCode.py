from helperLibrary import *
from .library import *
# /api/v3/analyst-estimates/AAPL?limit=30

from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure, show, output_notebook

from bokeh.transform import dodge, factor_cmap
from bokeh.palettes import Spectral6, Set3, Plasma6

output_notebook()
#       <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<   VBAR  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
url = ("https://financialmodelingprep.com/api/v3/analyst-estimates/NVDA?limit=4&apikey=ce687b3fe0554890e65d6a5e48f601f9")
estimatedEarningsDF = pd.DataFrame.from_dict(get_jsonparsed_data(url))

# QUARTER : api/v3/income-statement/AAPL?period=quarter&limit=400&apikey=ce687b3fe0554890e65d6a5e48f601f9
incomeStatURL = ("https://financialmodelingprep.com/api/v3/income-statement/NVDA?limit=4&apikey=ce687b3fe0554890e65d6a5e48f601f9")
incomeStatementDF  = pd.DataFrame.from_dict(get_jsonparsed_data(incomeStatURL))

incomeStatURLquarter = ("https://financialmodelingprep.com/api/v3/income-statement/NVDA?period=quarter&limit=16&apikey=ce687b3fe0554890e65d6a5e48f601f9")
incomeStatDFQuart = pd.DataFrame.from_dict(get_jsonparsed_data(incomeStatURLquarter))


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
output_file("radar.html")
p = figure(x_range=FactorRange(*x), height=250, title="Fruit counts by year",
           toolbar_location=None, tools="")

p.vbar(x='x', top='counts', width=0.9, source=source, line_color="white",
       fill_color=factor_cmap('x', palette=Plasma6, factors=years, start=1, end=2))

p.y_range.start = 0
p.x_range.range_padding = 0.1
p.xaxis.major_label_orientation = 1
p.xgrid.grid_line_color = None

show(p)

from bokeh.plotting import figure, show

num_vars = 6
outlookURL = ("https://financialmodelingprep.com/api/v4/company-outlook?symbol=AAPL&apikey=ce687b3fe0554890e65d6a5e48f601f9")
aaplOutlook  =  pd.DataFrame.from_dict(get_jsonparsed_data(outlookURL)["rating"])

outlookURL2 = ("https://financialmodelingprep.com/api/v4/company-outlook?symbol=MSFT&apikey=ce687b3fe0554890e65d6a5e48f601f9")
peerOutlook  =  pd.DataFrame.from_dict(get_jsonparsed_data(outlookURL2)["rating"])



import numpy as np
import pandas as pd
import holoviews as hv
from holoviews import dim, opts

from bokeh.models import Div

hv.extension('bokeh')
img = hv.Image(np.random.rand(10, 10))

fig = hv.render(img)

print('Figure: ', fig)
print('Renderers: ', fig.renderers[-1].glyph)


violin = hv.Violin(np.random.randn(100))

hv.output(violin, fig='png')
hv.save(violin, 'violin.png')


html = file_html(violin, CDN, "my plot")


div = Div(text="""Your <img src="" alt="Italian Trulli"> """,
width=200, height=100)

show(div)


import numpy as np
import matplotlib.pyplot as plt


categories = ['Food Quality', 'Food Variety', 'Service Quality', 'Ambiance', 'Affordability']

restaurant_1 = [4, 4, 5, 4, 3]
restaurant_2 = [5, 5, 4, 5, 2]
restaurant_3 = [3, 4, 5, 3, 5]

label_loc = np.linspace(start=0, stop=2 * np.pi, num=len(restaurant_1))

plt.figure(figsize=(8, 8))
plt.subplot(polar=True)
plt.plot(label_loc, restaurant_1, label='Restaurant 1')
plt.plot(label_loc, restaurant_2, label='Restaurant 2')
plt.plot(label_loc, restaurant_3, label='Restaurant 3')
plt.title('Restaurant comparison', size=20)
lines, labels = plt.thetagrids(np.degrees(label_loc), labels=categories)
plt.legend()
plt.show()




import plotly.graph_objects as go
import plotly.offline as pyo

categories = ["DCF", "ROE", "ROA", "D/E", "P/E", "P/B"]
categories=[*categories, factors[0]]
x =  [aaplOutlook.ratingDetailsDCFScore[0], aaplOutlook.ratingDetailsROEScore[0], aaplOutlook.ratingDetailsROAScore[0], 
               aaplOutlook.ratingDetailsDEScore[0], aaplOutlook.ratingDetailsPEScore[0], aaplOutlook.ratingDetailsPBScore[0]]
x2 =  [peerOutlook.ratingDetailsDCFScore[0], peerOutlook.ratingDetailsROEScore[0], peerOutlook.ratingDetailsROAScore[0], 
               peerOutlook.ratingDetailsDEScore[0], peerOutlook.ratingDetailsPEScore[0], peerOutlook.ratingDetailsPBScore[0]]
x3 =  [peerOutlook3.ratingDetailsDCFScore[0], peerOutlook3.ratingDetailsROEScore[0], peerOutlook3.ratingDetailsROAScore[0], 
               peerOutlook3.ratingDetailsDEScore[0], peerOutlook3.ratingDetailsPEScore[0], peerOutlook3.ratingDetailsPBScore[0]]
x=[*x, x[0]]
x2=[*x2, x2[0]]
x3=[*x3, x3[0]]

fig = go.Figure(
    data=[
        go.Scatterpolar(r=x, theta=categories, fill='toself', name='AAPL'),
        go.Scatterpolar(r=x2, theta=categories, fill='toself', name='MSFT'),
        go.Scatterpolar(r=x3, theta=categories, fill='toself', name='GOOGL')
    ],
    layout=go.Layout(
        #title=go.layout.Title(text='COMPANY HEALTH COMPARISON'),
        #polar={'radialaxis': {'visible': True}},
        showlegend=True,
        width=400,
        height=400
    )
)

pyo.plot(fig)

fig.write_image("bokeh_dashboard/static_content/radarChart.png")


















import numpy as np
from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource, LabelSet

num_vars = 6
outlookURL = ("https://financialmodelingprep.com/api/v4/company-outlook?symbol=AAPL&apikey=ce687b3fe0554890e65d6a5e48f601f9")
aaplOutlook  =  pd.DataFrame.from_dict(get_jsonparsed_data(outlookURL)["rating"])

outlookURL2 = ("https://financialmodelingprep.com/api/v4/company-outlook?symbol=MSFT&apikey=ce687b3fe0554890e65d6a5e48f601f9")
peerOutlook  =  pd.DataFrame.from_dict(get_jsonparsed_data(outlookURL2)["rating"])


centre = 0.5

theta = np.linspace(0, 2*np.pi, num_vars, endpoint=False)
# rotate theta such that the first axis is at the top
theta += np.pi/2
print(theta)
def unit_poly_verts(theta, centre ):
    """Return vertices of polygon for subplot axes.
    This polygon is circumscribed by a unit circle centered at (0.5, 0.5)
    """
    x0, y0, r = [centre ] * 3
    print(x0)
    print(y0)
    print(r)
    verts = [(r*np.cos(t) + x0, r*np.sin(t) + y0) for t in theta]
    return verts

def radar_patch(r, theta, centre ):
    """ Returns the x and y coordinates corresponding to the magnitudes of 
    each variable displayed in the radar plot
    """
    # offset from centre of circle
    offset = 0.01
    yt = (r*centre + offset) * np.sin(theta) + centre 
    xt = (r*centre + offset) * np.cos(theta) + centre 
    return xt, yt

verts = unit_poly_verts(theta, centre)
x = [v[0] for v in verts] 
y = [v[1] for v in verts] 

p = figure(title="Baseline - Radar plot")
factors = ["DCF", "ROE", "ROI", "D/E", "P/E", "P/B"]
years = ['AAPL', 'PEER1', 'PEER2']
source = ColumnDataSource({'x':x + [centre ],'y':y + [1],'factors':factors})

p.line(x="x", y="y", source=source)
x =  [aaplOutlook.ratingDetailsDCFScore[0], aaplOutlook.ratingDetailsROEScore[0], aaplOutlook.ratingDetailsROAScore[0], 
               aaplOutlook.ratingDetailsDEScore[0], aaplOutlook.ratingDetailsPEScore[0], aaplOutlook.ratingDetailsPBScore[0]]
x2 =  [peerOutlook.ratingDetailsDCFScore[0], peerOutlook.ratingDetailsROEScore[0], peerOutlook.ratingDetailsROAScore[0], 
               peerOutlook.ratingDetailsDEScore[0], peerOutlook.ratingDetailsPEScore[0], peerOutlook.ratingDetailsPBScore[0]]
x3 =  [peerOutlook3.ratingDetailsDCFScore[0], peerOutlook3.ratingDetailsROEScore[0], peerOutlook3.ratingDetailsROAScore[0], 
               peerOutlook3.ratingDetailsDEScore[0], peerOutlook3.ratingDetailsPEScore[0], peerOutlook3.ratingDetailsPBScore[0]]

labels = LabelSet(x="x",y="y",text="factors",source=source)

p.add_layout(labels)

# example factor:
f1 = np.array(x)
f2 = np.array(x2)
f3 = np.array(x3)

#xt = np.array(x)
flist = [f1,f2,f3]
colors = ['blue','green','red', 'orange','purple']
for i in range(len(flist)):
    xt, yt = radar_patch(flist[i], theta, centre)
    p.patch(x=xt, y=yt, fill_alpha=0.15, fill_color=colors[i])
show(p)
