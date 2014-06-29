from p2pool.bitcoin import networks
from p2pool.util import math

# CHAIN_LENGTH = number of shares back client keeps
# REAL_CHAIN_LENGTH = maximum number of shares back client uses to compute payout
# REAL_CHAIN_LENGTH must always be <= CHAIN_LENGTH
# REAL_CHAIN_LENGTH must be changed in sync with all other clients
# changes can be done by changing one, then the other

nets = dict(
    x14=math.Object(
        PARENT=networks.nets['x14'],
        SHARE_PERIOD=15, # seconds
        CHAIN_LENGTH=24*60*60//15, # shares
        REAL_CHAIN_LENGTH=24*60*60//15, # shares
        TARGET_LOOKBEHIND=60, # shares  //with that the pools share diff is adjusting faster, important if huge hash$
        SPREAD=12, # blocks
        IDENTIFIER='dc2833941c8eb8b3'.decode('hex'),
        PREFIX='13a00a1fac114afd'.decode('hex'),
        P2P_PORT=1404,
        MIN_TARGET=4,
        MAX_TARGET=2**256//2**20 - 1,
        PERSIST=False,
        WORKER_PORT=1400,
        BOOTSTRAP_ADDRS='p2pool.x14.info'.split(' '),
        ANNOUNCE_CHANNEL='#p2pool-x14',
        VERSION_CHECK=lambda v: True,
    ),
)
for net_name, net in nets.iteritems():
    net.NAME = net_name
