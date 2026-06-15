# exact.py

from typing import List, Tuple

def exact_tsp(
    distance_matrix: List[List[float]],
    start_node: int = 0
) -> Tuple[List[int], float]:
    """
    Algoritma Exact (Backtracking with Pruning) untuk Traveling Salesperson Problem (TSP).

    Strategi:
    Mencari rute terbaik menggunakan rekursi dengan memotong cabang (pruning)
    jika jarak sementara sudah lebih besar atau sama dengan jarak minimum yang ditemukan sejauh ini.

    Parameters:
        distance_matrix : matriks jarak
        start_node      : node awal (hub)

    Returns:
        best_route      : urutan perjalanan dengan jarak terpendek
        min_distance    : total jarak tempuh terpendek
    """
    total_nodes = len(distance_matrix)
    visited = [False] * total_nodes
    
    best_route = []
    min_distance = float('inf')
    
    def solve(current_node: int, visited_count: int, current_distance: float, current_path: List[int]):
        nonlocal min_distance, best_route
        
        # Pruning: Jika jarak saat ini sudah lebih besar atau sama dengan min_distance,
        # maka tidak perlu melanjutkan eksplorasi rute pada cabang ini.
        if current_distance >= min_distance:
            return
            
        # Base case: Semua node telah dikunjungi
        if visited_count == total_nodes:
            # Tambahkan jarak kembali ke start_node (hub)
            final_distance = current_distance + distance_matrix[current_node][start_node]
            if final_distance < min_distance:
                min_distance = final_distance
                best_route = list(current_path) + [start_node]
            return
            
        # Eksplorasi node-node selanjutnya yang belum dikunjungi
        for next_node in range(total_nodes):
            if not visited[next_node]:
                # Tandai sudah dikunjungi dan masukkan ke path
                visited[next_node] = True
                current_path.append(next_node)
                
                # Pemanggilan rekursif
                solve(
                    next_node, 
                    visited_count + 1, 
                    current_distance + distance_matrix[current_node][next_node], 
                    current_path
                )
                
                # Backtrack: kembalikan state untuk eksplorasi cabang lain
                current_path.pop()
                visited[next_node] = False

    # Inisialisasi awal
    visited[start_node] = True
    solve(start_node, 1, 0.0, [start_node])
    
    return best_route, min_distance

def print_exact_route_summary(
    route: List[int],
    total_distance: float
) -> None:
    """
    Menampilkan hasil rute exact ke terminal.
    """
    print("\n=== Hasil Exact (Backtracking with Pruning) ===")
    print("Rute:", " -> ".join(map(str, route)))
    print(f"Jarak: {total_distance:.2f} km")
