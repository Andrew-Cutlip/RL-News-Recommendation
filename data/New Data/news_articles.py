from newsapi import NewsApiClient
import json

# ddd3987e0e0944adbb0826bc363fb411
# a949d05d1df84a7ebb18a161bf31b376
output = {}
categories = ['business','entertainment','general','health','science','sports','technology']
countries = ['au','ca','gb','nz','us']
p = 1
for i in categories:
    articles = []
    for j in countries:
        newsapi = NewsApiClient(api_key='e5583bcca0024296a777dcc361ecefb2')
        news = newsapi.get_top_headlines(category=i,language='en',country=j,page_size=100,page=p)

        for k in news['articles']:
            if k not in articles:
                articles.append(k)
            
    news['articles'] = articles
    news['totalResults'] = len(articles)
    output[i] = news
    
    jsonString = json.dumps(output[i])
    jsonFile = open(i + ".json", "w")
    jsonFile.write(jsonString)
    jsonFile.close()