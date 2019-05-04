import json

from app import app
from app.artistrank import generate_graph
from app.forms import SearchArtistForm
from flask import render_template


@app.route('/', methods=['GET', 'POST'])
def index():
    form = SearchArtistForm()
    if form.validate_on_submit():
        graph_dict = generate_graph(form.search_artist.data)
        root_node = graph_dict.get('root_node')
        max_artist = graph_dict.get('max_node')
        min_artist = graph_dict.get('min_node')
        max_artist_edges = len(max_artist.out_artists) + len(max_artist.in_artists)
        min_artist_edges = len(min_artist.out_artists) + len(min_artist.in_artists)
        artist_graph = graph_dict.get('graph')

        # artist_blurb = "hey baebay"
        # artist_graph = {
        #     "nodes": [
        #         {
        #             "id": "n0",
        #             "label": "A node",
        #             "x": 0,
        #             "y": 0,
        #             "size": 3
        #         },
        #         {
        #             "id": "n1",
        #             "label": "Another node",
        #             "x": 3,
        #             "y": 1,
        #             "size": 2
        #         },
        #         {
        #             "id": "n2",
        #             "label": "And a last one",
        #             "x": 1,
        #             "y": 3,
        #             "size": 1
        #         }
        #     ],
        #     "edges": [
        #         {
        #             "id": "e0",
        #             "source": "n0",
        #             "target": "n1"
        #         },
        #         {
        #             "id": "e1",
        #             "source": "n1",
        #             "target": "n2"
        #         },
        #         {
        #             "id": "e2",
        #             "source": "n2",
        #             "target": "n0"
        #         }
        #     ]
        # }

        return render_template('render_graph.html', max_artist=max_artist, min_artist=min_artist, root_node=root_node,
                               max_artist_edges=max_artist_edges, min_artist_edges=min_artist_edges, artist_graph=json.dumps(artist_graph))
    else:
        return render_template('index.html', form=form)

