# ses-alerts
AWS SES alerts to Slack

## Infrastructure

Cloudwatch Alarms -> AWS SNS -> Lambda -> Slack

## Setup

```
$ serverless plugin install --name serverless-package-python-functions
$ serverless deploy
```