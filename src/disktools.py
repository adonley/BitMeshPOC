import os

# path to file to save private / public key to
transaction_file = './key_store.txt'

def write_keys_to_file(private_key, public_key):

	with open(transaction_file,"w") as f:
		f.write(private_key)
		f.write('\n')
		f.write(public_key)
		f.write('\n')
		f.close()

	pass

def read_keys_from_file():

	private_key = ''
	public_key = ''

	with open(transaction_file,'r') as f:
		private_key = f.readline();
		public_key = f.readline();

	return (private_key, public_key)