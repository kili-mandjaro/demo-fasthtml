from fasthtml.common import *
from uuid import uuid4
import json


def get_map_with_marker(lat, lon):

    data = [
        {
            "type": "scattermap",
            "lat": [lat],
            "lon": [lon],
            "mode": "markers",
            "marker": {
                "size": 20,
                "color": "#EE4823",
            },
            "text": ["Miam"],
        }
    ]

    layout = {
        "autosize": True,
        "hovermode": "closest",
        "margin": {"r": 0, "t": 0, "b": 0, "l": 0},
        "map": {
            "center": {
                "lat": lat,
                "lon": lon,
            },
            "bearing": 0,
            "zoom": 2,
            "pitch": 0,
        },
    }

    id_div = str(uuid4()).replace("-", "_")
    return Div(
        Div(id=id_div, cls="map"),
        Script(f"Plotly.newPlot('{id_div}', {json.dumps(data)}, {json.dumps(layout)})"),
    )
