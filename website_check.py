from botocore.vendored import requests
import boto3
 
websiteURL = 'https://www.google.com'
topicArnCode = 'arn:aws:sns:eu-central-1::website-offline'

def lambda_handler(event, context):
    r = requests.head(websiteURL) 
    if r.status_code == 200:
        print "Website Is Alive!"
    else:
        sns = boto3.client('sns')
        sns.publish(
            TopicArn = topicArnCode,
            Subject = 'Website Offline' ,
            Message = 'Status code 200 was expected but returned was '+ str(r.status_code)
        )
