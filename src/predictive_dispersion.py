import numpy as np

def predictive_dispersion(attention_weights, target_means, target_variances):
    """
    attention_weights: [K]
    target_means: [K,H]
    target_variances: [K,H]
    """
    a = np.asarray(attention_weights, float)
    mu = np.asarray(target_means, float)
    var = np.asarray(target_variances, float)
    weighted_mean = np.sum(a[:, None] * mu, axis=0)
    within = np.sum(a[:, None] * var, axis=0)
    between = np.sum(a[:, None] * (mu - weighted_mean[None, :])**2, axis=0)
    raw = within + between
    return weighted_mean, within, between, raw
