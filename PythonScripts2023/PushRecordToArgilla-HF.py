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

print(os.environ.get("API_URL"))
print(os.environ.get("API_KEY"))
print(os.environ.get("ARGILLA_WORKSPACE"))
print(os.environ.get("VISHNURAMOV_PUSH_TO_HF_HUB_TOKEN"))
print(os.environ.get("SCRIPTS_DIR"))

issue_json= os.environ.get("SCRIPTS_DIR") + '/issue.out'
print("current working dir = "+os.getcwd())
print("issue_json = "+issue_json)

with open(issue_json, 'r') as json_file:
    json_object = json.load(json_file)

issue_body=json_object["event"]["issue"]["body"]
issue_body_list=issue_body.split("###")
print(issue_body_list)