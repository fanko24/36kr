ts=`date +"%Y-%m-%d %H:%M:%S"`
echo "restart $ts" >> update.log
sh stop-update.sh
sleep 2s
sh start-update.sh
