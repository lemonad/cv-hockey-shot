Alternative model (2)
Switched to MAE optimization (makes sense from a geometric perspective?) but should plot both MSE and MAE for comparison.

Best MAE loss: 0.0060 (trn)
               0.0110 (val)
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
batch_normalization_1 (Batch (None, 224, 224, 1)       4
_________________________________________________________________
conv2d_1 (Conv2D)            (None, 224, 224, 24)      624
_________________________________________________________________
activation_1 (Activation)    (None, 224, 224, 24)      0
_________________________________________________________________
max_pooling2d_1 (MaxPooling2 (None, 112, 112, 24)      0
_________________________________________________________________
conv2d_2 (Conv2D)            (None, 108, 108, 36)      21636
_________________________________________________________________
activation_2 (Activation)    (None, 108, 108, 36)      0
_________________________________________________________________
max_pooling2d_2 (MaxPooling2 (None, 54, 54, 36)        0
_________________________________________________________________
conv2d_3 (Conv2D)            (None, 50, 50, 48)        43248
_________________________________________________________________
activation_3 (Activation)    (None, 50, 50, 48)        0
_________________________________________________________________
max_pooling2d_3 (MaxPooling2 (None, 25, 25, 48)        0
_________________________________________________________________
conv2d_4 (Conv2D)            (None, 23, 23, 64)        27712
_________________________________________________________________
activation_4 (Activation)    (None, 23, 23, 64)        0
_________________________________________________________________
max_pooling2d_4 (MaxPooling2 (None, 11, 11, 64)        0
_________________________________________________________________
conv2d_5 (Conv2D)            (None, 9, 9, 64)          36928
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
Total params: 207,924
Trainable params: 207,922
Non-trainable params: 2
_________________________________________________________________
WARNING:tensorflow:From /Users/lemonad/.pyenv/versions/hockey/lib/python3.7/site-packages/tensorflow/python/ops/math_ops.py:3066: to_int32 (from tensorflow.python.ops.math_ops) is deprecated and will be removed in a future version.
Instructions for updating:
Use tf.cast instead.
Epoch 1/30
100/100 [==============================] - 306s 3s/step - loss: 0.1422 - mean_absolute_error: 0.1422 - val_loss: 0.1341 - val_mean_absolute_error: 0.1341

Epoch 00001: val_loss improved from inf to 0.13410, saving model to puck_coords_weights.best.hdf5
Epoch 2/30
100/100 [==============================] - 268s 3s/step - loss: 0.1292 - mean_absolute_error: 0.1292 - val_loss: 0.0989 - val_mean_absolute_error: 0.0989

Epoch 00002: val_loss improved from 0.13410 to 0.09895, saving model to puck_coords_weights.best.hdf5
Epoch 3/30
100/100 [==============================] - 311s 3s/step - loss: 0.0604 - mean_absolute_error: 0.0604 - val_loss: 0.0487 - val_mean_absolute_error: 0.0487

Epoch 00003: val_loss improved from 0.09895 to 0.04866, saving model to puck_coords_weights.best.hdf5
Epoch 4/30
100/100 [==============================] - 252s 3s/step - loss: 0.0384 - mean_absolute_error: 0.0384 - val_loss: 0.0361 - val_mean_absolute_error: 0.0361

Epoch 00004: val_loss improved from 0.04866 to 0.03606, saving model to puck_coords_weights.best.hdf5
Epoch 5/30
100/100 [==============================] - 289s 3s/step - loss: 0.0298 - mean_absolute_error: 0.0298 - val_loss: 0.0296 - val_mean_absolute_error: 0.0296

Epoch 00005: val_loss improved from 0.03606 to 0.02961, saving model to puck_coords_weights.best.hdf5
Epoch 6/30
100/100 [==============================] - 275s 3s/step - loss: 0.0268 - mean_absolute_error: 0.0268 - val_loss: 0.0247 - val_mean_absolute_error: 0.0247

Epoch 00006: val_loss improved from 0.02961 to 0.02475, saving model to puck_coords_weights.best.hdf5
Epoch 7/30
100/100 [==============================] - 259s 3s/step - loss: 0.0216 - mean_absolute_error: 0.0216 - val_loss: 0.0233 - val_mean_absolute_error: 0.0233

Epoch 00007: val_loss improved from 0.02475 to 0.02332, saving model to puck_coords_weights.best.hdf5
Epoch 8/30
100/100 [==============================] - 253s 3s/step - loss: 0.0183 - mean_absolute_error: 0.0183 - val_loss: 0.0194 - val_mean_absolute_error: 0.0194

Epoch 00008: val_loss improved from 0.02332 to 0.01940, saving model to puck_coords_weights.best.hdf5
Epoch 9/30
100/100 [==============================] - 274s 3s/step - loss: 0.0156 - mean_absolute_error: 0.0156 - val_loss: 0.0196 - val_mean_absolute_error: 0.0196

Epoch 00009: val_loss did not improve from 0.01940
Epoch 10/30
100/100 [==============================] - 245s 2s/step - loss: 0.0140 - mean_absolute_error: 0.0140 - val_loss: 0.0175 - val_mean_absolute_error: 0.0175

Epoch 00010: val_loss improved from 0.01940 to 0.01747, saving model to puck_coords_weights.best.hdf5
Epoch 11/30
100/100 [==============================] - 257s 3s/step - loss: 0.0125 - mean_absolute_error: 0.0125 - val_loss: 0.0164 - val_mean_absolute_error: 0.0164

Epoch 00011: val_loss improved from 0.01747 to 0.01639, saving model to puck_coords_weights.best.hdf5
Epoch 12/30
100/100 [==============================] - 288s 3s/step - loss: 0.0115 - mean_absolute_error: 0.0115 - val_loss: 0.0154 - val_mean_absolute_error: 0.0154

Epoch 00012: val_loss improved from 0.01639 to 0.01542, saving model to puck_coords_weights.best.hdf5
Epoch 13/30
100/100 [==============================] - 269s 3s/step - loss: 0.0116 - mean_absolute_error: 0.0116 - val_loss: 0.0169 - val_mean_absolute_error: 0.0169

Epoch 00013: val_loss did not improve from 0.01542
Epoch 14/30
100/100 [==============================] - 249s 2s/step - loss: 0.0109 - mean_absolute_error: 0.0109 - val_loss: 0.0157 - val_mean_absolute_error: 0.0157

Epoch 00014: val_loss did not improve from 0.01542
Epoch 15/30
100/100 [==============================] - 252s 3s/step - loss: 0.0099 - mean_absolute_error: 0.0099 - val_loss: 0.0144 - val_mean_absolute_error: 0.0144

Epoch 00015: val_loss improved from 0.01542 to 0.01443, saving model to puck_coords_weights.best.hdf5
Epoch 16/30
100/100 [==============================] - 253s 3s/step - loss: 0.0100 - mean_absolute_error: 0.0100 - val_loss: 0.0145 - val_mean_absolute_error: 0.0145

Epoch 00016: val_loss did not improve from 0.01443
Epoch 17/30
100/100 [==============================] - 276s 3s/step - loss: 0.0090 - mean_absolute_error: 0.0090 - val_loss: 0.0125 - val_mean_absolute_error: 0.0125

Epoch 00017: val_loss improved from 0.01443 to 0.01246, saving model to puck_coords_weights.best.hdf5
Epoch 18/30
100/100 [==============================] - 258s 3s/step - loss: 0.0094 - mean_absolute_error: 0.0094 - val_loss: 0.0149 - val_mean_absolute_error: 0.0149

Epoch 00018: val_loss did not improve from 0.01246
Epoch 19/30
100/100 [==============================] - 279s 3s/step - loss: 0.0103 - mean_absolute_error: 0.0103 - val_loss: 0.0149 - val_mean_absolute_error: 0.0149

Epoch 00019: val_loss did not improve from 0.01246
Epoch 20/30
100/100 [==============================] - 257s 3s/step - loss: 0.0089 - mean_absolute_error: 0.0089 - val_loss: 0.0135 - val_mean_absolute_error: 0.0135

Epoch 00020: val_loss did not improve from 0.01246
Epoch 21/30
100/100 [==============================] - 265s 3s/step - loss: 0.0075 - mean_absolute_error: 0.0075 - val_loss: 0.0139 - val_mean_absolute_error: 0.0139

Epoch 00021: val_loss did not improve from 0.01246
Epoch 22/30
100/100 [==============================] - 250s 2s/step - loss: 0.0073 - mean_absolute_error: 0.0073 - val_loss: 0.0118 - val_mean_absolute_error: 0.0118

Epoch 00022: val_loss improved from 0.01246 to 0.01181, saving model to puck_coords_weights.best.hdf5
Epoch 23/30
100/100 [==============================] - 302s 3s/step - loss: 0.0070 - mean_absolute_error: 0.0070 - val_loss: 0.0144 - val_mean_absolute_error: 0.0144

Epoch 00023: val_loss did not improve from 0.01181
Epoch 24/30
100/100 [==============================] - 252s 3s/step - loss: 0.0074 - mean_absolute_error: 0.0074 - val_loss: 0.0119 - val_mean_absolute_error: 0.0119

Epoch 00024: val_loss did not improve from 0.01181
Epoch 25/30
100/100 [==============================] - 243s 2s/step - loss: 0.0070 - mean_absolute_error: 0.0070 - val_loss: 0.0145 - val_mean_absolute_error: 0.0145

Epoch 00025: val_loss did not improve from 0.01181
Epoch 26/30
100/100 [==============================] - 243s 2s/step - loss: 0.0069 - mean_absolute_error: 0.0069 - val_loss: 0.0124 - val_mean_absolute_error: 0.0124

Epoch 00026: val_loss did not improve from 0.01181
Epoch 27/30
100/100 [==============================] - 241s 2s/step - loss: 0.0071 - mean_absolute_error: 0.0071 - val_loss: 0.0133 - val_mean_absolute_error: 0.0133

Epoch 00027: val_loss did not improve from 0.01181
Epoch 28/30
100/100 [==============================] - 241s 2s/step - loss: 0.0071 - mean_absolute_error: 0.0071 - val_loss: 0.0113 - val_mean_absolute_error: 0.0113

Epoch 00028: val_loss improved from 0.01181 to 0.01126, saving model to puck_coords_weights.best.hdf5
Epoch 29/30
100/100 [==============================] - 243s 2s/step - loss: 0.0062 - mean_absolute_error: 0.0062 - val_loss: 0.0115 - val_mean_absolute_error: 0.0115

Epoch 00029: val_loss did not improve from 0.01126
Epoch 30/30
100/100 [==============================] - 244s 2s/step - loss: 0.0060 - mean_absolute_error: 0.0060 - val_loss: 0.0110 - val_mean_absolute_error: 0.0110

Epoch 00030: val_loss improved from 0.01126 to 0.01099, saving model to puck_coords_weights.best.hdf5
