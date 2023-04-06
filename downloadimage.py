import os
import psycopg2


#database_name = "verify_api_dev"  
database_name = "verify_api_qa"

#Below given credentials are of Read only access.
conn = psycopg2.connect(database= database_name,
                        host="ennoventure-dev.cus8qzqzmghy.us-east-1.rds.amazonaws.com",
                        user="analytics",
                        password="nl89JR2hJ9FRpmOe87eo9eO0xKD7",
                        port="5432")

scan_id_to_search = 'holostick_label_01'    #Give the particular client scan_id that you want to download
start_date = '2023-03-09'   # "year-month-date"        #Give start_date and end_date for the date range that you want to download. 
end_date = '2023-03-10'
result = 'GENUINE'
# user_agent_g = 'Mozilla/5.0 (Linux; Android 12; Nokia G20) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36'

#Give the desired path where you want to download the images
image_save_path = "/mnt/c/Users/SouravChatterjee/Downloads/G"


cursor = conn.cursor()

cursor.execute("select input_file_name from verification_session vs left join verification_task vt on vt.session_id=vs.session_id join (select pc.id as product_config_id, pp.scan_id,pp.decoder_config_id, pc.product_package_id from product_config pc join product_package pp on pc.product_package_id=pp.id) pcp on pcp.product_config_id=vs.product_config_id where scan_id='{0}' and input_file_name!='NULL' and process_start_time>='{1}' and process_start_time<='{2}' and result = '{3}' order by vs.id desc;".format(scan_id_to_search, start_date, end_date,result ))



# where scan_id='jupyter_01' and user_agent='Mozilla/5.0 (Linux; Android 10; Redmi Note 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36'

# print(cursor.fetchall())  
xy = cursor.fetchall()
#To store all the images in the list that needs to be downloaded
image_names_to_download = [xy[i][0] for i in range(len(xy))]

for i in  image_names_to_download:
    #Command to download dev server scanned  images that are stored in AWS s3 bucket
    #os.system("aws s3 cp s3://enncrypto-input-images/verification-dev1-server-0/{} {}".format(i, image_save_path))

    #uncomment the below line To download images scanned from qa server microsite  
     os.system("aws s3 cp s3://enncrypto-input-images/qa_verification1/{} {}".format(i, image_save_path)) 