
# coding: utf-8

# # Assignment \#4 French names
# 
# Download page: https://www.insee.fr/fr/statistiques/2540004/
# 
# Section: `Fichiers France hors Mayotte`
# 
# File format: `txt`
# 
# File size: `2 Mo`
# 
# Zip name: `nat2017_txt.zip`
# 
# Tabulated separated file name: `nat2017.txt`

# #### Objective
# 
# The objective of this assignment is to load the dataset and to load and transform the `DataFrame` so that **it has exactly the same characteristics** than the full US `DataFrame`.
# 
# You should program the manipulations in a single Python function which should return the transformed `DataFrame`. Each requirement will be checked and will bring 1 point. As the aim of the assignment is to get a `DataFrame` that exactly conforms to the US one, **the final grade will be computed by applying a non-linear mapping to the total points**.
# 
# Points | Grade
# -|-
# 0 | 0
# 1 | 1
# 2 | 3
# 3 | 5
# 4 | 8
# 5 | 11
# 6 | 14
# 7 | 18
# 8 | 22
# 9 | 26
# 10 | 30
# 
# Requirements (in any order):
# 
# - The `DataFrame` has the appropriate shape: N rows x 4 columns
# 
# - The column names are properly set
# 
# - Columns are properly ordered: year, name, gender and births
# 
# - The data type of each column is properly set
# 
# - The values of the gender column are properly set: 'F' for female and 'M' for male
# 
# - Names with a single character are discarded
# 
# - The case of all names is properly modified: all initials should be upper case and other letters lower cases
# 
# - Rows with unusable values are discarded
# 
# - Data are properly sorted: year, gender, births (descending) and name
# 
# - The index of the `DataFrame` is properly set: 0 to N-1

# In[1]:


# YOU SHOULD IMPLEMENT A SINGLE FUNCTION
# IT SHOULD READ THE DATASET FROM THE FILE ALONG WITH THE NOTEBOOK
# IT SHOULD PERFORM THE APPROPRIATE TRANSFORMATIONS TO THE DATAFRAME
# IT SHOULD RETURN THE TRANSFORMED DATAFRAME

def exercise_01():
    df = None
    return df


# **Homework, out of the scope of the assignment**
# 
# After that you may use this dataset within the notebook 4 in order to perform with the French names the same analysis than we did perform with the US one.
