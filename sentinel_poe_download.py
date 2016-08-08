#!/root/.pyenv/versions/anaconda3-2.4.0/bin/python

############################################################
# V1.0 by Xiaowen Wang                         
# ESSC @ The Chinese University of Hong Kong	
# Aug-08, 2016	   
############################################################

"""
Python script for downloading the Sentinel-1 orbit data

1) Change the variable "work_path" to your own work_path, the work path
   should have the folder "RAW" where the unzipped S1A data are putted
2) run "python sentinel_poe_download.py"    
"""

import datetime
import urllib.request
import ssl
import re
import os
##############################################################################
# work_path and variables setting
work_path="/media/root/G/KunlunShan_S1A"

POE_path=work_path+"/POE"
RAW_path=work_path+"/RAW"
os.environ['POE_path']=str(POE_path);
os.environ['RAW_path']=str(RAW_path);

# Judge whether the POE folder is existing 
if os.path.exists(POE_path):
    print('Already having the POE foloder')
else:
    os.popen('mkdir $POE_path')

# List the raw list data 
im_list=os.popen('ls $RAW_path | grep ^S1A.*SAFE$').read().split()

######################
for im_var in im_list:
    print("Download the POE orbit file for the list Sentinel-1 image:\n", im_var)
    ###############################Read the image acquire time 
    Sensor=im_var[0:3];
    Sence_time=im_var[17:25];
    Year=int(Sence_time[0:4]);
    Month=int(Sence_time[4:6]);
    Day=int(Sence_time[6:8]);
    
    Sence_day=datetime.date(Year,Month,Day);
    Start_day=format(Sence_day-datetime.timedelta(days=1));
    End_day=format(Sence_day+datetime.timedelta(days=1));
    ##############################Generate the download url
    url_ymd=format(Sence_day);
    url_ym=url_ymd[0:7];
    url_pre='https://qc.sentinel1.eo.esa.int/aux_poeorb/?';
    url_poe='mission='+Sensor+'&validity_start_time='+str(Year)+'&validity_start_time='+url_ym+'&validity_start_time='+Start_day+'..'+End_day+'&validity_start_time='+url_ymd;
    url_download=url_pre+url_poe;
    
    ###############################Download the page_info and get the POE name 
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    up=urllib.request.urlopen(url_download,context=ctx)
    cont=up.read()
    
    #file_object = open('./dl.html', 'w') 
    #file_object.write(str(cont))
    #file_object.close()
    
    ###############################Download the POE data 
    #file_object = open('text.html').read()
    pat=re.compile(Sensor+"_OPER.*.EOF");
    pat_mat=pat.search(str(cont));
    
    if pat_mat is None:
        print("****The precise oribt data for this image is not avaible now****")
        continue
    else:    
        mat=pat_mat.group()
        POE_name=mat[0:77];
        POE_file=POE_path+'/'+POE_name
        if  os.path.exists(POE_file):
            print("****The orbit file has been download already****")
            continue
        else:
            dl_head="https://qc.sentinel1.eo.esa.int/aux_poeorb//"
            dl_url=dl_head+POE_name;
            data_tmp=urllib.request.urlopen(dl_url,context=ctx)
            data_w=data_tmp.read()
            with open(POE_file, "wb") as flg:     
                flg.write(data_w)
##############################################################################
