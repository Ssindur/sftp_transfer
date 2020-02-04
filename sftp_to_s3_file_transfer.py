import boto3
from botocore.exceptions import NoCredentialsError
import pysftp as sftp
import Crypto
import paramiko 
import os as os
import shutil
from datetime import datetime, date

ACCESS_KEY = 'XXXXXXXXXXXXXXXXXXXXXXX'
SECRET_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
remotedirectorypath = "XXXXXXXXXXXXXXXX"
s3_file_path = "XXXXXXXXXXXXXXXX"
localdirectorypath = "C:\\Users\\Sindur\\Downloads\\sftp\\"


def sftpDownload():
    cnopts = sftp.CnOpts()
    cnopts.hostkeys = None
    localpath = "C:\\Users\\Sindur\\Downloads\\sftp\\"
    try:

        with sftp.Connection(host = "conduit.novonordisk-us.com",username = "XXXXX",password = "XXXXX",cnopts = cnopts)as conn:
            print("Connection succesfully established ... ")
            print("Directory Information")
            #print(conn.chdir('/Folders/Impact/Test'))
            # Switch to a remote directory= '/Folders/Impact/Test/'
            conn.cwd('/Folders/Impact/Test/')

            remotedirectorypath = '/Folders/Impact/Test/'
            # Obtain structure of the remote directory on sftp server
            directory_structure = conn.listdir_attr()
            #Checking folder empty
            # Print data and load data
            for attr in directory_structure:
                print(remotedirectorypath + str(attr.filename), attr)
                remotefilepath = remotedirectorypath + str(attr.filename)
                print(remotefilepath)
                #To download the file from the remote directory to localpath
                conn.get(remotefilepath, os.path.join(localpath,attr.filename))

        conn.close()
        return True

    except PermissionError:
        print(f"Files could not be downloaded from remote directory. Please Investigate. ")
        return False

    except Exception as Error:
        print(f"Connection to remote directory is not established. Please Investigate. ")
        return False



def UploadToS3(local_file, bucket, s3_file):

    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)

    try:
        
        local_file = "C:\\Users\\Sindur\\Downloads\\NOVONORDISK\\sftp\\"
        for filename in os.listdir(local_file):
            print("file: ", filename)
            file_path= str(Path_folder+filename)
            print("file_path: ",file_path)
            s3.Bucket('bucket').upload_file(file_path, '%s/%s' %('s3_file',filename))
            print("Upload Successful")
        return True

    except FileNotFoundError:
        print("The file was not found. Please Investigate.")
        return False

    except NoCredentialsError:
        print("Credentials not available.Please Investigate.")
        return False
    
    except Exception as Error:
        print(f"Files are not uploaded to s3. Please Investigate. ")
        return False

def CleanUpBackUP():
    localpath = "C:\\Users\\Sindur\\Downloads\\NOVONORDISK\\sftp"
    #Adding date fro the backup file
    backuppath = "C:\\Users\\Sindur\\Downloads\\NOVONORDISK\\sftp\\backup_" + str(date.today()).replace("-","_")
    print(backuppath)
    #print(datetime.now().strftime("%H:%M:%S").replace(":","_"))
    backuppath = backuppath + "_" + str(datetime.now().strftime("%H:%M:%S")).replace(":","_") + "\\"
    
    print(backuppath)
    os.mkdir(backuppath)
    
    try:
        for file_name in os.listdir(localpath):
            full_file_name  = os.path.join(localpath,file_name)
            print(full_file_name)
            if (os.path.isfile(full_file_name)):
                shutil.copy(full_file_name,os.path.join(backuppath,file_name))
                print("file copied and it can be deleted")
                os.remove(full_file_name)
                print("file deleted")
        return True
                
    except Exception as Error:
        print(f"Flies are not copied or deleted. Please Investigate.")
        return False
    


uploaded = UploadToS3('localdirectorypath', 'bucket_name', 's3_file_path')
sftpDownload()
CleanUpBackUP()



