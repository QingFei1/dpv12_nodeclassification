# DBLP paper classification

## Prerequisites

- Linux
- Python 3.9
- PyTorch 1.10.0+cu111

## Getting Started

### Installation

Clone this repo.

```bash
git clone https://github.com/QingFei1/dpv12_nodeclassification.git
cd dpv12_nodeclassification
```

Please install dependencies by

```bash
pip install -r requirements.txt
```

### Dataset
The DBLP paper dataset can be downloaded from [AMiner](https://originalstatic.aminer.cn/misc/dblp.v12.7z) and the venue-to-label data can be downloaded from [Baidu Pan](https://pan.baidu.com/s/11Nz3OmyPj0eRlKC93Sp_oA) (with password ihj6).
Put downloaded files into the _data_ directory of the project directory and unzip DBLP papers.

## How to run
Processing: run cell by cell in data_filter.ipynb
```bash
python x_oag_bert.py  # generate node embeddings
python test_dpv12.py  # uncomment the corresponding lines to run sgc, sign, and graphsage.
```
