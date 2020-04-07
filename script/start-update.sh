ts=`date +"%Y-%m-%d %H:%M:%S"`
echo "update start $ts" >> /Users/fanko/work/36kr/log/update.log
nohup /usr/local/bin/python3 -u /Users/fanko/work/36kr/bin/main_update.py &
