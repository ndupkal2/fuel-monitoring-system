def evaluate_transaction_rules(preprocessed_data: dict) -> dict:
    """
    Mengevaluasi data transaksi menggunakan aturan bisnis fisik (Rule-Based Baseline):
    1. Anomali Kapasitas Tangki: Apakah jumlah liter BBM melebihi kapasitas tangki kendaraan?
    2. Anomali Harga per Liter: Apakah biaya per liter berada di luar batas kewajaran normal?
    """
    if not preprocessed_data:
        raise ValueError("Data preprocessing kosong, tidak dapat menjalankan rule engine.")

    transaction_id = preprocessed_data.get("transaction_id")
    fuel_amount = preprocessed_data.get("fuel_amount", 0.0)
    tank_capacity = preprocessed_data.get("fuel_tank_capacity", 0.0)
    cost_per_liter = preprocessed_data.get("cost_per_liter", 0.0)

    is_anomaly = False
    anomaly_score = 0.0
    reasons = []

    # ATURAN 1: Validasi Kapasitas Tangki Fisik
    if tank_capacity > 0 and fuel_amount > tank_capacity:
        is_anomaly = True
        anomaly_score = 1.0  # Skor maksimal karena melanggar batas fisik mutlak
        reasons.append(f"Jumlah BBM ({fuel_amount} L) melebihi kapasitas maksimal tangki ({tank_capacity} L).")

    # ATURAN 2: Validasi Harga per Liter yang Tidak Wajar (Contoh batas: di bawah Rp 5.000 atau di atas Rp 20.000)
    # Asumsi harga solar/bensin industri/subsidi berada di kisaran wajar tersebut.
    if cost_per_liter > 0:
        if cost_per_liter < 5000:
            is_anomaly = True
            anomaly_score = max(anomaly_score, 0.7)
            reasons.append(f"Harga per liter terlalu murah/tidak wajar (Rp {cost_per_liter:,.0f}).")
        elif cost_per_liter > 20000:
            is_anomaly = True
            anomaly_score = max(anomaly_score, 0.8)
            reasons.append(f"Harga per liter terlalu mahal/tidak wajar (Rp {cost_per_liter:,.0f}).")

    # Jika tidak ada pelanggaran aturan
    if not reasons:
        reasons.append("Transaksi normal, sesuai dengan batasan fisik dan standar operasional.")

    result = {
        "transaction_id": transaction_id,
        "is_anomaly": is_anomaly,
        "anomaly_score": round(anomaly_score, 2),
        "detection_engine": "rule_based_baseline_v1",
        "notes": " | ".join(reasons)
    }

    print(f"[Python Rule Engine] Evaluasi selesai untuk Transaction ID {transaction_id}. Anomali: {is_anomaly}")
    return result