import json
import os
import re

class HouseTypeCnnversion:
	data = {}
	data_path = './data'

	def openFile(self):
		for filename in os.listdir(self.data_path):
			self.convertHouseType(filename)

	def convertHouseType