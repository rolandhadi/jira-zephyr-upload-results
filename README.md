# jira-zephyr-upload-results
Upload JUnit Automated Test Execution Reports to Jira-Zephyr using Python for Devops/CI/CD


Zephyr for JIRA is a native application that exists in JIRA and brings quality test management capabilities to any JIRA project. When Zephyr is used with JIRA, the test can be created, viewed in any JIRA project, and executed immediately or as part of a testing cycle that may be linked to other issues

# update config [sample values]

```
zfj.cloud.jwt.url=https://prod-vortexapi.zephyr4jiracloud.com/api/v1/jwt/generate
zfj.cloud.create.url=https://prod-vortexapi.zephyr4jiracloud.com/api/v1/automation/job/create
zfj.cloud.execute.url=https://prod-vortexapi.zephyr4jiracloud.com/api/v1/automation/job/execute
zfj.cloud.access.key=ZaIxOGRiY2ItMjE1ZC0zNzg2LfhkMDctODMwOTA4NmU3YmVkIDU1NzA1OCUzRWUzMGNhYjE3LTc5BjUtNDVhOS1iPTBkLWMyOSAzNzZjMmUwYyBLU0VSX0RFRkFVTFRfTkFNR1
zfj.cloud.secret.key=Mal-xPzBV8XuIHPeYN8_FReQ2Ae-PqVX9dRmIFA4K7f
zfj.cloud.account.id=517051:e30cab15-79b4-45a9-b60d-c290376c1e0c
zfj.cloud.account.user=roland.hadi@email.com
zfj.cloud.projectKey=PRJ
zfj.cloud.report.jobName=Appium
zfj.cloud.report.automationFramework=Tricentis Tosca
jira.cloud.server=https://company.atlassian.net
jira.cloud.auth.name=roland.hadi@email.com
jira.cloud.auth.password=a62Yy3AiTPvB3gacCcP3A081
jira.cloud.attachment.extension=html
jira.cloud.report.issuekey=PRJ-80
```

jira.cloud.report.issuekey is a jira id where you want to upload screenshots, other reports etc.

# usage
```
python TestAutomation.py attach "<junit_report.xml>" "<jira_version>" "<zephyr_test_cycle>"
```
