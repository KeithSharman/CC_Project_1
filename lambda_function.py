import os
import io
import json
from datetime import datetime
import pandas as pd
from azure.storage.blob import BlobServiceClient


def process_nutritional_data_from_azurite():
    connect_str = (
        "DefaultEndpointsProtocol=http;"
        "AccountName=devstoreaccount1;"
        "AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;"
        "BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"
    )

    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Function started.")

    blob_service_client = BlobServiceClient.from_connection_string(connect_str)

    container_name = "datasets"
    blob_name = "All_Diets.csv"

    try:
        container_client = blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        stream = blob_client.download_blob().readall()
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Successfully downloaded '{blob_name}' from container '{container_name}'.")
    except Exception as e:
        return f"Failed to download blob: {e}"

    df = pd.read_csv(io.BytesIO(stream))
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Columns found: {df.columns.tolist()}")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Rows loaded: {len(df)}")

    avg_macros = df.groupby("Diet_type")[["Protein(g)", "Carbs(g)", "Fat(g)"]].mean().round(2)
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Averages calculated for {len(avg_macros)} diet types.")

    result = {
        "processed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "source": f"{container_name}/{blob_name}",
        "row_count": len(df),
        "diet_macro_averages": avg_macros.reset_index().to_dict(orient="records"),
    }

    os.makedirs("simulated_nosql", exist_ok=True)
    with open("simulated_nosql/results.json", "w") as f:
        json.dump(result, f, indent=2)

    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Results saved to simulated_nosql/results.json.")
    return f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Data processed and stored successfully."


print(process_nutritional_data_from_azurite())