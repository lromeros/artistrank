import random
from typing import Callable, Dict, List, Any


class ArtistGraph:
    """ Description """

    def __init__(self, node: 'ArtistNode') -> None:
        """"""
        self.node = node
        self.max_pr_node = node
        self.min_pr_node = node
        self.id_to_nodes = {node.aid: self.node}
        self.all_node_ids = self.id_to_nodes.keys()
        self.page_rank_sum = 2

    def _set_node_lists(self, node_dict: Dict[str, 'ArtistNode']) -> None:
        self.id_to_nodes = node_dict
        self.all_node_ids = node_dict.keys()

    def _initialize_page_rank(self):
        initial_value = 1

        for node_id in self.all_node_ids:
            artist_node = self.id_to_nodes.get(node_id)
            artist_node.set_page_rank(initial_value)

    def populate(self, relational_func: Callable[[str], Dict], max_size: int = 10) -> None:
        """
        Generates a unique list of a given size of ArtistNodes related to each other.

        :param function relational_func: function based on which to build the graph
        :param int max_size: maximum number of artists to include in the graph

        """
        nodes_left = [self.node]
        examined_nodes: Dict[str, ArtistNode] = {}

        while len(nodes_left) > 0:
            current_node = nodes_left.pop()
            if current_node.aid not in examined_nodes and len(examined_nodes.keys()) < max_size:
                for artist_array in relational_func(current_node.aid):
                    related_node = examined_nodes.get(
                        artist_array.get('id')) or ArtistNode.create_artist_node_from_json(artist_array)

                    current_node.add_artist_out(related_node)
                    related_node.add_artist_in(current_node)
                    nodes_left.append(related_node)
            examined_nodes[current_node.aid] = current_node

        self._set_node_lists(examined_nodes)
        self._initialize_page_rank()

    def run_page_rank(self, d_factor: float) -> None:
        for i in range(150):  # TODO
            # while self.page_rank_sum > 1:
            self.page_rank_sum = self._run_iteration_page_rank(d_factor)

        self._update_max_min_nodes()

    def _run_iteration_page_rank(self, d_factor: float) -> float:
        # PR(A) = (1-d) + d (PR(T1)/C(T1) + ... + PR(Tn)/C(Tn))
        page_rank_sum = 0

        for node_id in self.all_node_ids:
            artist_node = self.id_to_nodes.get(node_id)
            if artist_node is not None:
                artist_node.generate_page_rank(d_factor)
                page_rank_sum += artist_node.page_rank

        return page_rank_sum

    def _update_max_min_nodes(self):
        self.max_pr_node = max(self.id_to_nodes.values(), key=lambda n: n.page_rank)
        self.min_pr_node = min(self.id_to_nodes.values(), key=lambda n: n.page_rank)

    def to_json(self):
        graph_json = {"nodes": [], "edges": []}

        for node_id in self.all_node_ids:
            artist_node = self.id_to_nodes.get(node_id)
            graph_json.get("nodes").append(artist_node.to_json(self.max_pr_node.page_rank, self.min_pr_node.page_rank))
            graph_json.get("edges").extend(artist_node.json_edges)

        return graph_json


class ArtistNode:
    """ Description """

    def __init__(self, artist_id: str, name: str, genres: List[str], img_href: str, popularity: int) -> None:
        """ """
        self.aid = artist_id
        self.name = name
        self.genres = genres
        self.img_href = img_href
        self.popularity = popularity
        self.in_artists: Dict[str, 'ArtistNode'] = {}  # id to node, artists pointing to this artist
        self.out_artists: Dict[str, 'ArtistNode'] = {}  # id to node, artists this artist points to
        self.json_edges: Dict[str, Any] = []
        self.page_rank = 0

    def add_artist_in(self, in_artist: 'ArtistNode') -> None:
        """ """
        self.in_artists[in_artist.aid] = in_artist

    def add_artist_out(self, out_artist: 'ArtistNode') -> None:
        """ """
        self.out_artists[out_artist.aid] = out_artist
        self._add_json_edge(out_artist.aid)

    def set_page_rank(self, page_rank: float):
        self.page_rank = page_rank

    def _in_artists_page_rank(self):
        page_rank_val = 0

        for in_artist in self.in_artists.values():
            page_rank_val += (in_artist.page_rank / len(in_artist.out_artists))

        return page_rank_val

    def generate_page_rank(self, d_factor: float) -> None:
        # PR(A) = (1-d) + d (PR(T1)/C(T1) + ... + PR(Tn)/C(Tn))
        page_rank_val = (1 - d_factor) + d_factor * self._in_artists_page_rank()
        self.page_rank = page_rank_val

    # def to_json(self, size_scale_factor: float):
    def to_json(self, min_pr: int, max_pr: int):
        min_px = 10  # TODO
        max_px = 50
        # y = [x(min pixels - max pixels) + (min PR * max pixels) - (min pixels * max PR)] /  min PR - max PR
        pr_relative_size = round((self.page_rank * (min_px - max_px) + (min_pr * max_px)
                                  - (min_px * max_pr)) / (min_pr - max_pr))
        print(self.page_rank, pr_relative_size)
        return {
            "id": self.aid,
            "label": self.name,
            "x": random.randint(1, 10),
            "y": random.randint(1, 10),
            "size": 100 - pr_relative_size,
            "color": "#EE651D"
        }

    def _add_json_edge(self, target_id: str):
        edge_dict = {
            "id": self.aid + target_id,
            "source": self.aid,
            "target": target_id
        }
        self.json_edges.append(edge_dict)

    @staticmethod
    def create_artist_node_from_json(artist_array):
        if len(artist_array.get('images')) > 0:
            img_href = artist_array.get('images')[0].get('url')
        else:
            img_href = 'https://via.placeholder.com/450'

        return ArtistNode(artist_array.get('id'), artist_array.get('name'), artist_array.get('genres'),
                          img_href, artist_array.get('popularity'))
