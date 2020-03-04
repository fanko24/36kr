
from urllib.request import urlopen
from urllib.request import Request
 
url = "http://www.baidu.com"
ua_header = {"User-Agent":"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;"}
#url作为Request（）方法的参数
request = Request(url, headers = ua_header)
 
#向指定的url发送请求
response = urlopen(request)
 
#类文件对象的支持 文件对象的操作方法
html = response.read()
#打印字符串

print(html.decode("utf8"))

