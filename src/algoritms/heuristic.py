# heuristic.py

from typing import List, Tuple


def find_nearest_unvisited(
    current_node: int,
    visited: List[bool],
    distance_matrix: List[List[float]]
) -> int:
    """
    Mencari node terdekat yang belum dikunjungi.
    """
    pass


def calculate_route_distance(
    route: List[int],
    distance_matrix: List[List[float]]
) -> float:
    """
    Menghitung total jarak suatu rute.
    """
    pass


def greedy_nearest_neighbor(
    distance_matrix: List[List[float]],
    start_node: int = 0
) -> Tuple[List[int], float]:
    """
    Algoritma Greedy Nearest Neighbor.

    Returns:
        route: urutan node yang dikunjungi
        total_distance: total jarak rute
    """
    pass


def validate_route(
    route: List[int],
    total_nodes: int
) -> bool:
    """
    Memastikan semua customer dikunjungi tepat satu kali.
    """
    pass


def print_route_summary(
    route: List[int],
    total_distance: float
) -> None:
    """
    Menampilkan hasil rute ke terminal.
    """
    pass
