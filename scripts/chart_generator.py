import pandas as pd
from bokeh.io import show, output_file, output_notebook
from bokeh.models import  ColumnDataSource, Span
from bokeh.plotting import figure

def linebarplot(year, woc, mh, wo_pmt, wo_rep):
    data = mh.merge(wo_pmt, on=['workcenter', 'year', 'month'])
    data = data.merge(wo_rep, on=['workcenter', 'year', 'month'])
    data = data[(data['workcenter'] == woc) & (data['year'] == year)].copy()
    x_ = [str(month) for month in data['month'].tolist()]
    y_mh = data['%_mhreal'].tolist()
    y_wo_p = data['%_wopmt'].tolist()
    y_wo_r = data['%_worep'].tolist()

    mh_src = ColumnDataSource(data = dict(x = x_, y = y_mh))
    wop_src = ColumnDataSource(data = dict(x = x_, y = y_wo_p))
    wor_src = ColumnDataSource(data = dict(x = x_, y = y_wo_r))

    p = figure(x_range = x_, plot_height = 400, title = '%_produktif vs %_wopmt vs %_worepair', toolbar_location = 'right', x_axis_label = 'month', y_axis_label = 'percent of realization')
    p.vbar(x = 'x', top = 'y', width = 0.9, source = mh_src, legend = 'MH')
    p.line(x = x_, y = y_wo_p, color = 'red', line_width = 2, legend = 'WO PMT')
    p.circle(x = 'x', y = 'y', fill_color = 'white', source = wop_src)
    p.line(x = x_, y = y_wo_r, color = 'blue', line_width = 2, legend = 'WO PJOL')
    p.circle(x = 'x', y = 'y', fill_color = 'white', source = wor_src)

    p.legend.location = 'bottom_right'
    p.legend.click_policy = 'hide'

    p.xgrid.grid_line_color = None
    p.y_range.start = 0

    target_line = Span(location = 70, dimension = 'width', line_color = 'red', line_dash = 'dashed', line_width = 2)
    p.add_layout(target_line)

    output_notebook()

    return show(p)