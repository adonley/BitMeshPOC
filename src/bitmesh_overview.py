from bitcoin.main import *

class Peer:
	
    def __init__(self, arg=None):
    	pass

class Price:

	def __init__(self, arg=None):
		pass

# channel_width determines how many bytes pass thru before Alice pays
# should be a multiple of MTU? change units to packets?
channel_width = 1024

# how long in seconds to delay refund tx for
refund_delay = 1000000000

# amount of satoshi to lock up in escrow
channel_fund = 100000


def get_bitmesh_peers():
	pass

def open_micropayment_channel_with_peer(peer):
	our_priv_key = random_key()
	# TODO: handle failure
	our_pub_key  = privkey_to_pubkey(our_priv_key)
	peer_pub_key = request_pub_key_from_peer(peer)
	# TODO: handle failure
	escrow_tx =	create_escrow_transaction(our_pub_key, peer_pub_key)
	refund_tx = create_refund_transaction(our_pub_key, peer_pub_key)
	# like a tab at a bar
	tab_tx    = create_tab_transaction(our_pub_key, peer_pub_key)
	refund_tx, tab_tx = send_refund_for_signature(refund_tx)
	broadcast_escrow_tx(escrow_tx)

def request_pub_key_from_peer(peer):
	pass

def create_escrow_transaction(our_pub_key, peer_pub_key):
	pass

def create_refund_transaction(our_pub_key, peer_pub_key):
	# must have non-zero lock time
	# lock time is in absolute time with UNIX timestamp format
	# at least one of the input's sequence numbers must have a non-maxed-out sequence number
	# use 0
	pass

def create_tab_transaction(our_pub_key, peer_pub_key):
	pass

def send_refund_for_signature(refund_tx):
	pass

def data_merchant_loop:
	while tab_not_exhausted() and service_is_available():	
		request = receive_request
		get_prices_from_peers(bitmesh_peers, request)

def get_prices_from_peers(peers, request):
	pass

