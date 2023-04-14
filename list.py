import csv
import json
import threading
from faker import Faker
import random
import requests

# Define the API endpoint URL and the data to be sent in the POST request


fake = Faker()

# Define list of genders
genders = ['Male', 'Female']

# Define number of rows to generate
num_rows = 500

# Create CSV file and write headers

def func():
    # Write random data for each row
    for i in range(num_rows):

        url = 'https://blog-app-o7s6emedkq-uc.a.run.app/create_user'
        data = {
            'name': fake.name(),
            'dob': fake.date_of_birth().strftime('%Y-%m-%d'),
            'gender': random.choice(genders)
        }
        headers = {'Content-Type': 'json'}

        json_data = json.dumps(data)


        # Send the POST request and get the response
        response = requests.post(url, data=json_data, headers = headers)
        res = str(response.content)
        lis=res.split('"')
        with open('file.txt', mode='a') as file:
            file.write(lis[-2]+'\n')

    
t1 = threading.Thread(target=func)
t2 = threading.Thread(target=func) 
t3 = threading.Thread(target=func)
t4 = threading.Thread(target=func)
t5 = threading.Thread(target=func)
t6 = threading.Thread(target=func)
t7 = threading.Thread(target=func)
t8 = threading.Thread(target=func)
t9 = threading.Thread(target=func)
t10 = threading.Thread(target=func)
# starting threads
t1.start()
t2.start()
t3.start()
t4.start()
t5.start()
t6.start()
t7.start()
t8.start()
t9.start()
t10.start()
# wait until all threads finish
t1.join()
t2.join()
t3.join()
t4.join()
t5.join()
t6.join()
t7.join()
t8.join()
t9.join()
t10.join()
