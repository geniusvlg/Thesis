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
    hn_counties = ["ba dinh",
                   "ba vi",
                   "bac tu liem",
                   "cau giay",
                   "chuong my",
                   "dan phuong",
                   "dong anh",
                   "dong da",
                   "gia lam",
                   "ha dong",
                   "hai ba trung",
                   "hau giang",
                   "hoai duc",
                   "hoan kiem",
                   "hoang mai",
                   "khac",
                   "long bien",
                   "me linh",
                   "my duc",
                   "nam tu liem",
                   "phu giao",
                   "phu xuyen",
                   "phuc tho",
                   "quoc oai",
                   "soc son",
                   "son tay",
                   "tan uyen",
                   "tay ho",
                   "thach that",
                   "thanh oai",
                   "thanh tri",
                   "thanh xuan",
                   "thuan an"
                   "thuong tin",
                   "ung hoa"]
    location = {"ho chi minh":  {
               "quan 1" : ["ben thanh", "cau kho", "cau ong lanh", "co giang", "da kao", "nguyen cu trinh", "nguyen thai binh", "pham ngu lao", "tan dinh"], 
               "quan 2" : ["an khanh", "an loi dong", "an phu", "binh an", "binh khanh", "binh trung dong", "binh trung tay", "cat lai", "thao dien", "thu thiem", "thanh my loi"],
               "quan 3": ["phuong 1", "phuong 2", "phuong 3", "phuong 4", "phuong 5", "phuong 6", "phuong 7", "phuong 8", "phuong 9", "phuong 10", "phuong 11", "phuong 12", "phuong 13", "phuong 14"],
               "quan 4": ["phuong 1", "phuong 2", "phuong 3", "phuong 4", "phuong 5", "phuong 6", "phuong 8", "phuong 9", "phuong 10", "phuong 12", "phuong 13", "phuong 14", "phuong 15", "phuong 16", "phuong 18"],
               "quan 5": ["phuong 1", "phuong 2", "phuong 3", "phuong 4", "phuong 5", "phuong 6", "phuong 7", "phuong 8", "phuong 9", "phuong 10", "phuong 11", "phuong 12", "phuong 13", "phuong 14", "phuong 15"],
               "quan 6": ["phuong 1", "phuong 2", "phuong 3", "phuong 4", "phuong 5", "phuong 6", "phuong 7", "phuong 8", "phuong 9", "phuong 10", "phuong 11", "phuong 12", "phuong 13", "phuong 14"],
               "quan 7": ["binh thuan", "phu my", "phu thuan", "tan hung", "tan phong", "tan phu", "tan kieng", "tan quy", "tan thuan dong", "tan thuan tay"],
               "quan 8": ["phuong 1", "phuong 2", "phuong 3", "phuong 4", "phuong 5", "phuong 6", "phuong 7", "phuong 8", "phuong 9", "phuong 10", "phuong 11", "phuong 12", "phuong 13", "phuong 14", "phuong 15", "phuong 16"],
               "quan 9": ["hiep phu", "long binh", "long phuong", "long truong", "long thanh my", "phu huu", "phuoc binh", "phuong long a", "phuoc long b", "tang nhon phu a", "tang nhon phu b", "tan phu", "truong thanh"],
               "quan 10": ["phuong 1", "phuong 2", "phuong 3", "phuong 4", "phuong 5", "phuong 6", "phuong 7", "phuong 8", "phuong 9", "phuong 10", "phuong 11", "phuong 12", "phuong 13", "phuong 14", "phuong 15"],
               "quan 11": ["phuong 1", "phuong 2", "phuong 3", "phuong 4", "phuong 5", "phuong 6", "phuong 7", "phuong 8", "phuong 9", "phuong 10", "phuong 11", "phuong 12", "phuong 13", "phuong 14", "phuong 15", "phuong 16"],
               "quan 12": ["an phu dong", "dong hung thuan", "hiep thanh", "tan chanh hiep", "tan thoi hiep", "tan thoi nhat", "thanh loc", "thanh xuan", "thoi an", "trung my tay"],
               "thu duc": ["binh chieu", "binh tho", "hiep binh chanh", "hiep binh phuoc", "linh chieu", "linh dong", "linh tay", "linh trung", "linh xuan", "tam binh", "tam phu", "truong tho"],
               "go vap": ["phuong 1", "phuong 3", "phuong 4", "phuong 5", "phuong 7", "phuong 10", "phuong 11", "phuong 12", "phuong 13", "phuong 15", "phuong 16", "phuong 17"],
               "binh thanh": ["phuong 1", "phuong 2", "phuong 3", "phuong 5", "phuong 6", "phuong 7", "phuong 11", "phuong 12", "phuong 13", "phuong 14", "phuong 15", "phuong 17", "phuong 19"],
               "tan binh": ["phuong 1", "phuong 2", "phuong 3", "phuong 4", "phuong 5", "phuong 6", "phuong 7", "phuong 8", "phuong 9", "phuong 10", "phuong 11", "phuong 12", "phuong 13", "phuong 14", "phuong 15"],
               "tan phu": ["hoa thanh", "hiep tan", "phu thanh", "phu tho hoa", "phu trung", "son ky", "tan thanh", "tan thoi hoa", "tan quy", "tan son nhi", "tay thanh"],
               "phu nhuan": ["phuong 1", "phuong 2", "phuong 3", "phuong 4", "phuong 5", "phuong 7", "phuong 8", "phuong 9", "phuong 10", "phuong 11", "phuong 12", "phuong 13", "phuong 14", "phuong 15", "phuong 17"],
               "binh tan": ["an lac", "an lac a", "binh hung hoa", "binh hung hoa a", "binh hung hoa b", "binh tri dong", "binh tri dong a", "binh tri dong b", "tan tao", "tan tao a"],
               "cu chi": ["cu chi", "an nhon tay", "an phu", "binh my", "hoa phu", "nhuan duc", "pham van coi", "phuoc hiep", "phuoc thiep", "phuoc thanh", "phu hoa dong", "phu my hung", "tan an hoi", "tan phu trung", "tan thanh dong", "tan thanh tay", "tan thong hoi", "thai my", "trung an", "trung lap ha", "trung lap thuong", "phuoc vinh an"],
               "hoc mon": ["hoc mon", "ba diem", "dong thanh", "nhi binh", "tan hiep", "tan thoi nhi", "tan xuan", "thoi tam thon", "trung chanh", "xuan thoi dong", "xuan thoi son", "xuan thoi thuong"],
               "binh chanh": ["tan tuc", "an phu tay", "binh chanh", "binh hung", "binh loi", "da phuoc", "hung long", "le minh xuan", "pham van hai", "phong phu", "quy duc", "tan kien", "tan nhut", "tan quy tay", "vinh loc a", "vinh loc b"],
               "nha be": ["nha be", "hiep phuoc", "long thoi", "nhon duc", "phu xuan", "phuoc kien", "phuoc loc"],
               "can gio": ["can gio", "can thanh", "an thoi dong", "binh khanh", "long hoa", "ly nhon", "tam thon hiep", "thanh an"]
              } ,
      "ha noi":     {
            "ba dinh" : ["phuc xa", "truc bach", "vinh phuc", "cong vi", "lieu giai", "nguyen trung truc", "quan thanh", "ngoc ha", "dien bien", "doi can", "ngoc khanh", "kim ma", "giang vo", "thanh cong"], 
            "hoan kiem" : ["chuong duong", "dong xuan", "hang bo", "hang gai", "ly thai to", "tran hung dao", "chuong duong do", "hai ba trung", "hang bong", "hang ma", "pham dinh ho", "trang thi", "cua dong", "hang bac", "hang buom", "hang trong", "phan chu trinh", "trang tien", "cua nam", "hang bai", "hang dao", "hoan kiem", "phuc tan"],
            "tay ho": ["phu thuong", "nhat tan", "tu lien", "quang an", "xuan la", "yen phu", "buoi", "thuy khue"],
            "long bien": ["thuong thanh", "ngoc thuy", "giang bien", "duc giang", "viet hung", "gia thuy", "ngoc lam", "phuc loi", "bo de", "sai dong", "long bien", "thach ban", "phuc dong", "cu khoi"],
            "cau giay": ["nghia do", "nghia tan", "mai dich", "dich vong", "dich vong hau", "quan hoa", "yen hoa", "trung hoa"],
            "dong da": ["cat linh", "van mieu", "quoc tu giam", "lang thuong", "o cho dua", "van chuong", "hang bot", "lang ha", "kham thien", "tho quan", "nam dong", "trung phung", "quang trung", "trung liet", "phuong liet", "thinh quang", "trung tu", "kim lien", "phuong mai", "nga tu so", "khuong thuong"],
            "hai ba trung": ["nguyen du", "bach dang", "pham dinh ho", "bui thi xuan", "ngo thi nham", "le dai hanh", "dong nhan", "pho hue", "dong mac", "thanh luong", "thanh nhan", "cau den", "bach khoa", "dong tam", "vinh tuy", "bach mai", "quynh mai", "quynh loi", "minh khai", "truong dinh"],
            "hoang mai": ["thanh tri", "dinh cong", "mai dong", "tuong mai", "dai kim", "tan mai", "hoang van thu", "giap bat", "linh nam", "thinh liet", "tran phu", "hoang liet", "yen so"],
            "thanh xuan": ["nhan chinh", "thuong dinh", "khuong trung", "khuong mai", "thanh xuan trung", "phuong liet", "ha dinh", "khuong dinh", "thanh xuan bac", "thanh xuan nam", "kim giang"],
            "soc son": ["soc son", "bac son", "minh tri", "hong ky", "nam son", "trung gia", "tan hung", "minh phu", "phu linh", "bac phu", "tan minh", "quang tien", "hien ninh", "tan dan", "tien duoc", "viet long", "xuan giang", "mai dinh", "duc hoa", "thanh xuan", "dong xuan", "kim lu", "phu cuong", "phu minh", "phu lo", "xuan thu"],
            "dong anh": ["dong anh", "xuan non", "thuy lam", "bac hong", "nguyen khe", "nam hong", "tien duong", "van ha", "uy no", "van noi", "lien ha", "viet hung", "kim no", "kim chung", "duc tu", "dai mach", "vinh ngoc", "co loa", "hai boi", "xuan canh", "vong la", "tam xa", "mai lam", "dong hoi"],
            "gia lam": ["yen vien", "yen thuong", "ninh hiep", "dinh xuyen", "duong ha", "phu dong", "trung mau", "le chi", "co bi", "dang xa", "phu thi", "kim son", "trau quy", "duong quang", "duong xa", "dong du", "da ton", "keu ky", "bat trang", "kim lan", "van duc"],
            "bac tu liem": ["cau dien", "xuan phuong", "phuong canh", "my dinh 1", "my dinh 2", "tay mo", "me tri", "phu do", "dai mo", "trung van"],
            "nam tu liem": ["thuong cat", "lien mac", "dong ngac", "duc thang", "thuy phuong", "tay tuu", "xuan dinh", "xuan tao", "minh khai", "co nhue 1", "co nhue 2", "phu dien", "phuc dien"],
            "thanh tri": ["van dien", "tan trieu", "thanh liet", "ta thanh oai", "huu hoa", "tam hiep", "tu hiep", "yen my", "vinh quynh", "duyen ha", "ngoc hoi", "van phuc", "dai ang", "lien ninh", "dong my"],
            "me linh": ["chi dong", "dai thinh", "kim hoa", "thach da", "tien thang", "tu lap", "quang minh", "thanh lam", "tam dong", "lien mac", "van yen", "chu phan", "tien thinh", "me linh", "van khe", "hoang kim", "tien phong", "trang viet"],
            "ha dong": ["nguyen trai", "mo lao", "van quan", "van phuc", "yet kieu", "quang trung", "la khe", "ha cau", "yen nghia", "kien hung", "phu lam", "phu luong", "duong noi", "dong mai", "bien giang"],
            "son tay": ["le loi", "phu thinh", "ngo quyen", "quang trung", "son loc", "xuan khanh", "duong lam", "vien son", "xuan son", "trung hung", "thanh my", "trung son tram", "kim son", "son dong", "co dong"],
            "ba vi": ["tay dang", "phu cuong", "co do", "tan hong", "van thang", "chau son", "phong van", "phu dong", "phu phuong", "phu chau", "thai hoa", "dong thai", "phu son", "minh chau", "vat lai", "chu minh", "tong bat", "cam linh", "son da", "dong quang", "tien phong", "thuy an", "cam thuong", "thuan my", "tan linh", "ba trai", "minh quang", "ba vi", "van hoa", "yen bai", "khanh thuong"],
            "phuc tho": ["phuc tho", "van ha", "van phuc", "van nam", "xuan phu", "phuong do", "sen chieu", "cam dinh", "vong xuyen", "tho loc", "long xuyen", "thuong coc", "hat mon", "tich giang", "thanh da", "trach my loc", "phuc hoa", "ngoc tao", "phung thuong", "tam thuan", "tam hiep", "hiep thuan", "lien hiep"],
            "dan phuong": ["phung", "trung chau", "tho an", "tho xuan", "hong ha", "lien hong", "lien ha", "ha mo", "lien trung", "phuong dinh", "thuong mo", "tan hoi", "tan lap", "dan phuong", "dong thap", "song phuong"],
            "hoai duc": ["tam troi", "duc thuong", "minh khai", "duong lieu", "di trach", "duc giang", "cat que", "kim chung", "yen so", "son dong", "van canh", "dac so", "lai yen", "tien yen", "song phuong", "an khanh", "an thuong", "van con", "la phu", "dong la"],
            "quoc oai": ["dong xuan", "quoc oai", "sai son", "phuong cach", "yen son", "ngoc liep", "ngoc my", "liep tuyet", "thach than", "dong quang", "phu cat", "tuyet nghia", "nghia huong", "cong hoa", "tan phu", "dai thanh", "phu man", "can huu", "tan hoa", "hoa thach", "dong yen"],
            "thach that": ["yen trung", "yen binh", "tien xuan", "lien quan", "dai dong", "cam yen", "lai thuong", "phu kim", "huong ngai", "canh nau", "kim quan", "di nau", "binh yen", "chang son", "thach hoa", "can kiem", "huu bang", "phung xa", "tan xa", "thach xa", "binh phu", "ha bang", "dong truc"],
            "chuong my": ["chuc son", "xuan mai", "phung chau", "tien duong", "dong son", "dong phuong yen", "phu nghia", "truong yen", "ngoc hoa", "thuy xuan tien", "thanh binh", "trung hoa", "dai yen", "thuy huong", "tot dong", "lam dien", "tan tien", "nam phuong tien", "hop dong", "hoang van thu", "hoang dieu", "huu van", "quang bi", "my luong", "thuong vuc", "hong phong", "dong phu", "tran phu", "van vo", "dong lac", "hoa chinh", "phu nam an"],
            "thanh oai": ["kim bai", "cu khe", "bich hoa", "my hung", "cao vien", "binh minh", "tam hung", "thanh cao", "thanh thuy", "thanh mai", "thanh van", "do dong", "kim an", "kim thu", "phuong trung", "tan uoc", "dan hoa", "lien chau", "cao duong", "xuan duong", "hong duong"],
            "thuong tin": ["thuong tin", "ninh so", "nhi khe", "duyen thai", "khanh ha", "hoa binh", "van binh", "hien giang", "hong van", "van tao", "lien phuong", "van phu", "tu nhien", "tien phong", "ha hoi", "thu phu", "nguyen trai", "quat dong", "chuong duong", "tan minh", "le loi", "thang loi", "dung tien", "thong nhat", "nghiem xuyen", "to hieu", "van tu", "van diem", "minh cuong"],
            "phu xuyen": ["phu minh", "phu xuyen", "hong minh", "phuong duc", "van nhan", "thuy phu", "tri trung", "dai thang", "phu tuc", "van hoang", "hong thai", "hoang long", "quang trung", "nam phong", "nam trieu", "tan dan", "son ha", "chuyen my", "khai thai", "phuc tien", "van tu", "tri thuy", "dai xuyen", "phu yen", "bach ha", "quang lang", "chau can", "minh tan"],
            "ung hoa": ["van dinh", "vien an", "vien noi", "hoa son", "quang phu cau", "truong thinh", "cao thanh", "lien bat", "son cong", "dong tien", "phuong tu", "trung tu", "dong tan", "tao duong van", "van thai", "minh duc", "hoa lam", "hoa xa", "tram long", "kim duong", "hoa nam", "hoa phu", "doi binh", "dai hung", "dong lo", "phu luu", "dai cuong", "luu hoang", "hong quang"],
            "my duc": ["dai nghia", "dong tam", "thuong lam", "tuy lai", "phuc lam", "my thanh", "bot xuyen", "an my", "hong son", "le thanh", "xuy xa", "phung xa", "phu luu te", "dai hung", "van kim", "doc tin", "huong son", "hung tien", "an tien", "hop tien", "hop thanh", "an phu"]
            }
}


    def merge_house_type(self):
        with open("house_type_conversion.json",'r') as f:
            self.convert_table=json.load(f)
        for filename in os.listdir(self.path):
            with open('./middle/'+filename,'w') as fo:
                with open(self.path+'/'+filename,'r',encoding='utf8') as f:
                    ite=0
                    print(filename)
                    for line in f:
                        # if(filename=="batdongsan1507.jl"):
                        #     print(ite)
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
            if location['county']=='q.hai ba trung':
                location['county']='hai ba trung'
        if website=='diaoconline.vn':
            if location['province']=='tp.hcm':
                location['province'] = 'ho chi minh'
            if location['county']=='tp.vung tau':
                location['county']='vung tau'
            if location['province']=='ba ria - vung tau':
                location['province']='ba ria vung tau'
            if re.search("vi tri:",item['location']['county'])!=-1:
                tmp = item['location']['county'].split(" ")
                if is_number(tmp[1]):
                    tmp[0] = tmp[0].replace('vi tri:','')
                else:
                    del tmp[0]
                item['location']['county']=tmp.join(" ")
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
                                location[att]=location[att].replace(keyword,'')
                                location[att]=location[att].strip()
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
                del_list=[]
                with open('./move_data_diaoconline.json','a') as of:
                  for i, item in enumerate(v):
                      # item['location']=self.merge_location(item['location'],item['website'])
                      if item['location']['province']=='tp.hcm':
                          item['location']['province'] = 'ho chi minh'
                      if item['location']['county']=='tp.vung tau':
                          item['location']['county']='vung tau'
                      if item['location']['county'].find("vi tri:")!=-1:
                          tmp = item['location']['county'].split(":")
                          tmp2 = tmp[1].split(" ");
                          if len(tmp2)>2:
                              del tmp2[0]
                      if item['location']['ward'].find("vi tri:")!=-1:
                          tmp = item['location']['ward'].split(":")
                          tmp2 = tmp[1].split(" ");
                          if len(tmp2)>2:
                              del tmp2[0]
                          item['location']['county']=" ".join(tmp2)
                      if item['location']['county']=='q.hai ba trung':
                          item['location']['county']='hai ba trung'
                      
                      if (item['location']['province'] in ['ho chi minh','ha noi']):
                        if (item['location']['county'] not in self.location[item['location']['province']].keys()):
                          del_list.append(i)
                          print(item['location'])
                        elif (item['location']['ward'] not in ['','khac','Khac'] and item['location']['ward'] not in self.location[item['location']['province']][item['location']['county']]):
                          del_list.append(i)
                          print(item['location'])
                            
                      if item['location']['ward'].find("so")==0 and item['location']['county']=='quan 7':
                          del_list.append(i)
                      if item['location']['ward'].find('phuong')==0 and len(item['location']['ward'].split(" "))==1:
                          item['location']['ward']=item['location']['ward'][:6]+" "+item['location']['ward'][6:]
                      if item['website']=='diaoconline.vn':
                          del_list.append(i)
                          json.dump(item,of)
                          of.write("\n")

                      # if (item['title'].find('Cho thue')!=-1 or item['title'].find('cho thue')!=-1) and item['transaction-type']=='can ban' and item['website']=='muabannhadat.vn':
                      #     del_list.append(i)
                      #     json.dump(item,of)
                      #     of.write("\n")
                      if item['website']=='muabannhadat.vn':
                          del_list.append(i)
                del_list = list(set(del_list))
                del_list.sort()
                for i in reversed(del_list):
                    del v[i]



if __name__=='__main__':
    main=Fix()
    # main.merge_house_type()
    main.fix_object()
