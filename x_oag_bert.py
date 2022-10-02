from cogdl.oag import oagbert
import torch
import json
import numpy as np
from tqdm import tqdm 


#分别将dpv12_train.json和test,valid运行一次，得到特征
#加载模型，注意，这里选择使用oagbert-v2版本
tokenizer, model = oagbert("oagbert-v2")
model.cuda()

roles = ["train", "valid", "test"]
# with open("data/dpv12_test.json",'r')as fin:
for role in roles:
    embedding=[]
    with open("data/dpv12_{}.json".format(role),'r')as fin:
        data=json.load(fin)
        
        for item in tqdm(data):
            #start=time.time()
            title=item['title']
            abstract=item['abstract']
            authors=[]
            concepts=[]
            author=item['authors']
            fos_name=item['fos']
            for i in author:
                authors.append(i.get('name'))
            if fos_name==None:
                concepts=[]
            else:
                for i in fos_name:
                    concepts.append(i.get('name'))

            input_ids, input_masks, token_type_ids, masked_lm_labels, position_ids, position_ids_second, masked_positions, num_spans = model.build_inputs(title=title, abstract=abstract, authors=authors, concepts=concepts)
            # 使用模型进行前向传播
            sequence_output, pooled_output = model.bert.forward(
                input_ids=torch.LongTensor(input_ids).unsqueeze(0).cuda(),
                token_type_ids=torch.LongTensor(token_type_ids).unsqueeze(0).cuda(),
                attention_mask=torch.LongTensor(input_masks).unsqueeze(0).cuda(),
                output_all_encoded_layers=False,
                checkpoint_activations=False,
                position_ids=torch.LongTensor(position_ids).unsqueeze(0).cuda(),
                position_ids_second=torch.LongTensor(position_ids).unsqueeze(0).cuda()
            )
            pooled_output=torch.squeeze(pooled_output)
            embedding.append(pooled_output.cpu().detach().numpy())
    em=np.array(embedding)
    # np.save('data/tx.npy',em)
    np.save('data/tx_{}.npy'.format(role),em)
