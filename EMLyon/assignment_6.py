# coding: utf-8

# # Assignment \#6 the Sentiment140 dataset
# 
# The sentiment140 dataset contains 1,600,000 tweets extracted using the twitter api from April to June 2009. The tweets have been annotated (0 = negative, 4 = positive) and they can be used to detect sentiment.
# 
# Source: kaggle.com

# As the file is quite large (230MB), we use a subset of this dataset, where we selected only tweets containing the strings (not only isolated words) `"good"` or `"bad"`. The subset for this assignment contains 103,259 tweets:
# 
# - date: datetime of the tweet in the format: year-month-day hours:minutes:seconds
# - score: polarity of the tweet: 0=negative and 4=positive
# - user: user who produced the tweet
# - text: text of the tweet

# **Caution**: Questions asking to return a floating point number (ratio, mean, percentage) should round it to 1 decimal place:
# - Such questions are marked with `(°)`
# - For instance, if the variable `result` is a floating point number, e.g. `3.14159265359`
# - The functions should return `round(result, 1)` instead of `result`, e.g. `3.1`
# - Sommetimes, rounding a floating point number to 1 decimal place leads to a strange number such as `3.100000001`. This is a common outcome with floating point numbers representation and will not affect the grade.
# - Percentages should be returned as floating point numbers (not with the % mark).

# #### Questions
# 
# **A. In this part, we explore the time series aspect of the dataset**
# 
# 1) Pick up the first datetime of the dataset and produce a string in the exact format `day/month/year`, example
# `"25/12/2019"`, using the `strftime()` method.
# 
# 2) Pick up the last datetime of the dataset and produce a string in the exact format `month day, year`, example
# `"Dec 25, 2019"`, using the `strftime()` method.
# 
# 3) How many days with at least one tweet do we have?
# 
# 4) What is the maximum number of tweets in a day?
# 
# 5) What is the minimum number of tweets in a day with at least one tweet?
# 
# 6) What is the average number of tweets in a day with at least one tweet (°)?
# 
# 7) If we consider only the hours of the day (0 to 23) where the tweets have been produced, at what hour do we have the minimum number of tweets?
# 
# 8) If we consider only the hours of the day (0 to 23) where the tweets have been produced, at what hour do we have the maximum number of tweets?
# 
# 9) Who is the most active user in the dataset?
# 
# 10) What is the average number of tweets in a day produced by the most active user (°)?
# 
# 
# (°) Result of functions should be rounded to 1 decimal place.

# **B. In this part, we explore the textual aspect of the dataset**
# 
# 11) What is the mean score of all tweets (°)?
# 
# 12) What is the mean score of tweets containing the string `"good"` (°)?
# 
# 13) What is the mean score of tweets containing the string `"bad"` (°)?
# 
# 14) What is the mean score of tweets issued by the most active user found in question 9 (°)?
# 
# 15) Which text is the most frequent one in all tweets?
# 
# 16) How many different users issued the most frequent tweet?
# 
# 17) What is the mean score of all tweets issued by those users (°)?
# 
# 18) In tweets, users are quoted with a string starting with an `@` and then containing possibly uppercase and lowercase letters, digits and underscore `_`. Which user is the most quoted one (the result should be a string starting with an `@`)?
# 
# 19) How many different users issued at least a tweet quoting the most quoted user?
# 
# 20) What is the mean score of tweets quoting the most quoted user (°)?
# 
# (°) Result of functions should be rounded to 1 decimal place.

# **Important import**
# 
# The cell below imports only the `pandas` module.
# 
# To achieve this assignment, you will need to import other modules. In order to avoid runtime errors when grading please import below the supplementary modules that you need.
# 
# Do not import the `locale` module. All written ouputs are supposed to be in English.

# In[19]:


# import
import pandas as pd

# Import here the supplementary modules that you need
# import
from collections import Counter
import re
import numpy as np

# In[20]:


# loading the data
# the dates are parsed!
# df = pd.read_csv('sample1600000.csv', parse_dates=['date'])
df = pd.read_csv('EMLyon/sample1600000.csv', parse_dates=['date'])
df.head()


# In[46]:


# Pick up the first datetime of the dataset and produce a string in the exact format "25/12/2019"
def exercise_01():
    first_datetime = df.iloc[0, 0]
    date = pd.to_datetime(first_datetime, format="%y-%m-%d-%H-%M")
    # date = datetime.datetime.strptime(first_datetime, format="%y-%m-%d-%H-%M")
    result = date.strftime("%d/%m/%Y")
    return result


# In[47]:


# run and check
# exercise_01()


# In[ ]:


# Pick up the last datetime of the dataset and produce a string in the exact format "Dec 25, 2019"
def exercise_02():
    first_datetime = df.iloc[-1, 0]
    date = pd.to_datetime(first_datetime, format="%y-%m-%d-%H-%M")
    result = date.strftime("%b %d, %Y")
    return result


# In[ ]:


# run and check
# exercise_02()


# In[ ]:


# How many days with at least one tweet do we have?
def exercise_03():
    df['day'] = pd.to_datetime(df['date'], format="%y-%m-%d-%H-%M").apply(lambda x: x.strftime("%y-%m-%d"))
    result = len(df.groupby(by='day').agg('count'))
    return result


# In[ ]:


# run and check
# exercise_03()


# In[ ]:


# What is the maximum number of tweets in a day?
def exercise_04():
    df['day'] = pd.to_datetime(df['date'], format="%y-%m-%d-%H-%M").apply(lambda x: x.strftime("%y-%m-%d"))
    result = df.groupby(by='day').agg('count')['text'].max()
    return result


# In[ ]:


# run and check
# exercise_04()


# In[ ]:


# What is the minimum number of tweets in a day with at least one tweet?
def exercise_05():
    df['day'] = pd.to_datetime(df['date'], format="%y-%m-%d-%H-%M").apply(lambda x: x.strftime("%y-%m-%d"))
    result = df.groupby(by='day').agg('count')['text'].min()
    return result


# In[ ]:


# run and check
# exercise_05()


# In[ ]:


# What is the average number of tweets in a day with at least one tweet (°)?
def exercise_06():
    df['day'] = pd.to_datetime(df['date'], format="%y-%m-%d-%H-%M").apply(lambda x: x.strftime("%y-%m-%d"))
    result = df.groupby(by='day').agg('count')['text'].mean()
    return result


# In[ ]:


# run and check
# exercise_06()


# In[ ]:


# At what hour do we have the minimum number of tweets?
def exercise_07():
    df['hour'] = pd.to_datetime(df['date'], format="%y-%m-%d-%H-%M").apply(lambda x: x.strftime("%H"))
    result = df.groupby(by='hour').agg('count')['text'].idxmin()
    return result


# In[ ]:


# run and check
# exercise_07()


# In[ ]:


# At what hour do we have the maximum number of tweets?
def exercise_08():
    df['hour'] = pd.to_datetime(df['date'], format="%y-%m-%d-%H-%M").apply(lambda x: x.strftime("%H"))
    result = df.groupby(by='hour').agg('count')['text'].idxmax()
    return result


# In[ ]:


# run and check
# exercise_08()


# In[ ]:


# Who is the most active user in the dataset?
def exercise_09():
    result = df.groupby(by='user').agg('count')['text'].idxmax()
    return result


# In[ ]:


# run and check
# exercise_09()


# In[ ]:


# What is the average number of tweets in a day produced by the most active user (°)?
def exercise_10():
    best_tweetos = df.groupby(by='user').agg('count')['text'].idxmax()
    df_best_tweetos = df[df.user == best_tweetos].copy()
    df_best_tweetos['day'] = pd.to_datetime(df_best_tweetos.loc[:, 'date'], format="%y-%m-%d-%H-%M").apply(
        lambda x: x.strftime("%y-%m-%d"))
    result = df_best_tweetos.groupby(by='day').agg('count')['text'].mean()
    return result


# In[ ]:


# run and check
# exercise_10()


# In[ ]:


# What is the mean score of all tweets (°)?
def exercise_11():
    result = df['score'].mean()
    return result


# In[ ]:


# run and check
exercise_11()


# In[ ]:


# What is the mean score of tweets containing the string "good" (°)?
def exercise_12():
    result = df[df['text'].str.contains("good")]['score'].mean()
    return result


# In[ ]:


# run and check
# exercise_12()


# In[ ]:


# What is the mean score of tweets containing the string "bad" (°)?
def exercise_13():
    result = df[df['text'].str.contains("bad")]['score'].mean()
    return result


# In[ ]:


# run and check
# exercise_13()

# In[ ]:


# What is the mean score of tweets issued by the most active user found in question 9 (°)?
def exercise_14():
    best_tweetos = df.groupby(by='user').agg('count')['text'].idxmax()
    df_best_tweetos = df[df.user == best_tweetos].copy()
    result = df_best_tweetos['score'].mean()
    return result


# In[ ]:


# run and check
# exercise_14()


# In[ ]:


# Which text is the most frequent one in all tweets?
def exercise_15():
    result = df.groupby(by='text').agg('count')['date'].idxmax()
    return result


# In[ ]:


# run and check
# exercise_15()


# In[ ]:


# How many different users issued the most frequent tweet?
def exercise_16():
    best_tweet = df.groupby(by='text').agg('count')['date'].idxmax()
    result = len(df[df.text == best_tweet]['user'].unique())
    return result


# In[ ]:


# run and check
# exercise_16()


# In[ ]:


# What is the mean score of all tweets issued by those users (°)?
def exercise_17():
    best_tweet = df.groupby(by='text').agg('count')['date'].idxmax()
    good_tweetos = df[df.text == best_tweet]['user'].unique()
    result = df[df.user.isin(good_tweetos)].score.mean()
    return result


# In[ ]:


# run and check
# exercise_17()


# In[ ]:


# Which user is the most quoted one (the result should be a string starting with an `@`)?
def exercise_18():
    regex = re.compile(r"(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z0-9_]+)")
    # result = regex.findall('@truc @truc_1 @_ @- -@_ _@a _@_ a@b @1 @1.1 tru')
    df['mentions'] = df.text.apply(lambda x: regex.findall(x))

    mentions = pd.Series(np.concatenate(df.mentions))
    mentions_count = Counter(mentions)
    most_mentionned = mentions_count.most_common(1)[0][0]

    # print(most_mentionned)

    result = '@' + most_mentionned
    return result


# In[ ]:


# run and check
exercise_18()


# In[ ]:


# How many different users issued at least a tweet quoting the most quoted user?
def exercise_19():
    regex = re.compile(r"(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z0-9_]+)")
    df['mentions'] = df.text.apply(lambda x: regex.findall(x))

    mentions = pd.Series(np.concatenate(df.mentions))
    mentions_count = Counter(mentions)
    most_mentionned = mentions_count.most_common(1)[0][0]

    mentionned_the_most_mentionned = df[df.mentions.str.contains(most_mentionned, regex=False)]
    result = len(mentionned_the_most_mentionned.user.unique())

    return result


# In[ ]:


# run and check
exercise_19()


# In[ ]:


# What is the mean score of tweets quoting the most quoted user (°)?
def exercise_20():
    regex = re.compile(r"(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z0-9_]+)")
    df['mentions'] = df.text.apply(lambda x: regex.findall(x))

    mentions = pd.Series(np.concatenate(df.mentions))
    mentions_count = Counter(mentions)
    most_mentionned = mentions_count.most_common(1)[0][0]

    result = df[df.mentions.str.contains(most_mentionned, regex=False)].score.mean()
    return result


# In[ ]:


# run and check
exercise_20()