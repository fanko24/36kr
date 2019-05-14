ts=`date +"%Y-%m-%d %H:%M:%S"`
echo "start $ts" >> history.log
touch history.error
nohup /usr/local/bin/python3 -u history.py >> history.log &
