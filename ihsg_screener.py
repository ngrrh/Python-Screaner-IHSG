import pandas as pd
import yfinance as yf
#defenisi fungsi skor fundamental (per,pbv,roe)
def score_per(per):
    if per is None:
        return 0
    if per < 10:
        return 40
    elif per < 15:
        return 30
    elif per < 20:
        return 20
    else:
        return 10

def score_pbv(pbv):
    if pbv is None:
        return 0
    if pbv < 1:
        return 30
    elif pbv < 2:
        return 25
    elif pbv < 4:
        return 15
    else:
        return 5

def score_roe(roe):
    if roe is None:
        return 0
    roe_percent = roe * 100
    if roe_percent > 20:
        return 30
    elif roe_percent > 15:
        return 25
    elif roe_percent > 10:
        return 15
    else:
        return 5

#pengaturan parameter input
ticker_saham = "BMRI.JK"
tanggal_mulai = "2026-01-01"
tanggal_akhir = "2026-10-25"

# penarikan dan pengolahan harga 
saham = yf.Ticker(ticker_saham)

#tarik harga historis
df_harga = saham.history(start=tanggal_mulai, end=tanggal_akhir) 

#rapikan nama kolom jika berupa multiindex
if isinstance(df_harga.columns, pd.MultiIndex):
    df_harga.columns = df_harga.columns.get_level_values(0)

#ambil harga terakhir dan hitung SMA20 
harga_terakhir = df_harga['Close'].iloc[-1]
df_harga["SMA20"] = df_harga['Close'].rolling(window=20).mean()
sma20_terakhir = df_harga["SMA20"].iloc[-1]

#penarikan dan skroring fundamental
info_perusahaan = saham.info
per = info_perusahaan.get('trailingPE', None)
pbv = info_perusahaan.get('priceToBook', None)
roe = info_perusahaan.get('returnOnEquity', None)
skor_per = score_per(per)
skor_pbv = score_pbv(pbv)
skor_roe = score_roe(roe)
total_skor = skor_per + skor_pbv + skor_roe

# tampilkan hasil rinkasan analisis 
print("=" * 45)
print(f"       HASIL ANALISIS SAHAM: {ticker_saham}")
print("=" * 45)

print("\n--- ANALISIS TEKNIKAL HARIAN ---")
print(f"Harga Penutupan Terakhir : Rp {harga_terakhir:,.2f}")
print(f"SMA 20 Hari              : Rp {sma20_terakhir:,.2f}")

print("\n--- ANALISIS FUNDAMENTAL & SKORING ---")

# Perbaikan logika f-string di bawah ini:
print(
    f"PER : {per:.2f} -> Skor PER: {skor_per} / 40"
    if per
    else f"PER : N/A -> Skor PER: {skor_per} / 40"
)
print(
    f"PBV : {pbv:.2f} -> Skor PBV: {skor_pbv} / 30"
    if pbv
    else f"PBV : N/A -> Skor PBV: {skor_pbv} / 30"
)
print(
    f"ROE : {roe * 100:.2f}% -> Skor ROE: {skor_roe} / 30"
    if roe
    else f"ROE : N/A -> Skor ROE: {skor_roe} / 30"
)

print("-" * 45)
print(f"TOTAL SKOR FUNDAMENTAL   : {total_skor} / 100")
print("=" * 45)
