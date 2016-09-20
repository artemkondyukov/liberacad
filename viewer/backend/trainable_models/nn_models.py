from keras.models import Model
from keras.layers import merge, Input
from keras.layers import Convolution2D, MaxPooling2D, UpSampling2D

from .util import LRN2D


def get_u_net(image_size, do_lrn):
    main_input = Input(shape=(1, image_size, image_size))
    input_shape = (-1, 1, image_size, image_size)

    convolution_1_1 = Convolution2D(8, 3, 3,
                                    input_shape=input_shape, activation='relu', border_mode='same')(main_input)
    convolution_1_2 = Convolution2D(8, 3, 3, activation='relu', border_mode='same')(convolution_1_1)
    pool_1 = MaxPooling2D(pool_size=(2, 2))(convolution_1_2)

    if do_lrn:
        normalize_1 = LRN2D()(pool_1)
        convolution_2_1 = Convolution2D(16, 3, 3, activation='relu', border_mode='same')(normalize_1)
    else:
        convolution_2_1 = Convolution2D(16, 3, 3, activation='relu', border_mode='same')(pool_1)
    convolution_2_2 = Convolution2D(16, 3, 3, activation='relu', border_mode='same')(convolution_2_1)
    pool_2 = MaxPooling2D(pool_size=(2, 2))(convolution_2_2)

    if do_lrn:
        normalize_2 = LRN2D()(pool_2)
        convolution_3_1 = Convolution2D(32, 3, 3, activation='relu', border_mode='same')(normalize_2)
    else:
        convolution_3_1 = Convolution2D(32, 3, 3, activation='relu', border_mode='same')(pool_2)
    convolution_3_2 = Convolution2D(32, 3, 3, activation='relu', border_mode='same')(convolution_3_1)
    pool_3 = MaxPooling2D(pool_size=(2, 2))(convolution_3_2)

    if do_lrn:
        normalize_3 = LRN2D()(pool_3)
        convolution_4_1 = Convolution2D(64, 3, 3, activation='relu', border_mode='same')(normalize_3)
    else:
        convolution_4_1 = Convolution2D(64, 3, 3, activation='relu', border_mode='same')(pool_3)
    convolution_4_2 = Convolution2D(64, 3, 3, activation='relu', border_mode='same')(convolution_4_1)
    pool_4 = MaxPooling2D(pool_size=(2, 2))(convolution_4_2)

    if do_lrn:
        normalize_4 = LRN2D()(pool_4)
        convolution_5_1 = Convolution2D(128, 3, 3, activation='relu', border_mode='same')(normalize_4)
    else:
        convolution_5_1 = Convolution2D(128, 3, 3, activation='relu', border_mode='same')(pool_4)
    convolution_5_2 = Convolution2D(128, 3, 3, activation='relu', border_mode='same')(convolution_5_1)

    first_upsampled = UpSampling2D(size=(2, 2))(convolution_5_2)
    first_merged = merge([first_upsampled, convolution_4_2], mode='concat', concat_axis=1)
    if do_lrn:
        normalize_5 = LRN2D()(first_merged)
        convolution_6_1 = Convolution2D(64, 3, 3, activation='relu', border_mode='same')(normalize_5)
    else:
        convolution_6_1 = Convolution2D(64, 3, 3, activation='relu', border_mode='same')(first_merged)
    convolution_6_2 = Convolution2D(64, 3, 3, activation='relu', border_mode='same')(convolution_6_1)

    second_upsampled = UpSampling2D(size=(2, 2))(convolution_6_2)
    second_merged = merge([second_upsampled, convolution_3_2], mode='concat', concat_axis=1)
    if do_lrn:
        normalize_6 = LRN2D()(second_merged)
        convolution_7_1 = Convolution2D(32, 3, 3, activation='relu', border_mode='same')(normalize_6)
    else:
        convolution_7_1 = Convolution2D(32, 3, 3, activation='relu', border_mode='same')(second_merged)
    convolution_7_2 = Convolution2D(32, 3, 3, activation='relu', border_mode='same')(convolution_7_1)

    third_upsampled = UpSampling2D(size=(2, 2))(convolution_7_2)
    third_merged = merge([third_upsampled, convolution_2_2], mode='concat', concat_axis=1)
    if do_lrn:
        normalize_7 = LRN2D()(third_merged)
        convolution_8_1 = Convolution2D(16, 3, 3, activation='relu', border_mode='same')(normalize_7)
    else:
        convolution_8_1 = Convolution2D(16, 3, 3, activation='relu', border_mode='same')(third_merged)
    convolution_8_2 = Convolution2D(16, 3, 3, activation='relu', border_mode='same')(convolution_8_1)

    fourth_upsampled = UpSampling2D(size=(2, 2))(convolution_8_2)
    fourth_merged = merge([fourth_upsampled, convolution_1_2], mode='concat', concat_axis=1)
    if do_lrn:
        normalize_8 = LRN2D()(fourth_merged)
        convolution_9_1 = Convolution2D(8, 3, 3, activation='relu', border_mode='same')(normalize_8)
    else:
        convolution_9_1 = Convolution2D(8, 3, 3, activation='relu', border_mode='same')(fourth_merged)
    convolution_9_2 = Convolution2D(8, 3, 3, activation='relu', border_mode='same')(convolution_9_1)

    convolution_10_1 = Convolution2D(1, 1, 1, activation='sigmoid')(convolution_9_2)

    return Model(input=main_input, output=convolution_10_1)
