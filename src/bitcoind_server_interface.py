from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import logging
import sys

access = None
connected = False

def connect_to_bitcoin_server(server_ip, port,user, password):
	global access 
	access = AuthServiceProxy("http://%s:%s@%s:%s"%(user,password,server_ip,port))
	pass


def get_addresses_and_balances():
	if access == None:
		raise Exception('Not Connected to server, cannot get addresses.')
		pass
	
	json_object = access.listaccounts()
	
	address_list = []
	privKey_list = []
	values_list  = []

	for account_name in json_object.keys():
		addresses = access.getaddressesbyaccount(account_name)
		for address in addresses:
			address_list.append(address)
			privKey_list.append(access.dumpprivkey(address))
			values_list.append(access.getreceivedbyaddress(address))

	return (address_list, privKey_list,values_list)

def import_private_key(private_key):
	logging.basicConfig()
	logging.getLogger("BitcoinRPC").setLevel(logging.DEBUG)
	if access == None:
		raise Exception('Not Connected to server, cannot import private key.')
		pass

	print(private_key)
	access.importprivkey(private_key,"rescan=false")
	
	pass