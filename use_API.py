#自动下载github上星最多的python项目
import requests
#执行API调用并存储响应
url = 'https://api.github.com/search/repositories?q=language:python&sort=starts'#q表查询,language表语言sort对starts进行排序
r = requests.get(url)
print("Status code:",r.status_code)#状态码200表示请求成功
#将API响应存储在一个变量中
respone_dict = r.json()
#处理结果
print(response_dict.keys())

#输出如下：
Status code:200
dict_ksys(['items','total_count','incomplete_results'])

#处理响应字典
print("Total repositories:",response_dict['total_count']) #打印与'total_count'相关的值
#探索有关仓库的信息
repo_dicts = response_dict['item']
print("Repositories returned:",len(repo_dicts))
#研究第一个仓库
repo_dict = repo_dicts[0]
print("\nKeys:",len(repo_dict))
for key in sorted(repo_dict.keys()):
  print(key)

#输出如下：
Status code:200
Toatal repositories:713062
Repositories returned:30

Keys:68
archive_url
assignees_url
blobs_url
--snip--
url
watchers
watchers_count
