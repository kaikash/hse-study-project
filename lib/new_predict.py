def make_prediction(filename):
    import tensorflow.keras
    from PIL import Image, ImageOps
    import numpy as np

    # Disable scientific notation for clarity
    np.set_printoptions(suppress=True)

    # Load the model
    model = tensorflow.keras.models.load_model('keras_model.h5')
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    # Replace this with the path to your image
    image = Image.open(filename)

    #resize the image to a 224x224 with the same strategy as in TM2:
    #resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.ANTIALIAS)

    #turn the image into a numpy array
    image_array = np.asarray(image)

    # display the resized image
    image.show()

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

    # Load the image into the array
    data[0] = normalized_image_array

    # run the inference
    prediction = model.predict(data)
    print("################ RESULT ################")
    print(*zip(prediction.tolist()[0], ['Circle', 'Shake', 'Square']), sep="\n")
    return [*zip(prediction.tolist()[0], ['Circle', 'Shake', 'Square'])]