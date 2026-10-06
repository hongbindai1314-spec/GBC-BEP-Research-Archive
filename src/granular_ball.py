from dataclasses import dataclass
import numpy as np

@dataclass
class RegressionGranularBall:
    center: np.ndarray
    covariance: np.ndarray
    precision: np.ndarray
    support: int
    target_mean: np.ndarray
    target_std: np.ndarray
    radius: float
    S: np.ndarray
    Y: np.ndarray

    @classmethod
    def from_arrays(cls, S, Y, lambda_reg=1e-3):
        S = np.asarray(S, dtype=float)
        Y = np.asarray(Y, dtype=float)
        n = len(S)
        c = S.mean(axis=0)
        mu = Y.mean(axis=0)
        sigma = Y.std(axis=0, ddof=0)
        if n > 1:
            cov = np.cov(S, rowvar=False)
            cov = np.atleast_2d(cov)
        else:
            cov = np.eye(S.shape[1], dtype=float)
        cov = cov + lambda_reg * np.eye(S.shape[1])
        precision = np.linalg.pinv(cov)
        d = S - c
        md2 = np.einsum("nd,dd,nd->n", d, precision, d)
        radius = float(np.median(np.sqrt(np.clip(md2, 0, None))))
        return cls(c, cov, precision, n, mu, sigma, radius, S, Y)

    def quality_components(self, global_target_var, reference_radius,
                           n0=20, epsilon=1e-6):
        q_state = np.exp(-self.radius / (reference_radius + epsilon))
        ratio = np.mean((self.target_std ** 2) /
                        (np.asarray(global_target_var) + epsilon))
        q_target = np.exp(-ratio)
        q_support = 1.0 - np.exp(-self.support / n0)
        return float(q_state), float(q_target), float(q_support)

    def quality(self, global_target_var, reference_radius,
                alpha=1.0, beta=1.0, gamma=0.5, n0=20, epsilon=1e-6):
        qs, qt, qn = self.quality_components(
            global_target_var, reference_radius, n0=n0, epsilon=epsilon
        )
        return (qs ** alpha) * (qt ** beta) * (qn ** gamma)

    def descriptor(self):
        return np.concatenate([
            self.center,
            np.array([np.log1p(self.support)]),
            self.target_mean,
            self.target_std,
        ])

    def retrieval_dispersion(self):
        return float(np.mean(self.target_std))

    def split_pc1_median(self, n_min=20, lambda_reg=1e-3):
        if self.support < 2 * n_min:
            return None
        X = self.S - self.center
        _, _, vt = np.linalg.svd(X, full_matrices=False)
        pc1 = vt[0]
        p = X @ pc1
        cut = np.median(p)
        left = p <= cut
        right = p > cut
        if left.sum() < n_min or right.sum() < n_min:
            return None
        return (
            RegressionGranularBall.from_arrays(self.S[left], self.Y[left], lambda_reg),
            RegressionGranularBall.from_arrays(self.S[right], self.Y[right], lambda_reg),
        )
