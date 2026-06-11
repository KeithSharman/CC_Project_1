import io
import pandas as pd
from azure.storage.blob import BlobServiceClient

connect_str = (
    "DefaultEndpointsProtocol=http;"
    "AccountName=devstoreaccount1;"
    "AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;"
    "BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"
)

blob_service_client = BlobServiceClient.from_connection_string(connect_str)

# 1. Create the container
container_client = blob_service_client.get_container_client("datasets")
if not container_client.exists():
    container_client.create_container()
    print("Container created.")
else:
    print("Container already exists.")

# 2. Upload your CSV file
blob_client = container_client.get_blob_client("All_Diets.csv")
with open("All_Diets.csv", "rb") as f:        # <-- make sure this path points to your actual CSV
    blob_client.upload_blob(f, overwrite=True)

print("CSV uploaded to Azurite successfully.")