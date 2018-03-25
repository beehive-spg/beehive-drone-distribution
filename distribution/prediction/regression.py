from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import tensorflow as tf
from distribution.service import routeservice

def main():
    try:
        prediction = start_regression(17592186046318)
        print(prediction)
    except Exception as e:
        print(e)
        print("prediction not ready")

def get_order_time_history(buildingid):
    all_routes = routeservice.get_all_routes()

    order_times = []
    for route in all_routes:
        if (is_starting_hive(route, buildingid)):
            order_times.append(route.hops[0].starttime)
    return sorted(order_times)

def is_starting_hive(route, buildingid):
    return route.hops[0].start.id == buildingid

def get_x_values(order_times):
    x_values = []
    for index in range(1, len(order_times)+1):
        x_values.append(index)
    return x_values

def get_y_values(buildingid):
    return get_order_time_history(buildingid)

def start_regression(buildingid):
    y_values = get_y_values(buildingid)
    x_values = get_x_values(y_values)
    amount_of_values = len(y_values)

    assert len(y_values) == len(x_values)

    y_norm = get_normalized_array(y_values)

    y_true = tf.constant(y_norm, dtype=tf.float32)
    x = tf.constant(x_values, dtype=tf.float32)

    y_true = tf.reshape(y_true, [amount_of_values, 1])
    x = tf.reshape(x, [amount_of_values, 1])

    linear_model = tf.layers.Dense(units=1)

    y_pred = linear_model(x)

    sess = tf.Session()
    init = tf.global_variables_initializer()
    sess.run(init)

    loss = tf.losses.mean_squared_error(labels=y_true, predictions=y_pred)

    optimizer = tf.train.GradientDescentOptimizer(0.0001)
    train = optimizer.minimize(loss)

    for i in range(10000):
      _, loss_value = sess.run((train, loss))
      print(loss_value)
      if (loss_value < 0.005):
        print("Training done")
        print(loss_value)
        break

    predcition = tf.constant([[1] ], dtype=tf.float32)

    predcition_value = sess.run(linear_model(predcition))

    print(y_values)
    print(y_norm[0])

    return int(get_denormalized_value(predcition_value, y_values) / 1000)

def get_normalized_array(y_values):
    maximum = max(y_values)
    minimum = min(y_values)
    array = []
    for y in y_values:
        array.append(get_normalized_value(y, y_values, maximum, minimum))
    print(array)
    return [ array ]

def get_normalized_value(y_value, y_values, maximum, minimum):
    return (y_value - minimum) / (maximum - minimum)

def get_denormalized_value(y_value, y_values):
    maximum = max(y_values)
    minimum = min(y_values)
    return (y_value * (maximum- minimum) + maximum)

if __name__ == '__main__':
    main()