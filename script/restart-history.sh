ts=`date +"%Y-%m-%d %H:%M:%S"`
echo "restart $ts" >> history.log
sh stop-history.sh
sleep 2s
sh start-history.sh
