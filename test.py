from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from acc_pass import ACCOUNT, PASS, USER_DATA_DIR


tiki = 'https://www.facebook.com/?stype=lo&deoia=1&jlou=AfczHBzuFgKc5jde3dWHkPnlaB20s2OgvO2xVhdv5IidANHiSADnJtBKCyAvR6aWz5VMH83wtWkYKvxYe9USaIG-fC_7HhCmNfGXIp6jg_Ax3w&smuh=37746&lh=Ac-dfKrOH4QAtVz7HRw'

CHROMIUM_ARGS = [
    '--disable-blink-features=AutomationControlled',
]

link_post = 'https://www.facebook.com/KikyoPam/videos/313260974537348?idorvanity=552152208714234'
link_post_1 = 'https://www.facebook.com/photo/?fbid=1854707468301557&set=gm.1441962346399878&idorvanity=552152208714234'
link_post_2 = 'https://www.facebook.com/photo/?fbid=919353339782828&set=gm.1434174500511996&idorvanity=552152208714234'
link_post_3 = 'https://www.facebook.com/KikyoPam/videos/313260974537348?idorvanity=552152208714234'
link_post_4 = 'https://www.facebook.com/photo/?fbid=932491698279008&set=gm.1635233520550462&idorvanity=317569278983566'
link_post_5 = 'https://www.facebook.com/photo/?fbid=1157238392318141&set=gm.1636010307139450&idorvanity=317569278983566'

def sign_out(page):
    page.locator("//div[@class='x1rg5ohu x1n2onr6 x3ajldb x1ja2u2z']").first.click()
    page.wait_for_timeout(500)
    page.locator("//div[@role='listitem'][5]").click()
   
def load_more_comments(page):
    try:
        while True:
            page.get_by_role('button', name="Xem thêm bình luận").click()
            print("load")
            page.wait_for_timeout(1000)
        
    except:
        pass
    print("Full load")

def show_all_comments(page):
    page.get_by_label("Viết bình luận", exact=True).click()
    page.locator("//div[@class='x6s0dn4 x78zum5 xdj266r x11i5rnm xat24cr x1mh8g0r xe0p6wg']").click()
    page.wait_for_timeout(1000)
    page.get_by_role('menuitem').last.click()
    page.wait_for_timeout(3000)

def click_read_more(page):
    btn = page.get_by_role('button', name = 'Xem thêm').all()
    
    print('------------')
    try:
        for _ in range(len(btn)):
            page.get_by_role('button', name = 'Xem thêm').first.click()
            page.wait_for_timeout(500)
    except Exception as e:
        print("Error in click_read_more")
        print(e)

def extract_comment(soup):
    output = []
    text = ''
    comments = soup.find_all("div", class_ = 'x1y1aw1k xn6708d xwib8y2 x1ye3gou')
    for comment in comments:
        user = comment.find('span', class_ ='x3nfvp2').get_text()
        try:
            cmt = comment.find('div', {'dir':'auto'}).get_text()
        except:
            cmt = "#sticker"

        text = ' '.join([text, cmt])
        output.append([user, cmt])
        print(user, ' ', cmt)
    return output, text

def visualize_text(text):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
                                user_data_dir=USER_DATA_DIR,
                                channel='chrome',
                                headless=False,
                                slow_mo=20,
                                args=CHROMIUM_ARGS,
                                ignore_default_args=['--enable-automation'])
    page = browser.new_page()
    stealth_sync(page)
     
    page.goto(tiki, timeout=0)
    page.goto(link_post)
    page.wait_for_timeout(2000)

    page.get_by_label("Email hoặc số điện thoại").locator('nth=0').fill(ACCOUNT)
    page.wait_for_timeout(500)

    page.get_by_label("Mật khẩu").locator('nth=1').fill(PASS)
    page.wait_for_timeout(500)

    page.keyboard.press('Enter')
    page.wait_for_timeout(2000)
    try:
        
        show_all_comments(page)
        load_more_comments(page)
        click_read_more(page)
        
        log_out = False

    except:
        sign_out(page)
        log_out = True
    
    sleep(1)
    soup = BeautifulSoup(page.content(), 'lxml')
    
    if not log_out:
        sign_out(page)
    
    page.wait_for_timeout(1000)
    page.close()
    browser.close()

output, text = extract_comment(soup)

df = pd.DataFrame(output)
df.to_csv('output.csv', index=False)

# visualize
visualize_text(text)