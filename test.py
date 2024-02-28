from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd
from acc_pass import ACCOUNT, PASS, USER_DATA_DIR


tiki = 'https://www.facebook.com/?stype=lo&deoia=1&jlou=AfczHBzuFgKc5jde3dWHkPnlaB20s2OgvO2xVhdv5IidANHiSADnJtBKCyAvR6aWz5VMH83wtWkYKvxYe9USaIG-fC_7HhCmNfGXIp6jg_Ax3w&smuh=37746&lh=Ac-dfKrOH4QAtVz7HRw'

CHROMIUM_ARGS = [
    '--disable-blink-features=AutomationControlled',
]

link_post = 'https://www.facebook.com/KikyoPam/videos/313260974537348?idorvanity=552152208714234'
link_post_1 = 'https://www.facebook.com/photo/?fbid=1854707468301557&set=gm.1441962346399878&idorvanity=552152208714234'
link_post_2 = 'https://www.facebook.com/photo/?fbid=919353339782828&set=gm.1434174500511996&idorvanity=552152208714234'
link_post_3 = 'https://www.facebook.com/KikyoPam/videos/313260974537348?idorvanity=552152208714234'
link_post_4 = 'https://www.facebook.com/photo/?fbid=387709377302443&set=a.145994268140623'

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
    sleep(2)

    page.get_by_label("Email hoặc số điện thoại").locator('nth=0').fill(ACCOUNT)
    sleep(0.5)

    page.get_by_label("Mật khẩu").locator('nth=1').fill(PASS)

    page.keyboard.press('Enter')
    sleep(2)
    try:
        page.get_by_label("Viết bình luận", exact=True).click()
        page.locator("//div[@class='x6s0dn4 x78zum5 xdj266r x11i5rnm xat24cr x1mh8g0r xe0p6wg']").click()
        # try:
        #     page.get_by_role('button', name="Gần đây nhất").click()
        # except:
        #     page.get_by_role('button', name="Phù hợp nhất").click()
        sleep(5)
        # page.get_by_role('menuitem', name="Tất cả bình luận").click()
        page.get_by_role('menuitem').last.click()
        sleep(5)
        try:
            while True:
                page.get_by_role('button', name="Xem thêm bình luận").click()
                print("load")
                sleep(3)
        except: 
            pass
        print("Full load")
        sleep(3)
        log_out = False
    except:
        page.locator("//div[@class='x1rg5ohu x1n2onr6 x3ajldb x1ja2u2z']").first.click()
        sleep(1)
        page.locator("//div[@role='listitem'][5]").click()
        log_out = True
    
    sleep(3)
    soup = BeautifulSoup(page.content(), 'lxml')
    
    
    if not log_out:
        page.locator("//div[@class='x1rg5ohu x1n2onr6 x3ajldb x1ja2u2z']").first.click()
        sleep(0.5)
        page.locator("//div[@role='listitem'][5]").click()

    
    #page.get_by_label("Đăng xuất").click()
    sleep(5)
    page.close()
    browser.close()

output = []
comments = soup.find_all("div", class_ = 'x1y1aw1k xn6708d xwib8y2 x1ye3gou')
for comment in comments:
    user = comment.find('span', class_ ='x3nfvp2').get_text()
    try:
        cmt = comment.find('div', {'dir':'auto'}).get_text()
    except:
        cmt = "#sticker"

    output.append([user, cmt])
    print(user, ' ', cmt)

df = pd.DataFrame(output[1:])
df.to_csv('output.csv', index=False)
