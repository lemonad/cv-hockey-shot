"""
Categorize keyframes into training/cross-validation and test sets.

"""
from glob import glob
from os import listdir, mkdir, path, symlink
import random
import shutil

from ..common.Datafiles import (
    get_all_paths,
    get_paths,
    get_prefix_for_session,
    get_round_names_for_session,
    get_session_names,
)
from ..common.AppData import AppSettings, TestData, VideoData


datasets = ["dataset", "dataset-croponly"]
for original_dataset_dir in datasets:
    # Source directory.
    # original_dataset_dir = 'dataset'
    # original_dataset_hits_dir = path.join(original_dataset_dir, 'hit')
    # original_dataset_not_hits_dir = path.join(original_dataset_dir, 'not_hit')

    # Destination directory.
    base_dir = "split-" + original_dataset_dir
    mkdir(base_dir)

    train_dir = path.join(base_dir, "train")
    mkdir(train_dir)
    validate_dir = path.join(base_dir, "validate")
    mkdir(validate_dir)
    test_dir = path.join(base_dir, "test")
    mkdir(test_dir)

    # Directory with training hits pictures
    train_hits_dir = path.join(train_dir, "hit")
    mkdir(train_hits_dir)

    # Directory with training not hits pictures
    train_not_hits_dir = path.join(train_dir, "not_hit")
    mkdir(train_not_hits_dir)

    # Directory with validation hits pictures
    validate_hits_dir = path.join(validate_dir, 'hit')
    mkdir(validate_hits_dir)

    # Directory with validation not hits pictures
    validate_not_hits_dir = path.join(validate_dir, 'not_hit')
    mkdir(validate_not_hits_dir)

    # Directory with test hits pictures
    test_hits_dir = path.join(test_dir, "hit")
    mkdir(test_hits_dir)

    # Directory with test not hits pictures
    test_not_hits_dir = path.join(test_dir, "not_hit")
    mkdir(test_not_hits_dir)

    hit_images = []
    not_hit_images = []
    test_hit_images = []
    test_not_hit_images = []

    session_names = get_session_names()
    for session_name in session_names:
        prefix = get_prefix_for_session(session_name)
        round_names = get_round_names_for_session(
            session_name, training=True, testing=False
        )
        for round_name in round_names:
            print(
                "Training session {:s}, round {:s}...".format(session_name, round_name)
            )
            for imfile in glob(
                "{:s}/hit/{:s}_{:s}_*.png".format(
                    original_dataset_dir, prefix, round_name
                )
            ):
                hit_images.append(imfile)
            for imfile in glob(
                "{:s}/not_hit/{:s}_{:s}_*.png".format(
                    original_dataset_dir, prefix, round_name
                )
            ):
                not_hit_images.append(imfile)

    for session_name in session_names:
        prefix = get_prefix_for_session(session_name)
        round_names = get_round_names_for_session(
            session_name, training=False, testing=True
        )
        for round_name in round_names:
            print(
                "Testing session {:s}, round {:s}...".format(session_name, round_name)
            )
            for imfile in glob(
                "{:s}/hit/{:s}_{:s}_*.png".format(
                    original_dataset_dir, prefix, round_name
                )
            ):
                test_hit_images.append(imfile)
            for imfile in glob(
                "{:s}/not_hit/{:s}_{:s}_*.png".format(
                    original_dataset_dir, prefix, round_name
                )
            ):
                test_not_hit_images.append(imfile)

    n_hits = len(hit_images)
    n_not_hits = len(not_hit_images)
    print(
        "Found {:d} hit images and {:d} not hit images in training dataset".format(
            n_hits, n_not_hits
        )
    )

    test_n_hits = len(test_hit_images)
    test_n_not_hits = len(test_not_hit_images)
    print(
        "Found {:d} hit images and {:d} not hit images in testing dataset".format(
            test_n_hits, test_n_not_hits
        )
    )

    random.shuffle(hit_images)
    random.shuffle(not_hit_images)
    n_validation_hits = int(n_hits * 0.2)
    n_validation_not_hits = int(n_not_hits * 0.2)
    n_training_hits = n_hits - n_validation_hits
    n_training_not_hits = n_not_hits - n_validation_not_hits

    print("Splitting into {:d} hit images and {:d} not hit images for training.".format(
            n_training_hits, n_training_not_hits))
    print("               {:d} hit images and {:d} not hit images for validate.".format(
            n_validation_hits, n_validation_not_hits))

    #
    # Testing images.
    #
    for src in test_hit_images:
        dst = path.join(test_hits_dir, path.basename(src))
        src = path.join("../../..", src)
        symlink(src, dst)

    for src in test_not_hit_images:
        dst = path.join(test_not_hits_dir, path.basename(src))
        src = path.join("../../..", src)
        symlink(src, dst)

    #
    # Validation images.
    #
    for src in hit_images[:n_validation_hits]:
        dst = path.join(validate_hits_dir, path.basename(src))
        src = path.join("../../..", src)
        symlink(src, dst)

    for src in not_hit_images[:n_validation_not_hits]:
        dst = path.join(validate_not_hits_dir, path.basename(src))
        src = path.join("../../..", src)
        symlink(src, dst)

    #
    # Training images.
    #

    for src in hit_images[n_validation_hits:]:
        dst = path.join(train_hits_dir, path.basename(src))
        src = path.join("../../..", src)
        symlink(src, dst)

    for src in not_hit_images[n_validation_not_hits:]:
        dst = path.join(train_not_hits_dir, path.basename(src))
        src = path.join("../../..", src)
        symlink(src, dst)

    print('total training hits images:', len(listdir(train_hits_dir)))
    print('total training not hits images:', len(listdir(train_not_hits_dir)))
    print('total validation hits images:', len(listdir(validate_hits_dir)))
    print('total validation not hits images:', len(listdir(validate_not_hits_dir)))
    print('total test hits images:', len(listdir(test_hits_dir)))
    print('total test not hits images:', len(listdir(test_not_hits_dir)))
