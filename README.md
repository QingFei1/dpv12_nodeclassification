#dpv12节点分类
```
1.data_filter是处理数据集的code,del_noref是在使用data_filter的过程中要使用的一个处理步骤，得到最终需要的文件
2.x_oag_bert是使用oag_bert处理title+abstract+author+fos.name获得的768维的特征
3.test_dpv12是使用cogdl训练的代码
```
##测试结果
```
训练500个epoch
1.graphsage
| Variant                 | test_acc      | val_acc       |
|-------------------------|---------------|---------------|
| (data1.pt, 'graphsage') | 0.4560±0.0000 | 0.4020±0.0000 |
2.sgc
| Variant           | test_acc      | val_acc       |
|-------------------|---------------|---------------|
| (data1.pt, 'sgc') | 0.2918±0.0000 | 0.2539±0.0000 |
3.srgcn
| Variant             | test_acc      | val_acc       |
|---------------------|---------------|---------------|
| (data1.pt, 'srgcn') | 0.2241±0.0000 | 0.2037±0.0000 |
```

