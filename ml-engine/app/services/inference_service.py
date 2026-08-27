from app.config.db_client import get_db_connection
from app.services.validation_service import validate_transaction_data
from app.services.feature_service import extract_features
from app.preprocessing.preprocessing_service import preprocess_features
from app.services.rule_engine import evaluate_transaction_rules

def run_inference_for_transaction(transaction_id: int) -> dict:
    """
    Menjalankan seluruh pipeline inference untuk sebuah transaction_id:
    1. Mengambil data transaksi & master kendaraan dari PostgreSQL.
    2. Validasi input.
    3. Ekstraksi fitur.
    4. Preprocessing data.
    5. Evaluasi Rule Engine (Baseline Anomaly Detection).
    """
    connection = None
    cursor = None
    try:
        # 1. Buka koneksi database PostgreSQL
        connection = get_db_connection()
        cursor = connection.cursor()

        # Query untuk menggabungkan data fuel_transactions dengan master vehicles (mengambil kapasitas tangki)
        query = """
            SELECT 
                ft.id,
                ft.vehicle_id,
                ft.fuel_amount,
                ft.total_cost,
                ft.odometer,
                v.fuel_tank_capacity,
                v.fuel_consumption_rate
            FROM fuel_transactions ft
            JOIN vehicles v ON ft.vehicle_id = v.id
            WHERE ft.id = %s;
        """
        cursor.execute(query, (transaction_id,))
        transaction_data = cursor.fetchone()

        if not transaction_data:
            raise ValueError(f"Transaction ID {transaction_id} tidak ditemukan di database atau relasi kendaraan invalid.")

        # Konversi RealDictRow ke dictionary biasa agar mudah dimanipulasi
        tx_dict = dict(transaction_data)

        # 2. Input Validation
        validate_transaction_data(tx_dict)

        # 3. Feature Engineering
        features = extract_features(tx_dict)

        # 4. Data Preprocessing
        preprocessed = preprocess_features(features)

        # 5. Rule Engine Evaluation (Inference Prediction)
        inference_result = evaluate_transaction_rules(preprocessed)

        print(f"[Python Inference] Berhasil menyelesaikan analisis untuk Transaction ID {transaction_id}.")
        return inference_result

    except Exception as e:
        print(f"[Python Inference Error] Gagal memproses Transaction ID {transaction_id}: {e}")
        raise e
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()