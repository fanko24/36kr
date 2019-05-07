awk -F '"created_time": "' '{print $2}' history.36kr | awk '{print $1}' | awk '{sum[$1]+=1}END{for(key in sum) print key,sum[key]}' | sort -n
