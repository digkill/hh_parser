import requests
import time
import csv



def takePosts():
    token = 'TOKEN'
    version = 5.103
    domain = 'papclub1'
    offset = 0
    count = 100
    allPost = []


    while offset < 1000:
        response = requests.get('https://api.vk.com/method/wall.get',
                            params={
                                'access_token': token,
                                'v': version,
                                'domain': domain,
                                'count': count,
                                'offset': offset
                            })

        data = response.json()['response']['items']
        offset +=100
        allPost.extend(data)
        time.sleep(0.5)
    return allPost

def fileWriter(allPosts):
    with open('posts.csv', 'w', encoding='utf-8') as file:
        line = csv.writer(file)
        line.writerow(('likes', 'body', 'url'))
        for post in allPosts:
            try:
                if post['attachments'][0]['type']:
                    imgUrl = post['attachments'][0]['photo']['sizes'][-1]['url']
                else:
                    imgUrl = 'pass'
            except:
                pass
            line.writerow((post['likes']['count'], post['text'], imgUrl))


allPosts = takePosts()
fileWriter(allPosts)
