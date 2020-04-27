import sys
import pandas as pd
from pprint import pprint as pp
import requests
import json


def get_data_from_file(excel_filename, excel_sheetname):
    columns_to_include = ['login', 'firstName', 'lastName', 'email', 'ApplicationIdentifier']
    data = pd.read_excel(excel_filename, sheet_name=excel_sheetname)
    #print(data)
    df = pd.DataFrame(data, columns=columns_to_include)
    #print(df)
    #print(df.values)
    return df.values


def process_data(data):
    list_of_profiles = []
    user_profile = {}
    credentials = {
        "password": {"value": "tlpWENT2m@"}
    }
    groups = ["00gr5dcfp7YYKiLbr0h7"]
    for record in data:
        user_profile = {}
        profile = {}
        login, firstName, lastName, email, application_id = record
        profile["login"]=login
        profile["firstName"] = firstName
        profile["lastName"]= lastName
        profile["email"] = email
        #user_profile["profile"] = profile
        #user_profile["credentials"] = credentials
        #user_profile.append(profile)
        #user_profile.append(credentials)
        list_of_profiles.append([{"profile": profile}, {"credentials": credentials}, {"groupIds": groups}])
    #print(profiles)
    return list_of_profiles


def create_activated_user_with_password(url, api_key, data):
    if len(api_key)==0:
        message = "Please specify the api key to proceed with submitting requests"
        return message
    headers = {"Content-Type": "application/json", "Authorization": "SSWS"+api_key}
    payload = {}
    for info in data:
        payload.update(info)
    print("-------------------------------------------------------")
    print("Printing the required data before posting...")
    url = url+'api/v1/users?activate=false'
    print(url)
    print(headers)
    payload = json.dumps(payload)
    print(payload)
    response = requests.post(url, data=payload, headers=headers)
    #print(response.text)
    #print(response.status_code)
#    print("sending request for the following payload data: %s".format(payload))

    if(response.status_code == 200):
        print(response.text)
    else:
        print("request failed with the status code: {}".format(response.status_code))
        print("request failed with the error: {}".format(response.text))
    print("---------------------------------------------------------------------------------------")


def main(excel_filename, excel_sheetname):
    #'scc_test_upload_4_15.xlsx' 'in'
    data = get_data_from_file(excel_filename, excel_sheetname)
    profiles_payload = process_data(data)
    for user_payload in profiles_payload:
        #print(user_payload)
        create_activated_user_with_password(url, api_key, user_payload)


if __name__ == '__main__':
    url = 'https://wabtec.oktapreview.com/'
    api_key = '' #add your api_key here for submitting requests to okta
    if(len(sys.argv)==1):
        excel_filename, excel_sheetname= 'scc_test_upload_4_15.xlsx', 'in'
        main(excel_filename, excel_sheetname)
    else:
        main(sys.argv[1], sys.argv[2])