import os, shutil

from keras import layers
from keras import models
from keras import optimizers
from keras.preprocessing.image import ImageDataGenerator

PIXELS = 200

# Directories for the training, validation, and test splits
base_dir = "split_dataset"
train_dir = os.path.join(base_dir, "train")
validation_dir = os.path.join(base_dir, "validate")
test_dir = os.path.join(base_dir, "test")

model = models.Sequential()
model.add(layers.Conv2D(32, (3, 3), activation="relu", input_shape=(PIXELS, PIXELS, 1)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation="relu"))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(128, (3, 3), activation="relu"))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(128, (3, 3), activation="relu"))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Flatten())
# model.add(layers.Dropout(0.25))
model.add(layers.Dense(512, activation="relu"))
model.add(layers.Dense(1, activation="sigmoid"))

model.summary()

model.compile(
    loss="binary_crossentropy",
    optimizer=optimizers.RMSprop(lr=5e-4),
    metrics=["accuracy"],
)

# Rescales all images by 1/255
train_datagen = ImageDataGenerator(
    rescale=1.0 / 255,
    # rotation_range=40,
    # width_shift_range=0.2,
    # height_shift_range=0.2,
    # shear_range=0.2,
    # zoom_range=0.2,
    horizontal_flip=True,
)
validation_datagen = ImageDataGenerator(rescale=1.0 / 255)

train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(PIXELS, PIXELS),  # Resizes all images to 150 × 150
    color_mode="grayscale",
    # batch_size=20,
    # Because you use binary_crossentropy loss,
    # you need binary labels.
    # save_to_dir='augmented_images',
    interpolation="lanczos",
    class_mode="binary",
)
validation_generator = validation_datagen.flow_from_directory(
    validation_dir,
    target_size=(PIXELS, PIXELS),
    color_mode="grayscale",
    # batch_size=20,
    interpolation="lanczos",
    class_mode="binary",
)

for data_batch, labels_batch in train_generator:
    print("data batch shape:", data_batch.shape)
    print("labels batch shape:", labels_batch.shape)
    break

history = model.fit_generator(
    train_generator,
    steps_per_epoch=100,
    epochs=30,
    validation_data=validation_generator,
    validation_steps=50,
)
model.save("hockey.h5")

import matplotlib.pyplot as plt

acc = history.history["acc"]
val_acc = history.history["val_acc"]
loss = history.history["loss"]
val_loss = history.history["val_loss"]
epochs = range(1, len(acc) + 1)
plt.plot(epochs, acc, "bo", label="Training acc")
plt.plot(epochs, val_acc, "b", label="Validation acc")
plt.title("Training and validation accuracy")
plt.legend()
plt.figure()
plt.plot(epochs, loss, "bo", label="Training loss")
plt.plot(epochs, val_loss, "b", label="Validation loss")
plt.title("Training and validation loss")
plt.legend()
plt.show()
