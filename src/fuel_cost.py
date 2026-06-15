from typing import List, Dict

def calculate_fuel_consumption_ratio(
    current_load: float,
    max_load: float
) -> float:
    """
    Menghitung rasio konsumsi bahan bakar (liter/km).
    
    Parameters:
        current_load : berat paket saat ini
        max_load     : berat paket total saat berangkat
        
    Returns:
        rasio bahan bakar (liter/km)
    """
    
    # Jika tidak ada beban, gunakan rasio motor kosong
    if max_load <= 0:
        return 0.02
        
    return 0.02 + (current_load / max_load) * (0.05 - 0.02)


def calculate_route_fuel_cost(
    route: List[int],
    distance_matrix: List[List[float]],
    customers: List[Dict],
    fuel_price: float
) -> float:
    """
    Menghitung total biaya bahan bakar rute.
    
    Parameters:
        route           : urutan node yang dilalui
        distance_matrix : matriks jarak
        customers       : data pelanggan (termasuk berat)
        fuel_price      : harga bahan bakar per liter
        
    Returns:
        total biaya bahan bakar
    """
    
    total_fuel_cost = 0.0
    
    # Hitung total berat semua paket
    current_load = 0.0
    for customer in customers:
        current_load += customer["weight"]
        
    max_load = current_load
    
    if max_load <= 0:
        return 0.0
        
    # Iterasi setiap rute
    for i in range(len(route) - 1):
        from_node = route[i]
        to_node = route[i + 1]
        
        distance = distance_matrix[from_node][to_node]
        
        # Hitung rasio bensin
        fuel_ratio = calculate_fuel_consumption_ratio(
            current_load,
            max_load
        )
        
        # Hitung biaya segmen
        fuel_used = distance * fuel_ratio
        segment_cost = fuel_used * fuel_price
        
        total_fuel_cost += segment_cost
        
        # Kurangi beban paket saat tiba di lokasi pelanggan
        for customer in customers:
            if customer["id"] == to_node:
                current_load -= customer["weight"]
                break
                
    return total_fuel_cost