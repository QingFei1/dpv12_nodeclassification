# dpv12节点分类
```
1.data_filter是处理数据集的code,del_noref是在使用data_filter的过程中要使用的一个处理步骤，得到最终需要的文件
2.x_oag_bert是使用oag_bert处理title+abstract+author+fos.name获得的768维的特征
3.test_dpv12是使用cogdl训练的代码
```
## 测试结果
```
train集数量： 770898 ，test： 329902 ，valid： 130565 ，edge_index:[2,19544194]
使用以下三个模型训练500个epoch

<table>
    <tr>
        <th>Model</th>
        <th>test_acc</th>
        <th>val_acc</th>
    </tr>
    <tr>
        <th>graphsage</th>
        <td>0.4560±0.0000</td>
        <td>0.4020±0.0000</td>
    </tr>
    <tr>
        <th>sgc</th>
        <td>0.2918±0.0000</td>
        <td>0.2539±0.0000</td>
    </tr>
    <tr>
        <th>srgcn</th>
        <td>0.2241±0.0000</td>
        <td>0.2037±0.0000</td>
    </tr> 
</table>

```

