import math
from math import nan

import numpy as np
import pandas as pd
from pandas import Series


def to_file(df, file_name):
    return df.to_csv(file_name)


def get_weights_and_biases(df):
    weights = []
    biases = []

    weights_tmp = []
    biases_tmp = []

    weight_slice = slice(0, -1)

    last_layer_index = -1
    for column, data in df.items():
        if column == "Unnamed: 0":
            continue

        layer_index, neuron_index = column.split(' ')
        if last_layer_index != layer_index:
            if len(weights_tmp) > 0:
                m_weights = np.matrix(weights_tmp)
                weights.append(m_weights.transpose())
                weights_tmp = []

                biases.append(np.matrix(biases_tmp))
                biases_tmp = []
            last_layer_index = layer_index

        weights_tmp.append(trim(data)[weight_slice])
        biases_tmp.append(trim(data)[-1])

    m_weights = np.matrix(weights_tmp)
    weights.append(m_weights.transpose())
    biases.append(np.matrix(biases_tmp))

    return weights, biases




def to_df(file):
    df = pd.read_csv(filepath_or_buffer=file)
    return df


def get_df(weights_in, biases_in):
    df = pd.DataFrame()

    number_of_layers = len(biases_in)

    for layer in range(number_of_layers):
        weights = weights_in[layer].transpose()
        weights_l = weights.tolist()

        biases_l = biases_in[layer].tolist()[0]

        for neuron in range(len(weights_l)):

            w = Series(weights_l[neuron])
            b = Series(biases_l[neuron])
            s = pd.concat([w, b], ignore_index=True)

            df[str(layer) + " " + str(neuron)] = s

    return df


def trim(arr):
    n_array = []
    for el in arr:
        if not math.isnan(el):
            n_array.append(el)
    return n_array