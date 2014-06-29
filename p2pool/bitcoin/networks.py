import os
import platform

from twisted.internet import defer

from . import data
from p2pool.util import math, pack, jsonrpc
from operator import *


@defer.inlineCallbacks
def check_genesis_block(bitcoind, genesis_block_hash):
    try:
        yield bitcoind.rpc_getblock(genesis_block_hash)
    except jsonrpc.Error_for_code(-5):
        defer.returnValue(False)
    else:
        defer.returnValue(True)

nets = dict(
    x14=math.Object(
        P2P_PREFIX='c1c2c2c1'.decode('hex'),
        P2P_PORT=26027,
        ADDRESS_VERSION=76,
        RPC_PORT=26026,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'X14Coinaddress' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda nBits, height: 140*100000000 >> (height + 1)//140000,
        BLOCKHASH_FUNC=lambda data: pack.IntType(256).unpack(__import__('x14_hash').getPoWHash(data)),
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('x14_hash').getPoWHash(data)),
        BLOCK_PERIOD=140, # s
        SYMBOL='X14',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'X14Coin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/X14Coin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.X14Coin'), 'X14Coin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://explorer.x14.info/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://explorer.x14.info/address/',
        TX_EXPLORER_URL_PREFIX='http://explorer.x14.info/tx/',
        SANE_TARGET_RANGE=(2**256//2**32//1000 - 1, 2**256//2**20 - 1),
        DUMB_SCRYPT_DIFF=1,
        DUST_THRESHOLD=0.001e8,
    ),
)
for net_name, net in nets.iteritems():
    net.NAME = net_name
