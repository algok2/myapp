import os
import sys
import zipfile
import shutil
import datetime
import socket
import logging.config
 
#copy files and folder and compress into a zip file
def doprocess(source_folder, target_zip):
    zipf = zipfile.ZipFile(target_zip, "w")
    for subdir, dirs, files in os.walk(source_folder):
        for file in files:
            print(os.path.join(subdir, file))
            zipf.write(os.path.join(subdir, file))    
    print( "Created ", target_zip)    
 
#copy files in the folder to a target folder
def doDcopy(source_folder, target_folder):
    for subdir, dirs, files in os.walk(source_folder):
        for file in files:
            print(os.path.join(subdir, file))
            shutil.copy2(os.path.join(subdir, file), target_folder)
            
#copy a file to a target folder
def doFcopy(source_file):
    shutil.copy2(source_file, target_folder)
    print("Copied ", source_file)
 #%%
if __name__ =='__main__':
    print('Starting backup')
    hostName = socket.gethostname()
    yearDate = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
    currDir = hostName+'_'+yearDate
   
    backup_list = sys.argv[1]
    
    backup_folder = sys.argv[2]
    target_folder = os.path.join(backup_folder, currDir)   
#%%   
    if not os.path.exists(target_folder):
        os.mkdir(target_folder)
        print("Directory " , target_folder ,  " Created. ")
    else:
        print("Directory " , target_folder ,  " already exists.")   
#%%   
    for filelineno, line in enumerate(open(backup_list, encoding="utf-8")):
        source_file = line.strip()
        if os.path.isdir(source_file):             
            #compress to zip
            fileDir, lastName = os.path.split(source_file)       
            backup_zip = lastName+'.zip'
            target_zip = os.path.join(target_folder, backup_zip)
            doprocess(source_file, target_zip) 
            ##copy to backup dirctory
            #doDcopy(source_folder, target_folder)
        elif os.path.isfile(source_file):
            #copy to backup file
            doFcopy(source_file)
        else: 
            print("It is a special file (socket, FIFO, device file)", source_file)
        print()