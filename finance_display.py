from datetime import timedelta
from bokeh.plotting import figure, output_file, show
from bokeh.layouts import column, row
from bokeh.models import Label, Title, NumeralTickFormatter, ColumnDataSource

colors = ['red', 'blue', 'green', 'yellow', 'purple', 'orange']

def finance_sort_key(f):
    return f["date"]


def append_totals(totals, totals_list):
    for k,v in totals.items():
        if not k in totals_list:
            totals_list[k] = []
        totals_list[k].append(v)


def generate_chart(finances):
    finances.sort(key=finance_sort_key)

    dates_list = []
    totals_list = {}
    totals = {}

    date = finances[0]['date']

    # This algorithm is meant to handle multiple exchanges on the same day
    # so if it doesn't do that, then there's a bug
    for f in finances:
        # write all dates' totals up to this entry's date
        while date < f['date']:
            dates_list.append(date)
            append_totals(totals, totals_list)
            date += timedelta(days=1)
        
        # work out all finance changes for this entry
        account = str(f['account'])
        if not account in totals:
            totals[account] = 0
        if f['is_checkpoint']:
            # TODO: track unaccounted for expenses
            totals[account] = f['amount']
        else:
            totals[account] += f['amount']

    # Input the last date, which should only be one day after the previous entry
    date += timedelta(days=1)
    dates_list.append(date)
    append_totals(totals, totals_list)
    
    # Now draw the charts...
    history = figure(
        title='finances',
        x_axis_type='datetime',
        x_axis_label='date',
        y_axis_label='¥',
        y_axis_type='linear',
    )

    color_idx = 0
    for k in totals_list.keys():
        history.line(dates_list, totals_list[k],
                     color=colors[color_idx], legend=k, line_width=2)
        color_idx = (color_idx + 1) % len(colors)
    history.yaxis.formatter = NumeralTickFormatter(format="¥000,000,000")

    show(row(history))
