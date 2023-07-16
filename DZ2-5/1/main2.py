import sys
import platform
import asyncio
import logging
import json
from datetime import date, timedelta

from aiofile import async_open
import aiohttp


currency = ['USD', 'EUR']
ccy_list = currency
rates = []

def set_rate(data):
    global rates
    for data_key in data.keys():
        for ix in range(len(rates)):
            for key in rates[ix]:
                if key == data_key:
                    rates[ix] = data
                    return


async def consumer(filename: str, queue: asyncio.Queue):
    global rates
    async with async_open(filename, 'w', encoding='utf-8') as afd:
        while True:
            try:
                url, data = await queue.get()
                logging.info(f'Operation with url {url}')
                if len(data) > 0:
                    set_rate(data)
                s = json.dumps(rates, ensure_ascii=False, indent=2)
                afd.seek(0)
                await afd.write(s)
            except Exception as err:
                logging.error(f'Save file error : {err}')
                break
            finally:
                queue.task_done()


async def producer(url: str, queue: asyncio.Queue):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    res = await response.json()

                    rate = {}
                    if res:
                        sdt = res["date"]
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
                        rate.update({sdt: day_rate})
                    await queue.put((url, rate))
                    return None
                
                logging.error(f'Error status {response.status} for {url}')
        except aiohttp.ClientConnectorError as e:
            logging.error(f'Connection error {url}: {e}')
    return None


async def run(day_count: int=1):
    global rates
    rates = []
    rate_queue = asyncio.Queue()
    producers = []
    dt = date.today()
    for k in range(day_count):
        cdt = dt - timedelta(days=k)
        sdate = cdt.strftime('%d.%m.%Y')
        rates.append({sdate: {}})
        url = f'https://api.privatbank.ua/p24api/exchange_rates?json&date={sdate}'
        producers.append(asyncio.create_task(producer(url, rate_queue)))
    rate_consumer = asyncio.create_task(consumer('rates.json', rate_queue))

    await asyncio.gather(*producers)
    await rate_queue.join()
    rate_consumer.cancel()
    logging.info('Completed.')
    logging.info('Exchange rates are in the file "rates.json"')



if __name__ == '__main__':
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
    
    asyncio.run(run(day_count))
