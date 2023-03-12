import pickle
import json
import xml.etree.ElementTree as ET
import requests
from cryptography.fernet import Fernet

# Create a dictionary and a text file
my_dict = {'name': 'Alice', 'age': 25, 'city': 'New York'}
with open('text_file.txt', 'w') as f:
    f.write('This is a text file.')

# Serialize the dictionary using the specified format
pickling_format = input("Enter the pickling format (binary, JSON, or XML): ")
pickling_format = pickling_format.upper()
if pickling_format == "BINARY":
    serialized_dict = pickle.dumps(my_dict)
elif pickling_format == "JSON":
    serialized_dict = json.dumps(my_dict)
elif pickling_format == "XML":
    root = ET.Element('dict')
    for key, value in my_dict.items():
        child = ET.SubElement(root, key)
        child.text = str(value)
    serialized_dict = ET.tostring(root)
else:
    print("Invalid pickling format. Using JSON as default.")
    serialized_dict = json.dumps(my_dict)

key = None
# Encrypt the contents of the text file
encrypt = input("Do you want to encrypt the text file? (yes or no): ")
if encrypt == "yes":
    # Generate a random encryption key
    key = Fernet.generate_key()

    # Encrypt the contents of the text file using the encryption key
    with open('text_file.txt', 'rb') as f:
        plaintext = f.read()
        fernet = Fernet(key)
        ciphertext = fernet.encrypt(plaintext)
else:
    # Set the ciphertext variable to an empty value
    ciphertext = b''

# Send the serialized dictionary and encrypted text file to the server
files = {'file': ('text_file.txt', ciphertext)}
response = requests.post('http://localhost:8000', data={'dict': serialized_dict}, files=files, headers={'Key': key})
print(response.text)
