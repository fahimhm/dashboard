import os
from os.path import join
import pandas as pd
import datetime as dt
import time
import numpy as np

def actransform(data_tek, data_wo, data_mesin, data_shift, data_nwo):
    # data kegiatan teknisi
    act = data_tek.sort_values(['name', 'waktu_mulai_dikerjakan2'], ascending=True)
    act.reset_index(inplace=True, drop=True)
    act.columns = ['name', 'task_cat', 'wo', 'machine', 'date_start', 'date_finish', 'duration']
    
    # data status wo
    dfwo = data_wo.loc[:, ['nomor_wo_repair', 'status_wo']].copy()
    dfwo.columns = ['wo', 'wo_status']
    act = act.merge(dfwo, on='wo', how='left')
    
    # data mesin
    actsy = data_mesin.loc[:, ["System", "Field's Name"]].copy()
    actsy.columns = ['system', 'machine']
    act = act.merge(actsy, on='machine', how='left')
    
    # tambahkan beberapa kolom
    act['date_start'] = pd.to_datetime(act['date_start'])
    act['date_finish'] = pd.to_datetime(act['date_finish'])
    act['year'] = act['date_start'].map(lambda x: x.strftime('%Y'))
    act['month'] = act['date_start'].map(lambda x: x.strftime('%m'))
    act['week'] = act['date_start'].dt.week
    act['day'] = act[['date_start']].apply(lambda x: dt.datetime.strftime(x['date_start'], '%A'), axis=1)
    
    # tag lembur atau normal
    act['day_cat'] = 'NaN'
    act['help_hour'] = act['date_start'].dt.hour + (act['date_start'].dt.minute / 60)
    for idx in act.index:
        if (act.loc[idx, 'day'] == 'Sunday' or (act.loc[idx, 'day'] == 'Saturday' and act.loc[idx, 'help_hour'] >= 6.0) or (act.loc[idx, 'day'] == 'Monday' and act.loc[idx, 'help_hour'] < 5.5)):
            act.at[idx, 'day_cat'] = 'overtime'
        else:
            act.at[idx, 'day_cat'] = 'normal'
    
    # pengecualian untuk day-on atau libur: ['5 Januari 2019', '3 April 2019', '13 April 2019', '18 Mei 2019']
    for idx in act.index:
        if (act.loc[idx, 'year'] == '2019') & (act.loc[idx, 'week'] == 1) & (act.loc[idx, 'day'] == 'Saturday'):
            act.at[idx, 'day_cat'] = 'normal'
    for idx in act.index:
        if (act.loc[idx, 'year'] == '2019') & (act.loc[idx, 'week'] == 14) & (act.loc[idx, 'day'] == 'Wednesday') & (act.loc[idx, 'help_hour'] >= 6.0):
            act.at[idx, 'day_cat'] = 'overtime'
    for idx in act.index:
        if (act.loc[idx, 'year'] == '2019') & (act.loc[idx, 'week'] == 15) & (act.loc[idx, 'day'] == 'Saturday'):
            act.at[idx, 'day_cat'] = 'normal'
    for idx in act.index:
        if (act.loc[idx, 'year'] == '2019') & (act.loc[idx, 'week'] == 20) & (act.loc[idx, 'day'] == 'Saturday'):
            act.at[idx, 'day_cat'] = 'normal'
    act = act.drop('help_hour', axis=1)
    
    # info shift
    data_shift = data_shift[['workcenter', 'name', 'year', 'week', 'day', 'day_cat', 'shift']].copy()
    data_shift.loc[:, 'year'] = data_shift.loc[:, 'year'].fillna(-1)
    data_shift.loc[:, 'year'] = data_shift['year'].astype(int)
    data_shift.loc[:, 'year'] = data_shift['year'].astype(str)
    data_shift.loc[:, 'year'] = data_shift['year'].replace('-1', np.nan)
    data_shift.loc[:, 'week'] = data_shift.loc[:, 'week'].fillna(-1)
    data_shift.loc[:, 'week'] = data_shift['week'].astype(int)
    data_shift.loc[:, 'week'] = data_shift['week'].astype(str)
    data_shift.loc[:, 'week'] = data_shift['week'].replace('-1', np.nan)
    data_shift.loc[:, 'shift'] = data_shift.loc[:, 'shift'].fillna(-1)
    data_shift.loc[:, 'shift'] = data_shift['shift'].astype(int)
    data_shift.loc[:, 'shift'] = data_shift['shift'].astype(str)
    data_shift.loc[:, 'shift'] = data_shift.loc[:, 'shift'].replace('-1', np.nan)
    act.loc[:, 'week'] = act['week'].astype(str)
    act = pd.merge(act, data_shift, on=['name', 'year', 'week', 'day', 'day_cat'], how='left')
    
    # ganti semua status close menjadi done
    for i in act.index:
        if (act.loc[i, 'wo_status'] == 'Verified' or act.loc[i, 'wo_status'] == 'repaired' or act.loc[i, 'wo_status'] == 'Need Follow up' or act.loc[i, 'wo_status'] == 'approved by executive' or act.loc[i, 'wo_status'] == 'Executive rejects follow up' or act.loc[i, 'wo_status'] == 'approved by T2'):
            act.at[i, 'wo_status'] = 'done'
    
    # hapus nama teknisi yg tidak relevan
    act = act.drop(act[act.name == 'Ahmad Ibnu Najib'].index, axis=0)
    act = act.drop(act[act.name == 'B. Betha Apreanda - Inspektor'].index, axis=0)
    act = act.drop(act[act.name == 'Deni Ramdani'].index, axis=0)
    act = act.drop(act[act.name == 'Gilang'].index, axis=0)
    act = act.drop(act[act.name == 'Operator Engineering PEA'].index, axis=0)
    act = act.drop(act[act.name == 'PKL 01'].index, axis=0)
    act = act.drop(act[act.name == 'PKL 02'].index, axis=0)
    act = act.drop(act[act.name == 'PKL 03'].index, axis=0)
    act = act.drop(act[act.name == 'PKL 26'].index, axis=0)
    act = act.drop(act[act.name == 'PKL 17'].index, axis=0)
    act = act.drop(act[act.name == 'PKL 20'].index, axis=0)
    act = act.drop(act[act.name == 'Teknisi External Utility'].index, axis=0)
    act = act.drop(act[act.name == 'Teknisi PEA - Utility'].index, axis=0)
    act = act.drop(act[act.name == 'Valen'].index, axis=0)
    act = act.drop(act[act.name == 'Asep Ramdan'].index, axis=0)
    act = act.drop(act[act.name == 'Refika Dameria'].index, axis=0)
    act = act.drop(act[act.name == 'Teknisi External Fillpack B'].index, axis=0)
    act = act.drop(act[act['workcenter'].isnull()].index, axis=0)
    
    # re-sort column
    act = act[['workcenter', 'name', 'year', 'month', 'week', 'day', 'day_cat', 'shift', 'task_cat', 'wo', 'wo_status', 'system', 'machine', 'date_start', 'date_finish', 'duration']]
    
    # ambil dataframe non wo
    data_nwo['date_start'] = pd.to_datetime(data_nwo['date_start'])
    data_nwo['date_finish'] = pd.to_datetime(data_nwo['date_finish'])
    act = pd.concat([act, data_nwo], ignore_index=True)
    act = act.sort_values(['workcenter', 'name', 'date_start'], ascending=True)
    act = act.drop_duplicates(subset=['name', 'wo', 'date_start', 'date_finish'], keep='first')
    act = act.dropna(axis=0, how='all')

    # convert data type
    act.loc[:, 'date_start'] = pd.to_datetime(act['date_start'])
    act.loc[:, 'date_finish'] = pd.to_datetime(act['date_finish'])
    act.loc[:, 'year'] = act['year'].astype('int64')
    act.loc[:, 'month'] = act['month'].astype('int64')
    act.loc[:, 'week'] = act['week'].astype('int64')
    act.loc[:, 'shift'] = act['shift'].fillna(-1)
    act.loc[:, 'shift'] = act['shift'].astype(int)
    act.loc[:, 'shift'] = act['shift'].replace(-1, np.nan)
    
    # correction in duration
    act.loc[:, 'duration'] = ((act['date_finish']-act['date_start'])/np.timedelta64(1, 'h'))
    
    # sort dataframe
    act = act.sort_values(['workcenter', 'name', 'date_start'])
    act.reset_index(inplace=True, drop=True)
    
    # produce data overlap
    act.loc[:, 'remark'] = 'no_overlap'
    for idx in range(1, len(act.index)-1):
        if ((act.loc[idx, 'name'] == act.loc[idx+1, 'name']) & (act.loc[idx+1, 'date_start'] < act.loc[idx, 'date_finish'])) or ((act.loc[idx, 'name'] == act.loc[idx-1, 'name']) & (act.loc[idx, 'date_start'] < act.loc[idx-1, 'date_finish'])):
            act.at[idx, 'remark'] = 'overlap'
    writer = pd.ExcelWriter('data_output/data_overlap.xlsx')
    act[act['remark'] == 'overlap'].to_excel(writer, 'overlap')
    writer.save()
    act = act.drop('remark', axis=1)
    
    # produce null-shift
    writer = pd.ExcelWriter('data_output/shift_kosong.xlsx')
    act[act['shift'].isnull()].to_excel(writer, 'kosong')
    writer.save()
    
    return act

def prep4chart(df, rpmtdata, rpairdata):
    # mh dataframe preparation
    group1 = df.groupby(['workcenter', 'year', 'month']).apply(lambda x: pd.Series({'mh_total': x[(x['task_cat'] != 'Break') & (x['task_cat'] != 'Planned')]['duration'].sum()})).reset_index()
    group2 = df.groupby(['workcenter', 'year', 'month']).apply(lambda x: pd.Series({'mh_real': x[(x['task_cat'] != 'Break') & (x['task_cat'] != 'Planned') & (x['task_cat'] != 'Unplanned')]['duration'].sum()})).reset_index()
    mergroup = group1.merge(group2, on=['workcenter', 'year', 'month'])
    mergroup['%_mhreal'] = mergroup['mh_real'] / mergroup['mh_total'] * 100.0
    
    # wo pmt dataframe preparation
    realpmt = rpmtdata.loc[rpmtdata['nomor_wo_pmt'].notnull(), ['nama_workcenter', 'nama_detail', 'nomor_wo_pmt', 'status_wo', 'tanggal_rencana', 'tanggal_selesai']]
    realpmt.columns = ['workcenter', 'machine', 'wo', 'wo_status', 'date', 'date_finish']
    realpmt.loc[:, 'date'] = pd.to_datetime(realpmt.loc[:, 'date'])
    realpmt.loc[:, 'date_finish'] = pd.to_datetime(realpmt.loc[:, 'date_finish'])
    realpmt['year'] = realpmt['date'].dt.year
    realpmt['year_help'] = realpmt['date_finish'].dt.year
    realpmt['month'] = realpmt['date'].dt.month
    realpmt['month_help'] = realpmt['date_finish'].dt.month
    realpmt['week'] = realpmt['date'].dt.week
    realpmt['week_help'] = realpmt['date_finish'].dt.week
    realpmt = realpmt[['workcenter', 'machine', 'year', 'year_help', 'month', 'month_help', 'week', 'week_help', 'wo', 'wo_status', 'date', 'date_finish']]
    realpmt = realpmt.sort_values('date', ascending=True)
    realpmt.reset_index(inplace=True, drop=True)
    for i in realpmt.index:
        if (realpmt.loc[i, 'wo_status'] == 'Verified') | (realpmt.loc[i, 'wo_status'] == 'Need Follow up') | (realpmt.loc[i, 'wo_status'] == 'approved by T2') | (realpmt.loc[i, 'wo_status'] == 'approved by executive'):
            realpmt.at[i, 'wo_status'] = 'done'
        elif realpmt.loc[i, 'wo_status'] == 'Ignored2':
            realpmt.at[i, 'wo_status'] = 'Cancel'
    group3 = realpmt.groupby(['workcenter','year', 'month']).apply(lambda x: pd.Series({'wo_total': x['wo'].nunique()})).reset_index()
    group4 = realpmt.groupby(['workcenter', 'year_help', 'month_help']).apply(lambda x: pd.Series({'wo_rlz': x[(x['wo_status'] == 'done') & (x['week'] == x['week_help'])]['wo'].nunique()})).reset_index()
    group4.columns = ['workcenter', 'year', 'month', 'wo_rlz']
    rlzpmt = group3.merge(group4, on=['workcenter', 'year', 'month'])
    rlzpmt['year'] = rlzpmt['year'].astype('int64')
    rlzpmt['month'] = rlzpmt['month'].astype('int64')
    
    rlzpmt['%_wopmt'] = rlzpmt['wo_rlz'] / rlzpmt['wo_total'] * 100.0

    # wo repair preparation
    realrep = rpairdata.loc[rpairdata['status_wo'] != 'rejected', ['nama_workcenter', 'nama_detail', 'nomor_wo_repair', 'status_wo', 'waktu_pengajuan_servis', 'waktu_selesai']]
    realrep.columns = ['workcenter', 'machine', 'wo', 'wo_status', 'date', 'date_finish']
    realrep.loc[:, 'date'] = pd.to_datetime(realrep.loc[:, 'date'])
    realrep.loc[:, 'date_finish'] = pd.to_datetime(realrep.loc[:, 'date_finish'])
    realrep['year'] = realrep['date'].dt.year
    realrep['year_help'] = realrep['date_finish'].dt.year
    realrep['month'] = realrep['date'].dt.month
    realrep['month_help'] = realrep['date_finish'].dt.month
    realrep['week'] = realrep['date'].dt.week
    realrep['week_help'] = realrep['date_finish'].dt.week
    realrep = realrep[['workcenter', 'machine', 'year', 'year_help', 'month', 'month_help', 'week', 'week_help', 'wo', 'wo_status', 'date', 'date_finish']]
    realrep = realrep.sort_values('date', ascending=True)
    realrep.reset_index(inplace=True, drop=True)
    
    for i in realrep.index:
        if (realrep.loc[i, 'wo_status'] == 'Executive rejects follow up') or (realrep.loc[i, 'wo_status'] == 'approved by executive') or (realrep.loc[i, 'wo_status'] == 'done not ok'):
            realrep.at[i, 'wo_status'] = 'done'
    group5 = realrep.groupby(['workcenter', 'year', 'month']).apply(lambda x: pd.Series({'wo_total': x['wo'].nunique()})).reset_index()
    group6 = realrep.groupby(['workcenter', 'year_help', 'month_help']).apply(lambda x: pd.Series({'wo_rlz': x[x['wo_status'] == 'done']['wo'].nunique()})).reset_index()
    group6.columns = ['workcenter', 'year', 'month', 'wo_rlz']
    datareprlz = group5.merge(group6, on=['workcenter', 'year', 'month'])
    datareprlz['year'] = datareprlz['year'].astype('int64')
    datareprlz['month'] = datareprlz['month'].astype('int64')

    for woc in datareprlz['workcenter'].unique():
        df = datareprlz[datareprlz['workcenter'] == woc].copy()    
        notrlz = 0
        for i in df.index:
            if i == 0:
                notrlz = datareprlz.loc[i, 'wo_total'] - datareprlz.loc[i, 'wo_rlz']
            else:
                datareprlz.at[i, 'wo_total'] = datareprlz.loc[i, 'wo_total'] + notrlz
                notrlz = datareprlz.loc[i, 'wo_total'] - datareprlz.loc[i, 'wo_rlz']
    
    datareprlz['%_worep'] = datareprlz['wo_rlz'] / datareprlz['wo_total'] * 100.0

    # join
    # datareal = rlzpmt.merge(datareprlz, on=['year', 'month'])
    # datareal['wo_total'] = datareal['wo_total_x'] + datareal['wo_total_y']
    # datareal['wo_rlz'] = datareal['wo_rlz_x'] + datareal['wo_rlz_y']
    # datareal = datareal.drop(['wo_total_x', 'wo_total_y', 'wo_rlz_x', 'wo_rlz_y'],axis=1)
    # datareal['%_woreal'] = datareal['wo_rlz'] / datareal['wo_total'] * 100.0
    
    # convert to string
    # mergroup.loc[:, 'year'] = mergroup.loc[:, 'year'].astype('str')
    # datareal.loc[:, 'year'] = datareal.loc[:, 'year'].astype('str')

    return mergroup, rlzpmt, datareprlz