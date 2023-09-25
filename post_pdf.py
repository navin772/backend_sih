# import requests

# # Define the API endpoint
# url = 'http://127.0.0.1:5000/calculate_similarity'

# # Specify the PDF file you want to send
# files = {'pdf_file': ('shyong2020.pdf', open('shyong2020.pdf', 'rb'))}

# # Make a POST request with the PDF file
# response = requests.post(url, files=files)

# # Check the response
# if response.status_code == 200:
#     data = response.json()
#     print("Similarity scores:", data)
# else:
#     print("Error:", response.status_code, response.text)


import requests

# Define the API endpoint
url = 'http://127.0.0.1:5000/plag_score'

# Specify the PDF file you want to send
files = {'pdf_file': ('app_permission.pdf', open('app_permission.pdf', 'rb'))}

# Make a POST request with the PDF file
response = requests.post(url, files=files)

# Check the response
if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print("Error:", response.status_code, response.text)