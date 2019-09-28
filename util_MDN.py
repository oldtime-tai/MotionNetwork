# -*- coding=UTF-8 -*-
"""
@Time : 2019/5/28
@Author : gzf
@File : util_MDN.py
@brief:  混合密度实现

参考：https://zhuanlan.zhihu.com/p/37992239
"""

import numpy as np
import tensorflow as tf


def mixture_density(y, out, m, c):

    # alpha 权重参数(m)；mu 均值(c*m)；sigma 标准差(m)
    alpha, mu, sigma = tf.split(out, [m, (c*m), m], 1)

    # mu reshape
    mu_out = tf.reshape((mu.shape[0], mu.shape[1], m, c))

    # 使用 softmax 保证概率和为 1
    alpha_out = tf.nn.softmax(alpha, name='prob_dist')

    # 使用 exp 保证标准差大于 0
    sigma_out = tf.exp(sigma, name='sigma')

    # 系数 1/(sqrt(2π)^c)
    factor = 1 / np.power((np.sqrt(2 * np.pi)), c)

    # 为了防止计算中可能出现除零的情况，当分母为零时，用一个极小值 epsilon 来代替
    epsilon = 1e-5

    tmp = - tf.square((y - mu_out)) / (2 * tf.square(tf.maximum(sigma_out, epsilon)))
    y_normal = factor * tf.exp(tmp) / tf.maximum(sigma_out, epsilon)

    # 计算loss
    loss = tf.reduce_sum(tf.multiply(y_normal, alpha_out), axis=1, keep_dims=True)
    loss = -tf.log(tf.maximum(loss, epsilon))
    loss = tf.reduce_mean(loss)

    return loss


