import tensorflow as tf
import numpy as np
import cv2

model = tf.keras.applications.MobileNetV2(
    weights="imagenet",
    include_top=False,
    input_shape=(224,224,3),
    pooling="avg"
)

def preprocess_image(image):

    image = cv2.resize(image, (224,224))
    image = image / 255.0
    image = np.expand_dims(image, axis=0)

    return image


def predict_image(image):

    processed = preprocess_image(image)

    features = model.predict(processed)

    score = np.mean(features)

    if score > 0.5:
        return "Real", score
    else:
        return "Fake", score