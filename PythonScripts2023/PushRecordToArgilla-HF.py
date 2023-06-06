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
#Called from the workflow sample-1.yml


import os
import json

import subprocess
import sys

reqs = subprocess.check_output([sys.executable, '-m', 'pip',
'freeze'])
installed_packages = [r.decode().split('==')[0] for r in reqs.split()]

print(installed_packages)

#subprocess.check_call([sys.executable, "-m", "pip", "install", "argilla"])
# process output with an API in the subprocess module:
#reqs = subprocess.check_output([sys.executable, '-m', 'pip',
#'freeze'])
#installed_packages = [r.decode().split('==')[0] for r in reqs.split()]

#print(installed_packages)
print(sys.path)

import argilla as rg

uri= os.environ.get("API_URL")
key= os.environ.get("API_KEY")
my_argilla_workspace = os.environ.get("ARGILLA_WORKSPACE")
my_push_to_hf_hub_token=os.environ.get("MY_PUSH_TO_HF_HUB_TOKEN")
my_db_name=os.environ.get("DB_NAME")
my_hf_hub_name=os.environ.get("HF_HUB_NAME")
my_issue_label=os.environ.get("MY_ISSUE_LABEL")


print(uri)
print(key)
print(my_argilla_workspace)
print(my_db_name)
print(my_hf_hub_name)
print(my_issue_label)

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

issue_label=json_object["event"]["issue"]["labels"][0]["name"]
print("issue_label= ", issue_label)

if (my_issue_label == issue_label):
    print("This is a use case submission! lets process it!")

    #NOTE- we use max split as 1 to avoid false positive of double \n\n in the body.
    team_name=issue_body_list[1].split("\n\n", 1)
    usecase_text=issue_body_list[2].split("\n\n", 1)
    ref=issue_body_list[3].split("\n\n", 1)

    team_name=team_name[1]
    usecase_text=usecase_text[1]
    ref=ref[1]

    print("team_name= ", team_name)
    print("usecase_text = ", usecase_text)
    print("ref = ", ref)

    record = rg.TextClassificationRecord(
                    text=usecase_text,
                        # Extra information about this record
                    metadata={
                            "split": "train",
                            "team_name": team_name,
                            "ref": ref
                        },
                    )

    #NOTE- sub-optimal: at this point, all records will configure the db
    settings = rg.TextClassificationSettings(label_schema=["Usecase", "Architecture", "PoC", "Other"])
    rg.configure_dataset(name=my_db_name, settings=settings)

    dataset_rg = rg.DatasetForTextClassification([record])
    rg.log(dataset_rg, my_db_name)

    ### push the dataset to the Hugging Face Hub
    from huggingface_hub import login
    login(token=my_push_to_hf_hub_token)

    #NOTE- sub-optimal: at this point, all records will push the entire db to hf hub
    from datasets import load_dataset
    dataset_rg = rg.load(my_db_name)
    dataset_ds = dataset_rg.to_datasets()

    #push the dataset to the Hugging Face Hub
    dataset_ds.push_to_hub(my_hf_hub_name)
else:
    print("This is not a use case submission! lets forget it!")
