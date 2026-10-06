import torch
import torch.nn as nn
import torch.nn.functional as F

class ScaleGate(nn.Module):
    def __init__(self, d_temporal, d_context, d_hidden=128):
        super().__init__()
        self.score = nn.Sequential(
            nn.Linear(d_temporal + d_context, d_hidden),
            nn.Tanh(),
            nn.Linear(d_hidden, 1),
        )

    def forward(self, h, contexts):
        # contexts: list of [B,d_context]
        scores = torch.cat(
            [self.score(torch.cat([h, z], dim=-1)) for z in contexts], dim=1
        )
        weights = F.softmax(scores, dim=1)
        stack = torch.stack(contexts, dim=1)
        fused = torch.sum(weights.unsqueeze(-1) * stack, dim=1)
        return fused, weights

class FusionNet(nn.Module):
    def __init__(self, d_temporal, d_context, horizon=24, dropout=0.2):
        super().__init__()
        dims = [d_temporal + d_context, 256, 128, 64, 32, horizon]
        layers = []
        for i in range(len(dims)-2):
            layers += [
                nn.Linear(dims[i], dims[i+1]),
                nn.BatchNorm1d(dims[i+1]),
                nn.ReLU(),
            ]
            if i < 2:
                layers.append(nn.Dropout(dropout))
        layers.append(nn.Linear(dims[-2], dims[-1]))
        self.net = nn.Sequential(*layers)

    def forward(self, h_temporal, fused_granular):
        return self.net(torch.cat([h_temporal, fused_granular], dim=-1))
