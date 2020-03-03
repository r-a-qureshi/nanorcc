# nanorcc
## Motivation
This is a Python package for parsing NanoString RCC files into pandas dataframes. 
This package also provides methods for preprocessing and normalizing NanoString Data.
## Tutorial
```python
from nanorcc.parse import get_rcc_data
from nanorcc.preprocess import CodeClassGeneSelector, FunctionGeneSelector, Normalize
# read the data files
exp,genes = get_rcc_data('path_to_my_files/.*RCC')
# pass genes to CodeClassGeneSelector for easy gene selection during normalization.
ccgs = CodeClassGeneSelector(genes)
# initialize a Normalize object on the raw data
norm = Normalize(exp)
# steps: subtract background, adjust counts by positive controls, adjust counts by 
# housekeeping genes
# a pipeline for normalization
normalized_df = (norm
    .background_subtract(genes=ccgs.get('Negative'))
    .scale_by_genes(genes=ccgs.get('Positive'))
    .scale_by_genes(genes=ccgs.get('Housekeeping'))
).norm_data
# can also scale by taking the 100 least variable genes instead of housekeeping
fgs = FunctionGeneSelector(func='std',n=100,select_least=True)
normalized_df = (norm
    .background_subtract(genes=ccgs.get('Negative'))
    .scale_by_genes(genes=ccgs.get('Positive'))
    .scale_by_genes(genes=fgs)
).norm_data
```