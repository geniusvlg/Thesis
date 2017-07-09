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
    keywords = ['thanh pho', 'thi xa', 'quan', 'huyen', 'dao', "phuong", "huyen dao", 'xa', "tp.", "h.", "p.",'thi tran',"q.","x."]

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
                        except BaseException as e:
                            print(item)
                            print("Exception",e)
    
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
            for keyword in keywords:
                arr=location[att].split(" ")
                if location[att].find(keyword)==0 and att!='location-detail':
                    
                    if len(arr)>1:
                        if not is_number(arr[1]):
                            # p.Tan Thanh (nhadat24h.net)
                            if keyword=='p.' or keyword == 'h.' or keyword =="q." or keyword == "x." or keyword=="tp.":
                                print(location[att])
                                space= ' ' if website !='muabannhadat.vn' else ''
                                location[att]=location[att].replace(keyword + space,'')
                            else:
                                location[att]=location[att].replace(keyword+' ','')
                            break
                if len(arr)==1:
                    if is_number(arr[0]):
                        if att=='county':
                            location[att]="quan "+location[att]
                        elif att=='ward':
                            location[att]='phuong' + location[att]
        return location

    def fix_object(self):
        data={} 
        with open("./processed/merge_output.json",'r') as f: 
            data=json.load(f)
        self.read_leaf(data)
        with open('./processed/merge_output_fix.json','w') as of:
            json.dump(data,of,indent=4)

    def read_leaf(self,data):
        del_list=[]
        for k,v in data.items():
            if isinstance(v,dict):
                self.read_leaf(v)
            else:
                for item in v:
                    item['location']=self.merge_location(item['location'],item['website'])

if __name__=='__main__':
    main=Fix()
    # main.merge_house_type()
    main.fix_object()
