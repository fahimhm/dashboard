# pandas for data management
import pandas as pd

# os for manipulating path
import os
from os.path import join

# to download dataset
from scripts.download_dataset import set_dataset

# to produce: data_overlap & shift_kosong
from scripts.data_prep import actransform
from scripts.data_prep import prep4chart

# to produce plot
from scripts.app import plot

# call dataset
file_name = ['Performance_Teknisi_Tracker', 'Performance_WO_Tracker', 'Data_Mentah_Maintenance', 'Data_Mentah']
url_report = "http://maula.fahim:welcometoparadise21@reportportal/Reports/Pages/Folder.aspx?ItemPath=%2f99.+Aplikasi+lain-lain%2f04.Aplikasi+Manufacturing%2fPortal+Engineering%2fWork+Order&ViewMode=List"
set_dataset(url_report, file_name)

# read data into dataframes
data_rpmt = pd.read_csv(join(os.getcwd(), 'datasets', 'Data_Mentah_Maintenance.csv'))
data_raw = pd.read_csv(join(os.getcwd(), 'datasets', 'Data_Mentah.csv'))
data_tek = pd.read_csv(join(os.getcwd(), 'datasets', 'Performance_Teknisi_Tracker.csv'))
data_wo = pd.read_csv(join(os.getcwd(), 'datasets', 'Performance_WO_Tracker.csv'), dayfirst=True, parse_dates=[0])
data_shft = pd.read_csv(join(os.getcwd(), 'datasets', 'data_shift.csv'), sep=';')
data_msn = pd.read_csv(join(os.getcwd(), 'datasets', 'Database Mesin PEA 2019.csv'), sep=';')
data_nwo = pd.read_csv(join(os.getcwd(), 'datasets', 'info_non_wo.csv'), sep=';', dayfirst=True, parse_dates=[0])

# merging dataset & produce new dataset to correction
df = actransform(data_tek, data_wo, data_msn, data_shft, data_nwo)
mh, wo_pmt, wo_rep = prep4chart(df=df, rpmtdata=data_rpmt, rpairdata=data_raw)

# start plot
plot()