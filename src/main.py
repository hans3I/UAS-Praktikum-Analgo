# main.py

import time

from load_data import (
    load_distance_matrix,
    load_customers,
    load_scenario
)

from algorithms.heuristic import (
    greedy_nearest_neighbor,
    validate_route,
    print_route_summary
)

from algorithms.exact import (
    exact_tsp,
    print_exact_route_summary
)

from scenario import calculate_cost

def run_heuristic(distance_matrix):
    """
    Menjalankan algoritma heuristik dan mengukur waktu eksekusi.
    """

    start_time = time.perf_counter()

    route, total_distance = greedy_nearest_neighbor(
        distance_matrix
    )

    end_time = time.perf_counter()

    execution_time_ms = (
        end_time - start_time
    ) * 1000

    return (
        route,
        total_distance,
        execution_time_ms
    )


def run_exact(distance_matrix):
    """
    Menjalankan algoritma exact dan mengukur waktu eksekusi.
    """

    start_time = time.perf_counter()

    route, total_distance = exact_tsp(
        distance_matrix
    )

    end_time = time.perf_counter()

    execution_time_ms = (
        end_time - start_time
    ) * 1000

    return (
        route,
        total_distance,
        execution_time_ms
    )


def main():

    print("=" * 50)
    print("LAST MILE DELIVERY OPTIMIZATION")
    print("=" * 50)

    # =====================
    # LOAD DATA
    # =====================

    distance_matrix = load_distance_matrix()
    customers = load_customers()

    # Ganti menjadi "crisis" untuk skenario krisis
    scenario = load_scenario("subsidy")

    print("\nScenario:")
    print(scenario)

    # =====================
    # GREEDY
    # =====================

    print("\nMenjalankan Greedy Nearest Neighbor...")

    route, total_distance, execution_time = run_heuristic(
        distance_matrix
    )

    is_valid = validate_route(
        route,
        len(distance_matrix)
    )

    print_route_summary(
        route,
        total_distance
    )

    print(
        f"Waktu Eksekusi: "
        f"{execution_time:.4f} ms"
    )

    print(
        f"Route Valid: "
        f"{is_valid}"
    )

    cost_result = calculate_cost(
        total_distance,
        execution_time,
        scenario
    )

    print("\n=== ANALISIS EKONOMI ===")

    print(
        f"BBM Digunakan: "
        f"{cost_result['fuel_used']:.2f} liter"
    )

    print(
        f"Biaya BBM: "
        f"Rp {cost_result['fuel_cost']:,.0f}"
    )

    print(
        f"Biaya Server: "
        f"Rp {cost_result['server_cost']:,.0f}"
    )

    print(
        f"Total Biaya: "
        f"Rp {cost_result['total_cost']:,.0f}"
    )

    # =====================
    # EXACT (BACKTRACKING)
    # =====================

    print("\nMenjalankan Exact (Backtracking with Pruning)...")

    route_exact, total_distance_exact, execution_time_exact = run_exact(
        distance_matrix
    )

    is_valid_exact = validate_route(
        route_exact,
        len(distance_matrix)
    )

    print_exact_route_summary(
        route_exact,
        total_distance_exact
    )

    print(
        f"Waktu Eksekusi: "
        f"{execution_time_exact:.4f} ms"
    )

    print(
        f"Route Valid: "
        f"{is_valid_exact}"
    )

    # =====================
    # DATA TAMBAHAN
    # =====================

    print("\nJumlah Lokasi:")
    print(len(customers))

    print("\nSelesai.")


if __name__ == "__main__":
    main()