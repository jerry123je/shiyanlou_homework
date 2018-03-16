#!/usr/bin/env python3
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


def data_plot():
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.set_title("StudyData")
    major_ticks_y = np.arange(0,3001,500)
    major_ticks_x = np.arange(0,200001,50000)

    ax.set_xticks(major_ticks_x)
    ax.set_yticks(major_ticks_y)

    ax.set_xlabel("User ID")
    ax.set_ylabel("Study Time")

    files = open('user_study.json').read()

    data = pd.read_json(files)

    data1 = data[['user_id','minutes']].groupby('user_id').sum()
    
    ax.plot(data1)

    plt.show()
    return ax

data_plot()
