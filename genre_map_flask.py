import locale
locale.setlocale(locale.LC_ALL, '')
import folium
from flask import Flask
from folium.plugins import marker_cluster
from pandas import read_csv

app = Flask(__name__)


@app.route('/')
def index():
    m = folium.Map(location=[6.5, 3.4],
                    zoom_start=3)
    
    data = read_csv('top_by_oixl_20211107.csv')

    popups = [
        folium.Popup(
            f"<p style='white-space:nowrap'>{loc} ({ctr}) is the modern home of: <strong>{ge}</strong><br/>\
            1 in {int(round(oixl,0))} artists from {loc} is a {ge} artist (one for every ~{ppa:n} people)<br/><br/>\
            <em>In this dataset, there are…\
            <ul><li>{ats} {ge} artists from {loc} ({round(pct * 100, 2):.1f}% of all {ge} artists)\
            <li>{lac} artists from {loc} in total\
            <li>{gac} {ge} artists in total</em><ul></p>"
        ) for loc, lt, pop, ctr, lat, lon, ge, ats, pct, oixl, oixg, ppa, gac, glc, lac, lgc in data.values
    ]

    cluster = marker_cluster.MarkerCluster(data[['lat','lon']].values,popups)

    m.add_child(cluster)
    
    pat = '<div style="width:100%;"><div style="position:relative;width:100%;height:0;padding-bottom:60%;">'
    repl = '<div style="width:100%;height:100%"><div style="position:relative;width:100%;height:100%;padding-bottom:0;">'

    html = m._repr_html_().replace(pat,repl)

    pat = '3Cmeta%20name%3D%22viewport%22%20content%3D%22width%3Ddevice-width%2C%0A'
    repl = '3Cmeta%20name%3D%22viewport%22%20content%3D%22width%3Ddevice-width%2C%20height%3Ddevice-height%2C%0A'

    return html.replace(pat,repl)


if __name__ == '__main__':
    app.run(debug=True)