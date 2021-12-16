import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

#title
st.set_page_config(layout="wide")  # this needs to be the first Streamlit command called
st.title("Statistik Produksi Minyak Mentah")
st.image("https://www.treehugger.com/thmb/vELzc83oZZa8XjFv7voHb5jBAuY=/667x667/smart/filters:no_upscale()/__opt__aboutcom__coeus__resources__content_migration__mnn__images__2010__05__shutterstock_680239339-67a685cc223f41778a8009fef2bcbbc3.jpg")

dataframe_csv = pd.read_csv("produksi_minyak_mentah.csv")
file_json = json.load(open("kode_negara_lengkap.json"))
dataframe_json = pd.DataFrame.from_dict(file_json, orient='columns')

list_kodekumpulannegara = []
for i in list(dataframe_csv['kode_negara']) :
    if i not in list(dataframe_json['alpha-3']) :
        list_kodekumpulannegara.append(i)
for i in list_kodekumpulannegara :
    dataframe_csv = dataframe_csv[dataframe_csv.kode_negara != i]

dataframe_jsonsingkat = dataframe_json[['name', 'region', 'sub-region', 'alpha-3']]
dataframe_jsonbaru = dataframe_jsonsingkat.rename(columns = {'alpha-3':'kode_negara'})
dataframe_gabungan = pd.merge(dataframe_csv, dataframe_jsonbaru, on = 'kode_negara')
dataframe_gabungan = dataframe_gabungan.rename(columns = {'name':'nama_negara'})

#nomor a
list_namanegara = []
for i in list(dataframe_gabungan['nama_negara']) :
    if i not in list_namanegara :
        list_namanegara.append(i)

N = st.selectbox("Pilih Negara", list_namanegara)

left_col, right_col = st.columns(2)

#upper left column
dataframe_jumlahproduksi = dataframe_gabungan.loc[dataframe_gabungan['nama_negara'] == N]
with left_col :
    st.subheader("Tabel Jumlah Produksi Suatu Negara")
    st.dataframe(dataframe_jumlahproduksi)

#upper right column
dataframe_jumlahproduksi.plot(x='tahun', y='produksi', title='Grafik Jumlah Produksi terhadap Tahun dari Suatu Negara', color='blue')
grafikbagian_a = plt.show()
with right_col :
    st.subheader("Grafik Jumlah Produksi terhadap Tahun dari Suatu Negara")
    st.pyplot(grafikbagian_a)

#nomor b
list_tahun = []
for i in list(dataframe_gabungan['tahun']) :
    if i not in list_tahun :
        list_tahun.append(i)

B = st.number_input("Banyak Negara", min_value = 1, max_value = None)
T = st.selectbox("Tahun", list_tahun)

left_col2, right_col2 = st.columns(2)

#middle left column
dataframe_jumlahproduksiterbesar = dataframe_gabungan.loc[dataframe_gabungan['tahun'] == T]
dataframe_jumlahproduksiterbesar = dataframe_jumlahproduksiterbesar.sort_values(by='produksi', ascending=False)
dataframe_jumlahproduksibaru = dataframe_jumlahproduksiterbesar[:B]
with left_col2 :
    st.subheader("Tabel Beberapa Negara dengan Jumlah Produksi Terbesar pada Suatu Tahun")
    st.dataframe(dataframe_jumlahproduksibaru)

#middle right column
dataframe_jumlahproduksibaru.plot.bar(x='nama_negara', y='produksi', color='red', title='Grafik Beberapa Negara dengan Jumlah Produksi Terbesar pada Suatu Tahun')
grafikbagian_b = plt.show()
with right_col2 :
    st.subheader("Grafik Jumlah Produksi terhadap Tahun dari Suatu Negara")
    st.pyplot(grafikbagian_b)

#nomor c
B2 = st.number_input("Banyak Negara", min_value = 1, max_value = None)

list_jumlahkumulatif = []
for i in list_namanegara :
    jumlahproduksi_negara = dataframe_gabungan.loc[dataframe_gabungan['nama_negara'] == i, 'produksi'].sum()
    list_jumlahkumulatif.append(jumlahproduksi_negara)

dataframe_kumulatifnegara = pd.DataFrame(list(zip(list_namanegara, list_jumlahkumulatif)), columns=['nama_negara', 'jumlah_kumulatif'])

left_col3, right_col3 = st.columns(2)

#lower left column
dataframe_jumlahkumulatifterbesar = dataframe_kumulatifnegara.sort_values(by='jumlah_kumulatif', ascending=False)
dataframe_jumlahkumulatifterbesarbaru = dataframe_jumlahkumulatifterbesar[:B2]
with left_col3 :
    st.subheader("Tabel Beberapa Negara dengan Jumlah Produksi Kumulatif Terbesar")
    st.dataframe(dataframe_jumlahkumulatifterbesarbaru)

#lower right column
dataframe_jumlahkumulatifterbesarbaru.plot.bar(x='nama_negara', y='jumlah_kumulatif', color='green', title='Grafik Beberapa Negara dengan Jumlah Produksi Kumulatif Terbesar')
grafikbagian_c = plt.show()
with right_col3 :
    st.subheader("Grafik Beberapa Negara dengan Jumlah Produksi Kumulatif Terbesar")
    st.pyplot(grafikbagian_c)

#nomor d
list_kodenegara = []
list_regionnegara = []
list_subregionnegara = []
for i in range(len(dataframe_kumulatifnegara)) :
    for j in range(len(dataframe_json)) :
        if list(dataframe_kumulatifnegara['nama_negara'])[i] == list(dataframe_json['name'])[j]:
            list_kodenegara.append(list(dataframe_json['alpha-3'])[j])
            list_regionnegara.append(list(dataframe_json['region'])[j])
            list_subregionnegara.append(list(dataframe_json['sub-region'])[j])

dataframe_kumulatifnegaralengkap = pd.DataFrame(list(zip(list_kodenegara, list_namanegara, list_jumlahkumulatif, list_regionnegara, list_subregionnegara)), columns=['kode_negara', 'nama_negara', 'jumlah_kumulatif', 'region', 'sub-region'])

T2 = st.selectbox("Tahun", list_tahun)

left_col4, right_col4 = st.columns(2)

#left column 4
#terbesar
dataframe_jumlahproduksiterbesar2 = dataframe_gabungan.loc[dataframe_gabungan['tahun'] == T2]
dataframe_jumlahproduksiterbesar2 = dataframe_jumlahproduksiterbesar2.sort_values(by='produksi', ascending=False)
dataframe_jumlahproduksibaru2 = dataframe_jumlahproduksiterbesar2[:1]
with left_col4 :
    st.subheader("Data Negara dengan Produksi Terbesar pada Tahun Tersebut")
    st.dataframe(dataframe_jumlahproduksibaru2)

#right column 4
#terkecil
dataframe_produksitanpanol = dataframe_gabungan[dataframe_gabungan.produksi != 0]
dataframe_jumlahproduksiterkecil = dataframe_produksitanpanol.loc[dataframe_produksitanpanol['tahun'] == T2]
dataframe_jumlahproduksiterkecil = dataframe_jumlahproduksiterkecil.sort_values(by='produksi', ascending=True)
dataframe_jumlahproduksiterkecilbaru = dataframe_jumlahproduksiterkecil[:1]
with right_col4 :
    st.subheader("Data Negara dengan Produksi Terkecil pada Tahun Tersebut")
    st.dataframe(dataframe_jumlahproduksiterkecilbaru)

left_col5, right_col5 = st.columns(2)

#left column 5
#terbesar keseluruhan tahun
dataframe_terbesarkeseluruhantahun = dataframe_kumulatifnegaralengkap.sort_values(by='jumlah_kumulatif', ascending=False)
dataframe_terbesarkeseluruhantahunbaru = dataframe_terbesarkeseluruhantahun[:1]
with left_col5 :
    st.subheader("Data Negara dengan Produksi Kumulatif Terbesar dari Keseluruhan Tahun")
    st.dataframe(dataframe_terbesarkeseluruhantahunbaru)

#right column 5
#terkecil keseluruhan tahun
dataframe_terkecilkeseluruhantahun = dataframe_terbesarkeseluruhantahun.sort_values(by='jumlah_kumulatif', ascending=True)
dataframe_kumulatiftanpanol = dataframe_terkecilkeseluruhantahun[dataframe_terkecilkeseluruhantahun.jumlah_kumulatif != 0]
dataframe_terkecilkeseluruhantahunbaru = dataframe_kumulatiftanpanol[:1]
with right_col5 :
    st.subheader("Data Negara dengan Produksi Kumulatif Terkecil dari Keseluruhan Tahun")
    st.dataframe(dataframe_terkecilkeseluruhantahunbaru)

left_col6, right_col6 = st.columns(2)

#nol
dataframe_produksinol = dataframe_gabungan[dataframe_gabungan.produksi == 0]
dataframe_jumlahproduksinol = dataframe_produksinol.loc[dataframe_produksinol['tahun'] == T2]
with left_col6 :
    st.subheader("Data Negara-Negara dengan Jumlah Produksi sama dengan Nol pada Tahun Tersebut")
    st.dataframe(dataframe_jumlahproduksinol)

#nol keseluruhan tahun
dataframe_kumulatifnol = dataframe_terkecilkeseluruhantahun[dataframe_terkecilkeseluruhantahun.jumlah_kumulatif == 0]
with right_col6 :
    st.subheader("Data Negara-Negara dengan Jumlah Produksi sama dengan Nol dari Keseluruhan Tahun")
    st.dataframe(dataframe_kumulatifnol)
