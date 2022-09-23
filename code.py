#import packages
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

sns.set_theme(style="whitegrid")

#Loading in the csv file
df = pd.read_csv('Georgia_COVID-19_Case_Data.csv')
df
len(df)
df.shape

#Describing the variables
df.info()
