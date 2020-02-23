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


###############################################################################

#flask

# @url_family(app, ENDPOINTS.keys(), methods=['POST'])
# def run(endpoint):
#     uploaded_file = request.files['image']
#
#     threshold = None
#     if 'threshold' in request.values.keys():
#         threshold = float(request.values['threshold'])
#
#     temp_dir = tempfile.mkdtemp(dir=app.config['UPLOAD_DIR'])
#     uploaded_file.save(os.path.join(temp_dir, uploaded_file.filename))
#
#     image_full_path = os.path.join(temp_dir, uploaded_file.filename)
#     image = cv2.imread(image_full_path)
#     if image is None:
#         abort(400)
#
#     model_id = ENDPOINTS[endpoint][1]
#     function_name = ENDPOINTS[endpoint][2]
#     function = make_func(function_name)
#
#     results = function(image, MODELS[model_id], threshold)
#
#     response = make_response()
#     response.data = json.dumps(results)
#     response.headers["Content-Type"] = "application/json"
#
#     shutil.rmtree(temp_dir)
#
#     return response


##############################

