import csv
import json
import threading
from faker import Faker
import random
import requests
import random


fake = Faker()

# Define list of genders
genders = ['Male', 'Female']

# Define number of rows to generate
num_rows = 100

# Create CSV file and write headers

def func():
    # Write random data for each row
    for i in range(num_rows):
        fname = fake.sentence()
        # Open the file and read all the lines into a list
        with open('file.txt') as file:
            lines = file.readlines()

        url = 'https://blog-app-o7s6emedkq-uc.a.run.app/create_blog'
        data = {
            'id': random.choice(lines).strip(),
            'name': fname,
            'content': fake.text()
        }
        headers = {'Content-Type': 'json'}

        json_data = json.dumps(data)


        # Send the POST request and get the response
        response = requests.post(url, data=json_data, headers = headers)
        with open('file1.txt', mode='a') as file:
            file.write(fname+'\n')
        

    
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
