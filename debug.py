import os
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('META_ACCESS_TOKEN')

# الـ ID الذي فشل قبل قليل
creation_id = "17881079004627937"

print("Fetching exact error from Meta...")
url = f"https://graph.facebook.com/v18.0/{creation_id}?fields=status_code,status&access_token={TOKEN}"

response = requests.get(url).json()
print(response)