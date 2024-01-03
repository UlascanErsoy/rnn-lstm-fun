class RNN(nn.Module):

    def __init__(self, input_size:int,
                        hidden_size:int,
                        output_size:int,
                        hidden_layers: int = 1):
        """Initialize an RNN
        for training purposes
        """
        super(RNN,self).__init__()

        self.hidden_size = hidden_size
        self._hid_lay_size = hidden_layers
        self.hidden_layers = [(
            nn.Linear(input_size + hidden_size, 
                      hidden_size).to(device),
            nn.Tanh().to(device),
            nn.Dropout(0.5).to(device)
        )]
        
        for _ in range(hidden_layers):
            self.hidden_layers.append((
            nn.Linear(hidden_size*2, 
                       hidden_size).to(device),
            nn.Tanh().to(device),
            nn.Dropout(0.5).to(device)
            ))
        
        self.h2o = nn.Linear(hidden_size, output_size)
        self.softmax = nn.LogSoftmax(dim=1)

    def forward(self, input, hidden):
        
        combined = torch.cat((input,hidden[0:1]), 1)
        hidden1 = self.hidden_layers[0][0](combined)
        hidden[0] = self.hidden_layers[0][2](self.hidden_layers[0][1](hidden1))

        for idx, (linear, tan, drop) in enumerate(self.hidden_layers[1:]): 
            combined = torch.cat((hidden[idx:idx+1],hidden[idx+1:idx+2]),1)
            hid = linear(combined)
            hidden[idx+1] = drop(tan(hid))

        output = self.h2o(hidden[idx+1:idx+2])
        output = self.softmax(output)

        return output, hidden 

    def init_hidden(self):
        return torch.zeros((self._hid_lay_size + 1), self.hidden_size).to(device)