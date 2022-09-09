import os
from cogdl.data import Graph
from cogdl.datasets import NodeDataset
import torch
import numpy as np
from cogdl import experiment

class MyNodeDataset(NodeDataset):
    def __init__(self, path="data.pt"):
        self.path = path
        super(MyNodeDataset, self).__init__(path, scale_feat=False, metric="accuracy")


    def remove_self_loops(self,indices, values=None):
        row, col = indices
        mask = indices[0] != indices[1]
        row = row[mask]
        col = col[mask]
        if values is not None:
            values = values[mask]
        return (row, col), values

    def coalesce(self,row, col, value=None):
        device = row.device
        if torch.is_tensor(row):
            row = row.cpu().numpy()
        if torch.is_tensor(col):
            col = col.cpu().numpy()
        indices = np.lexsort((col, row))
        row = torch.from_numpy(row[indices]).long().to(device)
        col = torch.from_numpy(col[indices]).long().to(device)

        num = col.shape[0] + 1
        idx = torch.full((num,), -1, dtype=torch.long).to(device)
        max_num = max(row.max(), col.max()) + 100
        idx[1:] = (row + 1) * max_num + col
        mask = idx[1:] > idx[:-1]

        if mask.all():
            return row, col, value
        row = row[mask]
        if value is not None:
            _value = torch.zeros(row.shape[0], dtype=torch.float).to(device)
            value = _value.scatter_add_(dim=0, src=value, index=col)
        col = col[mask]
        return row, col, value


    def edge_index_from_dict(self,graph, num_nodes=None):
        row, col = [], []
        for item in graph:
            items=item.strip().split()
            key=[int(items[1])]
            value=[int(items[0])]
            row.append(np.array(key))
            col.append(np.array(value))
        _row = np.concatenate(row)
        _col = np.concatenate(col)
        edge_index = np.stack([_row, _col], axis=0)

        row_dom = edge_index[:, _row > _col]
        col_dom = edge_index[:, _col > _row][[1, 0]]
        edge_index = np.concatenate([row_dom, col_dom], axis=1)
        _row, _col = edge_index

        edge_index = np.stack([_row, _col], axis=0)

        order = np.lexsort((_col, _row))
        edge_index = edge_index[:, order]

        edge_index = torch.tensor(edge_index, dtype=torch.long)
        # There may be duplicated edges and self loops in the datasets.
        edge_index, _ = self.remove_self_loops(edge_index)
        row = torch.cat([edge_index[0], edge_index[1]])
        col = torch.cat([edge_index[1], edge_index[0]])

        row, col, _ = self.coalesce(row, col)
        edge_index = torch.stack([row, col])
        return edge_index 

    

    def raw_file(self,dir_path):
        names1 = ["x", "tx", "vx"]
        feature=[]
        label=[]
        for name in names1:
            path=os.path.join(dir_path,name)
            feature.append(np.load(path))
        x,tx,vx=feature
        names2 = ["y", "ty", "vy"]
        for name in names2:
            path=os.path.join(dir_path,name)
            lb=[]
            with open(path,'r')as fin:
                for i in fin:
                   lb.append(int(i.strip()))
            label.append(torch.tensor(lb))
        y,ty,vy=label
        path=os.path.join(dir_path,'graph.txt')
        with open(path,'r')as f2:
            graph=self.edge_index_from_dict(f2)
        test_length=len(tx)
        test_index = torch.arange(x.size(0), x.size(0) + test_length, dtype=torch.long)
       
        val_length=len(vx)
        train_index = torch.arange(y.size(0), dtype=torch.long)
        val_index = torch.arange(y.size(0)+ test_length , y.size(0) + test_length +val_length, dtype=torch.long)

        x = torch.cat([x, tx,vx], dim=0).float()
        y = torch.cat([y, ty,vy], dim=0).long()


        train_mask = self.index_to_mask(train_index, size=y.size(0))
        val_mask = self.index_to_mask(val_index, size=y.size(0))
        test_mask = self.index_to_mask(test_index, size=y.size(0))
        return x,y,graph,train_mask,val_mask,test_mask
    def index_to_mask(self,index, size):
        mask = torch.full((size,), False, dtype=torch.bool)
        mask[index] = True
        return mask


    def process(self):
        x,y,edge_index,train_mask,test_mask,val_mask=self.raw_file('/data') #写入文件夹路径
        data = Graph(x=x, edge_index=edge_index, y=y)
        data.train_mask = train_mask
        data.val_mask = val_mask
        data.test_mask = test_mask
        
        return data

if __name__ == "__main__":
    # Train customized dataset via defining a new class
    dataset = MyNodeDataset()
    experiment(dataset=dataset,model="graphsage",devices=[1])
