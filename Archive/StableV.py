import base64
import hashlib
import hmac
import json
import random
import re
import time

import aiohttp
from discord.ext import commands

import single_functions.config as config
master_user = 0
master_channel = 0
pump_signals_channels = [0, 1]

bot = commands.Bot(command_prefix=".", help_command=None)

symbols = {'SNX': '0.00000001', 'XLM': '0.0001', 'VET': '0.0001', 'GO': '0.0001', 'EOS': '0.0001', 'ETC': '0.000001', 'LTC': '0.000001', 'LYM': '0.0001', 'TKY': '0.0001', 'ONT': '0.0001', 'AOA': '0.0001', 'SUSD': '0.0001', 'TRX': '0.0001', 'BCHSV': '0.00000001', 'KCS': '0.0001', 'NEO': '0.000001', 'BCH': '0.0001', 'ETH': '0.0000001', 'BTC': '0.00000001', 'AVA': '0.0001', 'MHC': '0.0001', 'MTV': '0.0001', 'KMD': '0.0001', 'RFOX': '0.0001', 'TEL': '0.0001', 'AERGO': '0.0001', 'XMR': '0.0001', 'ATOM': '0.0001', 'ETN': '0.0001', 'FTM': '0.0001', 'TOMO': '0.0001', 'VSYS': '0.0001', 'CHR': '0.0001', 'COTI': '0.0001', 'BNB': '0.0001', 'JAR': '0.0001', 'ALGO': '0.0001', 'XEM': '0.0001', 'CIX100': '0.0001', 'XTZ': '0.0001', 'ZEC': '0.0001', 'ADA': '0.0001', 'R': '0.0001', 'WXT': '0.0001', 'FORESTPLUS': '0.0001', 'BOLT': '0.0001', 'ARPA': '0.0001', 'CHZ': '0.0001', 'DAPPT': '0.0001', 'NOIA': '0.0001', 'WIN': '0.0001', 'DERO': '0.0001', 'BTT': '0.0001', 'EOSC': '0.0001', 'ENQ': '0.0001', 'ONE': '0.0001', 'TOKO': '0.0001', 'VID': '0.0001', 'LUNA': '0.0001', 'MXW': '0.1', 'SXP': '0.0001', 'AKRO': '0.0001', 'MAP': '0.0001', 'AMPL': '0.01', 'DAG': '0.0001', 'POL': '0.0001', 'ARX': '0.0001', 'NWC': '0.0001', 'BEPRO': '0.0001', 'VRA': '0.0001', 'KSM': '0.0001', 'DASH': '0.0001', 'SUTER': '0.0001', 'ACOIN': '0.0001', 'SENSO': '0.0001', 'XDB': '0.0001', 'SYLO': '0.0001', 'WOM': '0.0001', 'DGB': '0.0001', 'LYXE': '0.0001', 'STX': '0.0001', 'USDN': '0.0001', 'XSR': '0.0001', 'COMP': '0.0001', 'CRO': '0.0001', 'KAI': '0.0001', 'WEST': '0.0001', 'WAVES': '0.0001', 'ORN': '0.0001', 'BNS': '0.0001', 'MKR': '0.0001', 'MLK': '0.0001', 'JST': '0.0001', 'SUKU': '0.0001', 'DIA': '0.0001', 'LINK': '0.0001', 'DOT': '0.0001', 'SHA': '0.0001', 'EWT': '0.0001', 'USDJ': '0.0001', 'CKB': '0.0001', 'UMA': '0.0001', 'ALEPH': '0.0001', 'VELO': '0.0001', 'SUN': '0.0001', 'BUY': '0.0001', 'YFI': '0.000001', 'LOKI': '0.0001', 'UNI': '0.0001', 'UOS': '0.0001', 'NIM': '0.0001', 'DEGO': '0.0001', 'RFUEL': '0.0001', 'FIL': '0.0001', 'REAP': '0.0001', 'AAVE': '0.0001', 'PRE': '0.0001', 'COMB': '0.0001', 'SHR': '0.0001', 'VIDT': '0.0001', 'UBXT': '0.0001', 'ROSE': '0.0001', 'USDC': '0.0001', 'CTI': '0.0001', 'XHV': '0.0001', 'PLU': '0.0001', 'GRT': '0.0001', 'CAS': '0.0001', 'MSWAP': '0.0001', 'GOM2': '0.0001', 'REVV': '0.0001', 'LON': '0.0001', '1INCH': '0.0001', 'LOC': '0.0001', 'API3': '0.0001', 'UNFI': '0.0001', 'HTR': '0.0001', 'FRONT': '0.0001', 'MIR': '0.0001', 'HYDRA': '0.0001', 'DFI': '0.0001', 'CRV': '0.0001', 'SUSHI': '0.0001', 'FRM': '0.0001', 'ZEN': '0.0001', 'CUDOS': '0.0001', 'REN': '0.0001', 'LRC': '0.0001', 'KLV': '0.0001', 'BOA': '0.0001', 'THETA': '0.0001', 'QNT': '0.0001', 'BAT': '0.0001', 'DOGE': '0.0001', 'DAO': '0.0001', 'STRONG': '0.0001', 'TRIAS': '0.0001', 'MITX': '0.0001', 'CAKE': '0.0001', 'ORAI': '0.0001', 'ZEE': '0.0001', 'LTX': '0.0001', 'MASK': '0.0001', 'IDEA': '0.0001', 'PHA': '0.0001', 'SRK': '0.0001', 'PIVX': '0.0001', 'SWINGBY': '0.0001', 'GAS': '0.0001', 'AVAX': '0.0001', 'KRL': '0.0001', 'POLK': '0.0001', 'ENJ': '0.0001', 'MANA': '0.0001', 'RNDR': '0.0001', 'RLY': '0.0001', 'ANC': '0.0001', 'SKEY': '0.0001', 'LAYER': '0.0001', 'TARA': '0.0001', 'IOST': '0.0001', 'DYP': '0.0001', 'XYM': '0.0001', 'PCX': '0.0001', 'ORBS': '0.0001', 'BTC3L': '0.0001', 'BTC3S': '0.0001', 'ETH3L': '0.0001', 'ETH3S': '0.0001', 'ANKR': '0.0001', 'DSLA': '0.0001', 'SPI': '0.0001', 'SAND': '0.0001', 'VAI': '0.0001', 'XCUR': '0.0001', 'FLUX': '0.0001', 'OMG': '0.0001', 'ZIL': '0.0001', 'DODO': '0.0001', 'CBC': '0.0001', 'MAN': '0.0001', 'BAX': '0.0001', 'BOSON': '0.0001', 'PUNDIX': '0.0001', 'WAX': '0.0001', 'HT': '0.0001', 'PDEX': '0.0001', 'LABS': '0.0001', 'GMB': '0.0001', 'PHNX': '0.0001', 'HAI': '0.0001', 'EQZ': '0.0001', 'FORTH': '0.0001', 'CARR': '0.0001', 'HORD': '0.0001', 'CGG': '0.0001', 'UBX': '0.0001', 'GHX': '0.0001', 'TCP': '0.0001', 'STND': '0.0001', 'TOWER': '0.0001', 'ACE': '0.0001', 'LOCG': '0.0001', 'CARD': '0.0001', 'FLY': '0.0001', 'CWS': '0.0001', 'XDC': '0.0001', 'SHIB': '0.0001', 'POLX': '0.0001', 'KDA': '0.0001', 'ICP': '0.0001', 'STC': '0.0001', 'GOVI': '0.0001', 'FKX': '0.0001', 'CELO': '0.0001', 'CUSD': '0.0001', 'FCL': '0.0001', 'MATIC': '0.0001', 'ELA': '0.0001', 'CRPT': '0.0001', 'OPCT': '0.0001', 'OGN': '0.0001', 'OUSD': '0.0001', 'TLOS': '0.0001', 'YOP': '0.0001', 'GLQ': '0.0001', 'NIF': '0.0001', 'MXC': '0.0001', 'ERSDL': '0.0001', 'HOTCROSS': '0.0001', 'ADA3L': '0.0001', 'ADA3S': '0.0001', 'HYVE': '0.0001', 'DAPPX': '0.0001', 'DPI': '0.0001', 'KONO': '0.0001', 'PRQ': '0.0001', 'MAHA': '0.0001', 'FEAR': '0.0001', 'PYR': '0.0001', 'PROM': '0.0001', 'GLCH': '0.0001', 'UNO': '0.0001', 'ALBT': '0.0001', 'XCAD': '0.0001', 'EOS3L': '0.0001', 'EOS3S': '0.0001', 'BCH3L': '0.0001', 'BCH3S': '0.0001', 'ELON': '0.0001', 'APL': '0.0001', 'VEED': '0.0001', 'DIVI': '0.0001', 'JUP': '0.0001', 'POLS': '0.0001', 'LPOOL': '0.0001', 'LSS': '0.0001', 'VET3L': '0.0001', 'VET3S': '0.0001', 'LTC3L': '0.0001', 'LTC3S': '0.0001', 'ETHO': '0.0001', 'ABBC': '0.0001', 'KOK': '0.0001', 'ROSN': '0.0001', 'DORA': '0.0001', 'ZCX': '0.0001', 'NORD': '0.0001', 'GMEE': '0.0001', 'SFUND': '0.0001', 'XAVA': '0.0001', 'AI': '0.0001', 'ALPACA': '0.0001', 'IOI': '0.0001', 'NFT': '0.0001', 'MNST': '0.0001', 'MEM': '0.0001', 'AGIX': '0.0001', 'CQT': '0.0001', 'AIOZ': '0.0001', 'MARSH': '0.0001', 'HAPI': '0.0001', 'MODEFI': '0.0001', 'YFDAI': '0.0001', 'GENS': '0.0001', 'FORM': '0.0001', 'ARRR': '0.0001', 'CEUR': '0.0001', 'EXRD': '0.0001', 'NGM': '0.0001', 'LPT': '0.0001', 'STMX': '0.0001',
           'ASD': '0.0001', 'BOND': '0.0001', 'SOUL': '0.0001', '2CRZ': '0.0001', 'NEAR': '0.0001', 'DFYN': '0.0001', 'OOE': '0.0001', 'CFG': '0.0001', 'AXS': '0.0001', 'CLV': '0.0001', 'ROUTE': '0.0001', 'KAR': '0.0001', 'EFX': '0.0001', 'BURP': '0.0001', 'SHFT': '0.0001', 'PMON': '0.0001', 'DPET': '0.0001', 'ERG': '0.0001', 'SOL': '0.0001', 'SLP': '0.0001', 'LITH': '0.0001', 'XCH': '0.0001', 'HAKA': '0.0001', 'MTL': '0.0001', 'IOTX': '0.0001', 'GALAX': '0.0001', 'REQ': '0.0001', 'TXA': '0.0001', 'CIRUS': '0.0001', 'QI': '0.0001', 'ODDZ': '0.0001', 'PNT': '0.0001', 'XPR': '0.0001', 'TRIBE': '0.0001', 'MOVR': '0.0001', 'WOO': '0.0001', 'WILD': '0.0001', 'QRDO': '0.0001', 'SDN': '0.0001', 'MAKI': '0.0001', 'REP': '0.0001', 'BNT': '0.0001', 'OXT': '0.0001', 'BAL': '0.0001', 'STORJ': '0.0001', 'YGG': '0.0001', 'NDAU': '0.0001', 'SDAO': '0.0001', 'XRP3L': '0.0001', 'XRP3S': '0.0001', 'SKL': '0.0001', 'NMR': '0.0001', 'IXS': '0.0001', 'TRB': '0.0001', 'DYDX': '0.0001', 'XYO': '0.0001', 'GTC': '0.0001', 'LUNA3L': '0.0001', 'LUNA3S': '0.0001', 'EQX': '0.0001', 'RLC': '0.0001', 'XPRT': '0.0001', 'EGLD': '0.0001', 'HBAR': '0.0001', 'DOGE3L': '0.0001', 'DOGE3S': '0.0001', 'FLOW': '0.0001', 'NKN': '0.0001', 'PBX': '0.0001', 'SOL3L': '0.0001', 'SOL3S': '0.0001', 'MLN': '0.0001', 'XNL': '0.0001', 'SOLVE': '0.0001', 'WNCG': '0.0001', 'DMTR': '0.0001', 'LINK3L': '0.0001', 'LINK3S': '0.0001', 'DOT3L': '0.0001', 'DOT3S': '0.0001', 'UMB': '0.0001', 'CTSI': '0.0001', 'ALICE': '0.0001', 'OPUL': '0.0001', 'DINO': '0.0001', 'ILV': '0.0001', 'BAND': '0.0001', 'FTT': '0.0001', 'DVPN': '0.0001', 'SKU': '0.0001', 'EDG': '0.0001', 'SLIM': '0.0001', 'TLM': '0.0001', 'DEXE': '0.0001', 'MATTER': '0.0001', 'RUNE': '0.0001', 'RMRK': '0.0001', 'SOV': '0.0001', 'BMON': '0.0001', 'C98': '0.0001', 'BLOK': '0.0001', 'SOLR': '0.0001', 'ATOM3L': '0.0001', 'ATOM3S': '0.0001', 'UNI3L': '0.0001', 'UNI3S': '0.0001', 'WSIENNA': '0.0001', 'PUSH': '0.0001', 'NTVRK': '0.0001', 'AXS3L': '0.0001', 'AXS3S': '0.0001', 'FTM3L': '0.0001', 'FTM3S': '0.0001', 'FLAME': '0.0001', 'AGLD': '0.0001', 'NAKA': '0.0001', 'YLD': '0.0001', 'TONE': '0.0001', 'REEF': '0.0001', 'TIDAL': '0.0001', 'TVK': '0.0001', 'INJ': '0.0001', 'BNB3L': '0.0001', 'BNB3S': '0.0001', 'MATIC3L': '0.0001', 'MATIC3S': '0.0001', 'NFTB': '0.0001', 'VEGA': '0.0001', 'ALPHA': '0.0001', 'BADGER': '0.0001', 'ZKT': '0.0001', 'AR': '0.0001', 'XVS': '0.0001', 'JASMY': '0.0001', 'PERP': '0.0001', 'GHST': '0.0001', 'SCLP': '0.0001', 'SUPER': '0.0001', 'CPOOL': '0.0001', 'HERO': '0.0001', 'BASIC': '0.0001', 'XED': '0.0001', 'AURY': '0.0001', 'SWASH': '0.0001', 'LTO': '0.0001', 'BUX': '0.0001', 'MTRG': '0.0001', 'DREAMS': '0.0001', 'QUICK': '0.0001', 'TRU': '0.0001', 'WRX': '0.0001', 'TKO': '0.0001', 'SUSHI3L': '0.0001', 'SUSHI3S': '0.0001', 'NEAR3L': '0.0001', 'NEAR3S': '0.0001', 'EPS': '0.0001', 'DATA': '0.0001', 'ISP': '0.0001', 'CERE': '0.0001', 'SHILL': '0.0001', 'HEGIC': '0.0001', 'ERN': '0.0001', 'FTG': '0.0001', 'PAXG': '0.0001', 'AUDIO': '0.0001', 'ENS': '0.0001', 'AAVE3L': '0.0001', 'AAVE3S': '0.0001', 'SAND3L': '0.0001', 'SAND3S': '0.0001', 'XTM': '0.0001', 'MNW': '0.0001', 'FXS': '0.0001', 'ATA': '0.0001', 'VXV': '0.0001', 'DPR': '0.0001', 'CWAR': '0.0001', 'PBR': '0.0001', 'WNXM': '0.0001', 'ANT': '0.0001', 'COV': '0.0001', 'SWP': '0.0001', 'TWT': '0.0001', 'OM': '0.0001', 'ADX': '0.0001', 'AVAX3L': '0.0001', 'AVAX3S': '0.0001', 'MANA3L': '0.0001', 'MANA3S': '0.0001', 'GLM': '0.0001', 'BAKE': '0.0001', 'NUM': '0.0001', 'VLX': '0.0001', 'TRADE': '0.0001', '1EARTH': '0.0001', 'MONI': '0.0001', 'LIKE': '0.0001', 'MFT': '0.0001', 'LIT': '0.0001', 'KAVA': '0.0001', 'SFP': '0.0001', 'BURGER': '0.0001', 'ILA': '0.0001', 'CREAM': '0.0001', 'RSR': '0.0001', 'IMX': '0.0001', 'GODS': '0.0001', 'KMA': '0.0001', 'SRM': '0.0001', 'POLC': '0.0001', 'XTAG': '0.0001', 'KIN': '0.0001', 'MNET': '0.0001', 'NGC': '0.0001', 'HARD': '0.0001', 'GALAX3L': '0.0001', 'GALAX3S': '0.0001', 'UNIC': '0.0001', 'POND': '0.0001', 'VR': '0.0001', 'EPIK': '0.0001', 'NGL': '0.0001', 'KDON': '0.0001', 'PEL': '0.0001', 'LINA': '0.0001', 'KLAY': '0.0001', 'CREDI': '0.0001', 'TRVL': '0.0001', 'LACE': '0.0001', 'ARKER': '0.0001', 'BONDLY': '0.0001', 'XEC': '0.0001', 'HEART': '0.0001', 'UNB': '0.0001', 'GAFI': '0.0001', 'KOL': '0.0001', 'H3RO3S': '0.0001', 'FALCONS': '0.0001', 'UFO': '0.0001', 'CHMB': '0.0001', 'GEEQ': '0.0001', 'ORC': '0.0001', 'RACEFI': '0.0001', 'PEOPLE': '0.0001', 'ADS': '0.0001', 'OCEAN': '0.0001', 'SOS': '0.0001', 'WHALE': '0.0001', 'TIME': '0.0001', 'CWEB': '0.0001', 'IOTA': '0.0001', 'OOKI': '0.0001', 'HNT': '0.0001', 'GGG': '0.0001', 'POWR': '0.0001', 'REVU': '0.0001', 'CLH': '0.0001', 'PLGR': '0.0001', 'GLMR': '0.0001', 'LOVE': '0.0001', 'CTC': '0.0001', 'GARI': '0.0001', 'FRR': '0.0001', 'ASTR': '0.0001', 'ERTHA': '0.0001', 'FCON': '0.0001', 'ACA': '0.0001', 'MTS': '0.0001', 'ROAR': '0.0001', 'HBB': '0.0001', 'SURV': '0.0001', 'CVX': '0.0001', 'AMP': '0.0001', 'ACT': '0.0001', 'MJT': '0.0001', 'SHX': '0.0001', 'STARLY': '0.0001', 'ONSTON': '0.0001', 'RANKER': '0.0001', 'WMT': '0.0001', 'XNO': '0.0001', 'MARS4': '0.0001', 'TFUEL': '0.0001', 'METIS': '0.0001', 'LAVAX': '0.0001', 'WAL': '0.0001', 'BULL': '0.0001', 'SON': '0.0001', 'MELOS': '0.0001', 'APE': '0.0001', 'GMT': '0.0001', 'BICO': '0.0001', 'STG': '0.0001', 'LMR': '0.0001', 'LOKA': '0.0001', 'URUS': '0.0001', 'JAM': '0.0001', 'BNC': '0.0001', 'LBP': '0.0001', 'CFX': '0.0001', 'LOOKS': '0.0001', 'XCN': '0.0001', 'KP3R': '0.0001', 'KAT': '0.0001', 'XRP': '0.0001', 'GRIN': '0.00000001'}


async def buy(coin: str, investment: int, session) -> str:
    endpoint = "/api/v1/orders"
    payload = {
        "clientOid": str(random.randint(1, 100000)),
        "side": "buy",
        "funds": str(investment),
        "symbol": f"{coin.upper()}-USDT",
        "type": "market",
    }

    data = json.dumps(payload)
    now = str(int(time.time() * 1000))
    str_to_sign = f"{now}POST{endpoint}{data}"

    signature = base64.b64encode(
        hmac.new(
            bot.api_secret.encode(
                "utf-8"), str_to_sign.encode("utf-8"), hashlib.sha256
        ).digest()
    )

    headers = {
        "KC-API-SIGN": signature.decode("utf-8"),
        "KC-API-TIMESTAMP": now,
        "KC-API-KEY": bot.api_key,
        "KC-API-PASSPHRASE": bot.passphrase,
        "KC-API-KEY-VERSION": "2",
    }

    response = await session.post(url=f"{bot.base}{endpoint}", headers=headers, json=payload)
    print(await response.json())
    return (await response.json())["data"]["orderId"]


async def get_order(orderId, session, full=False):
    endpoint = f"/api/v1/orders/{orderId}"
    payload = {
        "orderId": orderId,
    }
    data = json.dumps(payload)
    now = str(int(time.time() * 1000))
    str_to_sign = f"{now}GET{endpoint}{data}"
    signature = base64.b64encode(
        hmac.new(
            bot.api_secret.encode(
                "utf-8"), str_to_sign.encode("utf-8"), hashlib.sha256
        ).digest()
    )
    headers = {
        "KC-API-SIGN": signature.decode("utf-8"),
        "KC-API-TIMESTAMP": now,
        "KC-API-KEY": bot.api_key,
        "KC-API-PASSPHRASE": bot.passphrase,
        "KC-API-KEY-VERSION": "2",
    }

    response = await session.get(url=f"{bot.base}{endpoint}", headers=headers, json=payload)
    if full:
        return await response.json()
    return (await response.json())["data"]["dealSize"]


async def sell(coin: str, coin_bought: str, resale_price: str, session):
    endpoint = "/api/v1/orders"
    payload = {
        "clientOid": str(random.randint(1, 100000)),
        "side": "sell",
        "symbol": f"{coin}-USDT",
        "price": resale_price,
        "size": coin_bought,
        "type": "limit",
    }
    data = json.dumps(payload)
    now = str(int(time.time() * 1000))
    str_to_sign = f"{now}POST{endpoint}{data}"

    signature = base64.b64encode(
        hmac.new(
            bot.api_secret.encode(
                "utf-8"), str_to_sign.encode("utf-8"), hashlib.sha256
        ).digest()
    )

    headers = {
        "KC-API-SIGN": signature.decode("utf-8"),
        "KC-API-TIMESTAMP": now,
        "KC-API-KEY": bot.api_key,
        "KC-API-PASSPHRASE": bot.passphrase,
        "KC-API-KEY-VERSION": "2",
    }
    response = await session.post(url=f"{bot.base}{endpoint}", headers=headers, json=payload)
    return (await response.json())["data"]["orderId"]


@bot.listen("on_message")
async def pump(message):

    before = time.time()
    if message.channel.id not in pump_signals_channels:  # test, real
        return

    if not bot.reg.search(message.content):
        return

    coin = message.content.split("-")[0].split("/")[-1]
    orderId = await buy(coin, bot.investment, bot.session)
    buy_time = time.time()

    while True:
        coin_bought_amount = await get_order(orderId, bot.session)
        if coin_bought_amount != "0":
            coin_bought_amount = coin_bought_amount
            break

    int1, int2 = message.content.split("Gain: ")[-1].split("%")[0].split("-")
    int1, int2 = int(int1), int(int2)
    avg_expected_gain = float((int1 + int2) / 2)

    coin_to_sell = f"{coin_bought_amount.split('.')[0]}.{(coin_bought_amount.split('.')[-1])[:-(len(coin_bought_amount.split('.')[-1])-len(symbols[coin].split('.')[-1]))]}"

    total_sell_price = bot.investment + \
        (avg_expected_gain/100) * bot.investment
    sell_price_per_coin = total_sell_price/float(coin_bought_amount)
    sell_price_per_coin = float(f"{sell_price_per_coin:.5f}")
    before_sell = time.time()
    saleOrderId = await sell(
        coin,
        coin_to_sell,
        sell_price_per_coin,
        bot.session
    )
    end = time.time()
    channel = bot.get_channel(master_channel)
    await channel.send(
        f"""
@everyone Done.
Coin Bought: `{coin_bought_amount}` {coin.upper()} https://kucoin.com/trade/{coin.upper()}-USDT
Sold at:
        Total: `{total_sell_price}`
        Per Coin: `{sell_price_per_coin}`
Invested: `{bot.investment}`
Profit: `{total_sell_price - bot.investment}`
Time Taken:
        Total: `{end - before}`
        Buy: `{buy_time - before}`
        Get Order: `{before_sell - buy_time}`
        Sell: `{before_sell - buy_time}`

        Start: `{before}`
        After Buy: `{buy_time}`
        After Get Order: `{before_sell}`
        After Sell: `{end}`
Check status by `.status {saleOrderId}`
"""
    )

@bot.command(name="status")
async def status_(ctx, orderID):
    if ctx.author.id != master_user:
        return

    stuff = await get_order(orderID, bot.session, True)

    profit_on_sell = int(stuff["data"]["price"]) - int(bot.investment)
    await ctx.send(
        f"Expected profit is `{profit_on_sell}$`\n{stuff}"
    )


@bot.command(name="invest")
async def invest_instead(ctx, investment: int):
    if ctx.author.id != master_user:
        return

    bot.investment = investment
    await ctx.send(
        f"Investment set to `{investment}`"
    )
    open("investment.txt", "w").write(str(investment))


async def startup(bot):
    bot.investment = int(open("investment.txt", "r").read())
    bot.session = aiohttp.ClientSession()
    bot.api_key = config.api_key
    bot.api_secret = config.api_secret
    bot.api_passphrase = config.api_passphrase
    bot.base = "https://api.kucoin.com"
    bot.api_passphrase = config.api_passphrase
    bot.passphrase = config.passphrase
    bot.reg = re.compile(
        r"^Coin is: [A-V]{1,10}\n\nhttps:\/\/trade.kucoin.com\/[A-V]{1,10}-USDT\n\nProjected Gain: [0-9]{2,10}-[0-9]{2,10}%$")

bot.loop.create_task(startup(bot))
bot.run(config.token)
