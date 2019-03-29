import os

from keras.optimizers import Adam
from keras.preprocessing.image import ImageDataGenerator
import pandas as pd
from PIL import Image, ImageDraw

from .train_puck_coords import PuckCoordsModel


image_size = 224
validation_image_dir = "./dataset-croponly/hit"
alpha = 1

model = PuckCoordsModel(image_size, alpha)()
model.compile(optimizer=Adam(), loss=["mse"], metrics=["mae"])
weight_path = "{}_weights.best.hdf5".format("puck_coords")
model.load_weights(weight_path)

validation_label_df = pd.read_csv(
    "puck_validation.csv",
    delimiter=" ",
    header=None,
    names=["filename", "x", "y", "norm_x", "norm_y", "frame_x", "frame_y"],
)

datagen = ImageDataGenerator(rescale=1.0 / 255)
validation_generator = datagen.flow_from_dataframe(
    dataframe=validation_label_df,
    directory=validation_image_dir,
    x_col="filename",
    y_col=["x", "y", "norm_x", "norm_y"],
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
    val_x, val_y, val_norm_x, val_norm_y = validation_generator[i][1][0]
    x, y = coords[i]
    draw = ImageDraw.Draw(im)
    sz = 5
    draw.line([(val_x - sz, val_y - sz), (val_x + sz, val_y + sz)], fill=(0, 255, 0))
    draw.line([(val_x - sz, val_y + sz), (val_x + sz, val_y - sz)], fill=(0, 255, 0))

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
