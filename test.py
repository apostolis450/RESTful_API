import requests

BASE = "http://127.0.0.1:5000/"

"""
data = [ {"name": "frutotrela", "views": 10, "likes": 1000,},
		 {"name": "mpampinos", "views": 100, "likes": 1000,},
         {"name": "nikolakis", "views": 1000, "likes": 1000,} ]

for i in range(len(data)):
	response = requests.put(BASE + "video/" + str(i), data[i])
	print(response.json())	


input()
response = requests.get(BASE + "video/2")
print(response)
"""
response = requests.patch(BASE + "video/1", {"views":10})
print(response.json())