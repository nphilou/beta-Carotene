
# coding: utf-8

# # Assignment \#5 the Gapminder dataset
# 
# There are 4 files for this assignment:
# - `population_total.csv`: total population, per country and per year (1800 to 2018)
# - `life_expectancy_years.csv`: life expectancy, per country and per year (1800 to 2018)
# - `income_per_person.csv`: income per person, per country and per year (1800 to 2018)
# - `countries_total.csv`: countries and regions (Asia, Europe, Africa, Oceania, Americas)
# 
# As usual the files must be along with your notebook and not in a dedicated folder.

# **Important note about the `geo` columns accross the `DataFrame` objects**: 
# - The 3 first files contain a field named `geo` with the names of the different countries. The last file contains also a column with the different countries. It is renamed to `geo` on load to ease the merges that would have to be performed (option `on='geo'` of `merge()` function).
# - The name of the countries have to be processed as is, without trying to homogenize them accross the different files.
# - In order to avoid discrepancies between results, all joins should be performed by using the `how='inner'`option.

# **Hint about the `python_data_science_1` and `python_data_science_2` notebooks**
# 
# - The 20 following questions in parts A and B rely on materials that have been studied in the notebook `python_data_science_1`: 1 to 13, 16, 19 and 22 to 26
# - The 10 following questions in parts A and B rely on materials that will be studied in the notebook `python_data_science_2`: 14 to 15, 17 to 18, 20 to 21 and 27 to 30

# **Caution**: Questions asking to return a floating point number (ratio, mean, percentage) should round it to 1 decimal place:
# - Such questions are marked with `(°)`
# - For instance, if the variable `result` is a floting point number, e.g. `3.14159265359`
# - The functions should return `round(result, 1)` instead of `result`, e.g. `3.1`
# - Percentages should be returned as floating point numbers (not with the % mark).

# #### Questions
# 
# **A. In this part, we will only deal with the data for year 2018**
# 
# - Total population by country in 2018:
# 
# 1) What is the sum of the total population in 2018?
# 
# 2) Which country has the largest total population in 2018?
# 
# 3) Which country has the smallest total population in 2018?
# 
# - Life expectation by country in 2018:
# 
# 4) What is the average life expectancy in 2018 (°)?
# 
# 5) What is the difference between the largest and the smallest life expectancy in 2018?
# 
# 6) Which country has the largest life expectancy in 2018?
# 
# 7) Which country has the smallest life expectancy in 2018?
# 
# 8) In 2018, below which life expectancy threshold a country is in the first decile (°)?
# 
# - Income per person by country in 2018:
# 
# 9) What is the average income per person in 2018 (°)?
# 
# 10) What is the ratio between the largest and the smallest income per person in 2018 (°)?
# 
# 11) Which country has the largest income per person in 2018?
# 
# 12) Which country has the smallest income per person in 2018?
# 
# 13) In 2018, above which income per person threshold a country is in the last decile (°)?
# 
# - Perform an inner join between the population and the country `DataFrame` objects:
# 
# 14) Which region has the largest total population in 2018?
# 
# 15) Which region has the smallest total population in 2018?
# 
# - Perform an inner join between the life expectancy and the total population `DataFrame` objects, then an inner join with the result and the country `DataFrame` object. Remember that overlapping columns names are renamed automatically with the `_x` and `_y` suffixes in the left and right side:
# 
# 16) What is the weighted average life expectancy in 2018 (°) (+)?
# 
# 17) What is the largest weighted average life expectancy by region in 2018 (°) (+)?
# 
# 18) What is the smallest weighted average life expectancy by region in 2018 (°) (+)?
# 
# - Perform an inner join between the life expectancy and the total population `DataFrame` objects, then an inner join with the result and the country `DataFrame` objects. Remember that overlapping columns are renamed automatically with the `_x` and `_y` suffixes in the left and right side:
# 
# 19) What is the weighted average income per person in 2018 (°) (++)?
# 
# 20) Which region has the largest weighted average income per person in 2018 (++)?
# 
# 21) Which region has the smallest weighted average income per person in 2018 (++)?
# 
# (+) The *weighted average life expectancy* is computed with the sum of the products of life expectancy by total population of each country divided by the sum of total population of each country. It can be computed for all countries in the world or for all countries in each region.
# 
# Hint: weighted average life expectancy $= \frac{\displaystyle\sum_{i} life_{i} \times pop_{i}}{\displaystyle\sum_{i} pop_{i}}$
# 
# (++) The *weighted average income per person* is computed with the sum of the products of income per person by total population of each country divided by the sum of total population of each country. It can be computed for all countries in the world or for all countries in each region.
# 
# Hint: weighted average income per person $= \frac{\displaystyle\sum_{i} income_{i} \times pop_{i}}{\displaystyle\sum_{i} pop_{i}}$
# 
# (°) Result of functions should be rounded to 1 decimal place.

# **B. In this part, we deal with data for all years**
# 
# 22) Which country has the smallest mean life expectancy accross years?
# 
# 23) Which country has the smallest mean income per person accross years?
# 
# 24) Compute the correlation of total population between all countries accross years. Which country has the highest mean correlation with the other ones? 
# 
# 25) Compute the correlation of life expectancy between all countries accross years. Which country has the highest mean correlation of life expectancy with the other ones? 
# 
# 26) Compute the correlation of income per person between all countries accross years. Which country has the highest mean correlation of income per person with the other ones?
# 
# 27) Perform a wide to long format transformation of the total population `DataFrame` object by using the `melt()` function. What is the length of the new `DataFrame` object for total population?
# 
# 28) Perform a wide to long format transformation of the life expectancy `DataFrame` object by using the `melt()` function. What is the length of the new `DataFrame` object for life expectancy?
# 
# 29) Perform a wide to long format transformation of the income per person `DataFrame` object by using the `melt()` function. What is the length of the new `DataFrame` object for income per person?
# 
# 30) Perform 3 wide to long format transformations of the total population, life expectancy and income per person `DataFrame` objects by using the `melt()` function. Then perform an inner join of the 2 first `DataFrame` objects on both `geo` and `Year` by using the `merge()` function. Then perform another inner join of this `DataFrame` object and the third one. You should obtain a final `DataFrame` object with 5 columns: `geo`, `Year`, `Total Population`, `Life Expectancy` and `Income Per Person`. Remove lines with `NA` . What is the length of the final `DataFrame` object obtained?

# **Homework, out of the scope of the assignment**
# 
# - Homogenize the country names accross the different files and compare the results of the 30 exercises.
# 
# - Implement a graphics showing, for a given year, all countries positionned with their income per person on the `x` axis and their life expectancy on the `y` axis, and represented by their name, as well as, a circle which radius is linked to their total population and which color is linked to their region.

# In[37]:


# import
import numpy as np
import pandas as pd

# In[38]:


# loading the data

df_population = pd.read_csv('population_total.csv')
df_life = pd.read_csv('life_expectancy_years.csv')
df_income = pd.read_csv('income_per_person.csv')
df_country = pd.read_csv('countries_total.csv',
                         engine='python',
                         usecols=[0, 5],
                         header=0,
                         names=['geo', 'region'])

# In[39]:


df_population = pd.read_csv('EMLyon/population_total.csv')
df_life = pd.read_csv('EMLyon/life_expectancy_years.csv')
df_income = pd.read_csv('EMLyon/income_per_person.csv')
df_country = pd.read_csv('EMLyon/countries_total.csv',
                         skipinitialspace=True,
                         usecols=[0, 5],
                         header=0,
                         names=['geo', 'region'])
df_population.rename(columns=lambda x: x.strip(), inplace=True)
df_life.rename(columns=lambda x: x.strip(), inplace=True)
df_income.rename(columns=lambda x: x.strip(), inplace=True)

# In[40]:


# What is the sum of the total population in 2018?
def exercise_01():
    result = df_population['2018'].sum()
    return result


# In[41]:


# run and check
exercise_01()


# In[42]:


# Which country has the largest total population in 2018?
def exercise_02():
    idx = df_population['2018'].idxmax()
    result = df_population.iloc[idx, 0]
    return result


# In[43]:


# run and check
exercise_02()


# In[44]:


# Which country has the smallest total population in 2018?
def exercise_03():
    idx = df_population['2018'].idxmin()
    result = df_population.iloc[idx, 0]
    return result


# In[45]:


# run and check
exercise_03()


# In[46]:


# What is the average life expectancy in 2018 (°)?
def exercise_04():
    result = df_life['2018'].mean()
    return round(result, 1)


# In[47]:


# run and check
exercise_04()


# In[48]:


# What is the difference between the largest and the smallest life expectancy in 2018?
def exercise_05():
    result = df_life['2018'].max() - df_life['2018'].min()
    return result


# In[49]:


# run and check
exercise_05()


# In[50]:


# Which country has the largest life expectancy in 2018?

def exercise_06():
    result = df_life.iloc[df_life['2018'].idxmax(), 0]
    return result


# In[51]:


# run and check
exercise_06()


# In[52]:


# Which country has the smallest life expectancy in 2018?
def exercise_07():
    result = df_life.iloc[df_life['2018'].idxmin(), 0]
    return result


# In[53]:


# run and check
exercise_07()


# In[102]:


# In 2018, below which life expectancy threshold a country is in the first decile (°)?
def exercise_08():
    result = pd.qcut(df_life['2018'], 10, retbins=True)
    return round(result[1][1], 1)


# In[103]:


# run and check
exercise_08()


# In[56]:


# What is the average income per person in 2018 (°)?
def exercise_09():
    result = df_income['2018'].mean()
    return round(result, 1)


# In[57]:


# run and check
exercise_09()


# In[58]:


# What is the ratio between the largest and the smallest income per person in 2018
def exercise_10():
    result = df_income['2018'].min() / df_income['2018'].max()
    return result


# In[59]:


# run and check
exercise_10()


# In[60]:


# Which country has the largest income per person in 2018?
def exercise_11():
    result = df_income.iloc[df_income['2018'].idxmax(), 0]
    return result


# In[61]:


# run and check
exercise_11()


# In[62]:


# Which country has the smallest income per person in 2018?
def exercise_12():
    result = df_income.iloc[df_income['2018'].idxmin(), 0]
    return result


# In[63]:


# run and check
exercise_12()


# In[64]:


# In 2018, above which income per person threshold a country is in the last decile (°)?
def exercise_13():
    result = pd.qcut(df_income['2018'], 10, retbins=True)
    return result[1][9]


# In[65]:


# run and check
exercise_13()


# In[66]:


# Which region has the largest total population in 2018?
def exercise_14():
    pop_regions = df_population.loc[:, ['2018']].join(df_country)

    pop_grouped = pop_regions.groupby('region').sum()
    result = pop_grouped['2018'].idxmax()
    return result


# In[67]:


# run and check
exercise_14()


# In[68]:


# Which region has the smallest total population in 2018?
def exercise_15():
    pop_regions = df_population.loc[:, ['2018']].join(df_country)

    pop_grouped = pop_regions.groupby('region').sum()
    result = pop_grouped['2018'].idxmin()
    return result


# In[69]:


# run and check
exercise_15()


# In[70]:
life = df_life.loc[:, ['geo', '2018']].set_index('geo')
life.rename(columns={'2018': 'life'}, inplace=True)

pop = df_population.loc[:, ['geo', '2018']].set_index('geo')
pop.rename(columns={'2018': 'pop'}, inplace=True)

life_pop = life.join(pop)
life_pop['sumprod'] = life_pop['life'] * life_pop['pop']

# What is the weighted average life expectancy in 2018 (°)?
def exercise_16():
    result = life_pop['sumprod'].sum() / life_pop['pop'].sum()
    return round(result, 1)


# In[71]:


# run and check
exercise_16()


# In[132]:
life_pop_region = life_pop.join(df_country.set_index('geo'))
grouped = life_pop_region.loc[:, ['sumprod', 'pop', 'region']].groupby('region').sum()
grouped['sumprod_by_pop'] = grouped['sumprod'] / grouped['pop']

print(life_pop_region.head())


# What is the largest weighted average life expectancy by region in 2018 (°)?
def exercise_17():
    result = grouped['sumprod_by_pop'].max()
    return round(result, 1)


# In[133]:


# run and check
exercise_17()


# In[134]:


# What is the smallest weighted average life expectancy by region in 2018 (°)?
def exercise_18():

    result = grouped['sumprod_by_pop'].min()
    return round(result, 1)


# In[135]:


# run and check
exercise_18()


# In[76]:


# What is the weighted average income per person in 2018 (°)?
def exercise_19():
    income = df_income.loc[:, ['geo', '2018']].set_index('geo')
    income.rename(columns={'2018': 'income'}, inplace=True)
    pop = df_population.loc[:, ['geo', '2018']].set_index('geo')
    pop.rename(columns={'2018': 'pop'}, inplace=True)
    
    income_pop = income.join(pop)
    income_pop['sumprod'] = income_pop['income'] * income_pop['pop']

    result = income_pop['sumprod'].sum() / income_pop['pop'].sum()

    return round(result, 1)


# In[77]:


# run and check
exercise_19()


# In[78]:


# Which region has the largest weighted average income per person in 2018?
def exercise_20():
    income = df_income.loc[:, ['geo', '2018']].set_index('geo')
    income.rename(columns={'2018': 'income'}, inplace=True)
    pop = df_population.loc[:, ['geo', '2018']].set_index('geo')
    pop.rename(columns={'2018': 'pop'}, inplace=True)
    
    income_pop = income.join(pop)
    income_pop['sumprod'] = income_pop['income'] * income_pop['pop']

    income_pop_region = income_pop.join(df_country.set_index('geo'))
    
    grouped = income_pop_region.loc[:, ['sumprod', 'region']].groupby('region').sum()
    result = grouped['sumprod'].idxmax()
    return result


# In[79]:


# run and check
exercise_20()


# In[80]:


# Which region has the smallest weighted average income per person in 2018?
def exercise_21():
    income = df_income.loc[:, ['geo', '2018']].set_index('geo')
    income.rename(columns={'2018': 'income'}, inplace=True)
    pop = df_population.loc[:, ['geo', '2018']].set_index('geo')
    pop.rename(columns={'2018': 'pop'}, inplace=True)
    
    income_pop = income.join(pop)
    income_pop['sumprod'] = income_pop['income'] * income_pop['pop']

    income_pop_region = income_pop.join(df_country.set_index('geo'))
    
    grouped = income_pop_region.loc[:, ['sumprod', 'region']].groupby('region').sum()
    result = grouped['sumprod'].idxmin()
    return result


# In[81]:


# run and check
exercise_21()


# In[82]:


# Which country has the smallest average life expectancy accross years?
def exercise_22():
    df_life['mean'] = df_life.mean(axis=1)
    df_life.set_index('geo', inplace=True)
    result = df_life['mean'].idxmin()
    return result


# In[83]:


# run and check
exercise_22()


# In[84]:


# Which country has the smallest average income per person accross years?
def exercise_23():
    df_income['mean'] = df_income.mean(axis=1)
    df_income.set_index('geo', inplace=True)
    result = df_income['mean'].idxmin()
    return result


# In[85]:


# run and check
exercise_23()


# In[146]:


# Which country has the highest mean correlation of total population with other countries? 
def exercise_24():
    corr = df_population.set_index('geo').T.corr()
    corr['mean'] = corr.mean(axis=1)
    result = corr['mean'].idxmax()
    return result


# In[147]:


# run and check
exercise_24()


# In[150]:


# Which country has the highest mean correlation of life expectancy with other countries? 
def exercise_25():
    corr = df_life.T.corr()
    corr['mean'] = corr.mean(axis=1)
    result = corr['mean'].idxmax()
    return result


# In[151]:


# run and check
exercise_25()


# In[140]:


# Which country has the highest mean correlation of income per person with other countries? 
def exercise_26():
    corr = df_income.T.corr()
    result = corr['mean'] = corr.mean(axis=1).idxmax()
    return result


# In[141]:


# run and check
exercise_26()


# In[188]:


# What is the length of the new DataFrame object for total population?
def exercise_27():
    result = len(df_population.melt(id_vars='geo'))
    return result


# In[189]:


# run and check
exercise_27()


# In[192]:


# What is the length of the new DataFrame object for life expectancy?
def exercise_28():
    result = len(df_life.reset_index().melt(id_vars='geo'))
    return result


# In[193]:


# run and check
exercise_28()


# In[196]:


# What is the length of the new DataFrame object for income per person?
def exercise_29():
    result = len(df_income.reset_index().melt(id_vars='geo'))
    return result


# In[197]:


# run and check
exercise_29()


# In[210]:


# What is the length of the DataFrame object merging total population, life expectancy and income per person in a long format?
def exercise_30():
    pop = df_population.melt(id_vars='geo', var_name='year', value_name='pop')
    life = df_life.reset_index().melt(id_vars='geo', var_name='year', value_name='life')
    income = df_income.reset_index().melt(id_vars='geo', var_name='year', value_name='income')

    pop_life = pd.merge(pop, life, on=['geo', 'year'])
    pop_life_income = pd.merge(pop_life, income, on=['geo', 'year'])

    result = len(pop_life_income.dropna())
    
    return result


# In[212]:


# run and check
exercise_30()

