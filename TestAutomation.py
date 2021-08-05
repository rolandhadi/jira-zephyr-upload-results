import re
import os
import sys
import json
import pdfkit
import requests
import configparser
from jira import JIRA

from ConvertReport import convert_xml


def upload_feature_report(filename, attachment):
    filename = filename.replace('"', "")
    if '.htmlx' in attachment:
        pdfkit.from_file(attachment, attachment.replace(".htmlx", ".pdf"), options={
            'page-size': 'Legal',
            'margin-top': '0in',
            'margin-right': '0in',
            'margin-bottom': '0in',
            'margin-left': '0in',
            'encoding': "UTF-8",
            'no-outline': None,
            "orientation": "Landscape"
        })
        filename = filename.replace(".htmlx", ".pdf")
        attachment = attachment.replace(".htmlx", ".pdf")
    config_parameters = configparser.ConfigParser()
    config_parameters.read('application.ini')
    issue_key = config_parameters['DEFAULT']['jira.cloud.report.issuekey']
    jira = JIRA(server=config_parameters['DEFAULT']['jira.cloud.server'],
                basic_auth=(config_parameters['DEFAULT']['jira.cloud.auth.name'],
                            config_parameters['DEFAULT']['jira.cloud.auth.password']))
    jira.add_attachment(issue=str(issue_key),
                        attachment=attachment,
                        filename=filename)
    print(filename + ' uploaded!')


if __name__ == "__main__":
    config_parameters = configparser.ConfigParser()
    config_parameters.read('application.ini')
    if sys.argv[1] == "":
        print("Command not found!")
        exit()
    if sys.argv[1] == "create":
        if sys.argv[2] == "":
            print("Result path not found!")
            exit()
        if sys.argv[3] == "":
            print("Version name not found!")
            exit()
        if sys.argv[4] == "":
            print("Cycle name not found!")
            exit()
        sys.argv[3] = sys.argv[3].replace('"', "")
        sys.argv[4] = sys.argv[4].replace('"', "")
        print("Result path: " + sys.argv[2])
        print("Version name: " + sys.argv[3])
        print("Cycle name: " + sys.argv[4])

        url = config_parameters['DEFAULT']['zfj.cloud.jwt.url']

        payload = json.dumps({
            "accessKey": config_parameters['DEFAULT']['zfj.cloud.access.key'],
            "secretKey": config_parameters['DEFAULT']['zfj.cloud.secret.key'],
            "accountId": config_parameters['DEFAULT']['zfj.cloud.account.id']
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        jwt_token = response.text
        print("jwt token: " + jwt_token)

        result_path = sys.argv[2]
        file_list = [f for f in os.listdir(result_path) if f.endswith(".xml") and f != "MetaSettings.xml"]
        for f in file_list:
            convert_xml(result_path + "/" + f)
            url = config_parameters['DEFAULT']['zfj.cloud.create.url']
            payload = {'jobName': config_parameters['DEFAULT']['zfj.cloud.report.jobName'],
                       'automationFramework': config_parameters['DEFAULT']['zfj.cloud.report.automationFramework'],
                       'versionName': sys.argv[3],
                       'cycleName': sys.argv[4],
                       'projectKey': config_parameters['DEFAULT']['zfj.cloud.projectKey'],
                       'assigneeUser': config_parameters['DEFAULT']['zfj.cloud.account.id'],
                       'mandatoryFields': '{"reporter": {"id": "' + config_parameters['DEFAULT'][
                           'zfj.cloud.account.id'] + '"}}'
                       }
            headers = {
                'jwt': jwt_token,
                'accessKey': config_parameters['DEFAULT']['zfj.cloud.access.key']
            }
            files = [
                ('file', (f,
                          open(result_path + "/" + f, 'rb'),
                          'text/xml'))
            ]
            response = requests.request("POST", url, headers=headers, data=payload, files=files)
            print(f + ": " + response.text)
            x = re.search('Job id is : (.*)"', response.text)
            url = config_parameters['DEFAULT']['zfj.cloud.execute.url']
            payload = {'jobId': x[1]}
            headers = {
                'jwt': jwt_token,
                'accessKey': config_parameters['DEFAULT']['zfj.cloud.access.key']
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            print(f + ": " + response.text)
            # os.remove(os.path.join(result_path, f))
    elif sys.argv[1] == "attach":
        if sys.argv[2] == "":
            print("Attachment not found!")
            exit()
        if sys.argv[3] == "":
            print("Version not found!")
            exit()
        if sys.argv[4] == "":
            print("Cycle not found!")
            exit()
        upload_feature_report(
            sys.argv[3] + "|" + sys.argv[4] + "." + config_parameters['DEFAULT']['jira.cloud.attachment.extension'],
            sys.argv[2])
    else:
        print("Invalid command!")
