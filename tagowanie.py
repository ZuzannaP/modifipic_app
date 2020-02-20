"""
pip install keras
pip insall tensorflow
https://blog.keras.io/building-a-simple-keras-deep-learning-rest-api.html
"""


#zwraca numer klasy
from keras.applications import ResNet50
#zwraca nazwę klasy zamiast numeru
from keras.applications import imagenet_utils

#wczytuje macierz do numpy x*y*3
def read_image(path):
    image = cv2.imread(path)
    if image is None:
        return None
    else:
        return image


def load_model():
    # load the pre-trained Keras model (here we are using a model
    # pre-trained on ImageNet and provided by Keras, but you can
    # substitute in your own networks just as easily)
    model = ResNet50(weights="imagenet")
    return model

# aby foto miało rozmiar zgodny z architekturą sieci neuronowej
def prepare_image(image, target=(224, 224)):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    image = cv2.resize(image, target)
    image = np.expand_dims(image, axis=0)
    image = imagenet_utils.preprocess_input(image)

    # return the processed image
    return image

model = load_model()

kurcze = '/home/zuzanna/Desktop/zdjęcia/kaczki.jpg'

kurcze_img = read_image(kurcze)

preds = model.predict(prepare_image(kurcze_img))
results = imagenet_utils.decode_predictions(preds)
print(results[0][0][1])



