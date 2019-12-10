def get_prediction():
    import os
    import tensorflow as tf
    from keras.preprocessing import image
    import numpy as np
    import keras
    import pandas as pd
    # from app.routes import model

    from keras.models import load_model

    model = load_model('backend/weight.checkpoint4.cont.h5')
    graph = tf.get_default_graph()
    print('Load_Model Completed')
    # model._make_predict_function()
    print('Loading images...')
    path = 'app/static/user_input/input_mfccs/'
    img_width = 200
    img_height = 200
    images = []
    for img in os.listdir(path):
        if img != '.DS_Store':
            img = os.path.join(path, img)
            img = image.load_img(img, target_size=(img_width, img_height))
            img = image.img_to_array(img)
            img = np.expand_dims(img, axis=0)
            images.append(img)

    images = np.vstack(images)
    classes = ['A','A#','A#m','Am','B','Bm','C','C#','C#m','Cm','D','D#',"D#m",'Dm','E','Em','F','F#','F#m','Fm','G','G#','G#m','Gm']

    string_output = ''
    output=pd.DataFrame(columns=['chords'])
    idx = 0

    print('making predictions...')

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
            string_output = string_output + '.'
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
    return output