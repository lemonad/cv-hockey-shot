from math import ceil

from keras import backend as K
from keras.applications.mobilenet import MobileNet
from keras.callbacks import (
    ModelCheckpoint,
    LearningRateScheduler,
    EarlyStopping,
    ReduceLROnPlateau,
)
from keras.layers import (
    Conv2D,
    Input,
    Activation,
    add,
    Dense,
    Flatten,
    Dropout,
    Multiply,
    Embedding,
    Lambda,
    Add,
    Concatenate,
    GlobalAveragePooling2D,
)
from keras.layers.convolutional import AveragePooling2D, Conv2D, MaxPooling2D
from keras.layers.normalization import BatchNormalization
from keras.models import Model, Sequential
from keras.optimizers import SGD, Adam
from keras.preprocessing.image import ImageDataGenerator
from keras.regularizers import l2
import numpy as np
import pandas as pd


class PuckCoordsModel:
    def __init__(self, image_size, batch_norm):
        self._input_shape = (image_size, image_size, 1)
        self.batch_norm = batch_norm

    def __call__(self):
        inputs = Input(shape=self._input_shape)

        # model.add(BatchNormalization(input_shape=(224, 224, 1)))
        x = Conv2D(
                24,
                (5, 5),
                padding="same",
                kernel_initializer="he_normal",
                input_shape=(224, 224, 1),
                data_format="channels_last"
            )(inputs)
        if self.batch_norm:
            x = BatchNormalization()(x)
        x = Activation("relu")(x)
        x = MaxPooling2D(pool_size=(2, 2), strides=(2, 2), padding="valid")(x)
        x = Conv2D(36, (5, 5))(x)
        if self.batch_norm:
            x = BatchNormalization()(x)
        x = Activation("relu")(x)
        x = MaxPooling2D(pool_size=(2, 2), strides=(2, 2), padding="valid")(x)
        x = Conv2D(48, (5, 5))(x)
        if self.batch_norm:
            x = BatchNormalization()(x)
        x = Activation("relu")(x)
        x = MaxPooling2D(pool_size=(2, 2), strides=(2, 2), padding="valid")(x)
        x = Conv2D(64, (3, 3))(x)
        if self.batch_norm:
            x = BatchNormalization()(x)
        x = Activation("relu")(x)
        x = MaxPooling2D(pool_size=(2, 2), strides=(2, 2), padding="valid")(x)
        x = Conv2D(64, (3, 3))(x)
        if self.batch_norm:
            x = BatchNormalization()(x)
        x = Activation("relu")(x)
        x = GlobalAveragePooling2D()(x)
        x = Dense(500, activation="relu")(x)
        x = Dense(90, activation="relu")(x)
        coords = Dense(2, activation="sigmoid")(x)

        model = Model(inputs=inputs, outputs=coords)
        return model


def train():
    batch_size = 32
    image_size = 224
    train_image_dir = "./dataset-croponly/hit"
    validation_image_dir = "./dataset-croponly/hit"

    train_label_df = pd.read_csv(
        "puck_training.csv",
        delimiter=" ",
        header=None,
        names=["filename", "x", "y", "norm_x", "norm_y", "frame_xmin", "frame_ymin",
            "frame_xmax", "frame_ymax"],
    )
    validation_label_df = pd.read_csv(
        "puck_validation.csv",
        delimiter=" ",
        header=None,
        names=["filename", "x", "y", "norm_x", "norm_y", "frame_xmin", "frame_ymin",
            "frame_xmax", "frame_ymax"],
    )

    datagen = ImageDataGenerator(rescale=1.0 / 255)
    train_generator = datagen.flow_from_dataframe(
        dataframe=train_label_df,
        directory=train_image_dir,
        x_col="filename",
        y_col=["norm_x", "norm_y"],
        target_size=(image_size, image_size),
        class_mode="other",
        color_mode="grayscale",
        interpolation="lanczos",
        batch_size=batch_size,
        seed=42,
    )

    validation_generator = datagen.flow_from_dataframe(
        dataframe=validation_label_df,
        directory=validation_image_dir,
        x_col="filename",
        y_col=["norm_x", "norm_y"],
        target_size=(image_size, image_size),
        class_mode="other",
        color_mode="grayscale",
        interpolation="lanczos",
        batch_size=batch_size,
        seed=42,
    )

    model = PuckCoordsModel(image_size, batch_norm=True)()
    model.compile(optimizer=Adam(lr=1e-3), loss=["mse"], metrics=["mse", "mae"])
    # model.compile(optimizer="rmsprop", loss="mse", metrics=["mae"])
    model.count_params()
    model.summary()

    # weight_path = "{}_weights.best.hdf5".format("puck_coords")
    model_path = "{}.best.h5".format("puck_coords")
    checkpoint = ModelCheckpoint(
        # weight_path,
        # save_weights_only=True,
        model_path,
        save_weights_only=False,
        monitor="val_loss",
        verbose=1,
        save_best_only=True,
        mode="min",
    )

    reduceLROnPlat = ReduceLROnPlateau(
        monitor="val_loss",
        factor=0.1,
        patience=10,
        verbose=1,
        mode="auto",
        cooldown=5,
        min_lr=1e-6,
    )
    # probably needs to be more patient, but kaggle time is limited
    # early = EarlyStopping(monitor="val_loss", mode="min", patience=10)
    callbacks_list = [checkpoint, reduceLROnPlat]

    # save_name = "mobilenet_reg_%s_%d" % (alpha, image_size)
    # model.compile(optimizer=Adam(), loss=["mae"], metrics={'pred_a': 'mae'})

    print(ceil(train_generator.n / batch_size))
    history = model.fit_generator(
        train_generator,
        steps_per_epoch=2, #ceil(train_generator.n / batch_size),
        epochs=2,
        validation_data=validation_generator,
        validation_steps=ceil(validation_generator.n / batch_size),
        callbacks=callbacks_list,
    )

    model.save("hockey-puck-localization2-model.h5")

    #
    # Training history.
    #

    import matplotlib.pyplot as plt

    mae = history.history["mean_absolute_error"]
    val_mae = history.history["val_mean_absolute_error"]
    loss = history.history["loss"]
    val_loss = history.history["val_loss"]

    print("Best MSE: {:f} (trn), {:f} (val)".format(np.min(loss), np.min(val_loss)))
    print("Best MAE: {:f} (trn), {:f} (val)".format(np.min(mae), np.min(val_mae)))

    epochs = range(1, len(loss) + 1)
    plt.plot(epochs, mae, "b--", label="Training")
    plt.plot(epochs, val_mae, "b", label="Validation")
    plt.title("Training and validation MAE")
    plt.legend()
    plt.figure()
    plt.plot(epochs, loss, "r--", label="Training")
    plt.plot(epochs, val_loss, "r", label="Validation")
    plt.title("Training and validation loss (MSE)")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    train()
