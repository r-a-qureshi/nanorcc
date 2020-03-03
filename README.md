# nanorcc
## Motivation
This is a Python package for parsing NanoString RCC files into pandas dataframes. 
This package also provides methods for preprocessing and normalizing NanoString Data.
## TODO
*Create Documentation

*Write function or class to adjust data from the same platform across different code sets

*Write function or class to perform quality control checks

*Write test cases for above code
## Tutorial
```python
from nanorcc.parse import get_rcc_data
from nanorcc.preprocess import CodeClassGeneSelector, FunctionGeneSelector, Normalize
# read the data files
counts,genes = get_rcc_data('path_to_my_files/.*RCC')
# pass genes to CodeClassGeneSelector for easy gene selection during normalization.
ccgs = CodeClassGeneSelector(genes)
# initialize a Normalize object on the raw data
norm = Normalize(counts)
# steps: subtract background, adjust counts by positive controls, adjust counts by 
# housekeeping genes
# a pipeline for normalization
normalized_df = (norm
    .background_subtract(genes=ccgs.get('Negative'))
    .scale_by_genes(genes=ccgs.get('Positive'))
    .scale_by_genes(genes=ccgs.get('Housekeeping'))
).norm_data
# can also scale by taking the 100 least variable genes instead of housekeeping
norm = Normalize(counts)
fgs = FunctionGeneSelector(func='std',n=100,select_least=True)
normalized_df = (norm
    .background_subtract(genes=ccgs.get('Negative'))
    .scale_by_genes(genes=ccgs.get('Positive'))
    .scale_by_genes(genes=fgs)
).norm_data
# quantile normalization with no other preprocessing
norm = Normalize(counts)
normalized_df = (norm
    .drop_genes(genes=ccgs.get('Positive')+ccgs.get('Negative'))
    .quantile()
    .include_annot_cols()
).norm_data
# Normalize().include_annot_cols puts the annotation columns from the raw data
# back into the normalized dataframe
```