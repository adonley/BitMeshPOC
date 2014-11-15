from bitcoin.main import *

class Peer:
	
    def __init__(self, arg=None):
    	pass

class Price:

	def __init__(self, arg=None):
		pass

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
	refund_tx, tab_tx = send_refund_and_tab_for_signatures(refund_tx, tab_tx)
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

def send_refund_and_tab_for_signatures(refund_tx, tab_tx):
	pass

def data_merchant_loop:
	while tab_not_exhausted() and service_is_available():	
		request = receive_request
		get_prices_from_peers(bitmesh_peers, request)

