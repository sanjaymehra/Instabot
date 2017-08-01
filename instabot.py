import requests, urllib
from termcolor import colored
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import matplotlib.pyplot as plt

APP_ACCESS_TOKEN = '1564517276.c95a6d1.e551b2ee62a04323891285dd76ac4aa9'
#Token Owner : AVinstaBot.main
#Sandbox Users : AVinstaBot.test0, AVinstaBot.test1, AVinstaBot.test2...... AVinstaBot.test10

BASE_URL = 'https://api.instagram.com/v1/'

'''
Function declaration to get your own info
'''


def self_info():
    request_url = (BASE_URL + 'users/self/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'User does not exist!'
    else:
        print 'Status code other than 200 received!'


'''
Function declaration to get the ID of a user by username
'''


def get_user_id(insta_username):
    request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_username, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            return user_info['data'][0]['id']
        else:
            return None
    else:
        print 'Status code other than 200 received!'
        exit()


'''
Function declaration to get the info of a user by username
'''


def get_user_info(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'There is no data for this user!'
    else:
        print 'Status code other than 200 received!'


'''
Function declaration to get your recent post
'''


def get_own_post():
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    own_media = requests.get(request_url).json()

    if own_media['meta']['code'] == 200:
        if len(own_media['data']):
            image_name = own_media['data'][0]['id'] + '.jpeg'
            image_url = own_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'


'''
Function declaration to get the recent post of a user by username
'''


def get_user_post(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            image_name = user_media['data'][0]['id'] + '.jpeg'
            image_url = user_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'

'''
Function declaration to get the ID of the recent post of a user by username
'''

def get_post_id(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            return user_media['data'][0]['id']
        else:
            print 'There is no recent post of the user!'
            exit()
    else:
        print 'Status code other than 200 received!'
        exit()

'''
Function declaration to get a list of people who have liked the recent post of a user
'''


def get_like_list(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + "media/%s/likes?access_token=%s") % (media_id ,APP_ACCESS_TOKEN)
    print "Get request url : %s" % (request_url)
    likes_list = requests.get(request_url).json()
    print likes_list
    if len(likes_list['data']):
       for x in likes_list['data']:
           print x['username']
    else:
       print "Unsuccessful"



'''
Function declaration to like the recent post of a user
'''


def like_a_post(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/likes') % (media_id)
    payload = {"access_token": APP_ACCESS_TOKEN}
    print 'POST request url : %s' % (request_url)
    post_a_like = requests.post(request_url, payload).json()
    if post_a_like['meta']['code'] == 200:
        print 'Like was successful!'
    else:
        print 'Your like was unsuccessful. Try again!'


'''
Function declaration to make a comment on the recent post of the user
'''


def post_a_comment(insta_username):
    media_id = get_post_id(insta_username)
    comment_text = raw_input("Your comment: ")
    payload = {"access_token": APP_ACCESS_TOKEN, "text" : comment_text}
    request_url = (BASE_URL + 'media/%s/comments') % (media_id)
    print 'POST request url : %s' % (request_url)

    make_comment = requests.post(request_url, payload).json()

    if make_comment['meta']['code'] == 200:
        print "Successfully added a new comment!"
    else:
        print "Unable to add comment. Try again!"


'''
Function declaration to get a list of comments on the recent post of a user
'''


def get_comment_list(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    print "Get request url : %s" % (request_url)
    comment_list = requests.get(request_url).json()
    print comment_list
    if len(comment_list['data']):
        for x in comment_list['data']:
            print x['from']['username']
            print x['text']
    else:
        print "Unsuccessful"


'''
Function declaration to delete recent comments from the recent post
'''


def delete_comment(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    comment_info = requests.get(request_url).json()
    print comment_info
    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']):
            comment_id = comment_info['data'][0]['id']
            delete_url = (BASE_URL + 'media/%s/comments/%s/?access_token=%s') % (media_id, comment_id, APP_ACCESS_TOKEN)
            print 'DELETE request url : %s' % (delete_url)
            delete_info = requests.delete(delete_url).json()
            if delete_info['meta']['code'] == 200:
                print 'Comment successfully deleted!\n'
            else:
                print 'Unable to delete comment!'
        else:
            print 'There are no existing comments on the post!'
    else:
        print 'Status code other than 200 received!'


'''
Function declaration to delete negative comments from the recent post
'''

def delete_negative_comment(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    comment_info = requests.get(request_url).json()

    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']):
            #Here's a naive implementation of how to delete the negative comments :)
            for x in range(0, len(comment_info['data'])):
                comment_id = comment_info['data'][x]['id']
                comment_text = comment_info['data'][x]['text']
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                if (blob.sentiment.p_neg > blob.sentiment.p_pos):
                    print 'Negative comment : %s' % (comment_text)
                    delete_url = (BASE_URL + 'media/%s/comments/%s/?access_token=%s') % (media_id, comment_id, APP_ACCESS_TOKEN)
                    print 'DELETE request url : %s' % (delete_url)
                    delete_info = requests.delete(delete_url).json()

                    if delete_info['meta']['code'] == 200:
                        print 'Comment successfully deleted!\n'
                    else:
                        print 'Unable to delete comment!'
                else:
                    print 'Positive comment : %s\n' % (comment_text)
        else:
            print 'There are no existing comments on the post!'
    else:
        print 'Status code other than 200 received!'


'''
Sentimental analysis of online persona using pie chart
'''


def pie_chart_function(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    comment_info = requests.get(request_url).json()

    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']):

            for x in range(0, len(comment_info['data'])):
                comment_id = comment_info['data'][x]['id']
                comment_text = comment_info['data'][x]['text']
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                positive_comment = blob.sentiment.p_pos
                negative_comment = blob.sentiment.p_neg
                labels = 'Positive Comment', 'Negative Comment'
                sizes = [positive_comment,negative_comment]
                colors = [ 'yellowgreen', 'lightcoral',]
                explode = ( 0, 0)

                plt.pie(sizes, explode=explode, labels=labels, colors=colors,
                        autopct='%1.1f%%', shadow=True, startangle=140)

                plt.axis('equal')
                plt.show()

        else:
            print 'There are no existing comments on the post!'
    else:
        print 'Status code other than 200 received!'



def start_bot():
    while True:
        print '\n'
        print colored('Welcome to instaBot!',"blue")
        print colored('What do you wanna do???', 'cyan')
        print colored('Here are your menu options:\n',"blue")
        choices=[
        "Get your own details",
        "Get details of a user by username",
        "Get your own recent post",
        "Get the recent post of a user by username",
        "Get a list of people who have liked the recent post of a user",
        "Like the recent post of a user",
        "Get a list of comments on the recent post of a user",
        "Make a comment on the recent post of a user",
        "Delete recent comments from the recent post of a user",
        "Delete negative comments from the recent post of a user",
        "Sentimental analysis of online persona using pie chart",
        "Exit"
        ]
        for i in range(0,len(choices)):
            print colored((i + 1), 'red'), colored(choices[i], 'grey')

        choice = raw_input("\nEnter you choice: ")
        if choice == "1":
            self_info()
        elif choice == "2":
            insta_username = raw_input("\nEnter the username of the user: ")
            get_user_info(insta_username)
        elif choice == "3":
            get_own_post()
        elif choice == "4":
            insta_username = raw_input("\nEnter the username of the user: ")
            get_user_post(insta_username)
        elif choice=="5":
           insta_username = raw_input("\nEnter the username of the user: ")
           get_like_list(insta_username)
        elif choice=="6":
           insta_username = raw_input("\nEnter the username of the user: ")
           like_a_post(insta_username)
        elif choice=="7":
           insta_username = raw_input("\nEnter the username of the user: ")
           get_comment_list(insta_username)
        elif choice=="8":
           insta_username = raw_input("\nEnter the username of the user: ")
           post_a_comment(insta_username)
        elif choice=="9":
            insta_username = raw_input("Enter username of user:")
            print delete_comment(insta_username)
        elif choice=="10":
           insta_username = raw_input("\nEnter the username of the user: ")
           delete_negative_comment(insta_username)
        elif choice=="11":
            insta_username = raw_input("Enter the username")
            pie_chart_function(insta_username)
        elif choice == "12":
            exit()
        else:
            print "\nwrong choice"

start_bot()