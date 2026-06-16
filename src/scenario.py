def calculate_cost(
    total_distance,
    execution_time_ms,
    scenario,
    fuel_efficiency=10
):
    """
    Menghitung biaya operasional berdasarkan
    skenario ekonomi.
    """

    fuel_used = total_distance / fuel_efficiency

    fuel_cost = (
        fuel_used *
        scenario["fuel_price"]
    )

    server_cost = (
        execution_time_ms *
        scenario["server_cost_per_ms"]
    )

    total_cost = (
        fuel_cost +
        server_cost
    )

    return {
        "fuel_used": fuel_used,
        "fuel_cost": fuel_cost,
        "server_cost": server_cost,
        "total_cost": total_cost
    }