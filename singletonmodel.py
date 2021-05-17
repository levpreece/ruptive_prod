import tensorflow as tf

class SingletonModel():
    _instance = None

    def __new__(self, model_URL="/home/USE_MODEL"):
        if not self._instance:
            self._instance = super(SingletonModel, self).__new__(self)
            self.model = tf.saved_model.load(model_URL)
        return self.model
         