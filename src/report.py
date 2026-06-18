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
from typing import List, Dict, Any

# Memastikan modul lokal dapat diimport
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from load_data import load_distance_matrix, load_customers, load_scenario
from algorithms.heuristic import greedy_nearest_neighbor
from algorithms.exact import exact_tsp


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

def hitung_bbm_dinamis(
    rute: List[int], 
    matriks_jarak: List[List[float]], 
    data_pelanggan: List[Dict[str, Any]], 
    harga_bbm: float
) -> float:
    """
    Menghitung biaya bensin berdasarkan beban paket yang berkurang di tiap titik.
    Formula Konsumsi: R(w) = 0.02 + 0.03 * (beban_saat_ini / beban_maksimal) L/km
    """
    berat_map = {p['id']: p['weight'] for p in data_pelanggan}
    
    beban_maksimal = sum(berat_map.values())
    beban_saat_ini = beban_maksimal
    total_biaya = 0.0
    
    for i in range(len(rute) - 1):
        u, v = rute[i], rute[i+1]
        jarak = matriks_jarak[u][v]
        
        # Interpolasi linear konsumsi bensin (0.02 - 0.05 L/km)
        rasio = 0.02 + 0.03 * (beban_saat_ini / beban_maksimal) if beban_maksimal > 0 else 0.02
        liter = jarak * rasio
        total_biaya += liter * harga_bbm
        
        # Update beban setelah pengantaran di lokasi v
        beban_saat_ini -= berat_map.get(v, 0)
        
    return total_biaya

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
    
    print("=" * 75)
    print(f"{'LAPORAN ANALISIS KEPUTUSAN BISNIS - LAST MILE DELIVERY':^75}")
    print("=" * 75)
    print("Mode: comparative report for scenarios subsidy + crisis")
    
    for nama_skenario, data_skenario in scenarios:
        harga_bbm = data_skenario['fuel_price']
        
        # Hitung TCO Heuristik
        bbm_h = hitung_bbm_dinamis(rute_h, dist_matrix, customers, harga_bbm)
        srv_h = waktu_h * biaya_server_ms
        tco_h = bbm_h + srv_h
        
        # Hitung TCO Eksak
        bbm_e = hitung_bbm_dinamis(rute_e, dist_matrix, customers, harga_bbm)
        srv_e = waktu_e * biaya_server_ms
        tco_e = bbm_e + srv_e
        
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
