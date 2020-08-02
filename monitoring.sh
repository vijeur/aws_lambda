instance=\$(wget -q -O - http://169.254.169.254/latest/meta-data/instance-id)
account=\$(curl http://169.254.169.254/latest/dynamic/instance-identity/document|grep accountId| awk '{print \$3}'|sed  's/"//g'|sed 's/,//g' )
web_status=\$(systemctl | grep running | grep nginx| wc -l)
if [ "\$web_status" == "0" ]
then
    echo "nginx service not running"
    current=\$(cat /root/web_status)
    if [ \$current == "1" ]
    then
        echo "do nothing"
    else
        aws sns publish --region="us-west-2" --topic-arn "arn:aws:sns:us-west-2:\$account:${InstanceName}" --message "Nginx Service not running on \$instance ${InstanceName}"
        systemctl start nginx
        echo "1" > /root/web_status
        crontab alert-cron
    fi
fi

db_status=\$(systemctl | grep running | grep mongod| wc -l)
if [ "\$db_status" == "0" ]
then
    echo "db service not running"
    current=\$(cat /root/db_status)
    if [ \$current == "1" ]
    then
        echo "do nothing"
    else
        aws sns publish --region="us-west-2" --topic-arn "arn:aws:sns:us-west-2:\$account:${InstanceName}" --message "MongoDB Service is not running on \$instance ${InstanceName}"
        systemctl start mongod
        echo "1" > /root/db_status
        crontab alert-cron
    fi
fi            
EOF

cat <<EOF > /root/status.sh
#!/bin/bash
web_status=\$(systemctl | grep running | grep nginx| wc -l)
if [ \$web_status == "1" ]
then
    echo 0 > /root/web_status
    crontab /root/status-cron
fi
db_status=\$(systemctl | grep running | grep mongod| wc -l)
if [ \$db_status == "1" ]; then
    crontab /root/status-cron
    echo 0 > /root/db_status
fi            
EOF

cat <<EOF > /root/alert-cron
*/1 * * * * bash /root/status.sh      
EOF

cat <<EOF > /root/status-cron
*/1 * * * * bash /root/alert.sh      
EOF

echo "0" > /root/web_status
echo "0" > /root/db_status
crontab /root/status-cron            ꌀ        
