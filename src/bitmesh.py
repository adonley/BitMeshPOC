from bitcoin.main import *
import zmq
import requests

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
refund_delay = 100

# amount of satoshi to lock up in escrow
channel_fund = 100000

# tx fee for each tx
tx_fee = 5000

# port to communicate on
port = '5556'

# zmq context
context = zmq.Context()

# socket to communicate thru
socket = context.socket(zmq.PAIR)

# private key seller uses to sign multisig output
seller_multisig_priv_key = ''

# private key buyer uses to sign multisig output
buyer_multisig_priv_key = ''

# private key buyer uses to spend pre-existing funds
buyer_unspent_priv_key = ''

# complete refund tx signed and ready to broadcast
complete_refund_tx = {}

def get_new_pub_priv_key():
	priv_key = random_key()
	pub_key  = privkey_to_pubkey(priv_key)
	#TODO: handle failure
	#TODO: save to disk?
	return pub_key, priv_key

def data_merchant_loop():
	while tab_not_exhausted() and service_is_available():
		request = receive_request
		get_prices_from_peers(bitmesh_peers, request)


##################################
# MICROPAYMENT CHANNEL FUNCTIONS #
##################################

def get_unspent_outputs(min):
	# return outputs, total_in 
	# TODO hardwire it?
	pass

def buyer_open_micropayment_channel_with_peer(peer):
	global buyer_multisig_priv_key
	global complete_refund_tx
	buyer_multisig_pub_key, buyer_multisig_priv_key  = get_new_pub_priv_key()
	seller_multisig_pub_key    = request_pub_key_from_peer(peer)

	# create the escrow tx with multisig output
	escrow_tx =	create_escrow_transaction(buyer_multisig_pub_key, \
										  buyer_unspent_priv_key, \
										  seller_multisig_pub_key)
	
	# create the refund tx in case seller disappears
	refund_tx = create_refund_transaction(escrow_tx['outputs'][0])
	
	# send the refund, get it signed, check the signature
	seller_refund_signature = send_refund_for_signature(peer, refund_tx)

	# apply signatures to refund tx
	complete_refund_tx = buyer_sign_refund(refund_tx, seller_refund_signature)

	# send the escrow to seller, proving we have money on the table
	send_escrow_tx_to_seller(escrow_tx)

	# create a tab tx that sends seller bitcoin for services
	tab_tx = create_tab_transaction(escrow_tx['outputs'][0], peer_pub_key)

	return tab_tx


	# TODO: get data, update tab transaction
	while True:
		domain = raw_input('What website do you want')



# updates tab transaction by delta and re-signs the transaction, returns the signature
def buyer_update_tab_transaction(tab_tx, delta):
	refund_output   = tab_tx['outputs'][0]
	purchase_output = tab_tx['outputs'][1]

	if refund_output['value'] < delta:
		print 'not enough funds available'
		return

	refund_output['value']   = refund_output['value']   - delta
	purchase_output['value'] = purchase_output['value'] + delta

	buyer_signature = bitcoin.multisign(tab_tx, 0, tab_tx['inputs'][0]['script'], \
								buyer_multisig_priv_key)
	return buyer_signature

# create escrow transaction
# multisigs are applied in the following order: [0] buyer [1] seller
def create_escrow_transaction(buyer_pub_key, buyer_priv_key, seller_pub_key):
	inputs, total_in = get_unspent_outputs(channel_fund + tx_fee)

	# make a multisig output
	script = bitcoin.mk_multisig_script(buyer_pub_key, seller_pub_key, 2, 2)
	multisig_output           = {}
	multisig_output['script'] = script
	multisig_output['value']  = channel_fund

	# make a change address for the difference between inputs and outputs
	change_pub_key, _ 		 = get_new_pub_priv_key()
	change_addr       		 = pubkey_to_address(change_pub_key)
	change_output			 = {}
	change_output['address'] = change_addr
	change_output['value']   = total_in - channel_fund - tx_fee
	
	# make escrow_tx
	escrow_tx = bitcoin.mktx(inputs, multisig_output, change_output)

	# sign inputs
	# assumes there is one input and it's private key is buyer_priv_key
	return bitcoin.sign(escrow_tx, 0, buyer_priv_key)


# create a refund transaction with the escrow's multisig output as input
def create_refund_transaction(multisig_input):
	buyer_refund_pub_key, _  = get_new_pub_priv_key()
	buyer_refund_addr        = pubkey_to_address(buyer_refund_pub_key)

	# just send all the money back to the buyer
	refund_output     		 = {}
	refund_output['address'] = buyer_refund_addr
	refund_output['value']	 = channel_fund - tx_fee

	return build_refund_transaction(multisig_input, refund_output)

# create refund transaction
# it must have non-zero lock time
# lock time is in absolute time with UNIX timestamp format
# at least one of the input's sequence numbers must have a non-maxed-out sequence number
# using 0 for all sequence numbers
def build_refund_transaction(*args):
    # [in0, in1...],[out0, out1...] or in0, in1 ... out0 out1 ...
    ins, outs = [], []
    for arg in args:
        if isinstance(arg, list):
            for a in arg: (ins if is_inp(a) else outs).append(a)
        else:
            (ins if is_inp(arg) else outs).append(arg)

    txobj = {"locktime": refund_delay, "version": 1, "ins": [], "outs": []}
    for i in ins:
        if isinstance(i, dict) and "outpoint" in i:
            txobj["ins"].append(i)
        else:
            if isinstance(i, dict) and "output" in i:
                i = i["output"]
            txobj["ins"].append({
                "outpoint": {"hash": i[:64], "index": int(i[65:])},
                "script": "",
                "sequence": 0
            })
    for o in outs:
        if isinstance(o, (str, unicode)):
            addr = o[:o.find(':')]
            val = int(o[o.find(':')+1:])
            o = {}
            if re.match('^[0-9a-fA-F]*$', addr):
                o["script"] = addr
            else:
                o["address"] = addr
            o["value"] = val

        outobj = {}
        if "address" in o:
            outobj["script"] = address_to_script(o["address"])
        elif "script" in o:
            outobj["script"] = o["script"]
        else:
            raise Exception("Could not find 'address' or 'script' in output.")
        outobj["value"] = o["value"]
        txobj["outs"].append(outobj)

    return serialize(txobj)

def create_tab_transaction(multisig_input, seller_pub_key):

	# make a refund output with the entire input
	refund_pub_key, _ 		   = get_new_pub_priv_key()
	refund_addr       	       = pubkey_to_address(refund_pub_key)

	refund_output     		   = {}
	refund_output['address']   = refund_addr
	refund_output['value']	   = channel_fund - tx_fee

	# make a purchase output that goes to the seller
	# this gets incrementally increased as more data is delivered
	purchase_output            = {}
	purchase_output['address'] = seller_pub_key
	purchase_output['value']   = 0
	
	# make the tab tx
	return bitcoin.mktx(multisig_input, refund_output, purchase_output)


# seller signs refund, returns signature
def seller_sign_refund(refund_tx):
	signature = bitcoin.multisign(refund_tx, 0, refund_tx['inputs'][0]['script'], \
						seller_multisig_priv_key)
	return signature
	
def buyer_sign_refund(refund_tx, seller_signature):
	# get buyer's signature on refund
	buyer_signature = bitcoin.multisign(refund_tx, 0, refund_tx['inputs'][0]['script'], \
										buyer_multisig_priv_key)
	

	# apply signatures and return completed tx 
	return bitcoin.apply_multisignatures(refund_tx, 0, refund_tx['inputs'][0]['script'], \
									buyer_signature, seller_signature)

def seller_validate_escrow_tx(escrow_tx):
	pass

################################
# PEER COMMUNICATION FUNCTIONS #
################################

def send_refund_for_signature(peer, refund_tx):
	socket.send(refund_tx)
	print 'sent refund_tx for signature'

	signature = socket.recv()
	print 'received signature'
	
	#TODO: check signature

	

	return signature

def send_escrow_tx_to_seller(escrow_tx):
	socket.send(escrow_tx)

def get_bitmesh_peers():
	# TODO
	pass	

def get_prices_from_peers(peers, request):
	# TODO
	pass

def request_pub_key_from_peer(peer):
	socket.connect('tcp://%s:%s' % (peer, port))
	socket.send('gimme dat pub key!!11')
	msg = socket.recv()
	print msg
	#socket.connect("tcp://localhost:%s" % port)

def seller_handle_refund_tx():

	# wait for the refund_tx from the buyer
	refund_tx = socket.recv()
	print 'received refund tx', refund_tx

	# validate refund tx (check that input is multisig with our key)
	# TODO

	# sign it and send signature back, ensuring the ability of the buyer
	# to get a refund if seller disappears
	signature = seller_sign_refund(refund)
	socket.send(signature)
	print 'returned signature for refund', signature

def seller_handle_escrow_tx():

	# wait for the escrow_tx from the buyer to prove money is on the table
	escrow_tx = socket.recv()

	# validate escrow tx (check input signatures, multisig output)
	valid = seller_validate_escrow_tx(escrow_tx)

	if valid:
		# broadcast it
		broadcast_tx(escrow_tx)
	else:
		print 'escrow_tx was not valid', escrow_tx
		# TODO 

	socket.send('escrow tx was %s' % valid)

def seller_handle_domain_request():

	# get the requested domain from the buyer
	domain = socket.recv()

	# TODO: validate the domain is a good one
	html = requests.get(domain).text

	socket.send(html)


def listen_for_buyers():
	socket.bind('tcp://*:%s' % port)
	while True:
		# listen for messages
		message = socket.recv()
		print 'received message', message	
		parse_message(message)


def parse_message(peer_message):
	# handle requests
	# probably should be on another thread
	# and another port

	if peer_message['intent'] is 'buy':
		send_pub_key_to_peer()
		seller_handle_refund_tx()
		seller_handle_escrow_tx()
		seller_handle_domain_request()
	# TODO

def send_pub_key_to_peer():

	global seller_multisig_priv_key
	pub, seller_multisig_priv_key = get_new_pub_priv_key()
	socket.send(pub)
	print 'sent', pub, 'waiting for refund tx'



#############################
# BITCOIN NETWORK FUNCTIONS #
#############################

def broadcast_tx(tx):
	bitcoin.blockr_pushtx(tx, network='testnet')
