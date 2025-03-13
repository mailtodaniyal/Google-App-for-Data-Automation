import gspread
import pandas as pd
import requests
import swisseph as swe
import json
from google.oauth2.service_account import Credentials

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SERVICE_ACCOUNT_FILE = "path/to/your/service-account.json"

creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(creds)

SPREADSHEET_ID = "your_google_sheet_id"
SHEET_NAME = "Sheet1"
sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)

def fetch_data():
    """Fetch data from APIs using Requests and swiss epherm"""
    
    response = requests.get("https://api.example.com/data")
    data = response.json()
    
    jd = swe.julday(2025, 3, 5, 12.0)
    planet_data = swe.calc_ut(jd, swe.SUN)
    
    return data, planet_data

def update_google_sheets(data):
    """Update Google Sheets with fetched data"""
    df = pd.DataFrame(data)
    sheet.update([df.columns.values.tolist()] + df.values.tolist())

def main():
    """Main function to automate workflow"""
    user_data = sheet.get_all_records()  
    
    for entry in user_data:
        fetched_data, astro_data = fetch_data()
        result = {"Fetched Data": fetched_data, "Astrology Data": astro_data}
        update_google_sheets(result)
    
    print("Google Sheets updated successfully!")

if __name__ == "__main__":
    main()
