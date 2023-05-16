#Build-a-thon 2023
#Register here https://github.com/vrra/FGAN-Build-a-thon/issues/new/choose
#Created: 16 May 2023
#Author: Vishnu Ram OV.   
#vishnu.n@ieee.org.   
#Licence: available for all purposes under the sun  
#but with acknowledgement and citation to "ITU FG AN Build-a-thon"

#CAUTION
#this runs inside the container spawned by github actions
#expects magik file issue.out in the same dir as this py script.

import os
import json

import subprocess
import sys

subprocess.check_call([sys.executable, "-m", "pip", "install", 'argilla'])
# process output with an API in the subprocess module:
reqs = subprocess.check_output([sys.executable, '-m', 'pip',
'freeze'])
installed_packages = [r.decode().split('==')[0] for r in reqs.split()]

print(installed_packages)

import argilla as rg

uri= os.environ.get("API_URL")
key= os.environ.get("API_KEY")
my_argilla_workspace = os.environ.get("ARGILLA_WORKSPACE")

rg.init(    
    api_url=uri, 
    api_key=key,
    workspace=my_argilla_workspace
)

issue_json= os.environ.get("SCRIPTS_DIR") + '/issue.out'
print("current working dir = "+os.getcwd())
print("issue_json = "+issue_json)

with open(issue_json, 'r') as json_file:
    json_object = json.load(json_file)

issue_body=json_object["event"]["issue"]["body"]
issue_body_list=issue_body.split("###")

#print("issue_body_list= ", issue_body_list)

#NOTE- we use max split as 1 to avoid false positive of double \n\n in the body.
team_name=issue_body_list[1].split("\n\n", 1)
usecase_text=issue_body_list[2].split("\n\n", 1)
ref=issue_body_list[3].split("\n\n", 1)

print(team_name)
print(usecase_text)
print(ref)

record = rg.TextClassificationRecord(
                text=usecase_text,
                    # Extra information about this record
                metadata={
                        "split": "train",
                        "team_name": team_name,
                        "ref": ref
                    },
                )
dataset_rg = rg.DatasetForTextClassification([record])
rg.log(dataset_rg, "fgan23allpages")