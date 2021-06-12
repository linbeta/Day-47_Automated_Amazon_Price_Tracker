from bs4 import BeautifulSoup
import requests
import smtplib
import os

target_items = {
    "TC20": "https://www.amazon.com/gp/product/B089SJGQBH/ref=ox_sc_saved_title_2",
    "TC30": "https://www.amazon.com/gp/product/B08CVP2HXP/ref=ox_sc_saved_title_3",
    "USB C HUB": "https://www.amazon.com/gp/product/B09229V9YS/ref=ox_sc_act_title_2"
}

target_price = {
    "TC20": 60,
    "TC30": 29,
    "USB C HUB": 30
}

### Format for the targets ###
# target_items = {
#     "name1": "url_1",
#     "name2": "url_2",
#     "name3": "url_3"
# }

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77"
                  " Safari/537.36",
    "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6"
}

new_updates = []

for item in target_items:
    response = requests.get(target_items[item], headers=header)
    soup = BeautifulSoup(response.text, "html.parser")
    price = soup.select_one("#price_inside_buybox").getText()
    # print(price)
    usd_price = price.split("$")[1].split("\n")[0]
    ### Find if there's a coupon ###
    coupon = soup.find(name="i", class_="a-icon-addon")
    # print(coupon)
    coupon_info = "none"
    if coupon.getText() == "優惠券：":
        coupon_info = f"There's a coupon for this item: {target_items[item]}"

    detail = f"item: {item}, current price: US${usd_price}, coupon: {coupon_info}."
    #------ Email Content --------#
    if float(usd_price) < target_price[item]:
        new_updates.append(detail)

#----Test code: Checke the search results----#
# print(new_updates)
email_content = "\n".join(new_updates)


MY_EMAIL = os.environ['my_email']
PW = os.environ['email_password']
USER_EMAIL = os.environ['user_email']

with smtplib.SMTP("smtp.gmail.com") as server:
    server.starttls()
    server.login(user=MY_EMAIL, password=PW)
    server.sendmail(from_addr=MY_EMAIL, to_addrs=USER_EMAIL, msg=f"Subject:Amazon Price Tracker\n\n{email_content}")
