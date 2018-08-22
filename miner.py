import requests
from bs4 import BeautifulSoup
import json
import time
# url="https://www.udemy.com/api-2.0/courses/628796/reviews/?courseId=628796&page=1&page_size=827&is_text_review=1&ordering=course_review_score__rank,-created&fields[course_review]=@default,response,content_html&fields[user]=@min,image_50x50,initials&fields[course_review_response]=@min,user,content_html"
# r = requests.get(url)
# with open('output.json', 'w') as w:
#     w.write(r.text)
#     w.flush()
j = dict()
headers = {
        'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'accept': 'application/json, text/plain, */*',
        'referer': 'https://www.udemy.com/courses/search/?q=ansible&src=ukw',
        'authority': 'www.udemy.com',
        # 'x-requested-with':'XMLHttpRequest'
}
user_urls = list()
def format_name(user):
    return user.replace(" ","-").lower()

with open('output.json', 'r') as r:
    j = json.loads(r.read())

# Display all the users

def generate_urls():
    user_url = "https://www.udemy.com/user/"
    for u in j['results']:
        # print(user_url + format_name(u['user']['title']))
        user_urls.append(user_url + format_name(u['user']['title']))

def get_user_id(url):
    r = requests.get(url,headers=headers)
    soup = BeautifulSoup(r.text,features="html5lib")
    try:
        user_data = json.loads(soup.find("div",{"class":"ud-app-loader ud-component--user-profile--app"})['data-module-args'])
        return user_data['user']['id']
    except TypeError:
        print("The user does not have any courses")
        return None
    

def get_user_courses():
    for url in user_urls:
        user_id = str(get_user_id(url))
        if user_id:
            url="https://www.udemy.com/api-2.0/users/" + user_id + "/subscribed-profile-courses/?fields[course]=@default,avg_rating_recent,rating,bestseller_badge_content,badges,content_info,discount,is_recently_published,is_wishlisted,num_published_lectures,num_reviews,num_subscribers,buyable_object_type,headline,instructional_level,objectives_summary,content_length_practice_test_questions,num_published_practice_tests,published_time,is_user_subscribed,has_closed_caption,preview_url,context_info&page=1&page_size=1000"
            r = requests.get(url,headers=headers)
            with open(user_id + ".json",'w') as w:
                print("Saving",user_id)
                w.write(r.text)
                time.sleep(5)
def get_sample_page():
    user_url = "https://www.udemy.com/user/"
    for u in j['results']:
        # print(user_url + format_name(u['user']['title']))
        sample_url = user_url + format_name(u['user']['title'])
        r = requests.get(sample_url,headers=headers)
        with open(format_name(u['user']['title']) + ".html","w") as w:
            w.write(r.text)

# generate_urls()
# get_user_courses()
get_sample_page()