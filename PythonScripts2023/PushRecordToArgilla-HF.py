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

with open('issue.out', 'r') as json_file:
    json_object = json.load(json_file)
print(json.dumps(json_object, indent=1))