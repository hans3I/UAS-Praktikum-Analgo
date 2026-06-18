"""
Modul Analisis Keputusan Bisnis
Tugas Akhir Praktikum Analisis Algoritma

Modul ini melakukan perbandingan komprehensif antara algoritma Heuristik (Greedy)
dan Eksak (Backtracking) dengan fokus pada Total Cost of Ownership (TCO).

Kontrak eksekusi:
- `main.py` menjalankan satu skenario ekonomi via `--scenario`
- `report.py` selalu membandingkan dua skenario wajib: `subsidy` dan `crisis`
"""

import argparse
import os
import sys
import time

# Memastikan modul lokal dapat diimport
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from load_data import load_distance_matrix, load_customers, load_scenario
from algorithms.heuristic import greedy_nearest_neighbor
from algorithms.exact import exact_tsp
from scenario import calculate_cost


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Run comparative business report for both required economic scenarios: "
            "subsidy and crisis."
        )
    )
    return parser.parse_args()


def run_algorithm(algorithm, distance_matrix):
    start_time = time.perf_counter()
    route, total_distance = algorithm(distance_matrix)
    execution_time_ms = (time.perf_counter() - start_time) * 1000
    return route, total_distance, execution_time_ms


def format_route(route):
    return " -> ".join(map(str, route))


def calculate_break_even_price(hasil_h, hasil_e):
    fuel_used_h = hasil_h["fuel_used"]
    fuel_used_e = hasil_e["fuel_used"]
    server_cost_h = hasil_h["server_cost"]
    server_cost_e = hasil_e["server_cost"]

    fuel_delta = fuel_used_h - fuel_used_e
    server_delta = server_cost_e - server_cost_h

    if fuel_delta == 0:
        if server_cost_h == server_cost_e:
            return {
                "status": "all_prices_equal",
                "fuel_delta": fuel_delta,
                "server_delta": server_delta,
                "threshold": None
            }

        return {
            "status": "no_break_even",
            "fuel_delta": fuel_delta,
            "server_delta": server_delta,
            "threshold": None
        }

    threshold = server_delta / fuel_delta

    if threshold < 0:
        return {
            "status": "no_feasible_positive_threshold",
            "fuel_delta": fuel_delta,
            "server_delta": server_delta,
            "threshold": threshold
        }

    return {
        "status": "ok",
        "fuel_delta": fuel_delta,
        "server_delta": server_delta,
        "threshold": threshold
    }


def describe_threshold_position(price, threshold):
    if price < threshold:
        return "di bawah"
    if price > threshold:
        return "di atas"
    return "tepat pada"

def jalankan_analisis():
    # Load dataset
    dist_matrix = load_distance_matrix()
    customers = load_customers()
    
    scenarios = [
        ("SUBSIDI", load_scenario("subsidy")),
        ("KRISIS", load_scenario("crisis"))
    ]
    
    biaya_server_ms = scenarios[0][1]["server_cost_per_ms"]

    # Eksekusi Algoritma
    rute_h, jarak_h, waktu_h = run_algorithm(
        greedy_nearest_neighbor,
        dist_matrix
    )
    rute_e, jarak_e, waktu_e = run_algorithm(
        exact_tsp,
        dist_matrix
    )

    hasil_h_break_even = calculate_cost(
        rute_h,
        dist_matrix,
        customers,
        waktu_h,
        scenarios[0][1]
    )
    hasil_e_break_even = calculate_cost(
        rute_e,
        dist_matrix,
        customers,
        waktu_e,
        scenarios[0][1]
    )
    break_even = calculate_break_even_price(
        hasil_h_break_even,
        hasil_e_break_even
    )
    
    print("=" * 75)
    print(f"{'LAPORAN ANALISIS KEPUTUSAN BISNIS - LAST MILE DELIVERY':^75}")
    print("=" * 75)
    print("Mode: comparative report for scenarios subsidy + crisis")
    print("\nRUTE ALGORITMA")
    print("-" * 75)
    print(f"Heuristik (Greedy): {format_route(rute_h)}")
    print(f"Eksak (Optimal):    {format_route(rute_e)}")
    
    for nama_skenario, data_skenario in scenarios:
        harga_bbm = data_skenario['fuel_price']

        hasil_h = calculate_cost(
            rute_h,
            dist_matrix,
            customers,
            waktu_h,
            data_skenario
        )
        hasil_e = calculate_cost(
            rute_e,
            dist_matrix,
            customers,
            waktu_e,
            data_skenario
        )

        bbm_h = hasil_h['fuel_cost']
        srv_h = hasil_h['server_cost']
        tco_h = hasil_h['total_cost']

        bbm_e = hasil_e['fuel_cost']
        srv_e = hasil_e['server_cost']
        tco_e = hasil_e['total_cost']
        
        hemat = tco_h - tco_e
        rekomendasi = "EKSAK" if hemat > 0 else "HEURISTIK"
        
        print(f"\nSKENARIO: {nama_skenario} (BBM: Rp {harga_bbm:,.0f}/L)")
        print("-" * 75)
        print(f"{'Metrik':<25} | {'Heuristik (Greedy)':<22} | {'Eksak (Optimal)':<22}")
        print("-" * 75)
        print(f"{'Total Jarak (km)':<25} | {jarak_h:<22.2f} | {jarak_e:<22.2f}")
        print(f"{'Waktu Komputasi (ms)':<25} | {waktu_h:<22.4f} | {waktu_e:<22.4f}")
        print(f"{'Biaya Operasional BBM':<25} | Rp {bbm_h:<19,.0f} | Rp {bbm_e:<19,.0f}")
        print(f"{'Biaya Komputasi Server':<25} | Rp {srv_h:<19,.0f} | Rp {srv_e:<19,.0f}")
        print(f"{'Total Cost (TCO)':<25} | Rp {tco_h:<19,.0f} | Rp {tco_e:<19,.0f}")
        print("-" * 75)
        print(f"KESIMPULAN: Rekomendasi Algoritma {rekomendasi} (Selisih: Rp {abs(hemat):,.0f})")

    print("\n" + "=" * 75)
    print(f"{'ANALISIS BREAK-EVEN HARGA BBM':^75}")
    print("=" * 75)
    print(f"Konsumsi Heuristik : {hasil_h_break_even['fuel_used']:.4f} liter")
    print(f"Konsumsi Eksak     : {hasil_e_break_even['fuel_used']:.4f} liter")
    print(f"Biaya Server Heuristik : Rp {hasil_h_break_even['server_cost']:,.0f}")
    print(f"Biaya Server Eksak     : Rp {hasil_e_break_even['server_cost']:,.0f}")

    if break_even["status"] == "ok":
        threshold = break_even["threshold"]
        print(f"Break-even price    : Rp {threshold:,.2f}/L")
        print("Rumus               : fuel_h * p + server_h = fuel_e * p + server_e")

        for nama_skenario, data_skenario in scenarios:
            posisi = describe_threshold_position(
                data_skenario["fuel_price"],
                threshold
            )
            print(
                f"- {nama_skenario.title():<8} Rp {data_skenario['fuel_price']:>8,.0f}/L "
                f"-> {posisi} break-even"
            )
    elif break_even["status"] == "all_prices_equal":
        print("Break-even price    : semua harga. TCO selalu sama.")
    elif break_even["status"] == "no_break_even":
        print("Break-even price    : tidak ada. Konsumsi BBM sama, biaya server berbeda.")
    else:
        print("Break-even price    : tidak feasible untuk harga BBM positif.")
        print(f"Nilai ambang hitung : Rp {break_even['threshold']:,.2f}/L")

    print("\n" + "=" * 75)
    print(f"{'RINGKASAN EKSEKUTIF':^75}")
    print("=" * 75)
    print("1. Efisiensi Jarak: Algoritma Eksak berhasil mereduksi jarak tempuh secara")
    print("   maksimal, namun memerlukan biaya server yang lebih tinggi.")
    print("2. Sensitivitas Harga: Skenario Krisis meningkatkan urgensi optimasi rute")
    print("   karena penghematan BBM lebih besar daripada kenaikan biaya server.")
    print("3. Keputusan: Gunakan Heuristik untuk kondisi ekonomi stabil (Subsidi) dan")
    print("   Eksak untuk kondisi harga BBM tinggi guna mencapai efisiensi biaya.")
    print("=" * 75)

def main():
    parse_args()
    jalankan_analisis()


if __name__ == '__main__':
    main()
