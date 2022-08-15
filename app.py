#!/usr/bin/env python
# coding: utf-8

# # Lab Assignment 12: Interactive Visualizations
# ## DS 6001: Practice and Application of Data Science
# 
# ### Instructions
# Please answer the following questions as completely as possible using text, code, and the results of code as needed. Format your answers in a Jupyter notebook. To receive full credit, make sure you address every part of the problem, and make sure your document is formatted in a clean and professional way.

# ## Problem 0
# Import the following libraries:

# In[3]:


import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import dash
from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


# For this lab, we will be working with the 2019 General Social Survey one last time.

# In[4]:


get_ipython().run_cell_magic('capture', '', 'gss = pd.read_csv("https://github.com/jkropko/DS-6001/raw/master/localdata/gss2018.csv",\n                 encoding=\'cp1252\', na_values=[\'IAP\',\'IAP,DK,NA,uncodeable\', \'NOT SURE\',\n                                               \'DK\', \'IAP, DK, NA, uncodeable\', \'.a\', "CAN\'T CHOOSE"])')


# Here is code that cleans the data and gets it ready to be used for data visualizations:

# In[5]:


mycols = ['id', 'wtss', 'sex', 'educ', 'region', 'age', 'coninc',
          'prestg10', 'mapres10', 'papres10', 'sei10', 'satjob',
          'fechld', 'fefam', 'fepol', 'fepresch', 'meovrwrk'] 
gss_clean = gss[mycols]
gss_clean = gss_clean.rename({'wtss':'weight', 
                              'educ':'education', 
                              'coninc':'income', 
                              'prestg10':'job_prestige',
                              'mapres10':'mother_job_prestige', 
                              'papres10':'father_job_prestige', 
                              'sei10':'socioeconomic_index', 
                              'fechld':'relationship', 
                              'fefam':'male_breadwinner', 
                              'fehire':'hire_women', 
                              'fejobaff':'preference_hire_women', 
                              'fepol':'men_bettersuited', 
                              'fepresch':'child_suffer',
                              'meovrwrk':'men_overwork'},axis=1)
gss_clean.age = gss_clean.age.replace({'89 or older':'89'})
gss_clean.age = gss_clean.age.astype('float')


# The `gss_clean` dataframe now contains the following features:
# 
# * `id` - a numeric unique ID for each person who responded to the survey
# * `weight` - survey sample weights
# * `sex` - male or female
# * `education` - years of formal education
# * `region` - region of the country where the respondent lives
# * `age` - age
# * `income` - the respondent's personal annual income
# * `job_prestige` - the respondent's occupational prestige score, as measured by the GSS using the methodology described above
# * `mother_job_prestige` - the respondent's mother's occupational prestige score, as measured by the GSS using the methodology described above
# * `father_job_prestige` -the respondent's father's occupational prestige score, as measured by the GSS using the methodology described above
# * `socioeconomic_index` - an index measuring the respondent's socioeconomic status
# * `satjob` - responses to "On the whole, how satisfied are you with the work you do?"
# * `relationship` - agree or disagree with: "A working mother can establish just as warm and secure a relationship with her children as a mother who does not work."
# * `male_breadwinner` - agree or disagree with: "It is much better for everyone involved if the man is the achiever outside the home and the woman takes care of the home and family."
# * `men_bettersuited` - agree or disagree with: "Most men are better suited emotionally for politics than are most women."
# * `child_suffer` - agree or disagree with: "A preschool child is likely to suffer if his or her mother works."
# * `men_overwork` - agree or disagree with: "Family life often suffers because men concentrate too much on their work."

# ## Problem 1
# Our goal in this lab is to build a dashboard that presents our findings from the GSS. A dashboard is meant to be shared with an audience, whether that audience is a manager, a client, a potential employer, or the general public. So we need to provide context for our results. One way to provide context is to write text using markdown code.
# 
# Find one or two websites that discuss the gender wage gap, and write a short paragraph in markdown code summarizing what these sources tell us. Include hyperlinks to these websites. Then write another short paragraph describing what the GSS is, what the data contain, how it was collected, and/or other information that you think your audience ought to know. A good starting point for information about the GSS is here: http://www.gss.norc.org/About-The-GSS
# 
# Then save the text as a Python string so that you can use the markdown code in your dashboard later.
# 
# It should go without saying, but no plagiarization! If you summarize a website, make sure you put the summary in your own words. Anything that is copied and pasted from the GSS webpage, Wikipedia, or another website without attribution will receive no credit.
# 
# (Don't spend too much time on this, and you might want to skip it during the Zoom session and return to it later so that you can focus on working on code with your classmates.) [1 point]

# In[109]:


markdown_text = '''
For every $1 that men earn, women earn $0.82. The disparity changes by race, where hispanic or latino women only make 
$0.54 compared to white men making $1. While some of these disparities are caused by things like amount of time worked, 
years working, and differences in industries worked, some disparities are caused by discrimination. Advancements in women 
recieving greater education has lessened the pay gap between men and women. 
https://www.americanprogress.org/article/quick-facts-gender-wage-gap/

The GSS (or General Social Survey) is a survey that collects on US adults about demographics as well as 
information on values ,general attitudes, and behaviors (like spending habits). The data includes demograhics 
(race, sex, income, etc) and responses to questions that asses agreeability with a statement (agree, disagree, etc).
The data is collected by in-person interviews typically, but also phone interviews. As time moved on, computer 
facilited interviews have also been used (CAPI). 
'''


# ## Problem 2
# Generate a table that shows the mean income, occupational prestige, socioeconomic index, and years of education for men and for women. Use a function from a `plotly` module to display a web-enabled version of this table. This table is for presentation purposes, so round every column to two decimal places and use more presentable column names. [3 points]

# In[15]:


gss_display = gss_clean.groupby('sex').agg({'socioeconomic_index':'mean',
                                            'income':'mean',
                                           'job_prestige' : 'mean',
                                           'education' : 'mean'})

gss_display = gss_display.rename({'socioeconomic_index':'Socioeconomic Index',
                                   'income':'Average Income',
                                   'job_prestige':'Job Prestige Score',
                                   'education':'Years of Educcation'}, axis=1)

gss_display = round(gss_display, 2)
gss_display = gss_display.reset_index().rename({'sex':'Sex'}, axis=1)

table = ff.create_table(gss_display)
table.show()


# ## Problem 3
# Create an interactive barplot that shows the number of men and women who respond with each level of agreement to `male_breadwinner`. Write presentable labels for the x and y-axes, but don't bother with a title because we will be using a subtitle on the dashboard for this graphic. [3 points]

# In[120]:


gss_bar = pd.crosstab(gss_clean['sex'], gss_clean['male_breadwinner']).reset_index()


bar = px.bar(gss_bar, x="sex",
             y=["strongly agree", 'agree', 'disagree', 'strongly disagree'],
            labels={'value':'Count', 'sex':'Sex', 'variable':'Level of Agreement'})
bar.show()


# ## Problem 4
# Create an interactive scatterplot with `job_prestige` on the x-axis and `income` on the y-axis. Color code the points by `sex` and make sure that the figure includes a legend for these colors. Also include two best-fit lines, one for men and one for women. Finally, include hover data that shows us the values of `education` and `socioeconomic_index` for any point the mouse hovers over. Write presentable labels for the x and y-axes, but don't bother with a title because we will be using a subtitle on the dashboard for this graphic. [3 points]

# In[113]:


scatter = px.scatter(gss_clean, x='job_prestige', y='income', color = 'sex',
                 height=600, width=600,
                 labels={'job_prestige':'Job Prestige Score', 
                        'income':'Income',
                        'sex':'Sex'},
                 hover_data=['education', 'socioeconomic_index'])
scatter.update(layout=dict(title=dict(x=0.5)))
scatter.show()


# ## Problem 5
# Create two interactive box plots: one that shows the distribution of `income` for men and for women, and one that shows the distribution of `job_prestige` for men and for women. Write presentable labels for the axis that contains `income` or `job_prestige` and remove the label for `sex`. Also, turn off the legend. Don't bother with titles because we will be using subtitles on the dashboard for these graphics. [3 points]

# In[114]:


gss_cand = pd.melt(gss_clean, id_vars = ['sex'], 
                    value_vars = ['income'])
gss_cand
gss_cand = gss_cand.rename({'variable':'identifier',
                             'value':'Job Prestige',
                           'sex': 'Sex'}, axis=1)
box1 = px.box(gss_cand, x='Job Prestige', y = 'Sex', color = 'Sex')
box1.update(layout=dict(title=dict(x=0.5)))
box1.show()


# In[115]:


gss_cand = pd.melt(gss_clean, id_vars = ['sex'], 
                    value_vars = ['job_prestige'])

gss_cand = gss_cand.rename({'variable':'indentifier',
                             'value':'Job Prestige',
                           'sex': 'Sex'}, axis=1)
box2 = px.box(gss_cand, x='Job Prestige', y = 'Sex', color = 'Sex')
box2.update(layout=dict(title=dict(x=0.5)))
box2.show()


# ## Problem 6
# Create a new dataframe that contains only `income`, `sex`, and `job_prestige`. Then create a new feature in this dataframe that breaks `job_prestige` into six categories with equally sized ranges. Finally, drop all rows with any missing values in this dataframe.
# 
# Then create a facet grid with three rows and two columns in which each cell contains an interactive box plot comparing the income distributions of men and women for each of these new categories. 
# 
# (If you want men to be represented by blue and women by red, you can include `color_discrete_map = {'male':'blue', 'female':'red'}` in your plotting function. Or use different colors if you want!) [3 points]

# In[101]:


gss_df = gss_clean[['sex','income', 'job_prestige']]
prestiges = [1, 2, 3, 4, 5, 6]
gss_df['Job Prestige'] = pd.cut(gss_df['job_prestige'], 6, labels = prestiges)

gss_df = gss_df.dropna()
gss_df


# In[116]:


boxes = px.box(gss_df, x='income', y = 'sex', color='sex', 
             facet_col='Job Prestige', facet_col_wrap=2,
             labels={'sex':'Sex', 'income':'Income'},
            color_discrete_map = {'male':'blue', 'female':'green'},
            )
boxes.update(layout=dict(title=dict(x=0.5)))
boxes.show()


# ## Problem 7
# Create a dashboard that displays the following elements:
# 
# * A descriptive title
# 
# * The markdown text you wrote in problem 1
# 
# * The table you made in problem 2
# 
# * The barplot you made in problem 3
# 
# * The scatterplot you made in problem 4
# 
# * The two boxplots you made in problem 5 side-by-side
# 
# * The faceted boxplots you made in problem 6
# 
# * Subtitles for all of the above elements
# 
# Use `JupyterDash` to display this dashboard directly in your Jupyter notebook.
# 
# Any working dashboard that displays all of the above elements will receive full credit. [4 points]

# In[132]:  


# ## Extra Credit (up to 10 bonus points)
# Dashboards are all about good design, functionality, and accessability. For this extra credit problem, create another version of the dashboard you built for problem 7, but take extra steps to improve the appearance of the dashboard, add user-inputs, and host it on the internet with its own URL.
# 
# **Challenge 1**: Be creative and use a layout that significantly departs from the one used for the ANES data in the module 12 notebook. A good place to look for inspiration is the [Dash gallery](https://dash-gallery.plotly.host/Portal/). We will award up to 3 bonus points for creativity, novelty, and style.
# 
# **Challenge 2**: Alter the barplot from problem 3 to include user inputs. Create two dropdown menus on the dashboard. The first one should allow a user to display bars for the categories of `satjob`, `relationship`, `male_breadwinner`, `men_bettersuited`, `child_suffer`, or `men_overwork`. The second one should allow a user to group the bars by `sex`, `region`, or `education`. After choosing a feature for the bars and one for the grouping, program the barplot to update automatically to display the user-inputted features. One bonus point will be awarded for a good effort, and 3 bonus points will be awarded for a working user-input barplot in the dashboard.
# 
# **Challenge 3**: Follow the steps listed in the module notebook to deploy your dashboard on Heroku. 1 bonus point will be awarded for a Heroku link to an app that isn't working. 4 bonus points will be awarded for a working Heroku link.

# In[152]:


external_stylesheets = ['https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css']




# ## Challenge 2

# In[127]:


bar_columns = ['satjob', 'relationship', 'male_breadwinner', 'men_bettersuited', 'child_suffer', 'men_overwork']


# In[128]:


group_columns = ['sex', 'region', 'education']


# In[136]:


gss_cleaned = gss_clean[bar_columns + group_columns].dropna()


# In[137]:


app = JupyterDash(__name__, external_stylesheets=external_stylesheets)


app.layout = html.Div(
    [
        html.H1("Exploring the General Society Survey"),
        
        dcc.Markdown(children = markdown_text),
        
        html.H2("Comparing Men and Women's Economics an Education"),
        
        dcc.Graph(figure=table),    
        
        html.H2("Level of Agreement in Values by Sex"),
        
        dcc.Graph(figure=bar),
        
        html.H2("Job Prestige vs Income by Sex"),
        
        dcc.Graph(figure=scatter),
        
        html.Div([
            
            html.H2("Distribution of Income By Sex"),
            
            dcc.Graph(figure=box1)
            
        ], style = {'width':'48%', 'float':'left'}),
        
        html.Div([
            
            html.H2("Distribution of Job Prestige by Sex"),
            
            dcc.Graph(figure=box2)
            
        ], style = {'width':'48%', 'float':'right'}),
        
        html.H2("Distribution of Income by Job Prestige and Sex"),
        
        dcc.Graph(figure=boxes),
        
        html.H2("Feeling Thermometer Scatterplot"),
        
        html.Div([
            
            html.H3("x-axis feature"),
            
            dcc.Dropdown(id='x-axis',
                         options=[{'label': i, 'value': i} for i in bar_columns],
                         value='satjob'),

            
            html.H3("colors"),
            
            dcc.Dropdown(id='color',
                         options=[{'label': i, 'value': i} for i in group_columns])
        
        ], style={'width': '25%', 'float': 'left'}),
        
        html.Div([
            
            dcc.Graph(id="graph")
        
        ], style={'width': '70%', 'float': 'right'})
    
    ]
)
@app.callback(Output(component_id="graph",component_property="figure"), 
                  [Input(component_id='x-axis',component_property="value"),
                   Input(component_id='color',component_property="value")])

def make_figure(x, color):
    return px.bar(
        gss_cleaned,
        x=x,
        color=color,
        height=700,
        opacity = .25
)


if __name__ == '__main__':
    app.run_server(debug=True)


# ## Challenge 3

# In[ ]:





