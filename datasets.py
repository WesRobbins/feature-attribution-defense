from settings import current_settings
if not current_settings.local:
    print('Dataset Imports')
    import torchvision
    import torchvision.transforms as transforms
    from torch.utils.data import DataLoader
    import torchvision.datasets as datasets
    from settings import current_settings


    if torch.cuda.is_available():
      device = torch.device('cuda:0')
      print('GPU')
    else:
      device = torch.device('cpu')
      print('cpu')

    transform = transforms.Compose(
        [transforms.ToTensor(),
         transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])


data = {}

batch_size = 64
if 'cifar' in current_settings.datasets:
    data['cifar_trs'] = datasets.CIFAR10(root='./data/cifar', train=True, download=True, transform=transform)
    data['cifar_trl'] = DataLoader(cifar_trs, batch_size=64,shuffle=True, num_workers=2)
    data['cifar_ts'] = datasets.CIFAR10(root='./data/cifar', train=False, download=True, transform=transform)
    data['cifar_tl'] = DataLoader(cifar_ts, batch_size=64, shuffle=False, num_workers=2)
    cifar_classes = ('plane', 'car', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck')

if 'mnist' in current_settings.datasets:
    data['mnist_trs'] = datasets.MNIST(root='./data/mnist', train=True, transform=transforms.ToTensor(), download=True)
    data['mnist_trl'] = DataLoader(dataset=mnist_trs, batch_size=batch_size, shuffle=True) # shuffle = true shuffles every epoch so new bacthes are made
    data['mnist_ts'] = datasets.MNIST(root='./data/mnist', train=False, transform=transforms.ToTensor(), download=True)
    data['mnist_tl'] = DataLoader(dataset=mnist_ts, batch_size=batch_size, shuffle=True)
