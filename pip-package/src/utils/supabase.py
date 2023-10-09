from supabase import Client, create_client
from utils.env import config_data

url: str = config_data["SUPABASE_URL"]
key: str = config_data["SUPABASE_ANON_KEY"]
supabase_client: Client = create_client(url, key)
