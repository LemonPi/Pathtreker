import pickle
def save():
	import loadaddress
	with open("address.pickle", "wb") as outfile:
		addresses = loadaddress.buildaddress()
		pickle.dump(addresses, outfile)

def load():
	with open("address.pickle", "rb") as infile:
		return pickle.load(infile)

if __name__ == "__main__":
	save()
