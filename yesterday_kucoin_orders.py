import requests
import json
import datetime
import pytz

url = "https://www.kucoin.com/_api/otc/order/history?page=1&pageSize=12&status=DONE&c=0ac18a0e9259443c9f3e2ad85851ace5&lang=en_US"

headers = {
    "Cookie":
    "__cfruid=aededd63cef31d9550afa26d1479a1ad01b6b4cb-1688289388; sajssdk_2015_cross_new_user=1; SESSION=NjBkYTA1M2YtYWYwNS00NmE1LTgyZjQtYzNmMjgzOGJhMzlm; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22168815944%22%2C%22first_id%22%3A%2218915e3aea8294-0d02cf301c17e1-13462c6c-1897064-18915e3aea92b8%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfbG9naW5faWQiOiIxNjg4MTU5NDQiLCIkaWRlbnRpdHlfY29va2llX2lkIjoiMTg5MTVlM2FlYTgyOTQtMGQwMmNmMzAxYzE3ZTEtMTM0NjJjNmMtMTg5NzA2NC0xODkxNWUzYWVhOTJiOCJ9%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%22168815944%22%7D%2C%22%24device_id%22%3A%2218915e3aea8294-0d02cf301c17e1-13462c6c-1897064-18915e3aea92b8%22%7D; __cf_bm=iM8PwiHfshpR3RE7onz1rJJrVX7H9x_g_u2bbcJF2zA-1688289450-0-ARhSw/C+/aSXNhqhOvLt8JA1IczmJy01FtYb6T6KKrgt3Fce7w/a7X7Ex3v4Kq2sAfznZWDmkDeAy6KaTWo6RR4vTlBzQ97Ccu2R5nWDjevU; X_GRAY_TEMP_UUID=878bf556-72c0-4025-b451-5438dec32a9c; X_GRAY_TMP=1686916541078; X-TRACE=b9UUWFhkk1Y4bX6IH0WlDINpiz+75U0itP40DAUMqGQ=; x-bullet-token=2neAiuYvAU5cbMXpmsXD5OJlewXCKryg8dSpDCgag8ZwbZpn3uIHi6siD_s132wYwoXOiOG0Q0HJAATz5DNEx6BQB2ytbg7w_YzjbJ0TFV47z9ceQ1ytEaqRyqznCVt1whuoNZhpWWE0LOX--r5WC3yT4Aypf7il.oKe7Bt_Kw_RvHiv7IKobyQ==; AWSALB=RVx5H1ZMWLXhdGdFN+04E7Mg81dPfquPs4jLWf3pZ9WI6MbC3ng3Hra4JY8JtmpBxv4hITmaPWyTJtGXQC/z4KseZ36vao2NS7SbD54WFsnl3rG8nUpu3LF9qHZk; AWSALBCORS=RVx5H1ZMWLXhdGdFN+04E7Mg81dPfquPs4jLWf3pZ9WI6MbC3ng3Hra4JY8JtmpBxv4hITmaPWyTJtGXQC/z4KseZ36vao2NS7SbD54WFsnl3rG8nUpu3LF9qHZk"
}

usdt_buy = 0
inr_buy = 0
usdt_sell = 0
inr_sell = 0
usdt_buy_str = ""
inr_buy_str = ""
usdt_sell_str = ""
inr_sell_str = ""

current_date_ist = datetime.datetime.now(pytz.timezone("Asia/Kolkata")).date()
yesterday_date_ist = current_date_ist - datetime.timedelta(days=1)

print("Data for ", yesterday_date_ist)
for page in range(1, 11):
    page_url = url.replace("page=1", f"page={page}")
    response = requests.get(page_url, headers=headers)

    if response.ok:
        json_response = response.json()
        items = json_response.get("items", [])
        for item in items:
            buyer_role = item["buyerRole"]
            currency_amount = float(item["currencyAmount"])
            legal_currency_amount = float(item["legalCurrencyAmount"])
            created_at = item["createdAt"] // 1000
            created_at_date = datetime.datetime.fromtimestamp(created_at).date()

            if created_at_date == yesterday_date_ist:
                if buyer_role:
                    usdt_buy += currency_amount
                    inr_buy += legal_currency_amount
                    usdt_buy_str += str(currency_amount) + ","
                    inr_buy_str += str(legal_currency_amount) + ","
                else:
                    usdt_sell += currency_amount
                    inr_sell += legal_currency_amount
                    usdt_sell_str += str(currency_amount) + ","
                    inr_sell_str += str(legal_currency_amount) + ","

    else:
        print("An error occurred while fetching data from page", page, ":", json_response)

print("USDT Buy:", "SUM(" + usdt_buy_str)
print("INR Buy:", "SUM(" +  inr_buy_str)
print("USDT Sell:", "SUM(" +  usdt_sell_str)
print("INR Sell:", "SUM(" +  inr_sell_str)

print("Total USDT Buy: ", usdt_buy)
print("Total INR Buy: ", inr_buy)
print("Total USDT SELL: ", usdt_sell)
print("Total INR SELL: ", inr_sell)
