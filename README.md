# si-206-final-project
W18 SI 206 final project - tumblr

XXX(Data sources used, including instructions for a user to access the data sources (e.g., API keys or client secrets needed, along with a pointer to instructions on how to obtain these and instructions for how to incorporate them into your program (e.g., secrets.py file format))

XXXAny other information needed to run the program (e.g., pointer to getting started info for plotly)

XXXBrief description of how your code is structured, including the names of significant data processing functions (just the 2-3 most important functions--not a complete list) and class definitions. If there are large data structures (e.g., lists, dictionaries) that you create to organize your data for presentation, briefly describe them.

Brief user guide, including how to run the program and how to choose presentation options.)


This program uses two data sources:
1.)	The Tumblr API (https://www.tumblr.com/docs/en/api/v2#blog_methods) which requires OAuth tokens, secrets, and an API key. 
    To obtain these things, go to https://www.tumblr.com/oauth/apps and register an application to receive a consumer key (API   
    key), consumer secret, token, and token secret which are neccessary for running the program. Then make a secrets.py file    
    and enter these keys obtained into the variables oauth_consumer_key, oauth_consumer_secret, oauth_token, oauth_secret (in  
    the respective order that the keys were listed in the previous sentence).

2.)	A singular web page that lists the best art and photo Tumblr accounts to follow according to Jeff Hamada 
    (https://www.booooooom.com/2017/02/21/ultimate-list-of-all-the-best-art-photo-tumblrs-to-follow/)

Additionally, this program utilizes plotly. To set up plotly go to https://plot.ly and create an account or login. Then, in secrets.py define two variables, plotly_api and username with the api key you obtain from plotly (found by going to settings then API keys on the plotly website) and your plotly username.

Program structure: 
- caching and oAuth 
- data collection by scraping the web page and using the Tumblr API
    - major functions in this part include get_best_tumblrs, get_account_info, and get_post_data
- storing the data into a database that has two tables, Blogs and Posts, and one primary key-foregin key relation
- accessing the data from these tables using SQL statements through a class called GraphData
- using plotly to create four different graphs by obtaining data through the methods within GraphData
- a function called interaction that takes in user input and calls the functions to display graphs accordingly

User guide:
To run the program, 
