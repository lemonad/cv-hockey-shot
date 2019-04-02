import os

from keras.models import load_model
from keras.optimizers import Adam
from keras.preprocessing.image import ImageDataGenerator
import pandas as pd
from PIL import Image, ImageDraw

from .train_puck_coords2 import PuckCoordsModel


image_size = 224
validation_image_dir = "./dataset-croponly/hit"
alpha = 1

model = load_model("train-puck7.h5")
# model = PuckCoordsModel(image_size, alpha)()
# model.compile(optimizer=Adam(), loss=["mse"], metrics=["accuracy", "mae"])
# weight_path = "{}_weights.best.hdf5".format("puck_coords")
# model.load_weights(weight_path)

validation_label_df = pd.read_csv(
    "puck_validation.csv",
    delimiter=" ",
    header=None,
    names=["filename", "x", "y", "norm_x", "norm_y", "frame_xmin", "frame_ymin",
    "frame_xmax", "frame_ymax"],
)

datagen = ImageDataGenerator(rescale=1.0 / 255)
validation_generator = datagen.flow_from_dataframe(
    dataframe=validation_label_df,
    directory=validation_image_dir,
    x_col="filename",
    y_col=["norm_x", "norm_y", "frame_xmin", "frame_ymin", "frame_xmax", "frame_ymax"],
    target_size=(image_size, image_size),
    class_mode="other",
    color_mode="grayscale",
    interpolation="lanczos",
    seed=42,
    batch_size=1,
    shuffle=False,
)

validation_generator.reset()
coords = model.predict_generator(
    generator=validation_generator, steps=validation_generator.n, verbose=True
)

validation_generator.reset()
for i in range(validation_generator.n):
    path = validation_generator.filepaths[i]
    filename = os.path.basename(path)
    im = Image.open(path)
    t = validation_generator[i][1][0]
    (val_norm_x, val_norm_y, frame_xmin, frame_ymin, frame_xmax, frame_ymax) = t
    norm_x, norm_y = coords[i]
    draw = ImageDraw.Draw(im)
    width = frame_xmax - frame_xmin
    height = frame_ymax - frame_ymin
    sz = int(width * 0.01)
    val_x = val_norm_x * width
    val_y = val_norm_y * height
    x = norm_x * width
    y = norm_y * height
    draw.line([(val_x - sz, val_y), (val_x + sz, val_y)], fill=(0, 255, 0))
    draw.line([(val_x, val_y + sz), (val_x, val_y - sz)], fill=(0, 255, 0))

    draw.line([(x - sz, y - sz), (x + sz, y + sz)], fill=(255, 0, 0))
    draw.line([(x - sz, y + sz), (x + sz, y - sz)], fill=(255, 0, 0))
    del draw
    outpath = os.path.join("./puck-predictions", filename)
    im.save(outpath, "png", compress_level=0)


# for i in range(len(validation_label_df)):
#     pred_x, pred_y = coords[i]
#     val_x = validation_label_df.x[i]
#     print(pred_x, val_x)
# 
#     filename = validation_label_df.filename[i]
#     im = Image.open(filename)
