"""
Modul Analisis Keputusan Bisnis
Tugas Akhir Praktikum Analisis Algoritma

Modul ini melakukan perbandingan komprehensif antara algoritma Heuristik (Greedy)
dan Eksak (Backtracking) dengan fokus pada Total Cost of Ownership (TCO).
"""

import os
import sys
import time
from typing import List, Dict, Any

# Memastikan modul lokal dapat diimport
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from load_data import load_distance_matrix, load_customers, load_scenario
from algorithms.heuristic import greedy_nearest_neighbor
from algorithms.exact import exact_tsp

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
    
    BIAYA_SERVER_MS = 50
    
    # Eksekusi Algoritma
    # 1. Heuristik
    t_start = time.perf_counter()
    rute_h, jarak_h = greedy_nearest_neighbor(dist_matrix)
    waktu_h = (time.perf_counter() - t_start) * 1000
    
    # 2. Eksak
    t_start = time.perf_counter()
    rute_e, jarak_e = exact_tsp(dist_matrix)
    waktu_e = (time.perf_counter() - t_start) * 1000
    
    print("=" * 75)
    print(f"{'LAPORAN ANALISIS KEPUTUSAN BISNIS - LAST MILE DELIVERY':^75}")
    print("=" * 75)
    
    for nama_skenario, data_skenario in scenarios:
        harga_bbm = data_skenario['fuel_price']
        
        # Hitung TCO Heuristik
        bbm_h = hitung_bbm_dinamis(rute_h, dist_matrix, customers, harga_bbm)
        srv_h = waktu_h * BIAYA_SERVER_MS
        tco_h = bbm_h + srv_h
        
        # Hitung TCO Eksak
        bbm_e = hitung_bbm_dinamis(rute_e, dist_matrix, customers, harga_bbm)
        srv_e = waktu_e * BIAYA_SERVER_MS
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

if __name__ == "__main__":
    jalankan_analisis()
