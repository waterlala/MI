#!/usr/bin/env python
# coding: utf-8

# In[2]:


from Patient import patient
from Record import record
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# In[120]:


class main():
    def __init__(self):
        self._patients = np.nan
        self._records = np.nan
        self._main_patient = np.nan
        self._main_records= np.nan
        self._name_mapper = np.nan
    #load 資料庫
    def load_data(self):
        self._patients = pd.read_pickle('../pickle/patients.pickle')
        self._records = pd.read_pickle('../pickle/records_inpatients.pickle')
        self._name_mapper = pd.read_pickle('name_mapper.pkl.zip')
    def set_patient_by_id(self, _id):
        self._main_patient = self._patients[self._patients['ID']==_id].reset_index(drop='True')
        self._main_records = self._records[self._records['PatientID']==_id].reset_index(drop='True')
    def get_patient_personal_data(self):
        return self._main_patient[['ID','Gender','Birth']].rename(columns={'ID':'id','Gender':'gender','Birth':'birthdate'})
    def get_patient_records(self):
        out = self._main_records[['InDate','Type','ICD9CM']].rename(columns={'InDate':'date','Type':'type','ICD9CM':'main_disease'})
        out['main_disease'] = out['main_disease'].apply(lambda x: x[0])
        return out
    def get_record_detial(self, _key):
        out_record = self._main_records[_key:_key+1].reset_index(drop = True)
        out_record = out_record[['Type','InDate','ICD9CM','Drug']]
        out_record = out_record.rename(columns={'InDate':'date','Type':'type','Drug':'drug','ICD9CM':'icd'})
        out_patient = self._main_patient[['ID','Gender']].rename(columns={'ID':'id','Gender':'gender'})
        out = pd.concat([out_patient,out_record],axis = 1)
        return out
    
    def get_patient_before_icd(self):
        record = pd.merge(self._main_records[['PatientID','InDate','ICD9CM']].rename(columns={'PatientID':'ID'}),self._main_patient[['ID','Birth']],on='ID',how='left')
        record['date'] = record['InDate'] - record['Birth']
        record['date'] = record['date'].apply(lambda x: x.days)
        record = record.sort_values('date')
        save_list = list()
        out = list()
        for r in list(record['ICD9CM']):
            save = list()
            save = save_list.copy()
            for single in r:
                single = str(single)
                if single.isdigit():
                    single = int(single)
                    if single not in save_list:
                        save_list.append(single)
                        save.append(single)
            out.append(save)
        record['total_icd'] = pd.Series(out)
        record['total_icd_len'] = record['total_icd'].apply(lambda x: len(x))
        record['year'] = record['date'] / 365
        x_out = list()
        for i in range(0,record['date'].max(),365):
            x_out.append(i+1)
        out_data = pd.DataFrame()
        out_data['x'] = pd.Series(x_out)
        def get_y(x):
            df = record[record['date']<=x]
            return df['total_icd_len'].max()
        out_data['y'] = out_data['x'].apply(get_y)
        out_data = out_data.fillna(0)
        return out_data
    def get_patient_before_big_icd(self):
        total_icd =  list(set(list(self._main_records[['PatientID','ICD9CM']].explode('ICD9CM')['ICD9CM'])))
        big_icd = list()
        key = list()
        for i in range(0,18,1):
            key.append(i+1)
            big_icd.append(0)
        for icd in total_icd:
            icd = str(icd)
            if icd.isdigit():
                icd = int(icd)
                if icd >=1 and icd<= 139:
                    big_icd[0] = big_icd[0] + 1
                elif icd >=140 and icd<= 239:
                    big_icd[1] = big_icd[1] + 1
                elif icd >=240 and icd<= 279:
                    big_icd[2] = big_icd[2] + 1
                elif icd >=280 and icd<= 289:
                    big_icd[3] = big_icd[3] + 1
                elif icd >=290 and icd<= 319:
                    big_icd[4] = big_icd[4] + 1
                elif icd >=320 and icd<= 359:
                    big_icd[5] = big_icd[5] + 1
                elif icd >=360 and icd<= 389:
                    big_icd[6] = big_icd[6] + 1
                elif icd >=390 and icd<= 459:
                    big_icd[7] = big_icd[7] + 1
                elif icd >=460 and icd<= 519:
                    big_icd[8] = big_icd[8] + 1
                elif icd >=520 and icd<= 579:
                    big_icd[9] = big_icd[9] + 1
                elif icd >=580 and icd<= 629:
                    big_icd[10] = big_icd[10] + 1
                elif icd >=630 and icd<= 679:
                    big_icd[11] = big_icd[11] + 1
                elif icd >=680 and icd<= 709:
                    big_icd[12] = big_icd[12] + 1
                elif icd >=710 and icd<= 739:
                    big_icd[13] = big_icd[13] + 1
                elif icd >=740 and icd<= 759:
                    big_icd[14] = big_icd[14] + 1
                elif icd >=760 and icd<= 779:
                    big_icd[15] = big_icd[15] + 1
                elif icd >=780 and icd<= 799:
                    big_icd[16] = big_icd[16] + 1
                elif icd >=800 and icd<= 999:
                    big_icd[17] = big_icd[17] + 1
        out_data = pd.DataFrame()
        out_data['key'] = key
        out_data['count'] = big_icd
        return out_data
    def get_special_tran_code(self):
        df = pd.DataFrame(test._main_records['TranCode'].value_counts()).reset_index()
        special_7 = 0
        special_8 = 0
        special_9 = 0
        special_A = 0
        for row in df.itertuples():
            if getattr(row, "index") == 7:
                special_7 = special_7 + getattr(row, "TranCode")
            if getattr(row, "index") == 8:
                special_8 = special_8 + getattr(row, "TranCode")
            if getattr(row, "index") == 9:
                special_9 = special_9 + getattr(row, "TranCode")
            if getattr(row, "index") == 'A':
                special_A = special_A + getattr(row, "TranCode")
        out =[[
            special_7,
            special_8,
            special_9,
            special_A
        ]]
        return pd.DataFrame(out,columns=['special_7','special_8','special_9','special_A'])
    def get_patient_inpatient_interval(self):
        data = test._main_records[test._main_records['Type']==2]
        data['sn'] = [x for x in range(0,len(data))]
        interval_list = [0]
        for i in range(0,len(data)-1):
            second = data.loc[data['sn'] == i+1 ,'InDate'].values[0] - data.loc[data['sn'] == i ,'InDate'].values[0]
            days = second.astype('timedelta64[D]') / np.timedelta64(1, 'D')
            if(days > 0): 
                interval_list.append(days)
                interval_list[0]+=interval_list[-1]
        if(interval_list[0] == 0):
            return 0
        else:
            return interval_list[0]//(len(interval_list)-1) 
    def get_icd_name(self,_icd):
        return self._name_mapper[_icd]
    

