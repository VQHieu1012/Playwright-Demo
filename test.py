from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
from bs4 import BeautifulSoup
from time import sleep
from acc_pass import ACCOUNT, PASS


tiki = 'https://www.facebook.com/?stype=lo&deoia=1&jlou=AfczHBzuFgKc5jde3dWHkPnlaB20s2OgvO2xVhdv5IidANHiSADnJtBKCyAvR6aWz5VMH83wtWkYKvxYe9USaIG-fC_7HhCmNfGXIp6jg_Ax3w&smuh=37746&lh=Ac-dfKrOH4QAtVz7HRw'

CHROMIUM_ARGS = [
    '--disable-blink-features=AutomationControlled',
]

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
                                user_data_dir='C:\\Users\\admin\\AppData\\Local\\Google\\Chrome\\User Data\\',
                                channel='chrome',
                                headless=False,
                                slow_mo=20,
                                args=CHROMIUM_ARGS,
                                ignore_default_args=['--enable-automation'])
    page = browser.new_page()
    stealth_sync(page)
     
    page.goto(tiki, timeout=0)
    page.locator("//input[@name='email']").fill(ACCOUNT)

    page.locator("//input[@name='pass']").fill(PASS)

    page.keyboard.press('Enter')

    page.get_by_text("Gordon Ramsaid").click()
    sleep(5)
    img = page.locator('//img[@class="x1ey2m1c xds687c x5yr21d x10l6tqk x17qophe x13vifvy xh8yej3 xl1xv1r"]').first.click()
    # img.click()
    sleep(5)
    soup = BeautifulSoup(page.content(), 'lxml')
    #print(soup)
    # comments = soup.find_all("div", class_='x78zum5 xdt5ytf')
    comments = soup.find_all("div", class_ = 'x1y1aw1k xn6708d xwib8y2 x1ye3gou')
    for comment in comments:
        comment = comment.get_text()
        print(comment)

    sleep(10)
    page.close()
    browser.close()