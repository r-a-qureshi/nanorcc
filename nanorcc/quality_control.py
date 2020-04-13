#TODO write tests
from scipy.stats import pearsonr

class QualityControl():
    def __init__(
        self,
        fov_pct=0.75,
        binding_density=(0.05,2.25),
        pos_control_linearity=0.95,
        pos_control_detection_limit=2,
    ):
        self.fov_pct = fov_pct
        self.binding_density = binding_density
        self.pos_control_linearity = pos_control_linearity
        self.pos_control_detection_limit = pos_control_detection_limit
    def fov_qc(self,raw):
        # FOV counts
        fov = raw['FovCounted']/raw['FovCount']
        raw['FOV QC'] = (fov <= self.fov_pct)
        return(raw)
    def binding_density_qc(self,raw):
        # Binding Density
        raw['Binding Density QC'] = (raw['BindingDensity'] <= self.binding_density[0])\
            | (raw['BindingDensity'] >= self.binding_density[1])
        return(raw)
    def pos_control_linearity_qc(self,raw):
        # Positive Control Linearity
        pos_cols = raw.filter(regex='POS_').columns
        pos_conc = pos_cols.str.extract('(\d+\.*\d*)').astype(float).values.reshape(-1)
        raw['Positive Control Linearity QC'] =\
            (
                raw[pos_cols].apply(lambda x: pearsonr(x,pos_conc)[0],axis=1)**2\
                <= self.pos_control_linearity
            )
        return(raw)
    def pos_control_detection_limit_qc(self,raw):
        # Positive Control Limit of Detection
        mean = raw.filter('^NEG_[A-Z]').mean(axis=1)
        std = raw.filter('^NEG_[A-Z]').std(axis=1)
        raw['Positive Control Detection Limit QC'] =\
            (raw['POS_E(0.5)']) >= (mean + (self.pos_control_detection_limit * std)) 
        return(raw)
    def flag_samples(self,raw):
        """Identify samples where QC metrics failed"""
        raw = self.fov_qc(raw)
        raw = self.binding_density_qc(raw)
        raw = self.pos_control_linearity_qc(raw)
        raw = self.pos_control_detection_limit_qc(raw)
        return(raw)
    def drop_failed_qc(self,raw,reindex=False):
        """Return a dataframe excluding samples that failed QC."""
        qc_cols = [
            "FOV QC",
            "Binding Density QC",
            "Positive Control Linearity QC",
            "Positive Control Detection Limit QC",
        ]
        raw = self.flag_samples(raw).copy()
        raw = raw.loc[~raw[qc_cols].any(axis=1)]
        raw.drop(qc_cols,axis=1,inplace=True)
        if reindex:
            raw.reset_index(drop=True,inplace=True)
        return(raw)
