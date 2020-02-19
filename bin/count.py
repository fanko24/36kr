import sys
import json

if __name__ == "__main__":
    dic = {}
    for line in sys.stdin:
        json_dict = json.loads(line.strip())
        for key in json_dict:
            if not isinstance(json_dict[key], str):
                continue
            if key not in dic:
                dic[key] = len(json_dict[key])
            else:
                if len(json_dict[key]) > dic[key]:
                    dic[key] = len(json_dict[key])
    
    for key in dic:
        print (key, dic[key])
