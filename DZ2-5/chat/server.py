import asyncio
import logging
from datetime import date, timedelta

import websockets
import names
from websockets import WebSocketServerProtocol, WebSocketProtocolError
from websockets.exceptions import ConnectionClosedOK
import aiohttp

logging.basicConfig(level=logging.INFO)


currency = ['USD', 'EUR']

# async def request(session, url):
#     try:
#         async with session.get(url) as response:
#             if response.status == 200:
#                 r = await response.json()
#                 return r
#             logging.error(f'Error status {response.status} for {url}')
#     except aiohttp.ClientConnectorError as e:
#         logging.error(f'Connection error {url}: {e}')
#     return None


# async def get_exchange(day_count: int=1, ccy_list: list=currency):
#     dt = date.today()
#     rates = []
#     async with aiohttp.ClientSession() as session:
#         for k in range(day_count):
#             cdt = dt - timedelta(days=k)
#             sdt = cdt.strftime('%d.%m.%Y')
#             res = await request(session, f'https://api.privatbank.ua/p24api/exchange_rates?json&date={sdt}')

#             if res:
#                 exchangeRate = res["exchangeRate"]
#                 day_rate = res["date"]
#                 rates.append(day_rate)
#                 for cur_rate in exchangeRate:
#                     ccy = cur_rate["currency"]
#                     if ccy in ccy_list:
#                         sale = cur_rate.get("saleRate")
#                         if not sale:
#                             sale = cur_rate.get("saleRateNB")
#                         purchase = cur_rate.get("purchaseRate")
#                         if not purchase:
#                             purchase = cur_rate.get("purchaseRateNB")
#                         rates.append(f"{ccy}: buy: {purchase}, sale: {sale}")
#     return rates

# async def get_exchange():
#     res = await request('https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5')
#     # res = await request('https://api.privatbank.ua/p24api/exchange_rates?json&date=12.07.2023&currency=840')
#     exchange, *_ = list(filter(lambda el: el['ccy'] == 'USD', res))
#     buy = exchange['buy']
#     sale = exchange['sale']
#     return f'USD: buy: {buy}, sale: {sale}'


class Server:
    clients = set()

    async def register(self, ws: WebSocketServerProtocol):
        ws.name = names.get_full_name()
        self.clients.add(ws)
        logging.info(f'{ws.remote_address} connects')

    async def unregister(self, ws: WebSocketServerProtocol):
        self.clients.remove(ws)
        logging.info(f'{ws.remote_address} disconnects')

    async def send_to_clients(self, message: str):
        if self.clients:
            [await client.send(message) for client in self.clients]

    async def send_to_client(self, message: str, ws: WebSocketServerProtocol):
        await ws.send(message)

    async def ws_handler(self, ws: WebSocketServerProtocol):
        await self.register(ws)
        try:
            await self.distrubute(ws)
        except ConnectionClosedOK:
            pass
        finally:
            await self.unregister(ws)

    async def distrubute(self, ws: WebSocketServerProtocol):
        async for message in ws:
            if message:
                args = message.split(' ')
                if args[0] == 'exchange':
                    args.pop(0)
                    day_count = 1
                    if len(args) > 0:
                        try:
                            day_count = int(args[0])
                            args.pop(0)
                            logging.info(f'Days count {day_count}')
                        except:
                            day_count = 1
                    
                    if len(args) > 0:
                        s = ",".join(args)
                        ccy_list = s.replace(' ', '').upper().split(',')
                        logging.info(f'Currencies {",".join(ccy_list)}')
                    else:
                        ccy_list = currency

                    res = await self.get_exchange(day_count, ccy_list)
                    for r in res:
                        await self.send_to_client(r, ws)   
                else:
                    await self.send_to_clients(f"{ws.name}: {message}")
            else:  
                await self.send_to_clients(f"{ws.name}: {message}")

    async def request(self, session, url):
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    r = await response.json()
                    return r
                logging.error(f'Error status {response.status} for {url}')
        except aiohttp.ClientConnectorError as e:
            logging.error(f'Connection error {url}: {e}')
        return None

    async def get_exchange(self, day_count: int=1, ccy_list: list=currency):
        dt = date.today()
        rates = []
        async with aiohttp.ClientSession() as session:
            for k in range(day_count):
                cdt = dt - timedelta(days=k)
                sdt = cdt.strftime('%d.%m.%Y')
                res = await self.request(session, f'https://api.privatbank.ua/p24api/exchange_rates?json&date={sdt}')

                if res:
                    exchangeRate = res["exchangeRate"]
                    day_rate = res["date"]
                    rates.append(day_rate)
                    for cur_rate in exchangeRate:
                        ccy = cur_rate["currency"]
                        if ccy in ccy_list:
                            sale = cur_rate.get("saleRate")
                            if not sale:
                                sale = cur_rate.get("saleRateNB")
                            purchase = cur_rate.get("purchaseRate")
                            if not purchase:
                                purchase = cur_rate.get("purchaseRateNB")
                            rates.append(f"{ccy}: buy: {purchase}, sale: {sale}")
        return rates


async def main():
    server = Server()
    async with websockets.serve(server.ws_handler, 'localhost', 8080):
        await asyncio.Future()  # run forever

if __name__ == '__main__':
    asyncio.run(main())
