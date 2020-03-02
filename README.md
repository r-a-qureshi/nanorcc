# nanorcc
## Motivation
This is a Python package for parsing NanoString RCC files into pandas dataframes. 
This package also provides methods for preprocessing and normalizing NanoString Data.
## Tutorial
```python
from nanorcc.parse import get_rcc_data
from nanorcc.preprocess import GeneSelector, BackgroundSubtract, NormalizeUsingControls
# read the data files
exp,genes = get_rcc_data('path_to_my_files/.*RCC')
# identify the Negative Control probes
neg = GeneSelector(genes,code_class='Negative')
# Subtract the background calculated from negative control probes
norm = BackgroundSubtract(cols=neg,func='mean').eval(exp)
# Identify positive control probes
pos = GeneSelector(genes,code_class='Positive')
# Normalize against positive control probes
norm = NormalizeUsingControls(cols=pos,func='mean').eval(norm)
# Identify Housekeeping probes
hk = GeneSelector(genes,code_class='Housekeeping')
# NOrmalize against Housekeeping probes
norm = NormalizeUsingControls(cols=hk,func='mean').eval(norm)
```