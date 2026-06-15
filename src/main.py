import time

# Import fungsi load data dari load_data.py
from load_data import (
    load_distance_matrix,
    load_customers,
    load_scenario
)

# Import fungsi algoritma dari algorithms/heuristic.py
from algorithms.heuristic import (
    greedy_nearest_neighbor,
    validate_route,
    print_route_summary
)


from fuel_cost import calculate_route_fuel_cost
from tco_calculator import calculate_tco


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


def main():

    print("=" * 50)
    print("LAST MILE DELIVERY OPTIMIZATION")
    print("=" * 50)

    # =====================
    # LOAD DATA
    # =====================
    distance_matrix = load_distance_matrix()
    customers = load_customers()

    # Ganti menjadi "crisis" untuk menguji skenario krisis ekonomi
    scenario_name = "subsidy" 
    scenario = load_scenario(scenario_name)

    print(f"\nSkenario Aktif  : {scenario_name.upper()}")
    print(f"Harga BBM       : Rp {scenario['fuel_price']:,}/liter")
    print(f"Biaya Komputasi : Rp {scenario['server_cost_per_ms']:,}/ms")

    # =====================
    # ALGORITMA A: GREEDY (HEURISTIK)
    # =====================
    print("\n" + "-" * 40)
    print("MENJALANKAN GREEDY NEAREST NEIGHBOR...")
    print("-" * 40)

    route, total_distance, execution_time = run_heuristic(
        distance_matrix
    )

    is_valid = validate_route(
        route,
        len(distance_matrix)
    )

    # Menampilkan urutan rute dan total jarak tempuh fisik
    print_route_summary(
        route,
        total_distance
    )

    print(f"Waktu Eksekusi  : {execution_time:.4f} ms")
    print(f"Status Rute     : {'VALID' if is_valid else 'TIDAK VALID'}")

    # =====================
    # KALKULASI FINANSIAL & TCO (BAGIAN ANDA)
    # =====================
    print("\n" + "-" * 40)
    print("ANALISIS BIAYA & TOTAL COST OF OWNERSHIP")
    print("-" * 40)

    # 1. Menghitung total pengeluaran bensin berdasarkan perubahan beban paket
    fuel_cost = calculate_route_fuel_cost(
        route,
        distance_matrix,
        customers,
        scenario["fuel_price"]
    )

    # 2. Menghitung akumulasi TCO (Biaya BBM + Biaya Server)
    tco_result = calculate_tco(
        fuel_cost,
        execution_time,
        scenario["server_cost_per_ms"]
    )

    # 3. Menampilkan metrik finansial dasar ke Terminal sesuai batasan output
    print(f"Total Biaya BBM      : Rp {tco_result['fuel_cost']:,.2f}")
    print(f"Total Biaya Server   : Rp {tco_result['computation_cost']:,.2f}")
    print(f"Total TCO (Heuristic): Rp {tco_result['total_tco']:,.2f}")

    # =====================
    # DATA DIAGNOSTIK
    # =====================
    print("\n" + "=" * 50)
    print(f"Total Titik Lokasi Terbaca: {len(customers)} (Termasuk Hub)")
    print("Selesai.")


if __name__ == "__main__":
    main()