import torch
import torch.nn as nn
import torch.nn.functional as F

from model.model import TwoLayerNet
from utils.dataset import GTADataSet


def main():
    batch_size = 64

    # Construct our model by instantiating the class defined above
    model = TwoLayerNet()
    # model = model.cuda()

    # Construct our loss function and an Optimizer. The call to model.parameters()
    # in the SGD constructor will contain the learnable parameters of the two
    # nn.Linear modules which are members of the model.
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)

    trainloader = torch.utils.data.DataLoader(GTADataSet(), batch_size=batch_size,
                                            shuffle=True, num_workers=2)


    for epoch in range(200):  # loop over the dataset multiple times

        running_loss = 0.0
        for i, data in enumerate(trainloader, 0):
            # get the inputs; data is a list of [inputs, labels]
            inputs, labels = data

            # zero the parameter gradients
            optimizer.zero_grad()

            # forward + backward + optimize
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            # print statistics
            running_loss += loss.item()
            # if i % 10 == 9:    # print every 2000 mini-batches
        print('[%d, %5d] loss: %.3f' %
            (epoch + 1, 200, running_loss / 10))
        running_loss = 0.0
        with torch.no_grad():
            _, pred = torch.max(outputs, 1)
            pred = pred.t()
            correct = pred.eq(labels)
        print(correct.float().sum(0).mul_(100.0 / labels.size(0)))

    print('Finished Training')
    torch.save(model.state_dict(), "saved_model")


if __name__ == '__main__':
    main()
