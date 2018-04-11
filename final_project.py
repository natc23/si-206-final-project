from requests_oauthlib import OAuth1Session
import pytumblr
import secrets
from bs4 import BeautifulSoup
import requests
import json
import sqlite3

#TO DO: write unit tests, plotly, interactive

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
        resp = client.posts(blog_identifier, limit=25)
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
                blog_title = blog['title']
                description1 = blog['description']
                description2 = description1.replace('<p>','')
                description = description2.replace('</p>', '')
                posts_count = blog['posts']
                info = (user_name,blog_title,description,posts_count)
                account_data.append(info)
            except:
                info = ('NULL', 'NULL', 'NULL', 'NULL')
                account_data.append(info)

    else:
        data = get_tumblr_data_using_cache(account_identifier)
        blog = data['blog']
        user_name = blog['name']
        blog_title = blog['title']
        description1 = blog['description']
        description2 = description1.replace('<p>','')
        description = description2.replace('</p>', '')
        posts_count = blog['posts']
        info = (user_name,blog_title,description,posts_count)
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
            post_type = post['type']
            date = post['date']
            note_count = post['note_count']
            info = (post_id, blog_name, post_url, post_type, date, note_count)
            post_data.append(info)

    return post_data

################################################ How to get tumblrs for table
scraped_list = get_best_tumblrs()
search = input("What tumblr user would you like to receive information on? (enter user's url): ")


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
            'UserName' TEXT NOT NULL,
            'BlogTitle' TEXT NOT NULL,
            'Description' TEXT NOT NULL,
            'PostsCount' INTEGER
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



def insert_data(scraped_list, search):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()


    total_account_data = get_account_info(scraped_list)
    total_account_data += get_account_info(search)




    for row in total_account_data:
        insertion = (None, row[0], row[1], row[2], row[3])
        statement = 'INSERT INTO "Blogs" '
        statement += 'VALUES (?, ?, ?, ?, ?)'
        cur.execute(statement, insertion)


    conn.commit()

    total_post_data = get_post_data(scraped_list)
    total_post_data += get_post_data(search)
    #print(total_post_data)

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
    cur.execute('''SELECT Id, UserName
                   FROM Blogs
    ''')
    user_id = {}
    for row in cur:
        user_id[row[1]] = row[0]
    print(user_id)


    cur.execute('''SELECT BlogName
                   FROM Posts
    ''')
    execution_tuple = []
    for row in cur:
        try:
            username = row[0]
            print(username)
            username_id = user_id[username]
            print(username_id)
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





account_identifiers = get_best_tumblrs()
#get_account_info(account_identifiers)
#get_post_data(scraped_list)
init_db()
insert_data(scraped_list, search)
update_id_data()
