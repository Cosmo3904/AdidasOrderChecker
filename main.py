import requests, json
from bs4 import BeautifulSoup as bs


def orderchecker(ordernum, email):
    s = requests.Session()
    s.headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
    res = s.get('https://www.adidas.com/us/order-tracker')
    soup = bs(res.text, 'lxml')
    posturl = soup.find('form', {'id':'dwfrm_ordersignup'})['action']
    payload = {
        'dwfrm_ordersignup_orderNo' : ordernum.upper(),
        'dwfrm_ordersignup_email' : email,
        'dwfrm_ordersignup_signup' : 'Track order'
    }
    res = s.post(posturl, data = payload)
    soup = bs(res.text, 'lxml')
    temp = soup.find('div', {'class':'order-step selected'}).find('div', {'class':'order-step-indicator'}).text
    if '2' in temp:
        orderstatus = 'Order Confirmed'
        trackingnum = 'N/A'
    elif '3' in temp:
        orderstatus = 'Shipped'
        for item in soup.find_all('span', {'class':'order-deliveries-date'}):
            if 'Tracking number' in item.text:
                trackingnum = item.text.replace('Tracking number: ', '')
    product = soup.find('div', {'class':'product'})['data-id']
    return({'Status' : orderstatus, 'Tracking' : trackingnum, 'Product': product})

def jsonripper():
    try:
        with open('orders.json', 'r') as f:
            data = json.loads(f.read())
        s = input('Add More Orders? (Y/N) : ').lower()
        if s == 'y':
            while True:
                ordernum = input('Enter Order Number (Enter "Done" when done adding orders) : ')
                if ordernum.lower() == 'done':
                    break
                email = input('Enter Email for Above Order : ')
                data['Orders'].append({"Order Number" : ordernum, "Email" : email})
            with open('orders.json', 'w') as f:
                json.dump(data, f)
            print('Orders Saved for Next Check!')
        else:
            pass
    except:
        data = {}
        data["Orders"] = []
        while True:
            ordernum = input('Enter Order Number (Enter "Done" when done adding orders) : ')
            if ordernum.lower() == 'done':
                break
            email = input('Enter Email for Above Order : ')
            data['Orders'].append({"Order Number" : ordernum, "Email" : email})
        with open('orders.json', 'w') as f:
            json.dump(data, f)
        print('Orders Saved for Next Check!')
    for item in data['Orders']:
        try:
            status = orderchecker(item['Order Number'], item['Email'])
            print('[{}] [{}] [Tracking : {}]'.format(status['Status'], status['Product'], status['Tracking']))
        except:
            print('Error in Item : ' + str(item))

jsonripper()
