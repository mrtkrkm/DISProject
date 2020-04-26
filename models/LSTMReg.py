import torch
import torch.nn as nn

class LSTM(nn.Module):
    def __init__(self, input_size, hidden_size, num_layer, output_dim, device):
        super(LSTM, self).__init__()
        self.input_size=input_size
        self.hidden_size=hidden_size
        self.num_layer=num_layer
        self.LSTM=nn.LSTM(input_size, hidden_size, num_layer, batch_first=True)
        self.fc=nn.Linear(hidden_size, output_dim)
        self.device=device
    
    def init_hidden(self, x):
        return(torch.zeros(self.num_layer, x.size(0), self.hidden_size).to(self.device),\
            torch.zeros(self.num_layer, x.size(0), self.hidden_size).to(self.device))
    
    def forward(self,x):
        h0,c0=self.init_hidden(x)

        out,(hn,cn)=self.LSTM(x,(h0,c0))

        out=self.fc(out[:,-1,:])
        return out


