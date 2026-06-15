# heuristic.py

# Import tipe data untuk type hinting
from typing import List, Tuple


def find_nearest_unvisited(
    current_node: int,
    visited: List[bool],
    distance_matrix: List[List[float]]
) -> int:
    """
    Mencari node terdekat yang belum dikunjungi.
    
    Parameters:
        current_node : posisi kurir saat ini
        visited      : daftar status node yang sudah dikunjungi
        distance_matrix : matriks jarak antar node

    Returns:
        node terdekat yang belum dikunjungi
    """

    # Nilai awal
    nearest_node = -1
    nearest_distance = float("inf")

    # Cek seluruh node dalam graf
    for node in range(len(distance_matrix)):

        # Hanya pertimbangkan node yang belum dikunjungi
        if not visited[node]:

            # Ambil jarak dari node saat ini ke kandidat node
            distance = distance_matrix[current_node][node]

            # Jika lebih dekat dari kandidat sebelumnya
            if distance < nearest_distance:
                nearest_distance = distance
                nearest_node = node

    return nearest_node


def calculate_route_distance(
    route: List[int],
    distance_matrix: List[List[float]]
) -> float:
    """
    Menghitung total jarak suatu rute.

    Parameters:
        route : urutan node yang dilalui
        distance_matrix : matriks jarak

    Returns:
        total jarak rute
    """

    total_distance = 0

    # Menjumlahkan jarak antar node berurutan
    for i in range(len(route) - 1):

        from_node = route[i]
        to_node = route[i + 1]

        total_distance += distance_matrix[from_node][to_node]

    return total_distance


def greedy_nearest_neighbor(
    distance_matrix: List[List[float]],
    start_node: int = 0
) -> Tuple[List[int], float]:
    """
    Algoritma Greedy Nearest Neighbor.

    Strategi:
    Selalu memilih node terdekat yang belum dikunjungi.

    Parameters:
        distance_matrix : matriks jarak
        start_node      : node awal (hub)

    Returns:
        route           : urutan perjalanan
        total_distance  : total jarak tempuh
    """

    # Jumlah seluruh node
    total_nodes = len(distance_matrix)

    # Menandai node yang sudah dikunjungi
    visited = [False] * total_nodes

    # Rute dimulai dari hub
    route = [start_node]

    current_node = start_node
    visited[start_node] = True

    # Kunjungi seluruh node satu per satu
    for _ in range(total_nodes - 1):

        # Cari node terdekat berikutnya
        next_node = find_nearest_unvisited(
            current_node,
            visited,
            distance_matrix
        )

        # Tambahkan ke rute
        route.append(next_node)

        # Tandai sudah dikunjungi
        visited[next_node] = True

        # Pindah ke node baru
        current_node = next_node

    # Setelah semua customer selesai,
    # kembali ke hub
    route.append(start_node)

    # Hitung total jarak rute
    total_distance = calculate_route_distance(
        route,
        distance_matrix
    )

    return route, total_distance


def validate_route(
    route: List[int],
    total_nodes: int
) -> bool:
    """
    Memastikan semua node dikunjungi tepat satu kali.

    Parameters:
        route : rute hasil algoritma
        total_nodes : jumlah node dalam graf

    Returns:
        True jika valid
        False jika ada duplikasi atau node terlewat
    """

    # Abaikan node terakhir karena itu adalah
    # perjalanan kembali ke hub
    visited_customers = route[:-1]

    # Jika jumlah elemen unik sama dengan jumlah node,
    # berarti semua node dikunjungi sekali
    return len(set(visited_customers)) == total_nodes


def print_route_summary(
    route: List[int],
    total_distance: float
) -> None:
    """
    Menampilkan hasil rute ke terminal.
    """

    print("\n=== Hasil Greedy ===")

    # Menampilkan urutan node
    print("Rute:", " -> ".join(map(str, route)))

    # Menampilkan total jarak
    print(f"Jarak: {total_distance:.2f} km")
