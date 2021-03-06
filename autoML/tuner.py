import numpy as np
import data
from data import brain_raw, eyes_raw

import utils
import net
from hyperas import optim
from hyperopt import Trials, STATUS_OK, tpe

#from __future__ import print_function
import numpy as np
from hyperopt import Trials, STATUS_OK, tpe
from hyperas import optim
from hyperas.distributions import choice, uniform, conditional

import tensorflow as tf
import keras
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Convolution2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense, BatchNormalization
from keras.preprocessing.image import ImageDataGenerator

import Augmentor

### for SqueezeNet
from keras.applications.imagenet_utils import _obtain_input_shape
from keras import backend as K
from keras.layers import Input, Convolution2D, MaxPooling2D, Activation, concatenate, Dropout, warnings
from keras.layers import GlobalAveragePooling2D, GlobalMaxPooling2D
from keras.models import Model
from keras.engine.topology import get_source_inputs
from keras.utils import get_file
from keras.utils import layer_utils

import argparse
parser = argparse.ArgumentParser(description='tuner')
parser.add_argument('--net', '-n', type=str,
                    help='image net file name')
parser.add_argument('--data', '-d', type=str,
                    help='set_data file name')
parser.add_argument('--id', '-i', type=str, default=None,
                    help='')
args = parser.parse_args()


best_run, best_model = optim.minimize(
    model=eval(args.net),
    data=eval(args.data),
    algo=tpe.suggest,
    max_evals=10,
    trials=Trials())
X_train, Y_train, X_test, Y_test = eval(args.data + '()')
# print("#####################################")
print("Evalutation of best performing model:")
score = best_model.evaluate(X_test, Y_test)
print('loss:', score[0])
print('acc:', score[1])
print("Best performing model chosen hyper-parameters:")
best_model.summary()
print(best_run)

# save model weights


def random_str(n):
    import string
    import random
    return ''.join(
        [random.choice(string.ascii_letters + string.digits) for i in range(n)])


import os

idx = args.id if bool(args.id) else random_str(8)
file_name = __file__.split('.')[0]
net_name = args.net.split('.')[1]
data_name = args.data.split('.')[1]
result_dir = './models/'

model_name = 'id={}.net={}.data={}.model.h5'.format(
    args.id, net_name, data_name)
weights_name = 'id={}.net={}.data={}.weights.h5'.format(
    args.id, net_name, data_name)
best_model.save(os.path.join(result_dir, model_name))
best_model.save_weights(os.path.join(result_dir, weights_name))

print(model_name, 'saved')
print(weights_name, 'saved')
