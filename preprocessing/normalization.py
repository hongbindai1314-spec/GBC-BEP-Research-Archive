import numpy as np

class RobustScalerTrainOnly:
    def fit(self, X):
        X = np.asarray(X, float)
        self.med_ = np.nanmedian(X, axis=0)
        q75 = np.nanpercentile(X, 75, axis=0)
        q25 = np.nanpercentile(X, 25, axis=0)
        self.iqr_ = np.where((q75-q25) > 0, q75-q25, 1.0)
        return self

    def transform(self, X):
        return (np.asarray(X, float) - self.med_) / self.iqr_
