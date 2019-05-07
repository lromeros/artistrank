import json

from flask import render_template
from app import app
from app.artistrank import generate_graph
from app.forms import SearchArtistForm


@app.route("/", methods=["GET", "POST"])
def index():
    form = SearchArtistForm()

    if form.validate_on_submit():
        graph_dict = generate_graph(form.search_artist.data)
        root_node = graph_dict.get("root_node")
        max_artist = graph_dict.get("max_node")
        min_artist = graph_dict.get("min_node")
        max_artist_edges = len(max_artist.out_artists) + len(max_artist.in_artists)
        min_artist_edges = len(min_artist.out_artists) + len(min_artist.in_artists)
        artist_graph = graph_dict.get("graph")

        return render_template(
            "render_graph.html",
            max_artist=max_artist,
            min_artist=min_artist,
            root_node=root_node,
            max_artist_edges=max_artist_edges,
            min_artist_edges=min_artist_edges,
            artist_graph=json.dumps(artist_graph),
        )
    else:
        return render_template("index.html", form=form)
