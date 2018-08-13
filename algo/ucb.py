# Import Libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import math
import random
from os import path


def ucb(N, d, ads_selected, numbers_of_selections, sums_of_rewards, total_reward, dataset):
    '''
    Implementing UCB
    :param N:
    :param d:
    :param ads_selected:
    :param numbers_of_selections:
    :param sums_of_rewards:
    :param total_reward:
    :return:
    '''

    for n in range(0, N):
        confidence = [0] * d
        max_upper_bound = 0
        upper_bound = 1e400
        for i in range(0, d):
            if (numbers_of_selections[i] > 0):

                average_reward = sums_of_rewards[i] / numbers_of_selections[i]
                delta_i = math.sqrt(3 / 2 * math.log(n + 1) / numbers_of_selections[i])
                upper_bound = average_reward + delta_i
                confidence[i] = upper_bound


            if upper_bound >= max_upper_bound:
                max_upper_bound = upper_bound
                #ad[i] = 1

        ad = predict_time_slots(confidence, max_upper_bound)

        ads_selected.append(ad)
        numbers_of_selections = sum_of_array(numbers_of_selections, ad)
        #print('actual_arr: '+str(dataset.values[n]))
        #print('predict_arr: '+str(ad))
        reward, hit = Reward(dataset.values[n], ad)
        sums_of_rewards = sum_of_array(sums_of_rewards, reward)
        total_reward = total_reward + hit


    return ads_selected, numbers_of_selections, sums_of_rewards, total_reward


def Reward(actual_arr, predict_arr):
    reward = [0] * len(actual_arr)
    hit = 0
    for i in range(0, len(actual_arr)):
        if actual_arr[i] == predict_arr[i] & predict_arr[i] == 1:
            reward[i] = 1
            hit+=1
    return reward, hit


def sum_of_array(arr1, arr2):
    for i in range(0, len(arr1)):
        arr1[i] += arr2[i]
    return arr1


def predict_time_slots(confidence, max):
    ad = [0] * len(confidence)
    sum = 0
    for i in range(0, len(confidence)):
        #print(confidence[i], max)
        if confidence[i] >= max:
            ad[i] = 1
            sum+=1
    if sum == 0:
        index = int(math.floor(random.uniform(0, 1) * len(confidence)))
        ad[index] = 1

    return ad

directory = "../public"

d = 28
ads_selected = []
numbers_of_selections = [0] * d
confidence  = [0] * d
sums_of_rewards = [0] * d
total_reward = 0


for filename in os.listdir(directory):
    if 'label' in filename:
        print filename
        dataset = pd.read_csv(os.path.join(directory, filename))
        N = len(dataset.values)
        dataset = dataset.drop(columns=['user_id'])
        ads_selected, numbers_of_selections, sums_of_rewards, total_reward = ucb(N, d, ads_selected, numbers_of_selections, sums_of_rewards, total_reward, dataset)
        #print(str(ads_selected))
        print(str(numbers_of_selections))
        print(str(sums_of_rewards))
        print(str(total_reward))

        continue
    else:
        continue





