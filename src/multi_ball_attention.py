import math
import torch
import torch.nn as nn
import torch.nn.functional as F

class MultiBallQueryAttention(nn.Module):
    def __init__(self, d_temporal, d_granule, d_attn=128, prior_weight=1.0):
        super().__init__()
        self.q = nn.Linear(d_temporal, d_attn)
        self.k = nn.Linear(d_granule, d_attn)
        self.v = nn.Linear(d_granule, d_attn)
        self.prior_weight = prior_weight

    def forward(self, h_temporal, granule_tokens, retrieval_weights):
        """
        h_temporal: [B, d_temporal]
        granule_tokens: [B, K, d_granule]
        retrieval_weights: [B, K], strictly positive / normalized
        """
        q = self.q(h_temporal).unsqueeze(1)         # [B,1,d]
        k = self.k(granule_tokens)                 # [B,K,d]
        v = self.v(granule_tokens)                 # [B,K,d]
        logits = torch.sum(q * k, dim=-1) / math.sqrt(k.shape[-1])
        logits = logits + self.prior_weight * torch.log(
            retrieval_weights.clamp_min(1e-8)
        )
        alpha = F.softmax(logits, dim=-1)
        z = torch.sum(alpha.unsqueeze(-1) * v, dim=1)
        return z, alpha
