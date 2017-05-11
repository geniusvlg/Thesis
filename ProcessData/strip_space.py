import os
import json


def main():
	path = './data'
	for filename in os.listdir(path):
		with open(filename, 'w') as outf:
			with open('./data/'+filename, 'r') as f:
				ite=0
				for line in f:
					item = json.loads(line)
					for att in item:
						if type(item[att]) == type(''):
							item[att]=str(item[att]).strip()
					outf.write(json.dumps(item))
					outf.write('\n')
					ite+=1
					if ite%5000 == 0:
						print("Process {}".format(ite))


main()
