def extract_features(transaction_data: dict) -> dict:
    """
    Melakukan ekstraksi fitur (feature engineering) dari data transaksi dan master kendaraan
    untuk mempersiapkan parameter evaluasi bagi rule-based anomaly engine.
    """
    if not transaction_data:
        raise ValueError("Data transaksi tidak tersedia untuk feature engineering.")

    # Ambil data dasar
    fuel_amount = float(transaction_data.get("fuel_amount", 0))
    total_cost = float(transaction_data.get("total_cost", 0))
    tank_capacity = float(transaction_data.get("fuel_tank_capacity", 0))
    
    # 1. Hitung Harga per Liter (Cost per Liter)
    # Berguna untuk mendeteksi apakah harga per liter di luar kewajaran pasar / SPBU resmi
    cost_per_liter = 0.0
    if fuel_amount > 0:
        cost_per_liter = total_cost / fuel_amount

    # 2. Hitung Rasio Penggunaan Kapasitas Tangki (Tank Capacity Ratio)
    # Mengetahui seberapa penuh pengisian dibandingkan kapasitas maksimal tangki kendaraan
    tank_fill_ratio = 0.0
    if tank_capacity > 0:
        tank_fill_ratio = (fuel_amount / tank_capacity) * 100

    # Kumpulkan fitur yang sudah diekstrak
    features = {
        "transaction_id": transaction_data.get("id"),
        "fuel_amount": fuel_amount,
        "total_cost": total_cost,
        "fuel_tank_capacity": tank_capacity,
        "cost_per_liter": round(cost_per_liter, 2),
        "tank_fill_ratio": round(tank_fill_ratio, 2)
    }

    print(f"[Python Feature Engineering] Fitur berhasil diekstrak untuk Transaction ID {features['transaction_id']}.")
    return features