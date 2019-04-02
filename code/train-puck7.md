Alternative model (2) with Batch Normalization.
Switched to MSE optimization (makes better sense from a geometric
perspective).

Best MSE loss: ~0.0004 (trn)
               0.00053 (val)
Best MAE loss: 0.0163 (val)
---
Using TensorFlow backend.
Found 867 images.
Found 96 images.
WARNING:tensorflow:From /Users/lemonad/.pyenv/versions/hockey/lib/python3.7/site-packages/tensorflow/python/framework/op_def_library.py:263: colocate_with (from tensorflow.python.framework.ops) is deprecated and will be removed in a future version.
Instructions for updating:
Colocations handled automatically by placer.
_________________________________________________________________
Layer (type)                 Output Shape              Param #
=================================================================
input_1 (InputLayer)         (None, 224, 224, 1)       0
_________________________________________________________________
conv2d_1 (Conv2D)            (None, 224, 224, 24)      624
_________________________________________________________________
batch_normalization_1 (Batch (None, 224, 224, 24)      96
_________________________________________________________________
activation_1 (Activation)    (None, 224, 224, 24)      0
_________________________________________________________________
max_pooling2d_1 (MaxPooling2 (None, 112, 112, 24)      0
_________________________________________________________________
conv2d_2 (Conv2D)            (None, 108, 108, 36)      21636
_________________________________________________________________
batch_normalization_2 (Batch (None, 108, 108, 36)      144
_________________________________________________________________
activation_2 (Activation)    (None, 108, 108, 36)      0
_________________________________________________________________
max_pooling2d_2 (MaxPooling2 (None, 54, 54, 36)        0
_________________________________________________________________
conv2d_3 (Conv2D)            (None, 50, 50, 48)        43248
_________________________________________________________________
batch_normalization_3 (Batch (None, 50, 50, 48)        192
_________________________________________________________________
activation_3 (Activation)    (None, 50, 50, 48)        0
_________________________________________________________________
max_pooling2d_3 (MaxPooling2 (None, 25, 25, 48)        0
_________________________________________________________________
conv2d_4 (Conv2D)            (None, 23, 23, 64)        27712
_________________________________________________________________
batch_normalization_4 (Batch (None, 23, 23, 64)        256
_________________________________________________________________
activation_4 (Activation)    (None, 23, 23, 64)        0
_________________________________________________________________
max_pooling2d_4 (MaxPooling2 (None, 11, 11, 64)        0
_________________________________________________________________
conv2d_5 (Conv2D)            (None, 9, 9, 64)          36928
_________________________________________________________________
batch_normalization_5 (Batch (None, 9, 9, 64)          256
_________________________________________________________________
activation_5 (Activation)    (None, 9, 9, 64)          0
_________________________________________________________________
global_average_pooling2d_1 ( (None, 64)                0
_________________________________________________________________
dense_1 (Dense)              (None, 500)               32500
_________________________________________________________________
dense_2 (Dense)              (None, 90)                45090
_________________________________________________________________
dense_3 (Dense)              (None, 2)                 182
=================================================================
Total params: 208,864
Trainable params: 208,392
Non-trainable params: 472
_________________________________________________________________
28
WARNING:tensorflow:From /Users/lemonad/.pyenv/versions/hockey/lib/python3.7/site-packages/tensorflow/python/ops/math_ops.py:3066: to_int32 (from tensorflow.python.ops.math_ops) is deprecated and will be removed in a future version.
Instructions for updating:
Use tf.cast instead.
Epoch 1/200
28/28 [==============================] - 105s 4s/step - loss: 0.0300 - mean_squared_error: 0.0300 - mean_absolute_error: 0.1403 - val_loss: 0.0305 - val_mean_squared_error: 0.0305 - val_mean_absolute_error: 0.1437

Epoch 00001: val_loss improved from inf to 0.03048, saving model to puck_coords.best.h5
Epoch 2/200
28/28 [==============================] - 100s 4s/step - loss: 0.0250 - mean_squared_error: 0.0250 - mean_absolute_error: 0.1262 - val_loss: 0.0274 - val_mean_squared_error: 0.0274 - val_mean_absolute_error: 0.1331

Epoch 00002: val_loss improved from 0.03048 to 0.02737, saving model to puck_coords.best.h5
Epoch 3/200
28/28 [==============================] - 100s 4s/step - loss: 0.0159 - mean_squared_error: 0.0159 - mean_absolute_error: 0.0959 - val_loss: 0.0372 - val_mean_squared_error: 0.0372 - val_mean_absolute_error: 0.1551

Epoch 00003: val_loss did not improve from 0.02737
Epoch 4/200
28/28 [==============================] - 99s 4s/step - loss: 0.0115 - mean_squared_error: 0.0115 - mean_absolute_error: 0.0815 - val_loss: 0.0295 - val_mean_squared_error: 0.0295 - val_mean_absolute_error: 0.1294

Epoch 00004: val_loss did not improve from 0.02737
Epoch 5/200
28/28 [==============================] - 100s 4s/step - loss: 0.0099 - mean_squared_error: 0.0099 - mean_absolute_error: 0.0741 - val_loss: 0.0205 - val_mean_squared_error: 0.0205 - val_mean_absolute_error: 0.1072

Epoch 00005: val_loss improved from 0.02737 to 0.02051, saving model to puck_coords.best.h5
Epoch 6/200
28/28 [==============================] - 110s 4s/step - loss: 0.0089 - mean_squared_error: 0.0089 - mean_absolute_error: 0.0703 - val_loss: 0.0130 - val_mean_squared_error: 0.0130 - val_mean_absolute_error: 0.0868

Epoch 00006: val_loss improved from 0.02051 to 0.01299, saving model to puck_coords.best.h5
Epoch 7/200
28/28 [==============================] - 121s 4s/step - loss: 0.0072 - mean_squared_error: 0.0072 - mean_absolute_error: 0.0607 - val_loss: 0.0064 - val_mean_squared_error: 0.0064 - val_mean_absolute_error: 0.0577

Epoch 00007: val_loss improved from 0.01299 to 0.00638, saving model to puck_coords.best.h5
Epoch 8/200
28/28 [==============================] - 112s 4s/step - loss: 0.0058 - mean_squared_error: 0.0058 - mean_absolute_error: 0.0537 - val_loss: 0.0067 - val_mean_squared_error: 0.0067 - val_mean_absolute_error: 0.0600

Epoch 00008: val_loss did not improve from 0.00638
Epoch 9/200
28/28 [==============================] - 108s 4s/step - loss: 0.0040 - mean_squared_error: 0.0040 - mean_absolute_error: 0.0440 - val_loss: 0.0037 - val_mean_squared_error: 0.0037 - val_mean_absolute_error: 0.0449

Epoch 00009: val_loss improved from 0.00638 to 0.00373, saving model to puck_coords.best.h5
Epoch 10/200
28/28 [==============================] - 108s 4s/step - loss: 0.0037 - mean_squared_error: 0.0037 - mean_absolute_error: 0.0433 - val_loss: 0.0050 - val_mean_squared_error: 0.0050 - val_mean_absolute_error: 0.0537

Epoch 00010: val_loss did not improve from 0.00373
Epoch 11/200
28/28 [==============================] - 129s 5s/step - loss: 0.0041 - mean_squared_error: 0.0041 - mean_absolute_error: 0.0464 - val_loss: 0.0037 - val_mean_squared_error: 0.0037 - val_mean_absolute_error: 0.0449

Epoch 00011: val_loss did not improve from 0.00373
Epoch 12/200
28/28 [==============================] - 145s 5s/step - loss: 0.0036 - mean_squared_error: 0.0036 - mean_absolute_error: 0.0434 - val_loss: 0.0132 - val_mean_squared_error: 0.0132 - val_mean_absolute_error: 0.0979

Epoch 00012: val_loss did not improve from 0.00373
Epoch 13/200
28/28 [==============================] - 146s 5s/step - loss: 0.0033 - mean_squared_error: 0.0033 - mean_absolute_error: 0.0416 - val_loss: 0.0032 - val_mean_squared_error: 0.0032 - val_mean_absolute_error: 0.0412

Epoch 00013: val_loss improved from 0.00373 to 0.00316, saving model to puck_coords.best.h5
Epoch 14/200
28/28 [==============================] - 147s 5s/step - loss: 0.0045 - mean_squared_error: 0.0045 - mean_absolute_error: 0.0486 - val_loss: 0.0099 - val_mean_squared_error: 0.0099 - val_mean_absolute_error: 0.0675

Epoch 00014: val_loss did not improve from 0.00316
Epoch 15/200
28/28 [==============================] - 158s 6s/step - loss: 0.0035 - mean_squared_error: 0.0035 - mean_absolute_error: 0.0433 - val_loss: 0.0033 - val_mean_squared_error: 0.0033 - val_mean_absolute_error: 0.0443

Epoch 00015: val_loss did not improve from 0.00316
Epoch 16/200
28/28 [==============================] - 150s 5s/step - loss: 0.0034 - mean_squared_error: 0.0034 - mean_absolute_error: 0.0409 - val_loss: 0.0038 - val_mean_squared_error: 0.0038 - val_mean_absolute_error: 0.0490

Epoch 00016: val_loss did not improve from 0.00316
Epoch 17/200
28/28 [==============================] - 150s 5s/step - loss: 0.0031 - mean_squared_error: 0.0031 - mean_absolute_error: 0.0395 - val_loss: 0.0033 - val_mean_squared_error: 0.0033 - val_mean_absolute_error: 0.0395

Epoch 00017: val_loss did not improve from 0.00316
Epoch 18/200
28/28 [==============================] - 149s 5s/step - loss: 0.0041 - mean_squared_error: 0.0041 - mean_absolute_error: 0.0440 - val_loss: 0.0031 - val_mean_squared_error: 0.0031 - val_mean_absolute_error: 0.0423

Epoch 00018: val_loss improved from 0.00316 to 0.00307, saving model to puck_coords.best.h5
Epoch 19/200
28/28 [==============================] - 150s 5s/step - loss: 0.0047 - mean_squared_error: 0.0047 - mean_absolute_error: 0.0526 - val_loss: 0.0062 - val_mean_squared_error: 0.0062 - val_mean_absolute_error: 0.0584

Epoch 00019: val_loss did not improve from 0.00307
Epoch 20/200
28/28 [==============================] - 149s 5s/step - loss: 0.0021 - mean_squared_error: 0.0021 - mean_absolute_error: 0.0344 - val_loss: 0.0037 - val_mean_squared_error: 0.0037 - val_mean_absolute_error: 0.0422

Epoch 00020: val_loss did not improve from 0.00307
Epoch 21/200
28/28 [==============================] - 149s 5s/step - loss: 0.0015 - mean_squared_error: 0.0015 - mean_absolute_error: 0.0285 - val_loss: 0.0033 - val_mean_squared_error: 0.0033 - val_mean_absolute_error: 0.0416

Epoch 00021: val_loss did not improve from 0.00307
Epoch 22/200
28/28 [==============================] - 149s 5s/step - loss: 0.0013 - mean_squared_error: 0.0013 - mean_absolute_error: 0.0268 - val_loss: 0.0027 - val_mean_squared_error: 0.0027 - val_mean_absolute_error: 0.0362

Epoch 00022: val_loss improved from 0.00307 to 0.00265, saving model to puck_coords.best.h5
Epoch 23/200
28/28 [==============================] - 149s 5s/step - loss: 0.0014 - mean_squared_error: 0.0014 - mean_absolute_error: 0.0270 - val_loss: 0.0026 - val_mean_squared_error: 0.0026 - val_mean_absolute_error: 0.0358

Epoch 00023: val_loss improved from 0.00265 to 0.00263, saving model to puck_coords.best.h5
Epoch 24/200
28/28 [==============================] - 149s 5s/step - loss: 0.0016 - mean_squared_error: 0.0016 - mean_absolute_error: 0.0292 - val_loss: 0.0016 - val_mean_squared_error: 0.0016 - val_mean_absolute_error: 0.0270

Epoch 00024: val_loss improved from 0.00263 to 0.00163, saving model to puck_coords.best.h5
Epoch 25/200
28/28 [==============================] - 150s 5s/step - loss: 0.0015 - mean_squared_error: 0.0015 - mean_absolute_error: 0.0295 - val_loss: 0.0016 - val_mean_squared_error: 0.0016 - val_mean_absolute_error: 0.0303

Epoch 00025: val_loss improved from 0.00163 to 0.00155, saving model to puck_coords.best.h5
Epoch 26/200
28/28 [==============================] - 150s 5s/step - loss: 0.0010 - mean_squared_error: 0.0010 - mean_absolute_error: 0.0238 - val_loss: 0.0015 - val_mean_squared_error: 0.0015 - val_mean_absolute_error: 0.0250

Epoch 00026: val_loss improved from 0.00155 to 0.00152, saving model to puck_coords.best.h5
Epoch 27/200
28/28 [==============================] - 150s 5s/step - loss: 0.0012 - mean_squared_error: 0.0012 - mean_absolute_error: 0.0271 - val_loss: 0.0018 - val_mean_squared_error: 0.0018 - val_mean_absolute_error: 0.0309

Epoch 00027: val_loss did not improve from 0.00152
Epoch 28/200
28/28 [==============================] - 150s 5s/step - loss: 0.0014 - mean_squared_error: 0.0014 - mean_absolute_error: 0.0283 - val_loss: 0.0027 - val_mean_squared_error: 0.0027 - val_mean_absolute_error: 0.0405

Epoch 00028: val_loss did not improve from 0.00152
Epoch 29/200
28/28 [==============================] - 149s 5s/step - loss: 0.0013 - mean_squared_error: 0.0013 - mean_absolute_error: 0.0277 - val_loss: 0.0023 - val_mean_squared_error: 0.0023 - val_mean_absolute_error: 0.0359

Epoch 00029: val_loss did not improve from 0.00152
Epoch 30/200
28/28 [==============================] - 144s 5s/step - loss: 0.0013 - mean_squared_error: 0.0013 - mean_absolute_error: 0.0276 - val_loss: 0.0023 - val_mean_squared_error: 0.0023 - val_mean_absolute_error: 0.0333

Epoch 00030: val_loss did not improve from 0.00152
Epoch 31/200
28/28 [==============================] - 143s 5s/step - loss: 0.0014 - mean_squared_error: 0.0014 - mean_absolute_error: 0.0283 - val_loss: 0.0013 - val_mean_squared_error: 0.0013 - val_mean_absolute_error: 0.0264

Epoch 00031: val_loss improved from 0.00152 to 0.00125, saving model to puck_coords.best.h5
Epoch 32/200
28/28 [==============================] - 141s 5s/step - loss: 0.0011 - mean_squared_error: 0.0011 - mean_absolute_error: 0.0259 - val_loss: 0.0019 - val_mean_squared_error: 0.0019 - val_mean_absolute_error: 0.0340

Epoch 00032: val_loss did not improve from 0.00125
Epoch 33/200
28/28 [==============================] - 141s 5s/step - loss: 8.8927e-04 - mean_squared_error: 8.8927e-04 - mean_absolute_error: 0.0228 - val_loss: 0.0018 - val_mean_squared_error: 0.0018 - val_mean_absolute_error: 0.0317

Epoch 00033: val_loss did not improve from 0.00125
Epoch 34/200
28/28 [==============================] - 141s 5s/step - loss: 0.0014 - mean_squared_error: 0.0014 - mean_absolute_error: 0.0258 - val_loss: 0.0014 - val_mean_squared_error: 0.0014 - val_mean_absolute_error: 0.0242

Epoch 00034: val_loss did not improve from 0.00125
Epoch 35/200
28/28 [==============================] - 142s 5s/step - loss: 0.0018 - mean_squared_error: 0.0018 - mean_absolute_error: 0.0317 - val_loss: 0.0026 - val_mean_squared_error: 0.0026 - val_mean_absolute_error: 0.0328

Epoch 00035: val_loss did not improve from 0.00125
Epoch 36/200
28/28 [==============================] - 143s 5s/step - loss: 0.0022 - mean_squared_error: 0.0022 - mean_absolute_error: 0.0340 - val_loss: 0.0024 - val_mean_squared_error: 0.0024 - val_mean_absolute_error: 0.0280

Epoch 00036: val_loss did not improve from 0.00125
Epoch 37/200
28/28 [==============================] - 145s 5s/step - loss: 0.0014 - mean_squared_error: 0.0014 - mean_absolute_error: 0.0289 - val_loss: 0.0025 - val_mean_squared_error: 0.0025 - val_mean_absolute_error: 0.0329

Epoch 00037: val_loss did not improve from 0.00125
Epoch 38/200
28/28 [==============================] - 143s 5s/step - loss: 0.0011 - mean_squared_error: 0.0011 - mean_absolute_error: 0.0251 - val_loss: 0.0020 - val_mean_squared_error: 0.0020 - val_mean_absolute_error: 0.0269

Epoch 00038: val_loss did not improve from 0.00125
Epoch 39/200
28/28 [==============================] - 145s 5s/step - loss: 9.2522e-04 - mean_squared_error: 9.2522e-04 - mean_absolute_error: 0.0224 - val_loss: 0.0010 - val_mean_squared_error: 0.0010 - val_mean_absolute_error: 0.0209

Epoch 00039: val_loss improved from 0.00125 to 0.00104, saving model to puck_coords.best.h5
Epoch 40/200
28/28 [==============================] - 140s 5s/step - loss: 6.5455e-04 - mean_squared_error: 6.5455e-04 - mean_absolute_error: 0.0191 - val_loss: 0.0017 - val_mean_squared_error: 0.0017 - val_mean_absolute_error: 0.0276

Epoch 00040: val_loss did not improve from 0.00104
Epoch 41/200
28/28 [==============================] - 143s 5s/step - loss: 9.1421e-04 - mean_squared_error: 9.1421e-04 - mean_absolute_error: 0.0227 - val_loss: 0.0012 - val_mean_squared_error: 0.0012 - val_mean_absolute_error: 0.0246

Epoch 00041: val_loss did not improve from 0.00104
Epoch 42/200
28/28 [==============================] - 143s 5s/step - loss: 0.0023 - mean_squared_error: 0.0023 - mean_absolute_error: 0.0278 - val_loss: 0.0021 - val_mean_squared_error: 0.0021 - val_mean_absolute_error: 0.0324

Epoch 00042: val_loss did not improve from 0.00104
Epoch 43/200
28/28 [==============================] - 144s 5s/step - loss: 0.0040 - mean_squared_error: 0.0040 - mean_absolute_error: 0.0474 - val_loss: 0.0237 - val_mean_squared_error: 0.0237 - val_mean_absolute_error: 0.1285

Epoch 00043: val_loss did not improve from 0.00104
Epoch 44/200
28/28 [==============================] - 143s 5s/step - loss: 0.0021 - mean_squared_error: 0.0021 - mean_absolute_error: 0.0346 - val_loss: 0.0066 - val_mean_squared_error: 0.0066 - val_mean_absolute_error: 0.0645

Epoch 00044: val_loss did not improve from 0.00104
Epoch 45/200
28/28 [==============================] - 158s 6s/step - loss: 0.0019 - mean_squared_error: 0.0019 - mean_absolute_error: 0.0326 - val_loss: 0.0015 - val_mean_squared_error: 0.0015 - val_mean_absolute_error: 0.0257

Epoch 00045: val_loss did not improve from 0.00104
Epoch 46/200
28/28 [==============================] - 150s 5s/step - loss: 9.1233e-04 - mean_squared_error: 9.1233e-04 - mean_absolute_error: 0.0229 - val_loss: 0.0012 - val_mean_squared_error: 0.0012 - val_mean_absolute_error: 0.0269

Epoch 00046: val_loss did not improve from 0.00104
Epoch 47/200
28/28 [==============================] - 151s 5s/step - loss: 9.8581e-04 - mean_squared_error: 9.8581e-04 - mean_absolute_error: 0.0235 - val_loss: 0.0017 - val_mean_squared_error: 0.0017 - val_mean_absolute_error: 0.0311

Epoch 00047: val_loss did not improve from 0.00104
Epoch 48/200
28/28 [==============================] - 143s 5s/step - loss: 7.0701e-04 - mean_squared_error: 7.0701e-04 - mean_absolute_error: 0.0202 - val_loss: 8.4545e-04 - val_mean_squared_error: 8.4545e-04 - val_mean_absolute_error: 0.0210

Epoch 00048: val_loss improved from 0.00104 to 0.00085, saving model to puck_coords.best.h5
Epoch 49/200
28/28 [==============================] - 142s 5s/step - loss: 8.6836e-04 - mean_squared_error: 8.6836e-04 - mean_absolute_error: 0.0227 - val_loss: 9.6410e-04 - val_mean_squared_error: 9.6410e-04 - val_mean_absolute_error: 0.0231

Epoch 00049: val_loss did not improve from 0.00085
Epoch 50/200
28/28 [==============================] - 142s 5s/step - loss: 7.1840e-04 - mean_squared_error: 7.1840e-04 - mean_absolute_error: 0.0199 - val_loss: 0.0010 - val_mean_squared_error: 0.0010 - val_mean_absolute_error: 0.0213

Epoch 00050: val_loss did not improve from 0.00085
Epoch 51/200
28/28 [==============================] - 143s 5s/step - loss: 0.0025 - mean_squared_error: 0.0025 - mean_absolute_error: 0.0270 - val_loss: 0.0017 - val_mean_squared_error: 0.0017 - val_mean_absolute_error: 0.0265

Epoch 00051: val_loss did not improve from 0.00085
Epoch 52/200
28/28 [==============================] - 141s 5s/step - loss: 0.0074 - mean_squared_error: 0.0074 - mean_absolute_error: 0.0619 - val_loss: 0.0985 - val_mean_squared_error: 0.0985 - val_mean_absolute_error: 0.2711

Epoch 00052: val_loss did not improve from 0.00085
Epoch 53/200
28/28 [==============================] - 142s 5s/step - loss: 0.0028 - mean_squared_error: 0.0028 - mean_absolute_error: 0.0388 - val_loss: 0.0117 - val_mean_squared_error: 0.0117 - val_mean_absolute_error: 0.0757

Epoch 00053: val_loss did not improve from 0.00085
Epoch 54/200
28/28 [==============================] - 141s 5s/step - loss: 0.0027 - mean_squared_error: 0.0027 - mean_absolute_error: 0.0378 - val_loss: 0.0149 - val_mean_squared_error: 0.0149 - val_mean_absolute_error: 0.0942

Epoch 00054: val_loss did not improve from 0.00085
Epoch 55/200
28/28 [==============================] - 141s 5s/step - loss: 0.0020 - mean_squared_error: 0.0020 - mean_absolute_error: 0.0338 - val_loss: 0.0030 - val_mean_squared_error: 0.0030 - val_mean_absolute_error: 0.0409

Epoch 00055: val_loss did not improve from 0.00085
Epoch 56/200
28/28 [==============================] - 143s 5s/step - loss: 0.0013 - mean_squared_error: 0.0013 - mean_absolute_error: 0.0263 - val_loss: 0.0012 - val_mean_squared_error: 0.0012 - val_mean_absolute_error: 0.0260

Epoch 00056: val_loss did not improve from 0.00085
Epoch 57/200
28/28 [==============================] - 142s 5s/step - loss: 8.0522e-04 - mean_squared_error: 8.0522e-04 - mean_absolute_error: 0.0217 - val_loss: 8.2091e-04 - val_mean_squared_error: 8.2091e-04 - val_mean_absolute_error: 0.0204

Epoch 00057: val_loss improved from 0.00085 to 0.00082, saving model to puck_coords.best.h5
Epoch 58/200
28/28 [==============================] - 143s 5s/step - loss: 7.3050e-04 - mean_squared_error: 7.3050e-04 - mean_absolute_error: 0.0208 - val_loss: 0.0012 - val_mean_squared_error: 0.0012 - val_mean_absolute_error: 0.0264

Epoch 00058: val_loss did not improve from 0.00082

Epoch 00058: ReduceLROnPlateau reducing learning rate to 0.00010000000474974513.
Epoch 59/200
28/28 [==============================] - 144s 5s/step - loss: 7.4973e-04 - mean_squared_error: 7.4973e-04 - mean_absolute_error: 0.0211 - val_loss: 8.5483e-04 - val_mean_squared_error: 8.5483e-04 - val_mean_absolute_error: 0.0209

Epoch 00059: val_loss did not improve from 0.00082
Epoch 60/200
28/28 [==============================] - 143s 5s/step - loss: 0.0014 - mean_squared_error: 0.0014 - mean_absolute_error: 0.0211 - val_loss: 7.3788e-04 - val_mean_squared_error: 7.3788e-04 - val_mean_absolute_error: 0.0194

Epoch 00060: val_loss improved from 0.00082 to 0.00074, saving model to puck_coords.best.h5
Epoch 61/200
28/28 [==============================] - 141s 5s/step - loss: 6.1534e-04 - mean_squared_error: 6.1534e-04 - mean_absolute_error: 0.0195 - val_loss: 8.2790e-04 - val_mean_squared_error: 8.2790e-04 - val_mean_absolute_error: 0.0213

Epoch 00061: val_loss did not improve from 0.00074
Epoch 62/200
28/28 [==============================] - 143s 5s/step - loss: 7.7407e-04 - mean_squared_error: 7.7407e-04 - mean_absolute_error: 0.0207 - val_loss: 7.1298e-04 - val_mean_squared_error: 7.1298e-04 - val_mean_absolute_error: 0.0192

Epoch 00062: val_loss improved from 0.00074 to 0.00071, saving model to puck_coords.best.h5
Epoch 63/200
28/28 [==============================] - 139s 5s/step - loss: 0.0013 - mean_squared_error: 0.0013 - mean_absolute_error: 0.0232 - val_loss: 6.7483e-04 - val_mean_squared_error: 6.7483e-04 - val_mean_absolute_error: 0.0185

Epoch 00063: val_loss improved from 0.00071 to 0.00067, saving model to puck_coords.best.h5
Epoch 64/200
28/28 [==============================] - 147s 5s/step - loss: 6.7068e-04 - mean_squared_error: 6.7068e-04 - mean_absolute_error: 0.0193 - val_loss: 7.1070e-04 - val_mean_squared_error: 7.1070e-04 - val_mean_absolute_error: 0.0188

Epoch 00064: val_loss did not improve from 0.00067
Epoch 65/200
28/28 [==============================] - 148s 5s/step - loss: 0.0010 - mean_squared_error: 0.0010 - mean_absolute_error: 0.0209 - val_loss: 6.0329e-04 - val_mean_squared_error: 6.0329e-04 - val_mean_absolute_error: 0.0173

Epoch 00065: val_loss improved from 0.00067 to 0.00060, saving model to puck_coords.best.h5
Epoch 66/200
28/28 [==============================] - 160s 6s/step - loss: 5.5522e-04 - mean_squared_error: 5.5522e-04 - mean_absolute_error: 0.0177 - val_loss: 6.2897e-04 - val_mean_squared_error: 6.2897e-04 - val_mean_absolute_error: 0.0178

Epoch 00066: val_loss did not improve from 0.00060
Epoch 67/200
28/28 [==============================] - 150s 5s/step - loss: 8.6301e-04 - mean_squared_error: 8.6301e-04 - mean_absolute_error: 0.0203 - val_loss: 5.7716e-04 - val_mean_squared_error: 5.7716e-04 - val_mean_absolute_error: 0.0169

Epoch 00067: val_loss improved from 0.00060 to 0.00058, saving model to puck_coords.best.h5
Epoch 68/200
28/28 [==============================] - 152s 5s/step - loss: 6.2665e-04 - mean_squared_error: 6.2665e-04 - mean_absolute_error: 0.0188 - val_loss: 5.9253e-04 - val_mean_squared_error: 5.9253e-04 - val_mean_absolute_error: 0.0177

Epoch 00068: val_loss did not improve from 0.00058
Epoch 69/200
28/28 [==============================] - 148s 5s/step - loss: 5.8353e-04 - mean_squared_error: 5.8353e-04 - mean_absolute_error: 0.0185 - val_loss: 5.8329e-04 - val_mean_squared_error: 5.8329e-04 - val_mean_absolute_error: 0.0174

Epoch 00069: val_loss did not improve from 0.00058
Epoch 70/200
28/28 [==============================] - 144s 5s/step - loss: 0.0012 - mean_squared_error: 0.0012 - mean_absolute_error: 0.0218 - val_loss: 5.7445e-04 - val_mean_squared_error: 5.7445e-04 - val_mean_absolute_error: 0.0172

Epoch 00070: val_loss improved from 0.00058 to 0.00057, saving model to puck_coords.best.h5
Epoch 71/200
28/28 [==============================] - 143s 5s/step - loss: 6.4689e-04 - mean_squared_error: 6.4689e-04 - mean_absolute_error: 0.0197 - val_loss: 6.3295e-04 - val_mean_squared_error: 6.3295e-04 - val_mean_absolute_error: 0.0181

Epoch 00071: val_loss did not improve from 0.00057
Epoch 72/200
28/28 [==============================] - 144s 5s/step - loss: 4.3602e-04 - mean_squared_error: 4.3602e-04 - mean_absolute_error: 0.0160 - val_loss: 5.9483e-04 - val_mean_squared_error: 5.9483e-04 - val_mean_absolute_error: 0.0176

Epoch 00072: val_loss did not improve from 0.00057
Epoch 73/200
28/28 [==============================] - 143s 5s/step - loss: 6.2793e-04 - mean_squared_error: 6.2793e-04 - mean_absolute_error: 0.0191 - val_loss: 5.7255e-04 - val_mean_squared_error: 5.7255e-04 - val_mean_absolute_error: 0.0173

Epoch 00073: val_loss improved from 0.00057 to 0.00057, saving model to puck_coords.best.h5
Epoch 74/200
28/28 [==============================] - 144s 5s/step - loss: 5.7493e-04 - mean_squared_error: 5.7493e-04 - mean_absolute_error: 0.0187 - val_loss: 5.7205e-04 - val_mean_squared_error: 5.7205e-04 - val_mean_absolute_error: 0.0173

Epoch 00074: val_loss improved from 0.00057 to 0.00057, saving model to puck_coords.best.h5
Epoch 75/200
28/28 [==============================] - 143s 5s/step - loss: 5.4687e-04 - mean_squared_error: 5.4687e-04 - mean_absolute_error: 0.0182 - val_loss: 5.5729e-04 - val_mean_squared_error: 5.5729e-04 - val_mean_absolute_error: 0.0169

Epoch 00075: val_loss improved from 0.00057 to 0.00056, saving model to puck_coords.best.h5

Epoch 00075: ReduceLROnPlateau reducing learning rate to 1.0000000474974514e-05.
Epoch 76/200
28/28 [==============================] - 140s 5s/step - loss: 5.4184e-04 - mean_squared_error: 5.4184e-04 - mean_absolute_error: 0.0173 - val_loss: 5.4987e-04 - val_mean_squared_error: 5.4987e-04 - val_mean_absolute_error: 0.0167

Epoch 00076: val_loss improved from 0.00056 to 0.00055, saving model to puck_coords.best.h5
Epoch 77/200
28/28 [==============================] - 142s 5s/step - loss: 7.4286e-04 - mean_squared_error: 7.4286e-04 - mean_absolute_error: 0.0179 - val_loss: 5.3474e-04 - val_mean_squared_error: 5.3474e-04 - val_mean_absolute_error: 0.0166

Epoch 00077: val_loss improved from 0.00055 to 0.00053, saving model to puck_coords.best.h5
Epoch 78/200
28/28 [==============================] - 143s 5s/step - loss: 4.5270e-04 - mean_squared_error: 4.5270e-04 - mean_absolute_error: 0.0167 - val_loss: 5.2970e-04 - val_mean_squared_error: 5.2970e-04 - val_mean_absolute_error: 0.0166

Epoch 00078: val_loss improved from 0.00053 to 0.00053, saving model to puck_coords.best.h5
Epoch 79/200
28/28 [==============================] - 144s 5s/step - loss: 4.7522e-04 - mean_squared_error: 4.7522e-04 - mean_absolute_error: 0.0169 - val_loss: 5.3162e-04 - val_mean_squared_error: 5.3162e-04 - val_mean_absolute_error: 0.0166

Epoch 00079: val_loss did not improve from 0.00053
Epoch 80/200
28/28 [==============================] - 146s 5s/step - loss: 5.5948e-04 - mean_squared_error: 5.5948e-04 - mean_absolute_error: 0.0177 - val_loss: 5.3183e-04 - val_mean_squared_error: 5.3183e-04 - val_mean_absolute_error: 0.0165

Epoch 00080: val_loss did not improve from 0.00053
Epoch 81/200
28/28 [==============================] - 144s 5s/step - loss: 7.7035e-04 - mean_squared_error: 7.7035e-04 - mean_absolute_error: 0.0205 - val_loss: 5.2690e-04 - val_mean_squared_error: 5.2690e-04 - val_mean_absolute_error: 0.0165

Epoch 00081: val_loss improved from 0.00053 to 0.00053, saving model to puck_coords.best.h5
Epoch 82/200
28/28 [==============================] - 143s 5s/step - loss: 5.4684e-04 - mean_squared_error: 5.4684e-04 - mean_absolute_error: 0.0175 - val_loss: 5.2756e-04 - val_mean_squared_error: 5.2756e-04 - val_mean_absolute_error: 0.0164

Epoch 00082: val_loss did not improve from 0.00053
Epoch 83/200
28/28 [==============================] - 144s 5s/step - loss: 4.8853e-04 - mean_squared_error: 4.8853e-04 - mean_absolute_error: 0.0173 - val_loss: 5.3385e-04 - val_mean_squared_error: 5.3385e-04 - val_mean_absolute_error: 0.0165

Epoch 00083: val_loss did not improve from 0.00053
Epoch 84/200
28/28 [==============================] - 146s 5s/step - loss: 7.8453e-04 - mean_squared_error: 7.8453e-04 - mean_absolute_error: 0.0194 - val_loss: 5.3297e-04 - val_mean_squared_error: 5.3297e-04 - val_mean_absolute_error: 0.0165

Epoch 00084: val_loss did not improve from 0.00053
Epoch 85/200
28/28 [==============================] - 144s 5s/step - loss: 5.5894e-04 - mean_squared_error: 5.5894e-04 - mean_absolute_error: 0.0176 - val_loss: 5.3501e-04 - val_mean_squared_error: 5.3501e-04 - val_mean_absolute_error: 0.0164

Epoch 00085: val_loss did not improve from 0.00053
Epoch 86/200
28/28 [==============================] - 143s 5s/step - loss: 0.0024 - mean_squared_error: 0.0024 - mean_absolute_error: 0.0217 - val_loss: 5.3353e-04 - val_mean_squared_error: 5.3353e-04 - val_mean_absolute_error: 0.0164

Epoch 00086: val_loss did not improve from 0.00053
Epoch 87/200
28/28 [==============================] - 145s 5s/step - loss: 6.4077e-04 - mean_squared_error: 6.4077e-04 - mean_absolute_error: 0.0182 - val_loss: 5.4798e-04 - val_mean_squared_error: 5.4798e-04 - val_mean_absolute_error: 0.0167

Epoch 00087: val_loss did not improve from 0.00053
Epoch 88/200
28/28 [==============================] - 150s 5s/step - loss: 6.8575e-04 - mean_squared_error: 6.8575e-04 - mean_absolute_error: 0.0197 - val_loss: 5.4542e-04 - val_mean_squared_error: 5.4542e-04 - val_mean_absolute_error: 0.0166

Epoch 00088: val_loss did not improve from 0.00053
Epoch 89/200
28/28 [==============================] - 146s 5s/step - loss: 4.5388e-04 - mean_squared_error: 4.5388e-04 - mean_absolute_error: 0.0163 - val_loss: 5.5017e-04 - val_mean_squared_error: 5.5017e-04 - val_mean_absolute_error: 0.0166

Epoch 00089: val_loss did not improve from 0.00053

Epoch 00089: ReduceLROnPlateau reducing learning rate to 1.0000000656873453e-06.
Epoch 90/200
28/28 [==============================] - 158s 6s/step - loss: 7.2485e-04 - mean_squared_error: 7.2485e-04 - mean_absolute_error: 0.0191 - val_loss: 5.5303e-04 - val_mean_squared_error: 5.5303e-04 - val_mean_absolute_error: 0.0166

Epoch 00090: val_loss did not improve from 0.00053
Epoch 91/200
28/28 [==============================] - 151s 5s/step - loss: 5.2070e-04 - mean_squared_error: 5.2070e-04 - mean_absolute_error: 0.0173 - val_loss: 5.5646e-04 - val_mean_squared_error: 5.5646e-04 - val_mean_absolute_error: 0.0166

Epoch 00091: val_loss did not improve from 0.00053
Epoch 92/200
28/28 [==============================] - 149s 5s/step - loss: 4.8742e-04 - mean_squared_error: 4.8742e-04 - mean_absolute_error: 0.0164 - val_loss: 5.5870e-04 - val_mean_squared_error: 5.5870e-04 - val_mean_absolute_error: 0.0166

Epoch 00092: val_loss did not improve from 0.00053
Epoch 93/200
28/28 [==============================] - 150s 5s/step - loss: 4.4182e-04 - mean_squared_error: 4.4182e-04 - mean_absolute_error: 0.0158 - val_loss: 5.6158e-04 - val_mean_squared_error: 5.6158e-04 - val_mean_absolute_error: 0.0167

Epoch 00093: val_loss did not improve from 0.00053
Epoch 94/200
28/28 [==============================] - 149s 5s/step - loss: 5.7460e-04 - mean_squared_error: 5.7460e-04 - mean_absolute_error: 0.0180 - val_loss: 5.6973e-04 - val_mean_squared_error: 5.6973e-04 - val_mean_absolute_error: 0.0168

Epoch 00094: val_loss did not improve from 0.00053
Epoch 95/200
28/28 [==============================] - 145s 5s/step - loss: 5.8302e-04 - mean_squared_error: 5.8302e-04 - mean_absolute_error: 0.0177 - val_loss: 5.7373e-04 - val_mean_squared_error: 5.7373e-04 - val_mean_absolute_error: 0.0168

Epoch 00095: val_loss did not improve from 0.00053
Epoch 96/200
28/28 [==============================] - 144s 5s/step - loss: 4.9137e-04 - mean_squared_error: 4.9137e-04 - mean_absolute_error: 0.0171 - val_loss: 5.7149e-04 - val_mean_squared_error: 5.7149e-04 - val_mean_absolute_error: 0.0168

Epoch 00096: val_loss did not improve from 0.00053
Epoch 97/200
28/28 [==============================] - 146s 5s/step - loss: 8.0738e-04 - mean_squared_error: 8.0738e-04 - mean_absolute_error: 0.0194 - val_loss: 5.6379e-04 - val_mean_squared_error: 5.6379e-04 - val_mean_absolute_error: 0.0167

Epoch 00097: val_loss did not improve from 0.00053
Epoch 98/200
28/28 [==============================] - 146s 5s/step - loss: 4.7638e-04 - mean_squared_error: 4.7638e-04 - mean_absolute_error: 0.0162 - val_loss: 5.6264e-04 - val_mean_squared_error: 5.6264e-04 - val_mean_absolute_error: 0.0167

Epoch 00098: val_loss did not improve from 0.00053
Epoch 99/200
28/28 [==============================] - 145s 5s/step - loss: 4.6195e-04 - mean_squared_error: 4.6195e-04 - mean_absolute_error: 0.0167 - val_loss: 5.6625e-04 - val_mean_squared_error: 5.6625e-04 - val_mean_absolute_error: 0.0167

Epoch 00099: val_loss did not improve from 0.00053
Epoch 100/200
28/28 [==============================] - 147s 5s/step - loss: 5.8203e-04 - mean_squared_error: 5.8203e-04 - mean_absolute_error: 0.0177 - val_loss: 5.6521e-04 - val_mean_squared_error: 5.6521e-04 - val_mean_absolute_error: 0.0167

Epoch 00100: val_loss did not improve from 0.00053
Epoch 101/200
28/28 [==============================] - 149s 5s/step - loss: 9.1623e-04 - mean_squared_error: 9.1623e-04 - mean_absolute_error: 0.0195 - val_loss: 5.5842e-04 - val_mean_squared_error: 5.5842e-04 - val_mean_absolute_error: 0.0166

Epoch 00101: val_loss did not improve from 0.00053
Epoch 102/200
28/28 [==============================] - 148s 5s/step - loss: 5.5524e-04 - mean_squared_error: 5.5524e-04 - mean_absolute_error: 0.0178 - val_loss: 5.6173e-04 - val_mean_squared_error: 5.6173e-04 - val_mean_absolute_error: 0.0167

Epoch 00102: val_loss did not improve from 0.00053
Epoch 103/200
28/28 [==============================] - 149s 5s/step - loss: 4.7360e-04 - mean_squared_error: 4.7360e-04 - mean_absolute_error: 0.0166 - val_loss: 5.5827e-04 - val_mean_squared_error: 5.5827e-04 - val_mean_absolute_error: 0.0166

Epoch 00103: val_loss did not improve from 0.00053

Epoch 00103: ReduceLROnPlateau reducing learning rate to 1e-06.
Epoch 104/200
28/28 [==============================] - 150s 5s/step - loss: 5.0426e-04 - mean_squared_error: 5.0426e-04 - mean_absolute_error: 0.0176 - val_loss: 5.6116e-04 - val_mean_squared_error: 5.6116e-04 - val_mean_absolute_error: 0.0167

Epoch 00104: val_loss did not improve from 0.00053
Epoch 105/200
28/28 [==============================] - 150s 5s/step - loss: 3.8419e-04 - mean_squared_error: 3.8419e-04 - mean_absolute_error: 0.0154 - val_loss: 5.6159e-04 - val_mean_squared_error: 5.6159e-04 - val_mean_absolute_error: 0.0167

Epoch 00105: val_loss did not improve from 0.00053
Epoch 106/200
28/28 [==============================] - 149s 5s/step - loss: 6.6259e-04 - mean_squared_error: 6.6259e-04 - mean_absolute_error: 0.0190 - val_loss: 5.6486e-04 - val_mean_squared_error: 5.6486e-04 - val_mean_absolute_error: 0.0167

Epoch 00106: val_loss did not improve from 0.00053
Epoch 107/200
28/28 [==============================] - 149s 5s/step - loss: 5.2636e-04 - mean_squared_error: 5.2636e-04 - mean_absolute_error: 0.0172 - val_loss: 5.6814e-04 - val_mean_squared_error: 5.6814e-04 - val_mean_absolute_error: 0.0168

Epoch 00107: val_loss did not improve from 0.00053
Epoch 108/200
28/28 [==============================] - 149s 5s/step - loss: 4.5094e-04 - mean_squared_error: 4.5094e-04 - mean_absolute_error: 0.0165 - val_loss: 5.6471e-04 - val_mean_squared_error: 5.6471e-04 - val_mean_absolute_error: 0.0167

Epoch 00108: val_loss did not improve from 0.00053
Epoch 109/200
28/28 [==============================] - 149s 5s/step - loss: 5.2765e-04 - mean_squared_error: 5.2765e-04 - mean_absolute_error: 0.0177 - val_loss: 5.6285e-04 - val_mean_squared_error: 5.6285e-04 - val_mean_absolute_error: 0.0167

Epoch 00109: val_loss did not improve from 0.00053
Epoch 110/200
28/28 [==============================] - 147s 5s/step - loss: 6.0950e-04 - mean_squared_error: 6.0950e-04 - mean_absolute_error: 0.0184 - val_loss: 5.5555e-04 - val_mean_squared_error: 5.5555e-04 - val_mean_absolute_error: 0.0166

Epoch 00110: val_loss did not improve from 0.00053
Epoch 111/200
28/28 [==============================] - 149s 5s/step - loss: 4.1267e-04 - mean_squared_error: 4.1267e-04 - mean_absolute_error: 0.0156 - val_loss: 5.5643e-04 - val_mean_squared_error: 5.5643e-04 - val_mean_absolute_error: 0.0166

Epoch 00111: val_loss did not improve from 0.00053
Epoch 112/200
28/28 [==============================] - 149s 5s/step - loss: 4.5507e-04 - mean_squared_error: 4.5507e-04 - mean_absolute_error: 0.0168 - val_loss: 5.6009e-04 - val_mean_squared_error: 5.6009e-04 - val_mean_absolute_error: 0.0167

Epoch 00112: val_loss did not improve from 0.00053
Epoch 113/200
28/28 [==============================] - 146s 5s/step - loss: 5.4252e-04 - mean_squared_error: 5.4252e-04 - mean_absolute_error: 0.0180 - val_loss: 5.6148e-04 - val_mean_squared_error: 5.6148e-04 - val_mean_absolute_error: 0.0167

Epoch 00113: val_loss did not improve from 0.00053
Epoch 114/200
28/28 [==============================] - 160s 6s/step - loss: 5.9263e-04 - mean_squared_error: 5.9263e-04 - mean_absolute_error: 0.0174 - val_loss: 5.6872e-04 - val_mean_squared_error: 5.6872e-04 - val_mean_absolute_error: 0.0168

Epoch 00114: val_loss did not improve from 0.00053
Epoch 115/200
28/28 [==============================] - 150s 5s/step - loss: 4.8581e-04 - mean_squared_error: 4.8581e-04 - mean_absolute_error: 0.0175 - val_loss: 5.6367e-04 - val_mean_squared_error: 5.6367e-04 - val_mean_absolute_error: 0.0167

Epoch 00115: val_loss did not improve from 0.00053
Epoch 116/200
28/28 [==============================] - 151s 5s/step - loss: 4.6295e-04 - mean_squared_error: 4.6295e-04 - mean_absolute_error: 0.0164 - val_loss: 5.6174e-04 - val_mean_squared_error: 5.6174e-04 - val_mean_absolute_error: 0.0167

Epoch 00116: val_loss did not improve from 0.00053
Epoch 117/200
28/28 [==============================] - 149s 5s/step - loss: 5.6501e-04 - mean_squared_error: 5.6501e-04 - mean_absolute_error: 0.0179 - val_loss: 5.5632e-04 - val_mean_squared_error: 5.5632e-04 - val_mean_absolute_error: 0.0166

Epoch 00117: val_loss did not improve from 0.00053
Epoch 118/200
28/28 [==============================] - 146s 5s/step - loss: 8.8855e-04 - mean_squared_error: 8.8855e-04 - mean_absolute_error: 0.0201 - val_loss: 5.5922e-04 - val_mean_squared_error: 5.5922e-04 - val_mean_absolute_error: 0.0167

Epoch 00118: val_loss did not improve from 0.00053
Epoch 119/200
28/28 [==============================] - 147s 5s/step - loss: 5.1667e-04 - mean_squared_error: 5.1667e-04 - mean_absolute_error: 0.0174 - val_loss: 5.5742e-04 - val_mean_squared_error: 5.5742e-04 - val_mean_absolute_error: 0.0166

Epoch 00119: val_loss did not improve from 0.00053
Epoch 120/200
28/28 [==============================] - 145s 5s/step - loss: 5.1137e-04 - mean_squared_error: 5.1137e-04 - mean_absolute_error: 0.0175 - val_loss: 5.6013e-04 - val_mean_squared_error: 5.6013e-04 - val_mean_absolute_error: 0.0167

Epoch 00120: val_loss did not improve from 0.00053
Epoch 121/200
28/28 [==============================] - 146s 5s/step - loss: 4.7056e-04 - mean_squared_error: 4.7056e-04 - mean_absolute_error: 0.0168 - val_loss: 5.5711e-04 - val_mean_squared_error: 5.5711e-04 - val_mean_absolute_error: 0.0166

Epoch 00121: val_loss did not improve from 0.00053
Epoch 122/200
28/28 [==============================] - 144s 5s/step - loss: 5.7153e-04 - mean_squared_error: 5.7153e-04 - mean_absolute_error: 0.0179 - val_loss: 5.5311e-04 - val_mean_squared_error: 5.5311e-04 - val_mean_absolute_error: 0.0166

Epoch 00122: val_loss did not improve from 0.00053
Epoch 123/200
28/28 [==============================] - 145s 5s/step - loss: 5.4951e-04 - mean_squared_error: 5.4951e-04 - mean_absolute_error: 0.0175 - val_loss: 5.5005e-04 - val_mean_squared_error: 5.5005e-04 - val_mean_absolute_error: 0.0166

Epoch 00123: val_loss did not improve from 0.00053
Epoch 124/200
28/28 [==============================] - 146s 5s/step - loss: 7.5973e-04 - mean_squared_error: 7.5973e-04 - mean_absolute_error: 0.0193 - val_loss: 5.5409e-04 - val_mean_squared_error: 5.5409e-04 - val_mean_absolute_error: 0.0166

Epoch 00124: val_loss did not improve from 0.00053
Epoch 125/200
28/28 [==============================] - 145s 5s/step - loss: 4.5549e-04 - mean_squared_error: 4.5549e-04 - mean_absolute_error: 0.0164 - val_loss: 5.5225e-04 - val_mean_squared_error: 5.5225e-04 - val_mean_absolute_error: 0.0166

Epoch 00125: val_loss did not improve from 0.00053
Epoch 126/200
28/28 [==============================] - 145s 5s/step - loss: 4.2322e-04 - mean_squared_error: 4.2322e-04 - mean_absolute_error: 0.0158 - val_loss: 5.5439e-04 - val_mean_squared_error: 5.5439e-04 - val_mean_absolute_error: 0.0166

Epoch 00126: val_loss did not improve from 0.00053
Epoch 127/200
28/28 [==============================] - 145s 5s/step - loss: 4.9523e-04 - mean_squared_error: 4.9523e-04 - mean_absolute_error: 0.0174 - val_loss: 5.5679e-04 - val_mean_squared_error: 5.5679e-04 - val_mean_absolute_error: 0.0167

Epoch 00127: val_loss did not improve from 0.00053
Epoch 128/200
28/28 [==============================] - 146s 5s/step - loss: 5.6271e-04 - mean_squared_error: 5.6271e-04 - mean_absolute_error: 0.0176 - val_loss: 5.5345e-04 - val_mean_squared_error: 5.5345e-04 - val_mean_absolute_error: 0.0166

Epoch 00128: val_loss did not improve from 0.00053
Epoch 129/200
28/28 [==============================] - 146s 5s/step - loss: 3.9061e-04 - mean_squared_error: 3.9061e-04 - mean_absolute_error: 0.0154 - val_loss: 5.5253e-04 - val_mean_squared_error: 5.5253e-04 - val_mean_absolute_error: 0.0166

Epoch 00129: val_loss did not improve from 0.00053
Epoch 130/200
28/28 [==============================] - 146s 5s/step - loss: 4.1978e-04 - mean_squared_error: 4.1978e-04 - mean_absolute_error: 0.0158 - val_loss: 5.5152e-04 - val_mean_squared_error: 5.5152e-04 - val_mean_absolute_error: 0.0166

Epoch 00130: val_loss did not improve from 0.00053
Epoch 131/200
28/28 [==============================] - 146s 5s/step - loss: 6.1702e-04 - mean_squared_error: 6.1702e-04 - mean_absolute_error: 0.0171 - val_loss: 5.4752e-04 - val_mean_squared_error: 5.4752e-04 - val_mean_absolute_error: 0.0165

Epoch 00131: val_loss did not improve from 0.00053
Epoch 132/200
28/28 [==============================] - 146s 5s/step - loss: 6.8618e-04 - mean_squared_error: 6.8618e-04 - mean_absolute_error: 0.0187 - val_loss: 5.5269e-04 - val_mean_squared_error: 5.5269e-04 - val_mean_absolute_error: 0.0166

Epoch 00132: val_loss did not improve from 0.00053
Epoch 133/200
28/28 [==============================] - 145s 5s/step - loss: 4.9043e-04 - mean_squared_error: 4.9043e-04 - mean_absolute_error: 0.0173 - val_loss: 5.5253e-04 - val_mean_squared_error: 5.5253e-04 - val_mean_absolute_error: 0.0166

Epoch 00133: val_loss did not improve from 0.00053
Epoch 134/200
28/28 [==============================] - 144s 5s/step - loss: 5.4026e-04 - mean_squared_error: 5.4026e-04 - mean_absolute_error: 0.0181 - val_loss: 5.5091e-04 - val_mean_squared_error: 5.5091e-04 - val_mean_absolute_error: 0.0166

Epoch 00134: val_loss did not improve from 0.00053
Epoch 135/200
28/28 [==============================] - 146s 5s/step - loss: 4.4092e-04 - mean_squared_error: 4.4092e-04 - mean_absolute_error: 0.0159 - val_loss: 5.5366e-04 - val_mean_squared_error: 5.5366e-04 - val_mean_absolute_error: 0.0166

Epoch 00135: val_loss did not improve from 0.00053
Epoch 136/200
28/28 [==============================] - 145s 5s/step - loss: 4.6221e-04 - mean_squared_error: 4.6221e-04 - mean_absolute_error: 0.0163 - val_loss: 5.5188e-04 - val_mean_squared_error: 5.5188e-04 - val_mean_absolute_error: 0.0166

Epoch 00136: val_loss did not improve from 0.00053
Epoch 137/200
28/28 [==============================] - 145s 5s/step - loss: 5.0745e-04 - mean_squared_error: 5.0745e-04 - mean_absolute_error: 0.0175 - val_loss: 5.5151e-04 - val_mean_squared_error: 5.5151e-04 - val_mean_absolute_error: 0.0166

Epoch 00137: val_loss did not improve from 0.00053
Epoch 138/200
28/28 [==============================] - 146s 5s/step - loss: 5.0679e-04 - mean_squared_error: 5.0679e-04 - mean_absolute_error: 0.0173 - val_loss: 5.5431e-04 - val_mean_squared_error: 5.5431e-04 - val_mean_absolute_error: 0.0166

Epoch 00138: val_loss did not improve from 0.00053
Epoch 139/200
28/28 [==============================] - 148s 5s/step - loss: 5.2365e-04 - mean_squared_error: 5.2365e-04 - mean_absolute_error: 0.0168 - val_loss: 5.5804e-04 - val_mean_squared_error: 5.5804e-04 - val_mean_absolute_error: 0.0166

Epoch 00139: val_loss did not improve from 0.00053
Epoch 140/200
28/28 [==============================] - 148s 5s/step - loss: 5.1329e-04 - mean_squared_error: 5.1329e-04 - mean_absolute_error: 0.0173 - val_loss: 5.5627e-04 - val_mean_squared_error: 5.5627e-04 - val_mean_absolute_error: 0.0166

Epoch 00140: val_loss did not improve from 0.00053
Epoch 141/200
28/28 [==============================] - 160s 6s/step - loss: 5.3296e-04 - mean_squared_error: 5.3296e-04 - mean_absolute_error: 0.0162 - val_loss: 5.5851e-04 - val_mean_squared_error: 5.5851e-04 - val_mean_absolute_error: 0.0167

Epoch 00141: val_loss did not improve from 0.00053
Epoch 142/200
28/28 [==============================] - 148s 5s/step - loss: 5.2329e-04 - mean_squared_error: 5.2329e-04 - mean_absolute_error: 0.0173 - val_loss: 5.5897e-04 - val_mean_squared_error: 5.5897e-04 - val_mean_absolute_error: 0.0167

Epoch 00142: val_loss did not improve from 0.00053
Epoch 143/200
28/28 [==============================] - 147s 5s/step - loss: 5.4251e-04 - mean_squared_error: 5.4251e-04 - mean_absolute_error: 0.0166 - val_loss: 5.6200e-04 - val_mean_squared_error: 5.6200e-04 - val_mean_absolute_error: 0.0167

Epoch 00143: val_loss did not improve from 0.00053
Epoch 144/200
28/28 [==============================] - 148s 5s/step - loss: 6.2826e-04 - mean_squared_error: 6.2826e-04 - mean_absolute_error: 0.0178 - val_loss: 5.6099e-04 - val_mean_squared_error: 5.6099e-04 - val_mean_absolute_error: 0.0167

Epoch 00144: val_loss did not improve from 0.00053
Epoch 145/200
28/28 [==============================] - 142s 5s/step - loss: 4.1708e-04 - mean_squared_error: 4.1708e-04 - mean_absolute_error: 0.0157 - val_loss: 5.5820e-04 - val_mean_squared_error: 5.5820e-04 - val_mean_absolute_error: 0.0167

Epoch 00145: val_loss did not improve from 0.00053
Epoch 146/200
28/28 [==============================] - 141s 5s/step - loss: 4.8177e-04 - mean_squared_error: 4.8177e-04 - mean_absolute_error: 0.0167 - val_loss: 5.5479e-04 - val_mean_squared_error: 5.5479e-04 - val_mean_absolute_error: 0.0166

Epoch 00146: val_loss did not improve from 0.00053
Epoch 147/200
28/28 [==============================] - 143s 5s/step - loss: 4.2840e-04 - mean_squared_error: 4.2840e-04 - mean_absolute_error: 0.0160 - val_loss: 5.5145e-04 - val_mean_squared_error: 5.5145e-04 - val_mean_absolute_error: 0.0166

Epoch 00147: val_loss did not improve from 0.00053
Epoch 148/200
28/28 [==============================] - 142s 5s/step - loss: 5.1334e-04 - mean_squared_error: 5.1334e-04 - mean_absolute_error: 0.0173 - val_loss: 5.4991e-04 - val_mean_squared_error: 5.4991e-04 - val_mean_absolute_error: 0.0166

Epoch 00148: val_loss did not improve from 0.00053
Epoch 149/200
28/28 [==============================] - 142s 5s/step - loss: 6.8344e-04 - mean_squared_error: 6.8344e-04 - mean_absolute_error: 0.0190 - val_loss: 5.4732e-04 - val_mean_squared_error: 5.4732e-04 - val_mean_absolute_error: 0.0165

Epoch 00149: val_loss did not improve from 0.00053
Epoch 150/200
28/28 [==============================] - 142s 5s/step - loss: 6.2101e-04 - mean_squared_error: 6.2101e-04 - mean_absolute_error: 0.0193 - val_loss: 5.5029e-04 - val_mean_squared_error: 5.5029e-04 - val_mean_absolute_error: 0.0166

Epoch 00150: val_loss did not improve from 0.00053
Epoch 151/200
28/28 [==============================] - 142s 5s/step - loss: 6.6281e-04 - mean_squared_error: 6.6281e-04 - mean_absolute_error: 0.0188 - val_loss: 5.5218e-04 - val_mean_squared_error: 5.5218e-04 - val_mean_absolute_error: 0.0166

Epoch 00151: val_loss did not improve from 0.00053
Epoch 152/200
28/28 [==============================] - 143s 5s/step - loss: 5.8516e-04 - mean_squared_error: 5.8516e-04 - mean_absolute_error: 0.0183 - val_loss: 5.5206e-04 - val_mean_squared_error: 5.5206e-04 - val_mean_absolute_error: 0.0165

Epoch 00152: val_loss did not improve from 0.00053
Epoch 153/200
28/28 [==============================] - 143s 5s/step - loss: 8.7683e-04 - mean_squared_error: 8.7683e-04 - mean_absolute_error: 0.0207 - val_loss: 5.5143e-04 - val_mean_squared_error: 5.5143e-04 - val_mean_absolute_error: 0.0166

Epoch 00153: val_loss did not improve from 0.00053
Epoch 154/200
28/28 [==============================] - 142s 5s/step - loss: 5.1459e-04 - mean_squared_error: 5.1459e-04 - mean_absolute_error: 0.0170 - val_loss: 5.4789e-04 - val_mean_squared_error: 5.4789e-04 - val_mean_absolute_error: 0.0165

Epoch 00154: val_loss did not improve from 0.00053
Epoch 155/200
28/28 [==============================] - 141s 5s/step - loss: 4.8250e-04 - mean_squared_error: 4.8250e-04 - mean_absolute_error: 0.0171 - val_loss: 5.4820e-04 - val_mean_squared_error: 5.4820e-04 - val_mean_absolute_error: 0.0165

Epoch 00155: val_loss did not improve from 0.00053
Epoch 156/200
28/28 [==============================] - 143s 5s/step - loss: 4.6244e-04 - mean_squared_error: 4.6244e-04 - mean_absolute_error: 0.0169 - val_loss: 5.4776e-04 - val_mean_squared_error: 5.4776e-04 - val_mean_absolute_error: 0.0165

Epoch 00156: val_loss did not improve from 0.00053
Epoch 157/200
28/28 [==============================] - 142s 5s/step - loss: 7.2002e-04 - mean_squared_error: 7.2002e-04 - mean_absolute_error: 0.0197 - val_loss: 5.4310e-04 - val_mean_squared_error: 5.4310e-04 - val_mean_absolute_error: 0.0165

Epoch 00157: val_loss did not improve from 0.00053
Epoch 158/200
28/28 [==============================] - 142s 5s/step - loss: 6.2076e-04 - mean_squared_error: 6.2076e-04 - mean_absolute_error: 0.0174 - val_loss: 5.4776e-04 - val_mean_squared_error: 5.4776e-04 - val_mean_absolute_error: 0.0165

Epoch 00158: val_loss did not improve from 0.00053
Epoch 159/200
28/28 [==============================] - 142s 5s/step - loss: 5.7243e-04 - mean_squared_error: 5.7243e-04 - mean_absolute_error: 0.0182 - val_loss: 5.4557e-04 - val_mean_squared_error: 5.4557e-04 - val_mean_absolute_error: 0.0165

Epoch 00159: val_loss did not improve from 0.00053
Epoch 160/200
28/28 [==============================] - 142s 5s/step - loss: 7.2237e-04 - mean_squared_error: 7.2237e-04 - mean_absolute_error: 0.0185 - val_loss: 5.4879e-04 - val_mean_squared_error: 5.4879e-04 - val_mean_absolute_error: 0.0165

Epoch 00160: val_loss did not improve from 0.00053
Epoch 161/200
28/28 [==============================] - 144s 5s/step - loss: 3.5433e-04 - mean_squared_error: 3.5433e-04 - mean_absolute_error: 0.0146 - val_loss: 5.4640e-04 - val_mean_squared_error: 5.4640e-04 - val_mean_absolute_error: 0.0165

Epoch 00161: val_loss did not improve from 0.00053
Epoch 162/200
28/28 [==============================] - 143s 5s/step - loss: 5.0189e-04 - mean_squared_error: 5.0189e-04 - mean_absolute_error: 0.0174 - val_loss: 5.4432e-04 - val_mean_squared_error: 5.4432e-04 - val_mean_absolute_error: 0.0165

Epoch 00162: val_loss did not improve from 0.00053
Epoch 163/200
28/28 [==============================] - 143s 5s/step - loss: 9.2716e-04 - mean_squared_error: 9.2716e-04 - mean_absolute_error: 0.0196 - val_loss: 5.5019e-04 - val_mean_squared_error: 5.5019e-04 - val_mean_absolute_error: 0.0165

Epoch 00163: val_loss did not improve from 0.00053
Epoch 164/200
28/28 [==============================] - 143s 5s/step - loss: 4.5178e-04 - mean_squared_error: 4.5178e-04 - mean_absolute_error: 0.0161 - val_loss: 5.4967e-04 - val_mean_squared_error: 5.4967e-04 - val_mean_absolute_error: 0.0165

Epoch 00164: val_loss did not improve from 0.00053
Epoch 165/200
28/28 [==============================] - 145s 5s/step - loss: 4.0812e-04 - mean_squared_error: 4.0812e-04 - mean_absolute_error: 0.0156 - val_loss: 5.4931e-04 - val_mean_squared_error: 5.4931e-04 - val_mean_absolute_error: 0.0165

Epoch 00165: val_loss did not improve from 0.00053
Epoch 166/200
28/28 [==============================] - 158s 6s/step - loss: 5.7121e-04 - mean_squared_error: 5.7121e-04 - mean_absolute_error: 0.0176 - val_loss: 5.4051e-04 - val_mean_squared_error: 5.4051e-04 - val_mean_absolute_error: 0.0164

Epoch 00166: val_loss did not improve from 0.00053
Epoch 167/200
28/28 [==============================] - 149s 5s/step - loss: 4.4360e-04 - mean_squared_error: 4.4360e-04 - mean_absolute_error: 0.0162 - val_loss: 5.3773e-04 - val_mean_squared_error: 5.3773e-04 - val_mean_absolute_error: 0.0164

Epoch 00167: val_loss did not improve from 0.00053
Epoch 168/200
28/28 [==============================] - 148s 5s/step - loss: 4.4717e-04 - mean_squared_error: 4.4717e-04 - mean_absolute_error: 0.0164 - val_loss: 5.3710e-04 - val_mean_squared_error: 5.3710e-04 - val_mean_absolute_error: 0.0164

Epoch 00168: val_loss did not improve from 0.00053
Epoch 169/200
28/28 [==============================] - 143s 5s/step - loss: 4.7637e-04 - mean_squared_error: 4.7637e-04 - mean_absolute_error: 0.0167 - val_loss: 5.3880e-04 - val_mean_squared_error: 5.3880e-04 - val_mean_absolute_error: 0.0164

Epoch 00169: val_loss did not improve from 0.00053
Epoch 170/200
28/28 [==============================] - 144s 5s/step - loss: 5.3280e-04 - mean_squared_error: 5.3280e-04 - mean_absolute_error: 0.0177 - val_loss: 5.4101e-04 - val_mean_squared_error: 5.4101e-04 - val_mean_absolute_error: 0.0165

Epoch 00170: val_loss did not improve from 0.00053
Epoch 171/200
28/28 [==============================] - 144s 5s/step - loss: 5.3745e-04 - mean_squared_error: 5.3745e-04 - mean_absolute_error: 0.0178 - val_loss: 5.3846e-04 - val_mean_squared_error: 5.3846e-04 - val_mean_absolute_error: 0.0164

Epoch 00171: val_loss did not improve from 0.00053
Epoch 172/200
28/28 [==============================] - 145s 5s/step - loss: 5.8433e-04 - mean_squared_error: 5.8433e-04 - mean_absolute_error: 0.0175 - val_loss: 5.3550e-04 - val_mean_squared_error: 5.3550e-04 - val_mean_absolute_error: 0.0164

Epoch 00172: val_loss did not improve from 0.00053
Epoch 173/200
28/28 [==============================] - 145s 5s/step - loss: 5.3651e-04 - mean_squared_error: 5.3651e-04 - mean_absolute_error: 0.0174 - val_loss: 5.3410e-04 - val_mean_squared_error: 5.3410e-04 - val_mean_absolute_error: 0.0163

Epoch 00173: val_loss did not improve from 0.00053
Epoch 174/200
28/28 [==============================] - 143s 5s/step - loss: 5.2264e-04 - mean_squared_error: 5.2264e-04 - mean_absolute_error: 0.0174 - val_loss: 5.3551e-04 - val_mean_squared_error: 5.3551e-04 - val_mean_absolute_error: 0.0164

Epoch 00174: val_loss did not improve from 0.00053
Epoch 175/200
28/28 [==============================] - 142s 5s/step - loss: 6.7463e-04 - mean_squared_error: 6.7463e-04 - mean_absolute_error: 0.0179 - val_loss: 5.4132e-04 - val_mean_squared_error: 5.4132e-04 - val_mean_absolute_error: 0.0165

Epoch 00175: val_loss did not improve from 0.00053
Epoch 176/200
28/28 [==============================] - 142s 5s/step - loss: 5.5298e-04 - mean_squared_error: 5.5298e-04 - mean_absolute_error: 0.0169 - val_loss: 5.4157e-04 - val_mean_squared_error: 5.4157e-04 - val_mean_absolute_error: 0.0164

Epoch 00176: val_loss did not improve from 0.00053
Epoch 177/200
28/28 [==============================] - 144s 5s/step - loss: 4.8471e-04 - mean_squared_error: 4.8471e-04 - mean_absolute_error: 0.0165 - val_loss: 5.4307e-04 - val_mean_squared_error: 5.4307e-04 - val_mean_absolute_error: 0.0165

Epoch 00177: val_loss did not improve from 0.00053
Epoch 178/200
28/28 [==============================] - 141s 5s/step - loss: 4.9971e-04 - mean_squared_error: 4.9971e-04 - mean_absolute_error: 0.0169 - val_loss: 5.4038e-04 - val_mean_squared_error: 5.4038e-04 - val_mean_absolute_error: 0.0164

Epoch 00178: val_loss did not improve from 0.00053
Epoch 179/200
28/28 [==============================] - 143s 5s/step - loss: 5.3979e-04 - mean_squared_error: 5.3979e-04 - mean_absolute_error: 0.0171 - val_loss: 5.4083e-04 - val_mean_squared_error: 5.4083e-04 - val_mean_absolute_error: 0.0164

Epoch 00179: val_loss did not improve from 0.00053
Epoch 180/200
28/28 [==============================] - 143s 5s/step - loss: 5.1639e-04 - mean_squared_error: 5.1639e-04 - mean_absolute_error: 0.0175 - val_loss: 5.3625e-04 - val_mean_squared_error: 5.3625e-04 - val_mean_absolute_error: 0.0164

Epoch 00180: val_loss did not improve from 0.00053
Epoch 181/200
28/28 [==============================] - 144s 5s/step - loss: 4.5886e-04 - mean_squared_error: 4.5886e-04 - mean_absolute_error: 0.0164 - val_loss: 5.3789e-04 - val_mean_squared_error: 5.3789e-04 - val_mean_absolute_error: 0.0164

Epoch 00181: val_loss did not improve from 0.00053
Epoch 182/200
28/28 [==============================] - 144s 5s/step - loss: 6.0086e-04 - mean_squared_error: 6.0086e-04 - mean_absolute_error: 0.0177 - val_loss: 5.4184e-04 - val_mean_squared_error: 5.4184e-04 - val_mean_absolute_error: 0.0165

Epoch 00182: val_loss did not improve from 0.00053
Epoch 183/200
28/28 [==============================] - 144s 5s/step - loss: 5.4301e-04 - mean_squared_error: 5.4301e-04 - mean_absolute_error: 0.0177 - val_loss: 5.3563e-04 - val_mean_squared_error: 5.3563e-04 - val_mean_absolute_error: 0.0164

Epoch 00183: val_loss did not improve from 0.00053
Epoch 184/200
28/28 [==============================] - 142s 5s/step - loss: 4.5571e-04 - mean_squared_error: 4.5571e-04 - mean_absolute_error: 0.0166 - val_loss: 5.3472e-04 - val_mean_squared_error: 5.3472e-04 - val_mean_absolute_error: 0.0164

Epoch 00184: val_loss did not improve from 0.00053
Epoch 185/200
28/28 [==============================] - 142s 5s/step - loss: 4.7234e-04 - mean_squared_error: 4.7234e-04 - mean_absolute_error: 0.0162 - val_loss: 5.3525e-04 - val_mean_squared_error: 5.3525e-04 - val_mean_absolute_error: 0.0164

Epoch 00185: val_loss did not improve from 0.00053
Epoch 186/200
28/28 [==============================] - 144s 5s/step - loss: 4.7385e-04 - mean_squared_error: 4.7385e-04 - mean_absolute_error: 0.0166 - val_loss: 5.3560e-04 - val_mean_squared_error: 5.3560e-04 - val_mean_absolute_error: 0.0164

Epoch 00186: val_loss did not improve from 0.00053
Epoch 187/200
28/28 [==============================] - 142s 5s/step - loss: 5.1105e-04 - mean_squared_error: 5.1105e-04 - mean_absolute_error: 0.0176 - val_loss: 5.3805e-04 - val_mean_squared_error: 5.3805e-04 - val_mean_absolute_error: 0.0164

Epoch 00187: val_loss did not improve from 0.00053
Epoch 188/200
28/28 [==============================] - 143s 5s/step - loss: 4.7568e-04 - mean_squared_error: 4.7568e-04 - mean_absolute_error: 0.0166 - val_loss: 5.3911e-04 - val_mean_squared_error: 5.3911e-04 - val_mean_absolute_error: 0.0164

Epoch 00188: val_loss did not improve from 0.00053
Epoch 189/200
28/28 [==============================] - 145s 5s/step - loss: 5.8620e-04 - mean_squared_error: 5.8620e-04 - mean_absolute_error: 0.0176 - val_loss: 5.3574e-04 - val_mean_squared_error: 5.3574e-04 - val_mean_absolute_error: 0.0164

Epoch 00189: val_loss did not improve from 0.00053
Epoch 190/200
28/28 [==============================] - 145s 5s/step - loss: 6.0382e-04 - mean_squared_error: 6.0382e-04 - mean_absolute_error: 0.0177 - val_loss: 5.3202e-04 - val_mean_squared_error: 5.3202e-04 - val_mean_absolute_error: 0.0163

Epoch 00190: val_loss did not improve from 0.00053
Epoch 191/200
28/28 [==============================] - 156s 6s/step - loss: 5.0577e-04 - mean_squared_error: 5.0577e-04 - mean_absolute_error: 0.0173 - val_loss: 5.3452e-04 - val_mean_squared_error: 5.3452e-04 - val_mean_absolute_error: 0.0163

Epoch 00191: val_loss did not improve from 0.00053
Epoch 192/200
28/28 [==============================] - 151s 5s/step - loss: 4.6718e-04 - mean_squared_error: 4.6718e-04 - mean_absolute_error: 0.0166 - val_loss: 5.3578e-04 - val_mean_squared_error: 5.3578e-04 - val_mean_absolute_error: 0.0164

Epoch 00192: val_loss did not improve from 0.00053
Epoch 193/200
28/28 [==============================] - 150s 5s/step - loss: 6.1060e-04 - mean_squared_error: 6.1060e-04 - mean_absolute_error: 0.0177 - val_loss: 5.3917e-04 - val_mean_squared_error: 5.3917e-04 - val_mean_absolute_error: 0.0164

Epoch 00193: val_loss did not improve from 0.00053
Epoch 194/200
28/28 [==============================] - 150s 5s/step - loss: 4.8654e-04 - mean_squared_error: 4.8654e-04 - mean_absolute_error: 0.0171 - val_loss: 5.3737e-04 - val_mean_squared_error: 5.3737e-04 - val_mean_absolute_error: 0.0164

Epoch 00194: val_loss did not improve from 0.00053
Epoch 195/200
28/28 [==============================] - 149s 5s/step - loss: 4.2323e-04 - mean_squared_error: 4.2323e-04 - mean_absolute_error: 0.0158 - val_loss: 5.3726e-04 - val_mean_squared_error: 5.3726e-04 - val_mean_absolute_error: 0.0164

Epoch 00195: val_loss did not improve from 0.00053
Epoch 196/200
28/28 [==============================] - 145s 5s/step - loss: 5.1632e-04 - mean_squared_error: 5.1632e-04 - mean_absolute_error: 0.0174 - val_loss: 5.4005e-04 - val_mean_squared_error: 5.4005e-04 - val_mean_absolute_error: 0.0164

Epoch 00196: val_loss did not improve from 0.00053
Epoch 197/200
28/28 [==============================] - 96s 3s/step - loss: 5.9729e-04 - mean_squared_error: 5.9729e-04 - mean_absolute_error: 0.0188 - val_loss: 5.3874e-04 - val_mean_squared_error: 5.3874e-04 - val_mean_absolute_error: 0.0164

Epoch 00197: val_loss did not improve from 0.00053
Epoch 198/200
28/28 [==============================] - 96s 3s/step - loss: 8.3407e-04 - mean_squared_error: 8.3407e-04 - mean_absolute_error: 0.0188 - val_loss: 5.4407e-04 - val_mean_squared_error: 5.4407e-04 - val_mean_absolute_error: 0.0165

Epoch 00198: val_loss did not improve from 0.00053
Epoch 199/200
28/28 [==============================] - 96s 3s/step - loss: 6.9889e-04 - mean_squared_error: 6.9889e-04 - mean_absolute_error: 0.0196 - val_loss: 5.3659e-04 - val_mean_squared_error: 5.3659e-04 - val_mean_absolute_error: 0.0164

Epoch 00199: val_loss did not improve from 0.00053
Epoch 200/200
28/28 [==============================] - 96s 3s/step - loss: 4.6080e-04 - mean_squared_error: 4.6080e-04 - mean_absolute_error: 0.0165 - val_loss: 5.3533e-04 - val_mean_squared_error: 5.3533e-04 - val_mean_absolute_error: 0.0164

Epoch 00200: val_loss did not improve from 0.00053
