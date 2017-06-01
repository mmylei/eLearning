import requests
import json_wrapper

course_id = {
    'html': 'LgWwihnoEeWDtQoum3sFeQ',
    'front': 'ycQnChn3EeWDtQoum3sFeQ',
    'server': 'ngZrURn5EeWwrBKfKrqlSQ',
    'angularJS': '52blABnqEeW9dA4X94-nLQ',
    'mobile': '-gcU5xn4EeWwrBKfKrqlSQ',
    'web': 'DzdXURoCEeWg_RJGAuFGjw'
}

for course in course_id:
    id = course_id[course]
    url = 'https://www.coursera.org/api/feedback.v1/?q=course&courseId=' + id + '&feedbackSystem=STAR&ratingValues=1%2C2%2C3%2C4%2C5&categories=generic&start=0&limit=1000000'
    r = json_wrapper.dumps(requests.get(url).json())
    with open('./cousera_comment_info_' + course + '_all.json', 'w') as fo:
        fo.write(r)
    f_completed = json_wrapper.dumps(requests.get(url + '&courseCompleted=true').json())
    with open('./cousera_comment_info_' + course + '_completed.json', 'w') as fo:
        fo.write(f_completed)
#
# r = requests.get("https://www.coursera.org/api/feedback.v1/?q=course&courseId=LgWwihnoEeWDtQoum3sFeQ&feedbackSystem=STAR&ratingValues=1%2C2%2C3%2C4%2C5&categories=generic&start=0&limit=1000000&courseCompleted=true").json()
# fo = open("./coursera_comment_info_html_completed.json", "w")
# fo.write(str(r))
#
# r = requests.get("https://www.coursera.org/api/feedback.v1/?q=course&courseId=LgWwihnoEeWDtQoum3sFeQ&feedbackSystem=STAR&ratingValues=1%2C2%2C3%2C4%2C5&categories=generic&start=0&limit=1000000").json()
# fo = open("./coursera_comment_info_html_all.json", "w")
# fo.write(str(r))
#
# r = requests.get("https://www.coursera.org/api/feedback.v1/?q=course&courseId=ycQnChn3EeWDtQoum3sFeQ&feedbackSystem=STAR&ratingValues=1%2C2%2C3%2C4%2C5&categories=generic&start=0&limit=100000&courseCompleted=true").json()
# fo = open("./coursera_comment_info_front_completed.json", "w")
# fo.write(str(r))
#
# r = requests.get("https://www.coursera.org/api/feedback.v1/?q=course&courseId=ycQnChn3EeWDtQoum3sFeQ&feedbackSystem=STAR&ratingValues=1%2C2%2C3%2C4%2C5&categories=generic&start=0&limit=100000").json()
# fo = open("./coursera_comment_info_front_all.json", "w")
# fo.write(str(r))
#
# r = requests.get("https://www.coursera.org/api/feedback.v1/?q=course&courseId=ngZrURn5EeWwrBKfKrqlSQ&feedbackSystem=STAR&ratingValues=1%2C2%2C3%2C4%2C5&categories=generic&start=0&limit=100000&courseCompleted=true").json()
# fo = open("./coursera_comment_info_server_completed.json", "w")
# fo.write(str(r))
#
# r = requests.get("https://www.coursera.org/api/feedback.v1/?q=course&courseId=ngZrURn5EeWwrBKfKrqlSQ&feedbackSystem=STAR&ratingValues=1%2C2%2C3%2C4%2C5&categories=generic&start=0&limit=100000").json()
# fo = open("./coursera_comment_info_server_all.json", "w")
# fo.write(str(r))
#
# r = requests.get("https://www.coursera.org/api/feedback.v1/?q=course&courseId=52blABnqEeW9dA4X94-nLQ&feedbackSystem=STAR&ratingValues=1%2C2%2C3%2C4%2C5&categories=generic&start=0&limit=100000&courseCompleted=true").json()
# fo = open("./coursera_comment_info_angularJS_completed.json", "w")
# fo.write(str(r))
#
# r = requests.get("https://www.coursera.org/api/feedback.v1/?q=course&courseId=52blABnqEeW9dA4X94-nLQ&feedbackSystem=STAR&ratingValues=1%2C2%2C3%2C4%2C5&categories=generic&start=0&limit=100000").json()
# fo = open("./coursera_comment_info_angularJS_all.json", "w")
# fo.write(str(r))
#
# r = requests.get("https://www.coursera.org/api/feedback.v1/?q=course&courseId=-gcU5xn4EeWwrBKfKrqlSQ&feedbackSystem=STAR&ratingValues=1%2C2%2C3%2C4%2C5&categories=generic&start=0&limit=100000&courseCompleted=true").json()
# fo = open("./coursera_comment_info_mobile_completed.json", "w")
# fo.write(str(r))
#
# r = requests.get("https://www.coursera.org/api/feedback.v1/?q=course&courseId=-gcU5xn4EeWwrBKfKrqlSQ&feedbackSystem=STAR&ratingValues=1%2C2%2C3%2C4%2C5&categories=generic&start=0&limit=100000").json()
# fo = open("./coursera_comment_info_mobile_all.json", "w")
# fo.write(str(r))
#
# r = requests.get("https://www.coursera.org/api/feedback.v1/?q=course&courseId=DzdXURoCEeWg_RJGAuFGjw&feedbackSystem=STAR&ratingValues=1%2C2%2C3%2C4%2C5&categories=generic&start=0&limit=100000&courseCompleted=true").json()
# fo = open("./coursera_comment_info_web_completed.json", "w")
# fo.write(str(r))
#
# r = requests.get("https://www.coursera.org/api/feedback.v1/?q=course&courseId=DzdXURoCEeWg_RJGAuFGjw&feedbackSystem=STAR&ratingValues=1%2C2%2C3%2C4%2C5&categories=generic&start=0&limit=100000").json()
# fo = open("./coursera_comment_info_web_all.json", "w")
# fo.write(str(r))
