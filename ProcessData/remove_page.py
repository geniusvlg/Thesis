import os
import json

def main():
    data={}
    with open("./processed/merge_output.json","r") as f:
        data=json.load(f)
        read_leaf(data,1)

    with open("./processed/merge_output_fix.json",'w') as f:
        json.dump(data,f,indent=4)


def read_leaf(data,layer):
    del_list=[]
    for k,v in data.items():
        if isinstance(v,dict):
            read_leaf(v,layer+1)
        else:
            #v[:] = [item for item in v if (item['website']!="alonhadat.com.vn")]
            v[:] = [item for item in v if (item["post-time"]['date'])[-2:]!='13']
        if k.count(" ")>=4:
            del_list.append(k)
    if layer<4:
        for item in del_list:
            data.pop(k,None)

if __name__ == '__main__':
    main()