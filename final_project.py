from requests_oauthlib import OAuth1Session
import pytumblr
import secrets
from bs4 import BeautifulSoup
import requests
import json
import sqlite3
import plotly.plotly as py
import plotly.graph_objs as go

import plotly

plotly_api_key = secrets.plotly_api

plotly.tools.set_credentials_file(username='natc23', api_key= plotly_api_key)

#TO DO: write unit tests
#FIX: connect blog_identifier (url) to username and get rid of blogname in posts
# Close sqlite connections !!! esp in graphs!!! and interactive !!!
# account for www. https:// and http:// in user input

consumer_key = secrets.oauth_consumer_key
consumer_secret = secrets.oauth_consumer_secret
oauth_token = secrets.oauth_token
oauth_secret = secrets.oauth_secret


#CACHING
baseurl = 'https://www.booooooom.com/2017/02/21/ultimate-list-of-all-the-best-art-photo-tumblrs-to-follow/'
try:
    fref = open('website_data.json', 'r')
    data = fref.read()
    CACHE_DICT = json.loads(data)
    fref.close()
except:
    CACHE_DICT = {}


def get_data_using_cache(baseurl):
    unique_ident = baseurl
    if baseurl in CACHE_DICT:
        return CACHE_DICT[unique_ident]

    else:
        resp = requests.get(baseurl)
        CACHE_DICT[unique_ident] = resp.text
        fref = open('website_data.json', 'w')
        dumped_data = json.dumps(CACHE_DICT)
        fref.write(dumped_data)
        fref.close()
        return CACHE_DICT[unique_ident]

try:
    fref = open('tumblr_data.json', 'r')
    data = fref.read()
    TUMBLR_CACHE_DICT = json.loads(data)
    fref.close()
except:
    TUMBLR_CACHE_DICT = {}

def get_tumblr_data_using_cache(blog_identifier):
    unique_ident = blog_identifier
    if blog_identifier in TUMBLR_CACHE_DICT:
        return TUMBLR_CACHE_DICT[unique_ident]

    else:
        resp = client.blog_info(blog_identifier)
        TUMBLR_CACHE_DICT[unique_ident] = resp
        fref = open('tumblr_data.json', 'w')
        dumped_data = json.dumps(TUMBLR_CACHE_DICT)
        fref.write(dumped_data)
        fref.close()
        return TUMBLR_CACHE_DICT[unique_ident]

try:
    fref = open('tumblr_post_data.json', 'r')
    data = fref.read()
    TUMBLR_POST_CACHE_DICT = json.loads(data)
    fref.close()
except:
    TUMBLR_POST_CACHE_DICT = {}

def get_tumblr_post_data_using_cache(blog_identifier):
    unique_ident = blog_identifier
    if blog_identifier in TUMBLR_POST_CACHE_DICT:
        return TUMBLR_POST_CACHE_DICT[unique_ident]

    else:
        resp = client.posts(blog_identifier, limit=75)
        TUMBLR_POST_CACHE_DICT[unique_ident] = resp
        fref = open('tumblr_post_data.json', 'w')
        dumped_data = json.dumps(TUMBLR_POST_CACHE_DICT)
        fref.write(dumped_data)
        fref.close()
        return TUMBLR_POST_CACHE_DICT[unique_ident]


#AUTHORIZATION


request_token_url = 'http://www.tumblr.com/oauth/request_token'
authorize_url = 'http://www.tumblr.com/oauth/authorize'
access_token_url = 'http://www.tumblr.com/oauth/access_token'

# STEP 1: Obtain request token
oauth_session = OAuth1Session(consumer_key, client_secret=consumer_secret)
fetch_response = oauth_session.fetch_request_token(request_token_url)
resource_owner_key = fetch_response.get('oauth_token')
resource_owner_secret = fetch_response.get('oauth_token_secret')

# STEP 2: Authorize URL + Rresponse
full_authorize_url = oauth_session.authorization_url(authorize_url)

# Redirect to authentication page
print('\nPlease go here and authorize:\n{}'.format(full_authorize_url))
redirect_response = input('Allow then paste the full redirect URL here:\n')

# Retrieve oauth verifier
oauth_response = oauth_session.parse_authorization_response(redirect_response)

verifier = oauth_response.get('oauth_verifier')

# STEP 3: Request final access token
oauth_session = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=resource_owner_key,
    resource_owner_secret=resource_owner_secret,
    verifier=verifier
)
oauth_tokens = oauth_session.fetch_access_token(access_token_url)

tokens = {
    'consumer_key': consumer_key,
    'consumer_secret': consumer_secret,
    'oauth_token': oauth_tokens.get('oauth_token'),
    'oauth_token_secret': oauth_tokens.get('oauth_token_secret')
}

client = pytumblr.TumblrRestClient(
        tokens['consumer_key'],
        tokens['consumer_secret'],
        tokens['oauth_token'],
        tokens['oauth_token_secret']
    )


#SCRAPE DATA FROM WEBSITE
def get_best_tumblrs():
    best_tumblrs = []
    html = get_data_using_cache('https://www.booooooom.com/2017/02/21/ultimate-list-of-all-the-best-art-photo-tumblrs-to-follow/')
    soup = BeautifulSoup(html, 'html.parser')
    main = soup.find(class_ = 'post-content')
    blogs = main.find_all('a')
    for blog in blogs[:-1]:
        #print(blog.text)
        #print(get_account_info(blog.text))
        best_tumblrs.append(blog.text)
    return best_tumblrs

#get_best_tumblrs()

#GET THE DATA FROM TUMBLR
def get_account_info(account_identifier):
    # Authenticate via API Key
    client = pytumblr.TumblrRestClient(consumer_key)
    account_data = []
    if type(account_identifier) == list:
        for account in account_identifier:
            data = get_tumblr_data_using_cache(account)
            #print(data)
            #account_data += account[data]
            try:
                blog = data['blog']
                user_name = blog['name']
                url = blog['url']
                blog_title = blog['title']
                description1 = blog['description']
                description2 = description1.replace('<p>','')
                description = description2.replace('</p>', '')
                posts_count = blog['posts']
                can_ask = blog['ask']
                if can_ask == True:
                    can_ask = 'yes'
                if can_ask == False:
                    can_ask = 'no'
                info = (user_name, url, blog_title,description,posts_count, can_ask)
                account_data.append(info)
            except:
                info = ('NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL')
                account_data.append(info)

    else:
        data = get_tumblr_data_using_cache(account_identifier)
        blog = data['blog']
        user_name = blog['name']
        url = blog['url']
        blog_title = blog['title']
        description1 = blog['description']
        description2 = description1.replace('<p>','')
        description = description2.replace('</p>', '')
        posts_count = blog['posts']
        can_ask = blog['ask']
        if can_ask == True:
            can_ask = 'yes'
        if can_ask == False:
            can_ask = 'no'
        info = (user_name, url, blog_title,description,posts_count, can_ask)
        account_data.append(info)
    return account_data

    #Make classes?? Account and Post then put into table?



def get_post_data(account_identifier):
    client = pytumblr.TumblrRestClient(consumer_key)
    post_data = []
    if type(account_identifier) == list:
        for account in account_identifier:
            data = get_tumblr_post_data_using_cache(account)
            #print(data)
            for post in data:
                #print(post)
                try:
                    posts = data['posts']
                    for post in posts:
                        #print(post)
                        #print("----------------------------------")
                        post_id = post['id']
                        blog_name = post['blog_name']
                        post_url = post['post_url']
                        if 'http://' in post_url:
                            post_url = post_url.replace('http://', '')
                        if 'https://' in post_url:
                            post_url = post_url.replace('https://', '')
                        post_type = post['type']
                        date = post['date']
                        note_count = post['note_count']
                        info = (post_id, blog_name, post_url, post_type, date, note_count)
                        post_data.append(info)
                except:
                    info = ('NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL')
                    post_data.append(info)
    else:
        data = get_tumblr_post_data_using_cache(account_identifier)
        for post in data['posts']:
            post_id = post['id']
            blog_name = post['blog_name']
            post_url = post['post_url']
            if 'http://' in post_url:
                post_url = post_url.replace('http://', '')
            if 'https://' in post_url:
                post_url = post_url.replace('https://', '')
            post_type = post['type']
            date = post['date']
            note_count = post['note_count']
            info = (post_id, blog_name, post_url, post_type, date, note_count)
            post_data.append(info)

    return post_data


#MAKE DATA BASE
DBNAME = 'tumblr.db'
def init_db():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    # Drop tables
    statement = '''
        DROP TABLE IF EXISTS 'Blogs';
    '''
    cur.execute(statement)
    statement = '''
        DROP TABLE IF EXISTS 'Posts';
    '''
    cur.execute(statement)

    conn.commit()

    statement = '''
        CREATE TABLE 'Blogs' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'Username' TEXT NOT NULL,
            'URL' TEXT NOT NULL,
            'BlogTitle' TEXT NOT NULL,
            'Description' TEXT NOT NULL,
            'PostsCount' INTEGER,
            'CanAsk' TEXT NOT NULL
        );
    '''

    cur.execute(statement)
    conn.commit()

    statement = '''
        CREATE TABLE 'Posts' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'UserId' INTEGER,
            'PostId' INTEGER,
            'BlogName' TEXT NOT NULL,
            'PostUrl' TEXT NOT NULL,
            'PostType' TEXT NOT NULL,
            'Date' TEXT NOT NULL,
            'NoteCount' INTEGER
        );
    '''

    cur.execute(statement)
    conn.commit()
    conn.close()



def insert_data(account):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    total_account_data = get_account_info(account)





    for row in total_account_data:
        insertion = (None, row[0], row[1], row[2], row[3], row[4], row[5])
        statement = 'INSERT INTO "Blogs" '
        statement += 'VALUES (?, ?, ?, ?, ?, ?,?)'
        cur.execute(statement, insertion)


    conn.commit()

    total_post_data = get_post_data(account)

    for row in total_post_data:
        insertion = (None, 0, row[0], row[1], row[2], row[3], row[4], row[5])
        statement = 'INSERT INTO "Posts" '
        statement += 'VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
        cur.execute(statement, insertion)

    conn.commit()
    conn.close()

def update_id_data():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    cur.execute('''SELECT Id, Username
                   FROM Blogs
    ''')
    user_id = {}
    for row in cur:
        user_id[row[1]] = row[0]
    #print(user_id)


    cur.execute('''SELECT BlogName
                   FROM Posts
    ''')
    execution_tuple = []
    for row in cur:
        try:
            username = row[0]
            username_id = user_id[username]
            t = (username_id, str(username))
            statement = 'UPDATE Posts '
            statement += 'SET UserId=? '
            statement += 'WHERE BlogName=? '
            execution_tuple.append((statement,t))
        except:
            pass


    try:
        for ex_tup in execution_tuple:
            cur.execute(ex_tup[0], ex_tup[1])
    except:
        pass

    conn.commit()
    conn.close()



# MAKE GRAPHS!

def notes_line_graph(username):

    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    statement = '''SELECT NoteCount, [Date]
                   FROM Posts
                   JOIN Blogs
                   ON Posts.UserId = Blogs.Id'''
    statement += " WHERE Blogs.Username = '{}'".format(username)
    statement += ' ORDER BY [Date]'

    cur.execute(statement)

    dates = []
    notes = []

    for row in cur:
        notes.append(row[0])
        dates.append(row[1][:19])

    trace0 = go.Scatter(
    x = dates,
    y = notes,
    mode = 'lines+markers',
    name = 'Notes Count',
    line = dict(
        color = ('#2ED8C1'),
        width = 2.5
        )
    )

    layout = go.Layout(title='Amount of Notes On Each Post',
                xaxis=dict(title='Date of Post'),
                yaxis=dict(title='Amount of Notes'))

    data = [trace0]
    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename = 'tumblr-notes-graph')







def post_type_pie(username):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    statement = '''SELECT PostType
                   FROM Posts
                   JOIN Blogs
                   ON Posts.UserId = Blogs.Id'''
    statement += " WHERE Blogs.Username = '{}'".format(username)

    cur.execute(statement)

    post_types = {}
    for row in cur:
        type = row[0]
        if type not in post_types:
            post_types[type] = 0
        post_types[type] += 1
    try:
        del post_types['NULL']
    except:
        pass

    types = [key for key in post_types.keys()]
    number = [value for value in post_types.values()]

    colors = ['#96D38C', '#EE76FC', '#4601B0', '#C4A7F0', '#0658F0', '#06E9F0']

    trace0 = go.Pie(labels=types, values=number,
               hoverinfo='label+percent', textinfo='value',
               textfont=dict(size=20),
               marker=dict(colors=colors,
                           line=dict(color='#000000', width=2)))

    layout = go.Layout(title='Type of Tumblr Posts')


    data = [trace0]
    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename = 'post-type-pie')



def ask_question_pie():

    yes = 0
    no = 0
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    cur.execute('''SELECT CanAsk
                   FROM Blogs''')

    for row in cur:
        try:
            if row[0] == 'no':
                no += 1
            elif row[0] == 'yes':
                yes += 1
        except:
            pass


    labels = ['Yes', 'No']
    values = [yes,no]


    colors = ['#FEBFB3', '#E1396C']

    trace0 = go.Pie(labels=labels, values=values,
               hoverinfo='label+percent', textinfo='value',
               textfont=dict(size=20),
               marker=dict(colors=colors,
                           line=dict(color='#000000', width=2)))

    layout = go.Layout(title='The Amount of Blogs that Allow Tumblr Users to Ask Them Questions')


    data = [trace0]
    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename = 'can-ask-questions-pie')




def number_posts_bar():

    data = []
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    cur.execute('''SELECT Username, PostsCount
                   FROM Blogs''')

    accounts = []
    posts_number = []
    for row in cur:
        if row[0] != 'NULL':
            accounts.append(row[0])
            posts_number.append(row[1])
            #print(row)

    trace0 = go.Bar(x=accounts,y=posts_number,
                    text = accounts,
                    marker=dict(color='rgb(171,217,233)',
                    line=dict(
                        color='rgb(8,48,107)',
                        width=1.5,
                            )
                        )
                    )

    data = [trace0]
    layout = go.Layout(
    title='Amount of Posts for Each Tumblr Account',
    xaxis=dict(title='Tumblr Username'),
    yaxis=dict(title='Number of Posts')
    )

    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename = 'amount-of-posts-bar')





scraped_list = get_best_tumblrs()
#search = input("What tumblr user would you like to receive information on? (enter user's url): ")
#blog_username = input("What tumblr user would you like to receive information on? (enter user's username): ")



def interaction():

    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    response = ''

    while response != 'exit':

        response = input('''\nWould you like to: look up a Tumblr user, see a list of Tumblr accounts to follow, or exit?\n
        Enter "look up a user" for information on that Tumblr blog.\n
        Enter "who to follow" to get a list of the best art and photo Tumblr accounts determined by Jeff Hamada.\n
        Enter "exit" to exit the program.
            ''')

        if response == 'look up a user':
            search = input("\nWhat Tumblr user would you like to receive information on? (enter username of that tumblr): \n")
            init_db()
            try:
                insert_data(search)
            except:
                print('\nThat Tumblr username is invalid.')
                continue
            update_id_data()

            username = search.split('.')[0]
            statement = '''SELECT *
                           FROM Blogs'''
            statement += ' WHERE Username = "{}"'.format(username)
            cur.execute(statement)
            for row in cur:
                print('username: ' + str(row[1]) + ', url: ' + str(row[2]) + ', blog title: ' + str(row[3]) + ', description: ' + str(row[4]) + ', amount of posts: ' + str(row[5]))
            graph_input = input('''\nWould you like to: view a line graph of the number of notes on posts by this user over time or view a pie chart of the types of Tumblr posts by this user?\n
            Enter a choice of "notes line graph" or "types pie chart" or "neither" to view neither: \n''')
            if graph_input == "notes line graph":
                notes_line_graph(username)
                continue
            elif graph_input =="types pie chart":
                post_type_pie(username)
                continue
            elif graph_input == 'neither':
                continue
            else:
                print('\nThat input is invalid.\n')
                continue


        elif response == 'who to follow':
            scraped_list = get_best_tumblrs()
            init_db()
            insert_data(scraped_list)
            update_id_data()

            cur.execute('''SELECT URL
                           FROM Blogs
            ''')

            print('\nThese are the best art and photo Tumblr accounts determined by Jeff Hamada: \n')
            for row in cur:
                if row[0] == 'NULL':
                    pass
                else:
                    print(row[0])
            graph_input = input('''\nWould you like to: view a pie chart that displays how many of these accounts allow users to ask them questions or view a bar graph that compares the number of posts these Tumblr users have made.\n
            Enter a choice of "ask pie chart" or "posts bar graph" or "neither" to view neither: \n''')
            if graph_input == 'ask pie chart':
                ask_question_pie()
                continue
            elif graph_input == 'posts bar graph':
                number_posts_bar()
            elif graph_input == 'neither':
                continue
            else:
                print('\nThat input is invalid.\n')
                continue




        elif response == 'exit':
            break

        else:
            print('\nSorry that input is invalid.\n')


#account_identifiers = get_best_tumblrs()
#get_account_info(account_identifiers)
#get_post_data(scraped_list)
# init_db()
# insert_data(scraped_list, search)
# update_id_data()
# number_posts_bar()
#ask_question_pie()
#post_type_pie(blog_username)
#notes_line_graph(blog_username)
interaction()
