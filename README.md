# Playwright-Demo
Simple code to extract comments from facebook
### How to run

First, you need to install:

```
pip install playwright

playwright install

pip install playwright-stealth

pip install beautifulsoup4

pip install wordcloud

pip install underthesea
```

If you want to store data to postgresql:

```
pip install psycopg2
```

Then you need to config acc_pass.py. Fill in your account, password and user data path (Chrome user data path).

To store data to postgres, you need to install Postgres in local or use Docker.

Change your link post in link_post variable in test.py and run the code.


Some example link: 

https://www.facebook.com/photo/?fbid=1854707468301557&set=gm.1441962346399878&idorvanity=552152208714234
https://www.facebook.com/photo/?fbid=919353339782828&set=gm.1434174500511996&idorvanity=552152208714234
