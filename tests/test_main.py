"""Unit tests for TODO"""

from app.artistgraph import ArtistGraph, ArtistNode
import pytest

default_node = ArtistNode("6lcwlkAjBPSKnFBZjjZFJs", "(Sandy) Alex G", 54)
default_graph = ArtistGraph(default_node)


def mock_get_related_artists(artist_id):
    with open("tests/files/mock_related_dict.txt", "r") as inf:
        mock_spotify_related = eval(inf.read())

    print(mock_spotify_related is None)
    return mock_spotify_related.get(artist_id)


default_graph.populate(relational_func=mock_get_related_artists)


def test_populate_artist_graph_not_empty():
    """."""
    assert len(default_graph.all_node_ids) == 399


def test_populate_artist_graph_no_repeats():
    """."""
    assert len(default_graph.all_node_ids) == len(set(default_graph.all_node_ids))


def test_populate_artist_graph_no_artist_in_repeats():
    """."""
    for artist_node in default_graph.id_to_nodes.values():
        in_list_ids = artist_node.in_artists.keys()
        assert len(in_list_ids) == len(set(in_list_ids))


def test_populate_artist_graph_no_artist_out_repeats():
    """."""
    for artist_node in default_graph.id_to_nodes.values():
        out_list_ids = artist_node.out_artists.keys()
        assert len(out_list_ids) == len(set(out_list_ids))


default_graph.run_page_rank(10, 0.85)


def test_page_rank_adds_to_one():
    """."""
    total_page_rank = 0

    for artist_node in default_graph.id_to_nodes.values():
        total_page_rank = artist_node.page_rank

    assert total_page_rank == 1
