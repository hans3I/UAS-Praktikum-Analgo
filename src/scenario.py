from typing import Any, Dict, List


MIN_FUEL_RATE = 0.02
LOAD_FUEL_RATE_DELTA = 0.03


def calculate_dynamic_fuel_usage(
    route: List[int],
    distance_matrix: List[List[float]],
    customers: List[Dict[str, Any]]
) -> float:
    """
    Menghitung konsumsi BBM dinamis berdasarkan beban paket
    yang berkurang di setiap titik pengantaran.

    Formula konsumsi:
    R(w) = 0.02 + 0.03 * (beban_saat_ini / beban_maksimal) L/km
    """

    customer_weights = {
        customer["id"]: customer["weight"]
        for customer in customers
    }

    max_load = sum(customer_weights.values())
    current_load = max_load
    total_fuel_used = 0.0

    for index in range(len(route) - 1):
        from_node = route[index]
        to_node = route[index + 1]
        distance = distance_matrix[from_node][to_node]

        if max_load > 0:
            fuel_rate = MIN_FUEL_RATE + (
                LOAD_FUEL_RATE_DELTA * (current_load / max_load)
            )
        else:
            fuel_rate = MIN_FUEL_RATE

        fuel_used = distance * fuel_rate
        total_fuel_used += fuel_used

        current_load -= customer_weights.get(to_node, 0)

    return total_fuel_used


def calculate_fuel_cost(
    route: List[int],
    distance_matrix: List[List[float]],
    customers: List[Dict[str, Any]],
    fuel_price: float
) -> Dict[str, float]:
    fuel_used = calculate_dynamic_fuel_usage(
        route,
        distance_matrix,
        customers
    )

    return {
        "fuel_used": fuel_used,
        "fuel_cost": fuel_used * fuel_price
    }


def calculate_cost(
    route: List[int],
    distance_matrix: List[List[float]],
    customers: List[Dict[str, Any]],
    execution_time_ms: float,
    scenario: Dict[str, float]
) -> Dict[str, float]:
    """
    Menghitung Total Cost of Ownership (TCO) menggunakan
    model BBM dinamis yang sama untuk seluruh codebase.
    """

    fuel_result = calculate_fuel_cost(
        route,
        distance_matrix,
        customers,
        scenario["fuel_price"]
    )

    server_cost = (
        execution_time_ms *
        scenario["server_cost_per_ms"]
    )

    total_cost = fuel_result["fuel_cost"] + server_cost

    return {
        "fuel_used": fuel_result["fuel_used"],
        "fuel_cost": fuel_result["fuel_cost"],
        "server_cost": server_cost,
        "total_cost": total_cost
    }