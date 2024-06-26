import torch
from torch import nn


class MultiHeadSelfAttention(nn.Module):
    def __init__(
        self,
        encoder_dim=128,
        num_heads: int = 8,
        dropout: float = 0.1,
        pos_embed_max_len=1024,
    ):
        super(MultiHeadSelfAttention, self).__init__()
        self.prenorm = nn.LayerNorm(encoder_dim)
        self.multihead = nn.MultiheadAttention(encoder_dim, num_heads=num_heads)
        self.pos_embedding = RelativePositionalEmbedding(
            input_dim=encoder_dim, max_len=pos_embed_max_len
        )
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        x_forward = self.prenorm(x)
        x_forward = self.pos_embedding(x_forward)
        x_forward = self.multihead(x_forward, x_forward, x_forward)[0]
        x_forward = self.dropout(x_forward)
        return x + x_forward


class RelativePositionalEmbedding(nn.Module):
    def __init__(self, input_dim, max_len=1024):
        super().__init__()
        self.embedding = nn.Embedding(max_len, input_dim)

    def forward(self, x):
        # Generate relative positional embeddings
        _, seq_len = x.size(0), x.size(1)
        pos = torch.arange(seq_len, dtype=torch.long, device=x.device)
        pos = self.embedding(pos)
        return pos
