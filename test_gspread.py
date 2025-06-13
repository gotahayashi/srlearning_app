import gspread
from google.oauth2.service_account import Credentials

print("🔄 認証開始...")

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
gc = gspread.authorize(creds)

print("✅ 認証完了")

print("📄 シートに接続中...")

sheet = gc.open("Learning Log").sheet1

print("✏️ 書き込み中...")

# ✅ 修正ポイント：値は2次元リストにする
sheet.update("A1", [["✅ Google Sheets connected!"]])

print("✅ 書き込み成功！")
