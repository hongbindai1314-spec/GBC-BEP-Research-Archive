import numpy as np
from .granular_ball import RegressionGranularBall

class AdaptiveGranularBallEngine:
    def __init__(self, theta=0.80, n_min=20, delta=0.10,
                 lambda_reg=1e-3, n0=20, alpha=1.0, beta=1.0,
                 gamma=0.5, epsilon=1e-6):
        self.theta = theta
        self.n_min = n_min
        self.delta = delta
        self.lambda_reg = lambda_reg
        self.n0 = n0
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.epsilon = epsilon

    def build(self, S, Y):
        S = np.asarray(S, float)
        Y = np.asarray(Y, float)
        global_target_var = np.var(Y, axis=0) + self.epsilon
        root = RegressionGranularBall.from_arrays(S, Y, self.lambda_reg)

        # A fixed level reference radius is used for a deterministic split pass.
        # If the final production pipeline recomputes a level-wide median radius,
        # update this function and the manuscript definition together.
        reference_radius = root.radius

        active = [root]
        final = []
        while active:
            parent = active.pop(0)
            q_parent = parent.quality(
                global_target_var, reference_radius,
                self.alpha, self.beta, self.gamma, self.n0, self.epsilon
            )
            accepted = False
            if q_parent < self.theta and parent.support >= 2 * self.n_min:
                children = parent.split_pc1_median(self.n_min, self.lambda_reg)
                if children is not None:
                    left, right = children
                    ql = left.quality(global_target_var, reference_radius,
                                      self.alpha, self.beta, self.gamma, self.n0, self.epsilon)
                    qr = right.quality(global_target_var, reference_radius,
                                       self.alpha, self.beta, self.gamma, self.n0, self.epsilon)
                    gain = (left.support * ql + right.support * qr) / parent.support - q_parent
                    if gain >= self.delta:
                        active.extend([left, right])
                        accepted = True
            if not accepted:
                final.append(parent)
        return final
