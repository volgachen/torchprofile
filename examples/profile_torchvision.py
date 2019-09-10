import torch
from torchvision import models

from torchprofile import profile_macs

if __name__ == '__main__':
    for name, model in models.__dict__.items():
        if not name.islower() or name.startswith('__') or not callable(model):
            continue

        model = model().eval()
        if 'inception' not in name:
            inputs = torch.randn(1, 3, 224, 224)
        else:
            inputs = torch.randn(1, 3, 299, 299)

        total_macs = profile_macs(model, (inputs,))
        print('{}: {:.4g} G'.format(name, total_macs / 1e9))
