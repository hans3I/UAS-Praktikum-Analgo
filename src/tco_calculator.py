from typing import Dict

def calculate_tco(
    fuel_cost: float,
    execution_time_ms: float,
    server_cost_per_ms: float
) -> Dict[str, float]:
    """
    Menghitung Total Cost of Ownership (TCO).
    
    Parameters:
        fuel_cost          : total biaya bahan bakar
        execution_time_ms  : waktu eksekusi dalam milidetik
        server_cost_per_ms : biaya server per milidetik
        
    Returns:
        dictionary berisi rincian TCO
    """
    
    computation_cost = execution_time_ms * server_cost_per_ms
    total_tco = fuel_cost + computation_cost
    
    return {
        "fuel_cost": fuel_cost,
        "computation_cost": computation_cost,
        "total_tco": total_tco
    }