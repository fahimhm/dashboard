# pandas for data management
import pandas as pd

# os for manipulating paths
import os
from os.path import join

# Bokeh basics
from bokeh.io import curdoc
from bokeh.models.widgets import Tabs

# to download dataset
from scripts.download_dataset import set_dataset

# to produce: data_overlap & shift_kosong
from scripts.data_prep import actransform
from scripts.data_prep import prep4chart

# Each plot-tab is drawn by one script
# 

# call dataset
file_name = ['Performance_Teknisi_Tracker', 'Performance_WO_Tracker', 'Data_Mentah_Maintenance', 'Data_Mentah']
url_report = "http://maula.fahim:fahimhadimaula28@reportportal/Reports/Pages/Folder.aspx?ItemPath=%2f99.+Aplikasi+lain-lain%2f04.Aplikasi+Manufacturing%2fPortal+Engineering%2fWork+Order&ViewMode=List"
set_dataset(url_report, file_name)

# read data into dataframes
data_rpmt = pd.read_csv(join(os.getcwd(), 'datasets', 'Data_Mentah_Maintenance.csv'))
data_raw = pd.read_csv(join(os.getcwd(), 'datasets', 'Data_Mentah.csv'))
data_tek = pd.read_csv(join(os.getcwd(), 'datasets', 'Performance_Teknisi_Tracker.csv'))
data_wo = pd.read_csv(join(os.getcwd(), 'datasets', 'Performance_WO_Tracker.csv'))
data_shft = pd.read_csv(join(os.getcwd(), 'datasets', 'data_shift.csv'), sep=';')
data_msn = pd.read_csv(join(os.getcwd(), 'datasets', 'Database Mesin PEA 2019.csv'), sep=';')
data_nwo = pd.read_csv(join(os.getcwd(), 'datasets', 'info_non_wo.csv'), sep=';')

# merging dataset & produce new dataset to correction
mh = actransform(data_tek, data_wo, data_msn, data_shft, data_nwo)
mergroup, datareal = prep4chart(df=mh, rpmtdata=data_rpmt, rpairdata=data_raw)

# Create each of the tabs
# tab1 = ...
# tab2 = ...

# Put all the tabs into one application
# tabs = Tabs(tabs = [tab1, tab2])

# Put the tabs in the current document for display
# curdoc().add_root(tabs)
