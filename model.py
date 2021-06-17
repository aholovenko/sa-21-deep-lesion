import segmentation_models_pytorch as smp
import torch
import flash

def initialize_neural_network():
    model = smp.Unet('efficientnet-b2', in_channels=1, classes=4, activation=None)
    classifier = flash.Task(model)
    checkpoint = torch.load(
        "static/model.ckpt",
        map_location=torch.device('cpu'))
    classifier.load_state_dict(checkpoint['state_dict'])
    return classifier

if __name__ == "__main__":
    classifier = initialize_neural_network()

    input_tensor = torch.rand(1, 512, 512)

    output = classifier(input_tensor)
    print(output.shape)