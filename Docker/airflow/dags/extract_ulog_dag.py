from pyulog import *
from minio import Minio
from minio.error import S3Error
import os
import datetime
import numpy as np

from airflow.utils.email import send_email
from airflow.decorators import dag, task

FLIGHTNAME = 'test'

def send_success_status_email(context):
    pass
def send_failure_status_email():
    print("ERROR EMAİL")


class minIOClientProcess:

    def convert_ulog2csv(self,ulog_file_name):
        ulog = ULog(ulog_file_name)
        data = ulog.data_list
        delimiter = ','
        
        time_s = None
        time_e = None
        
        output_file_prefix = ulog_file_name
        # strip '.ulg'
        if output_file_prefix.lower().endswith('.ulg'):
            output_file_prefix = output_file_prefix[:-4]

        base_name = os.path.basename(output_file_prefix)
        output_file_prefix = os.path.join("/opt/airflow/dags/outputs", base_name) #baseline

        for d in data:
            fmt = '{0}_{1}_{2}.csv'
            output_file_name = fmt.format(output_file_prefix, d.name.replace('/', '_'), d.multi_id)
            fmt = 'Writing {0} ({1} data points)'
    
            with open(output_file_name, 'w', encoding='utf-8') as csvfile:

                # use same field order as in the log, except for the timestamp
                data_keys = [f.field_name for f in d.field_data]
                data_keys.remove('timestamp')
                data_keys.insert(0, 'timestamp')  # we want timestamp at first position

                csvfile.write(delimiter.join(data_keys) + '\n')

                #get the index for row where timestamp exceeds or equals the required value
                time_s_i = np.where(d.data['timestamp'] >= time_s * 1e6)[0][0] \
                        if time_s else 0
                #get the index for row upto the timestamp of the required value
                time_e_i = np.where(d.data['timestamp'] >= time_e * 1e6)[0][0] \
                        if time_e else len(d.data['timestamp'])

                # write the data
                last_elem = len(data_keys)-1
                for i in range(time_s_i, time_e_i):
                    for k in range(len(data_keys)):
                        csvfile.write(str(d.data[data_keys[k]][i]))
                        if k != last_elem:
                            csvfile.write(delimiter)
                    csvfile.write('\n')

    def create_connection(self):
        try:
            client = Minio('192.168.1.149:9000',
                access_key="NhXO9L7ix4gh8Z9l9AWw",
                secret_key="GDs1wJZk1BrkzN4kVIez0JaC43KGHKKp28NPdmYl", 
                secure=False) 
        except:
            return "did not connect"
        return client

    def download_ulog(self,object_name,bucket_name='ulogs'):
        try:
            object_name = object_name+".ulog"
            print("UlogName:",object_name, './downloads/'+object_name)

            client = self.create_connection()
            print("Connected...")
            # Get the file content
            response = client.fget_object(bucket_name, object_name,'/opt/airflow/dags/downloads/'+object_name)
            print("ulog file download....",response)

            if response is None:
                return False
   
            if(os.path.exists('/opt/airflow/dags/'+object_name) ):
                print("File not found in directory.")
                
            return True
                
        except S3Error as err:
            print(err)


    def read_ulog_file(self,object_name):
        try:
            object_name = object_name+".ulog"
            if(os.path.exists('/opt/airflow/dags/outputs/') == False):
                print("outputs not found in dir. Directory will be create..")
                os.makedirs("/opt/airflow/dags/outputs")

            self.convert_ulog2csv('/opt/airflow/dags/downloads/'+object_name)
            print("Process Done!...")

        except S3Error as err:
            print(err)

    def upload_csv(self,object_name):
        client = self.create_connection()
        list_dir = os.listdir("/opt/airflow/dags/outputs/")
        for path in list_dir:
            print("upload this file", path)
            client.fput_object(
                "csv-outputs","{}/{}".format(object_name,path),"/opt/airflow/dags/outputs/"+path
            )
            #os.remove("./outputs/"+path)
        # os.remove("../downloads")
        return True

email = "titra.burak@gmail.com"
html_content = """
    Hi, <br>
    <br>
    Flight insert successfully .<br>
    <br>
    Forever yours,<br>
    Airflow bot <br>

"""
@dag(
     dag_id="Extract_Ulog_File",
     start_date=datetime.datetime(2024, 8, 18),
     schedule="@daily",
     tags=["ulog"]
 )
def ExtractUlog():
    @task()
    def parseUlog():
        mi = minIOClientProcess()

        status_read = mi.download_ulog(FLIGHTNAME)

        if(status_read == True):
            
            mi.read_ulog_file(FLIGHTNAME)

            status_upload = mi.upload_csv(FLIGHTNAME)

            if(status_upload != True):
                print("Upload Error")
        else:
            print("Download Error")


    @task
    def sendMail():
        send_email(to=email, subject= FLIGHTNAME +"Flight insert successfully", html_content=html_content)


        
    parseUlog() >> sendMail()
        
extart = ExtractUlog()