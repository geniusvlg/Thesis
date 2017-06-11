import json
import os


def is_number(text):
    try:
        float(text)
        return True
    except ValueError:
        return False

class Fix():
    path='./data'
    keywords = ['thanh pho', 'thi xa', 'quan', 'huyen', 'dao', "phuong", "huyen dao", 'xa', "tp.", "h.", "p.",'thi tran']

    def merge_house_type(self):
        with open("house_type_conversion.json",'r') as f:
            self.convert_table=json.load(f)
        for filename in os.listdir(self.path):
            with open('./middle/'+filename,'w') as fo:
                with open(self.path+'/'+filename,'r') as f:
                    ite=0
                    for line in f:
                        ite+=1
                        if ite%5000==0:
                            print("Processed {}".format(ite))
                        item=json.loads(line)
                        try:
                            merged_type=self.convert_table[item['website']][item['house-type']]
                            item['location']=self.merge_location(item['location'],item['website'])
                            item['house-type']=merged_type
                            item['transaction-type']=item['transaction-type'].lower()
                            if item['transaction-type']=='':
                                item['transaction-type']='Khac'
                            if item['transaction-type']=='ban':
                                item['transaction-type']='can ban'
                            json.dump(item,fo)
                            fo.write("\n");
                        except Exception:
                            print(item)
                            print(Exception)
    
    def merge_location(self,location,website):
        keywords=self.keywords

        if website=='nhadat24h.net':
            if location['province'] == 'BR - Vung Tau':
                location['province'] = 'Ba Ria Vung Tau'
                if location['ward']=="Thanh phoVung Tau":
                    location['ward']="Thanh pho Vung Tau"
            if location['province'].lower() == 'hcm':
                location['province'] = 'ho chi minh'

        for att in location:
            if location[att]=='':
                location[att]='Khac'
            location[att]=location[att].lower()
            location[att]=location[att].strip()
            if att=='county' or att == 'ward':
                for keyword in keywords:
                    if location[att].find(keyword)==0:
                        arr=location[att].split(" ")
                        if not is_number(arr[1]):
                            # p.Tan Thanh (nhadat24h.net)
                            if keyword=='p.' or keyword == 'h.':
                                space= ' ' if website !='muabannhadat.vn' else ''
                                location[att]=location[att].replace(keyword + space,'')
                            else:
                                location[att]=location[att].replace(keyword+' ','')

                        break
        return location




if __name__=='__main__':
    main=Fix()
    main.merge_house_type()
