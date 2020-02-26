ts=`date +"%Y-%m-%d %H:%M:%S"`
echo "start $ts" >> update.log
touch update.error
nohup /usr/local/bin/python3 -u update.py >> update.log &
