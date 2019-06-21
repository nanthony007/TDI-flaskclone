from flask import Flask, render_template, request
from bokeh.plotting import figure
from bokeh.embed import components
import quandl
import pandas as pd

quandl.ApiConfig.api_key = "vnujqUCqUbDqwaHEFxEk"

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def show_dashboard():
    if request.method == "POST":
        text = request.form['tickerInput']
        processed_text = text.upper()

        data = quandl.get_table('WIKI/PRICES', qopts = { 'columns': ['ticker', 'date', 'adj_close'] },
            ticker = processed_text, date = { 'gte': '2018-01-01', 'lte': '2018-02-01' }, paginate=True)
        data = data.set_index('date')

        plot = figure(plot_height=300, plot_width=700,
            title='Adjusted Close Price of ' + processed_text + ' for January 2018',
            x_axis_label='Day', x_axis_type='datetime',
            y_axis_label='Adjusted Close')
        plot.line(data.index, data.adj_close)
        script, div = components(plot)
        return render_template('index.html', div=div, script=script)
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
