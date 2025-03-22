from supabase import create_client
from config import api, url

def create_supabase_client():
    supabase = create_client(url, api) 
    return supabase

# Create a Supabase client instance
base = create_supabase_client()
print(base)  # ✅ Should print a Supabase client object if successful
