from keras import backend as K
from keras.applications.mobilenet import MobileNet
from keras.callbacks import (
    ModelCheckpoint,
    LearningRateScheduler,
    EarlyStopping,
    ReduceLROnPlateau,
)
from keras.layers import (
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
    def __init__(self, image_size, alpha):
        self._input_shape = (image_size, image_size, 1)
        self.alpha = alpha

    def __call__(self):
        mobilenet_model = MobileNet(
            input_shape=self._input_shape,
            alpha=self.alpha,
            depth_multiplier=1,
            dropout=1e-3,
            include_top=False,
            weights=None,
            input_tensor=None,
            pooling=None,
        )

        inputs = Input(shape=self._input_shape)
        # inputs = BatchNormalization(input_shape=self._input_shape)
        x = mobilenet_model(inputs)
        x = Conv2D(20, (1, 1), activation="relu")(x)
        x = Flatten()(x)
        # x = BatchNormalization()(x)
        # x = GlobalAveragePooling2D()(x)
        x = Dropout(0.2)(x)
        x = Dense(32, activation="relu")(x)
        pred = Dense(2, activation="linear")(x)

        # feat_a = Flatten()(feat_a)
        # feat_a = Dropout(0.2)(feat_a)
        # feat_a = Dense(32, activation="relu")(feat_a)

        # pred_a = Dense(2, activation="linear", name="pred_a")(feat_a)

        model = Model(inputs=inputs, outputs=[pred])
        return model


def train():
    image_size = 224
    train_image_dir = "./dataset-croponly/hit"
    validation_image_dir = "./dataset-croponly/hit"
    alpha = 1

    train_label_df = pd.read_csv(
        "puck_training.csv",
        delimiter=" ",
        header=None,
        names=["filename", "x", "y", "norm_x", "norm_y", "frame_x", "frame_y"],
    )
    validation_label_df = pd.read_csv(
        "puck_validation.csv",
        delimiter=" ",
        header=None,
        names=["filename", "x", "y", "norm_x", "norm_y", "frame_x", "frame_y"],
    )

    datagen = ImageDataGenerator(rescale=1./255)
    train_generator = datagen.flow_from_dataframe(
        dataframe=train_label_df,
        directory=train_image_dir,
        x_col="filename",
        y_col=["x", "y"],
        target_size=(image_size, image_size),
        class_mode="other",
        color_mode="grayscale",
        interpolation="lanczos",
        seed=42,
    )

    validation_generator = datagen.flow_from_dataframe(
        dataframe=validation_label_df,
        directory=validation_image_dir,
        x_col="filename",
        y_col=["x", "y"],
        target_size=(image_size, image_size),
        class_mode="other",
        color_mode="grayscale",
        interpolation="lanczos",
        seed=42,
    )

    model = PuckCoordsModel(image_size, alpha)()
    model.compile(optimizer=Adam(), loss=["mse"], metrics=["mae"])
    model.count_params()
    model.summary()

    weight_path = "{}_weights.best.hdf5".format("puck_coords")
    checkpoint = ModelCheckpoint(
        weight_path,
        monitor="val_loss",
        verbose=1,
        save_best_only=True,
        mode="min",
        save_weights_only=True,
    )

    reduceLROnPlat = ReduceLROnPlateau(
        monitor="val_loss",
        factor=0.8,
        patience=10,
        verbose=1,
        mode="auto",
        epsilon=0.0001,
        cooldown=5,
        min_lr=0.0001,
    )
    # probably needs to be more patient, but kaggle time is limited
    early = EarlyStopping(
        monitor="val_loss", mode="min", patience=5
    )
    callbacks_list = [checkpoint, early, reduceLROnPlat]

    # save_name = "mobilenet_reg_%s_%d" % (alpha, image_size)
    # model.compile(optimizer=Adam(), loss=["mae"], metrics={'pred_a': 'mae'})

    history = model.fit_generator(
        train_generator,
        steps_per_epoch=100,
        epochs=30,
        validation_data=validation_generator,
        validation_steps=50,
        callbacks=callbacks_list,
    )

    # model.save("hockey-puck-localization-adam.h5")

    #
    # Evaluation.
    #

    import matplotlib.pyplot as plt

    mae = history.history["mae"]
    val_mae = history.history["val_mae"]
    # mse = history.history["mse"]
    # val_mse = history.history["val_mse"]
    loss = history.history["loss"]
    val_loss = history.history["val_loss"]

    epochs = range(1, len(mae) + 1)
    plt.plot(epochs, mae, "bo", label="Training MAE")
    plt.plot(epochs, val_mae, "b", label="Validation MAE")
    plt.title("Training and validation MAE")
    plt.legend()
    plt.figure()
    plt.plot(epochs, loss, "bo", label="Training loss")
    plt.plot(epochs, val_loss, "b", label="Validation loss")
    plt.title("Training and validation loss")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    train()
