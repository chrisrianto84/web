def get_prediction():
    import os
    import tensorflow as tf
    from keras.preprocessing import image
    import numpy as np
    import keras
    import pandas as pd
    # from app.routes import model

    from keras.models import load_model

    string_output = ''
    output=pd.DataFrame(columns=['chords'])

    # model._make_predict_function()
    print('Loading images...')
    path = 'app/static/user_input/input_mfccs/'
    img_width = 200
    img_height = 200
    images = []
    image_name = []

    for img in os.listdir(path):
        if img != '.DS_Store':
            image_name.append(int(os.path.splitext(img)[0]))

    image_name.sort()

    for img in image_name:
        img = os.path.join(path, str(img))+'.png'
        img = image.load_img(img, target_size=(img_width, img_height))
        img = image.img_to_array(img)
        img = np.expand_dims(img, axis=0)
        images.append(img)

    if len(os.listdir(path)) < 16:
        print('Error Audio Length.' + ' Audio Beat is too small')
        return output, '500'

    images = np.vstack(images)
    classes = ['A','A#','A#m','Am','B','Bm','C','C#','C#m','Cm','D','D#',"D#m",'Dm','E','Em','F','F#','F#m','Fm','G','G#','G#m','Gm']

    idx = 0

    print('making predictions...')

    model = load_model('backend/model2.h5')
    graph = tf.get_default_graph()
    print('Load_Model Completed')

    with graph.as_default():
        prediction = model.predict_classes(images, batch_size=10)
    
    bars = 0
    token = 0
    count = 0

    for i in prediction:
        print(classes[i])
        if bars == 4:
            output.loc[idx]=string_output
            string_output = '|'
            idx = idx+1
            bars = 0
        if token == 0:
            string_output = '|'+string_output+classes[i]+'.'
            token = token+1
            count = count + 1
        elif count == 1:
            string_output = string_output
            count = count+1
        elif count == 3:            
            string_output = string_output+'|'
            bars = bars+1
            count = 0
        else:
            string_output = string_output+classes[i]+'.'
            count = count + 1
        
    # string_output = string_output.replace('\\n','<br />')

    print(output)
    keras.backend.clear_session()
    return output, ""