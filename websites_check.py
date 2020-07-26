import boto3
import urllib2
def write_metric(value, metric):
    d = boto3.client('cloudwatch')
    d.put_metric_data(Namespace='Website Status',
                      MetricData=[
                          {
                              'MetricName': metric,
                              'Dimensions': [
                                  {
                                      'Name': 'Status',
                                      'Value': 'WebsiteStatusCode',
                                  },
                              ],
                              'Value': value,
                          },
                      ]
                      )

def check_site(url, metric):
    STAT = 1

    print("Checking %s " % url)
    request = urllib2.Request("http://" + url)
    try:
        response = urllib2.urlopen(request)
    response.close()
    except urllib2.URLError as e:
    if hasattr(e, 'code'):
        print("[Error:] Connection to %s failed with c
        STAT = 100
        write_metric(STAT, metric)
        if hasattr(e, 'reason'):
            print("[Error:] Connection to %s failed with c
        STAT = 100
        write_metric(STAT, metric)
        except urllib2.HTTPError as e:
        if hasattr(e, 'code'):
            print("[Error:] Connection to %s failed with c
            STAT = 100
            write_metric(STAT, metric)
            if hasattr(e, 'reason'):
                print("[Error:] Connection to %s failed with c
            STAT = 100
            write_metric(STAT, metric)
            print('HTTPError!!!')
            if STAT != 100:
                STAT = response.getcode()
        return STAT

def lambda_handler(event, context):

    # Change these to your actual websites. Remember, the more web
    # the longer the lambda function will run
    websiteurls = [
        "example.com",
        "example2.com",
        "test.com"
    ]
    metricname = 'Site Availability'
    for site in websiteurls:
        r = check_site(site, metricname)
    if r == 200 or r == 304:
        print("Site %s is up" % site)
    write_metric(200, metricname)
    else:
    print("[Error:] Site %s down" % site)
    write_metric(50, metricname)
