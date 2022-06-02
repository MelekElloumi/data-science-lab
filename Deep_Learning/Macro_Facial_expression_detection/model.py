from tensorflow.python.keras.backend import set_session
from tensorflow.keras.models import model_from_json
import numpy as np
import tensorflow as tf

config=tf.compat.v1.ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction = 0.15
session = tf.compat.v1.Session(config=config)
set_session(session)

class FacialExpressionModel(object):
    #EMOTIONS_LIST =["Happy","Surprise","Fear", "Neutral","Sad", "Angry"]
    EMOTIONS_LIST = ["Angry", "Fear", "Happy","Neutral", "Sad", "Surprise"]
    def __init__(self,model_json_file, model_weights_file):
        with open(model_json_file,"r") as json_file:
            loaded_model_json = json_file.read()
            self.loaded_model = model_from_json(loaded_model_json)
        self.loaded_model.load_weights(model_weights_file)
        #self.loaded_model.predict_classes()
        #predict_x = self.loaded_model.predict(X_test)

    def predict_emotion(self,img):
        global session
        set_session(session)
        self.preds = self.loaded_model.predict(img)
        return FacialExpressionModel.EMOTIONS_LIST[np.argmax(self.preds)]
