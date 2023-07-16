import sys
import platform
import asyncio
import logging
import json
from datetime import date, timedelta

import aiohttp


currency = ['USD', 'EUR']

async def request(session, url):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                r = await response.json()
                return r
            logging.error(f'Error status {response.status} for {url}')
    except aiohttp.ClientConnectorError as e:
        logging.error(f'Connection error {url}: {e}')
    return None


async def get_exchange(day_count: int=1, ccy_list: list=currency):
    dt = date.today()
    rates = []
    async with aiohttp.ClientSession() as session:
        for k in range(day_count):
            cdt = dt - timedelta(days=k)
            sdt = cdt.strftime('%d.%m.%Y')
            res = await request(session, f'https://api.privatbank.ua/p24api/exchange_rates?json&date={sdt}')

            if res:
                exchangeRate = res["exchangeRate"]
                day_rate = {}
                for cur_rate in exchangeRate:
                    if cur_rate["currency"] in ccy_list:
                        sale = cur_rate.get("saleRate")
                        if not sale:
                            sale = cur_rate.get("saleRateNB")
                        purchase = cur_rate.get("purchaseRate")
                        if not purchase:
                            purchase = cur_rate.get("purchaseRateNB")
                        day_rate.update({cur_rate["currency"]: {'sale': sale, 'purchase': purchase}})
                rates.append({sdt: day_rate})
    return rates


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s  %(message)s',
        handlers=[logging.StreamHandler()]
    )

    day_count = 1
    args = sys.argv
    args.pop(0)
    if len(args) > 0:
        try:
            day_count = int(args[0])
            args.pop(0)
            logging.info(f'Days count {day_count}')
        except:
            day_count = 1
    
    if len(args) > 0:
        s = ",".join(args)
        ccy_list = s.upper().split(',')
        logging.info(f'Currencies {",".join(ccy_list)}')
    else:
        ccy_list = currency

    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    r = asyncio.run(get_exchange(day_count, ccy_list))
    
    with open('./cource.json', 'w', encoding='utf-8') as fd:
        json.dump(r, fd, ensure_ascii=False, indent=2)

    logging.info('Completed.')
    logging.info('Exchange rates are in the file "cource.json"')
