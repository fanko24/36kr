ts=`date +"%Y-%m-%d %H:%M:%S"`
echo "update restart $ts" >> /Users/fanko/work/36kr/log/update.log
sh stop-update.sh
sleep 2s
sh start-update.sh
