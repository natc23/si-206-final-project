# si-206-final-project
W18 SI 206 final project - tumblr


This program uses two data sources:
- The Tumblr API (https://www.tumblr.com/docs/en/api/v2#blog_methods) which requires OAuth tokens, secrets, and an API key.
    -  To obtain these things, go to https://www.tumblr.com/oauth/apps and register an application to receive a consumer key    
       (API key), consumer secret, token, and token secret which are neccessary for running the program. Then make a    
       secrets.py file and enter these keys obtained into the variables oauth_consumer_key, oauth_consumer_secret, 
       oauth_token, oauth_secret (in the respective order that the keys were listed in the previous sentence).

- A singular web page that lists the best art and photo Tumblr accounts to follow according to Jeff Hamada  
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
To run the program, open your terminal and type "python3 final_project.py" then hit enter. A URL will be printed that you will need to copy and paste into a web browser and load. When this page loads, click allow and let the si.umich.edu page load. Then, copy this new URL and paste it into the terminal and hit enter. The program will then prompt you for input - type in your answer and, depending on your input, it will present you with more options that will allow you to choose how you'd like to see the data presented in various types of graphs. Choose whatever option you would like. Then, when you are done using the program, type "exit" to quit.
