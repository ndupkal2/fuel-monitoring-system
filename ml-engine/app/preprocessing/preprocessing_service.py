def preprocess_features(features: dict) -> dict:
    """
    Melakukan pembersihan, penanganan nilai kosong, dan normalisasi tipe data 
    pada fitur transaksi agar siap dievaluasi oleh anomali engine secara konsisten.
    """
    if not features:
        raise ValueError("Fitur kosong, tidak dapat melakukan preprocessing.")

    # Salin data agar objek asli tidak berubah langsung (immutability)
    processed = features.copy()

    # Normalisasi tipe data numerik dan tangani nilai kosong/None menjadi 0.0
    processed["fuel_amount"] = float(processed.get("fuel_amount") or 0.0)
    processed["total_cost"] = float(processed.get("total_cost") or 0.0)
    processed["fuel_tank_capacity"] = float(processed.get("fuel_tank_capacity") or 0.0)
    processed["cost_per_liter"] = float(processed.get("cost_per_liter") or 0.0)
    processed["tank_fill_ratio"] = float(processed.get("tank_fill_ratio") or 0.0)

    print(f"[Python Preprocessing] Data untuk Transaction ID {processed.get('transaction_id')} berhasil dibersihkan dan dinormalisasi.")
    return processed