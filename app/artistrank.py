from app.artistgraph import ArtistGraph, ArtistNode

from app import spot


def generate_graph(artist_name: str):
    spot_api = spot.SpotifyAPI()

    if spot_api.token is not None:
        artist_json = spot_api.verify_valid_artist(artist_name)
        if len(artist_json.values()) > 0:
            artist_graph = ArtistGraph(
                ArtistNode.create_artist_node_from_json(artist_json)
            )
            artist_graph.populate(spot_api.get_related_artists)
            artist_graph.run_page_rank(150, 0.85)
            return {
                "max_node": artist_graph.max_pr_node,
                "min_node": artist_graph.min_pr_node,
                "root_node": artist_graph.node,
                "graph": artist_graph.to_json(),
            }
        else:  # TODO
            print("Not a valid artist")
    else:
        print("request not authorized")

    return None
