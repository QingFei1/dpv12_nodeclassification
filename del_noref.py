
#-----------------------------这是用来提取出有引用关系的代码-----------------------

import json
from tqdm import tqdm

print("loading dpv12_venue_id_filter.json")
with open ("data/dpv12_venue_id_filter.json",'r')as fin:
    data=json.load(fin)
print("loading dpv12_venue_id_filter.json done")

#处理边，没有引用关系的去除,去除reference有，但是id没有的
id=[] 
for index,da in enumerate(data):
    id.append(da.get('id'))
print("id长度",len(id))
no_re=[]
refer1=[]  
for index, da5 in enumerate(data):
    if da5['references']==None:
        continue
    for i in da5['references']:
        refer1.append(i)
print('references的总长度',len(refer1))

refer=set()
id_set=set(id)
for data_re in tqdm(data):   
    refer_del=data_re['references']  
    if refer_del==None:
        continue 
    data_re['references']=list(set(refer_del) & id_set)
    for re in data_re['references']:
        # refer.append(re)
        refer.add(re)
    if len(data_re['references'])==0:
        data_re['references']=None
print('删除比id多的之后，references的长度',len(refer))



del_id=set()
for index,datt in enumerate(tqdm(data)):
    if datt['references']==None:
        if datt['id'] not in refer:
            # del_id.append(index)
            del_id.add(index)
print("总数量",len(data),"要删除的索引长度",len(del_id))
data_del_id=[dat1 for i,dat1 in enumerate(data) if i not in del_id]
print("最后索引关系成立的有",len(data_del_id))


with open("data/dpv12_venue_id_filter_delrefid.json",'w')as foutr:
    json.dump(data_del_id,foutr,ensure_ascii=False)


