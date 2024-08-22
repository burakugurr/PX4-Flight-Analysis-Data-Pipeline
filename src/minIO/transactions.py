from minio import Minio
from minio.error import S3Error
from parser import ParseUlog
import os


class minIOClient:
    def create_connection(self):
        try:
            client = Minio('192.168.1.149:9000',
                access_key="NhXO9L7ix4gh8Z9l9AWw",
                secret_key="GDs1wJZk1BrkzN4kVIez0JaC43KGHKKp28NPdmYl", 
                secure=False) 
        except:
            return "did not connect"
        return client

    def read_ulog_file(self,object_name,bucket_name='ulogs'):
        try:
            object_name = object_name + ".ulog"
            client = self.create_connection()
            print("Connected...")
            # Get the file content
            response = client.fget_object(bucket_name, object_name,'../downloads/'+object_name )

            if response is None:
                return "Ulog file did not found..."
            
            parse_ulog = ParseUlog()
            parse_ulog.convert_ulog2csv('../downloads/'+object_name)
            print("Process Done!...")

        except S3Error as err:
            print(err)


    def upload_csv(self,object_name):
        object_name = object_name + ".ulog"

        client = self.create_connection()
        list_dir = os.listdir("../outputs")
        for path in list_dir:
            print("upload this file", path)
            client.fput_object(
                "csv-outputs","{}/{}".format(object_name,path),"../outputs/"+path
            )
            os.remove("../outputs/"+path)
        # os.remove("../downloads")

mi = minIOClient()
mi.read_ulog_file('test')

# upload_csv("burak_test")