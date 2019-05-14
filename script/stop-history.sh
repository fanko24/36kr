ts=`date +"%Y-%m-%d %H:%M:%S"`
echo "stop $ts" >> history.log
ids=`ps -ef | grep "history.py" | grep -v "$0" | grep -v "grep" | awk '{print $2}'`
for id in $ids
do
kill -9 $id
done
