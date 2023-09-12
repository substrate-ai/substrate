from resources.env import config_data
from supabase import create_client

supabase_url = config_data["SUPABASE_URL"]
supabase_anon_key = config_data["SUPABASE_ANON_KEY"]
supabase_admin_key = config_data["SUPABASE_SERVICE_ROLE_KEY"]
access_key_id = config_data["AWS_ACCESS_KEY_ID"]
secret_access_key = config_data["AWS_SECRET_ACCESS_KEY"]

supabase_anon = create_client(supabase_url, supabase_anon_key)
supabase_admin = create_client(supabase_url, supabase_admin_key)