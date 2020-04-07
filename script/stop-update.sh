ts=`date +"%Y-%m-%d %H:%M:%S"`
echo "update stop $ts" >> /Users/fanko/work/36kr/log/update.log
ids=`ps -ef | grep "main_update.py" | grep -v "$0" | grep -v "grep" | awk '{print $2}'`
for id in $ids
do
kill -9 $id
done
