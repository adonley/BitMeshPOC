from bitcoin.main import *
import zmq

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
port = "5556"

# zmq context
context = zmq.Context()

# socket to communicate thru
socket = context.socket(zmq.PAIR)


def get_bitmesh_peers():
	pass	

def get_new_pub_priv_key():
	priv_key = random_key()
	pub_key  = privkey_to_pubkey(priv_key)
	#TODO: handle failur
	#TODO: save to disk?
	return pub_key, priv_key

def open_micropayment_channel_with_peer(peer):
	our_pub_key, _  = get_new_pub_priv_key()
	peer_pub_key = request_pub_key_from_peer(peer)
	escrow_tx =	create_escrow_transaction(our_pub_key, peer_pub_key)
	refund_tx = create_refund_transaction(escrow_tx['outputs'][0], )
	
	# like a tab at a bar
	tab_tx    = create_tab_transaction(our_pub_key, peer_pub_key)
	refund_tx, tab_tx = send_refund_for_signature(refund_tx)
	broadcast_escrow_tx(escrow_tx)

def request_pub_key_from_peer(peer):
	socket.connect("tcp://%s:%s" % (peer, port))
	socket.send("gimme dat pub key!!11")
	msg = socket.recv()
	print msg
	#socket.connect("tcp://localhost:%s" % port)


def send_pub_key_to_peer():
	socket.bind("tcp://*:%s" % port)
	msg = socket.recv()
	print msg
	pub, _ = get_new_pub_priv_key()
	socket.send(pub)
	print 'sent', pub

def create_escrow_transaction(our_pub_key, peer_pub_key):
	script = bitcoin.mk_multisig_script(our_pub_key, peer_pub_key, 2, 2)
	return

def get_refund_transaction(multisig_output):
	# must have non-zero lock time
	# lock time is in absolute time with UNIX timestamp format
	# at least one of the input's sequence numbers must have a non-maxed-out sequence number
	# use 0
	refund_pub_key, _ 		 = get_new_pub_priv_key()
	refund_addr       		 = pubkey_to_address(refund_pub_key)
	refund_output     		 = {}
	refund_output['address'] = refund_addr
	refund_output['value']	 = channel_fund - (2 * tx_fee)

	return create_refund_transaction(multisig_output, refund_output)

def create_refund_transaction(*args):
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


def create_tab_transaction(our_pub_key, peer_pub_key):
	pass

def send_refund_for_signature(refund_tx):
	pass


def data_merchant_loop():
	while tab_not_exhausted() and service_is_available():
		request = receive_request
		get_prices_from_peers(bitmesh_peers, request)

def get_prices_from_peers(peers, request):
	pass

