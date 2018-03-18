#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd

def quarter_volume():
	data = pd.read_csv('apple.csv', parse_dates=['Date'], index_col=['Date'])
	quarter = data.resample('Q').sum()
	quarter_sort = quarter.sort_values(axis=0, ascending=False, by='Volume')
	second_volume = quarter_sort.ix[1]['Volume']
	
	return second_volume


print(quarter_volume())
