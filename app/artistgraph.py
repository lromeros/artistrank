import random
from typing import Callable, Dict, List, Any


class ArtistGraph:
    """Data structure representing a network of related Spotify Artists."""

    def __init__(self, node: "ArtistNode") -> None:
        """Create an ArtistGraph object with the given ArtistNode.

        :param ArtistNode node: root ArtistNode for this ArtistGraph.
        :var ArtistNode max_pr_node: the ArtistNode in this ArtistGraph with the highest
                                     calculated PageRank value.
        :var ArtistNode min_pr_node: the ArtistNode in this ArtistGraph with the lowest
                                     calculated PageRank value.
        :var Dict{str: ArtistNode]  id_to_nodes: a mapping the id of every ArtistNode id
                                    in this ArtistGraph to their ArtistNode objects.
        :var List[ArtistNode] all_node_ids: All the ArtistNode ids in this ArtistGraph.
        :var float page_rank_sum: a value representing the sum of the PageRank value of
                                  all ArtistNodes in this ArtistGraph.
        """
        self.node = node
        self.max_pr_node = node
        self.min_pr_node = node
        self.id_to_nodes = {node.aid: self.node}
        self.all_node_ids = self.id_to_nodes.keys()
        self.page_rank_sum = 2.0

    def _set_node_lists(self, node_dict: Dict[str, "ArtistNode"]) -> None:
        self.id_to_nodes = node_dict
        self.all_node_ids = node_dict.keys()

    def _initialize_page_rank(self):
        initial_value = 1

        for node_id in self.all_node_ids:
            artist_node = self.id_to_nodes.get(node_id)
            artist_node.set_page_rank(initial_value)

    def populate(self, relational_func: Callable[[str], Dict], max_size: int = 10) -> None:
        """
        Populates this ArtistGraph by working through a queue of ArtistNodes, nodes_left, to add
        to the graph, until there are no ArtistNodes left. Spotify related artists are found for
        each ArtistNodes in nodes_left, and ArtistNode objects are created for each of those
        related artists, and then added to nodes_left. Once an ArtistNode's related artists have
        been found and added to nodes_left, it is considered 'examined', and it is added to
        examined_nodes, which is a dict mapping ArtistNode id's to ArtistNode objects. This process
        occurs until nodes_left is empty or examined_nodes reaches a maximum number of ArtistNodes.

        :param function relational_func: function based on which to build the graph,
                        takes a Spotify artist ID, and returns a JSON array of Spotify artists.
        :param int max_size: maximum number of artists to include in the graph.

        """
        nodes_left = [self.node]
        examined_nodes: Dict[str, ArtistNode] = {}

        while len(nodes_left) > 0:
            current_node = nodes_left.pop()
            if current_node.aid not in examined_nodes and len(examined_nodes.keys()) < max_size:
                for artist_array in relational_func(current_node.aid):
                    related_node = examined_nodes.get(
                        artist_array.get("id")
                    ) or ArtistNode.create_artist_node_from_json(artist_array)

                    current_node.add_artist_out(related_node)
                    related_node.add_artist_in(current_node)
                    nodes_left.append(related_node)
            examined_nodes[current_node.aid] = current_node

        self._set_node_lists(examined_nodes)
        self._initialize_page_rank()

    def run_page_rank(self, iterations: int, d_factor: float) -> None:
        """
        Performs the PageRank algorithm the given number of times.

        :param int iterations: the number of iterations for which to run PageRank on this graph.
        :param float d_factor: the damping factor, in PageRank, the probability, at any step,
                               that a person will continue to click through links.
        """
        for i in range(iterations):
            self.page_rank_sum = self._run_iteration_page_rank(d_factor)

        self._update_max_min_nodes()

    def _run_iteration_page_rank(self, d_factor: float) -> float:
        page_rank_sum = 0.0

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
            graph_json.get("nodes").append(
                artist_node.to_json(self.max_pr_node.page_rank, self.min_pr_node.page_rank)
            )
            graph_json.get("edges").extend(artist_node.json_edges)

        return graph_json


class ArtistNode:
    """Data structure representing an individual Spotify Artist."""

    def __init__(
        self, artist_id: str, name: str, genres: List[str], img_href: str, popularity: int
    ) -> None:
        """ Create an ArtistNode object to represent a Spotify artist, ideally parameters
        are generated by querying the Spotify Web API.

        :param str artist_id: a unique artist ID.
        :param str name: this artist's name.
        :param List[str] genres: this artist's list of genre names.
        :param str  img_href: a url linking to an image of this Spotify artist.
        :param int popularity: this artist's numerical popularity value.
        :var Dict in_artists: a mapping of artist ID to ArtistNode, a collection of other artists
                              that list this artist as an artist they are related to.
        :var Dict out_artists: a mapping of artist ID to ArtistNode, a collection of other artists
                              this artist is related to.
        :var Dict json_edges: a json representation of out_artists.
        :var float page_rank: this artist's calculated PageRank.

        """
        self.aid = artist_id
        self.name = name
        self.genres = genres
        self.img_href = img_href
        self.popularity = popularity
        self.in_artists: Dict[str, "ArtistNode"] = {}
        self.out_artists: Dict[str, "ArtistNode"] = {}
        self.json_edges: List[Dict] = []
        self.page_rank = 0.0

    def add_artist_in(self, in_artist: "ArtistNode") -> None:
        self.in_artists[in_artist.aid] = in_artist

    def add_artist_out(self, out_artist: "ArtistNode") -> None:
        self.out_artists[out_artist.aid] = out_artist
        self._add_json_edge(out_artist.aid)

    def set_page_rank(self, page_rank: float):
        self.page_rank = page_rank

    def _in_artists_page_rank(self):
        page_rank_val = 0

        for in_artist in self.in_artists.values():
            page_rank_val += in_artist.page_rank / len(in_artist.out_artists)

        return page_rank_val

    def generate_page_rank(self, d_factor: float) -> None:
        page_rank_val = (1 - d_factor) + d_factor * self._in_artists_page_rank()
        self.page_rank = page_rank_val

    def to_json(self, min_pr: int, max_pr: int):
        min_px = 10
        max_px = 50

        pr_relative_size = round(
            (self.page_rank * (min_px - max_px) + (min_pr * max_px) - (min_px * max_pr))
            / (min_pr - max_pr)
        )
        return {
            "id": self.aid,
            "label": self.name,
            "x": random.randint(1, 10),
            "y": random.randint(1, 10),
            "size": 100 - pr_relative_size,
            "color": "#EE651D",
        }

    def _add_json_edge(self, target_id: str):
        edge_dict = {"id": self.aid + target_id, "source": self.aid, "target": target_id}
        self.json_edges.append(edge_dict)

    @staticmethod
    def create_artist_node_from_json(artist_array):
        if len(artist_array.get("images")) > 0:
            img_href = artist_array.get("images")[0].get("url")
        else:
            img_href = "https://via.placeholder.com/450"

        return ArtistNode(
            artist_array.get("id"),
            artist_array.get("name"),
            artist_array.get("genres"),
            img_href,
            artist_array.get("popularity"),
        )
