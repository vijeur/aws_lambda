import boto3
import httplib
websiteURL = ["www.google.com", "www.youtube.com"]
topicArnCode = 'arn:aws:sns:eu-central-1::website-offline'

def lambda_handler(event, context):
    for x in websiteURL:
        conn = httplib.HTTPConnection(x)
        conn.request("HEAD", "/")
        r1 = conn.getresponse()
        if r1.status == 200 or r1.status == 301:
            print(r1.status, r1.reason)
            print("Website %s Is Alive!" % x ) 
        else:
          sns = boto3.client('sns')
          sns.publish(
            TopicArn = topicArnCode,
            Subject = 'Website Offline' ,
            Message = 'Status code 200 was expected but returned was '+ str(r1.status)
        )
