import numpy as np

def mahalanobis_sq(query, ball):
    d = np.asarray(query) - ball.center
    return float(d @ ball.precision @ d)

def retrieve_topk(query, balls, top_k=8, tau=1.0, eta=0.1, xi=0.1):
    scores = []
    for idx, ball in enumerate(balls):
        d2 = mahalanobis_sq(query, ball)
        u = ball.retrieval_dispersion()
        logit = -d2 / tau + eta * np.log1p(ball.support) - xi * u
        scores.append((idx, logit))
    scores.sort(key=lambda x: x[1], reverse=True)
    selected = scores[:min(top_k, len(scores))]
    logits = np.array([x[1] for x in selected], dtype=float)
    logits -= logits.max()
    w = np.exp(logits)
    w /= w.sum()
    ids = [x[0] for x in selected]
    return ids, w

def token_matrix(balls, ids):
    return np.stack([balls[i].descriptor() for i in ids], axis=0)
