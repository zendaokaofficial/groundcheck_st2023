import streamlit as st
import pandas as pd
from datetime import date
import time
from streamlit_js_eval import streamlit_js_eval
import gspread
import streamlit as st
from google.oauth2 import service_account
from oauth2client.service_account import ServiceAccountCredentials
from gsheetsdb import connect
import datetime
import json
import pytz

tzInfo = pytz.timezone('Asia/Hong_Kong')
# Create a connection object.
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('st2023-tabanan-bd680f2e25f6.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("db Groundcheck")
worksheet1 = sheet.worksheet('Sheet1')

## Membaca db asal
sheet_url = "https://docs.google.com/spreadsheets/d/1S_7EnNm3_kkF0og9Iecu0jZJ8oo60PlPHuzn0USlylg/edit#gid=0"
url_1 = sheet_url.replace('/edit#gid=', '/export?format=csv&gid=')

df = pd.read_csv(url_1, header=0, on_bad_lines='skip')
#df["ID SLS"] = df["ID SLS"].astype(str)
hari = date.today()

         
st.set_page_config(
         page_title="Form Groundcheck",
         page_icon="📋"
)

if __name__ == "__main__":

    st.markdown("<h1 style='text-align: center; color: green;'>Form Pelaporan Groundcheck</h1>", unsafe_allow_html=True)
    #st.subheader(f"Tanggal: {hari}")
    #st.dataframe(df)

    lstKecamatan = list(df["Nama Kecamatan"].unique())
    lstKecamatan.insert(0, "PILIH KECAMATAN")
              
    FirstFilter = st.selectbox("Nama Kecamatan", lstKecamatan, 0)

    if FirstFilter != 'PILIH KECAMATAN':

        df2 = df[df["Nama Kecamatan"] == FirstFilter]  

        lstDesa = list(df2["Nama Desa"].unique())
        lstDesa.insert(0, "PILIH DESA")

        SecondFilter = st.selectbox("Nama Desa", lstDesa, 0)

        if SecondFilter != 'PILIH DESA':

            df3 = df2[df2["Nama Desa"] == SecondFilter]

            lstSLS = list(df3["Nama SLS"].unique())
            lstSLS.insert(0, "PILIH SLS")

            ThirdFilter = st.selectbox("Nama SLS", lstSLS, 0)

            if ThirdFilter != "PILIH SLS":

                JumlahL2 = st.text_input('Jumlah L2 yang didata hasil Groundcheck', )

                SudahSelesai = st.selectbox("Apakah Sudah Selesai Groundcheck6 ", ["PILIH", "Sudah", "Belum"], 0)


                if ((SudahSelesai == "Sudah") and (len(JumlahL2) != 0)):
                    if st.button('Submit'):
                        st.success(f'Data berhasil tersubmit', icon="✅")
                        worksheet1.append_row([datetime.datetime.now(tz=tzInfo).isoformat(), FirstFilter, SecondFilter, ThirdFilter, JumlahL2])
                        time.sleep(3)
                        streamlit_js_eval(js_expressions="parent.window.location.reload()")
