
# coding: utf-8

# # AIB to Bambora SF Cost Comparison Application

# In[2]:

from IPython.core.display import display, HTML
display(HTML("<style>.container { width:95% !important; }</style>"))
import sys
print (sys.version)


# ## Import the Necessary Libraries
# Below are the libraries required to assemble the project.

# In[3]:

import pyodbc #CONNECT VIA PYODBC IMPORT THE PYODBC LIBRARY
import pandas as pd #CONNECT TO THE PANDAS LIBRARY
import numpy as np #IMPORT NUMPY
import csv
import seaborn as sns
get_ipython().magic(u'matplotlib inline')
from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator
pd.options.mode.chained_assignment = None  # default='warn'
#print pyodbc.dataSources()
#conn=pyodbc.connect("Driver={NetezzaSQL};SERVER=10.80.10.70;PORT=5480;DATABASE=P_FDW;UID=djohnson;PWD=Sup3rm4n",ansi=True)


#   ## Card BIN Import

# In[4]:

bin_column_names=['IIN','BIN_DESC']
card_bin=pd.read_csv('d:\\djohnson\\Desktop\\card_class_bin.csv',error_bad_lines=False,sep=';',skiprows=4,names=bin_column_names,index_col=False)


# In[5]:

card_bin['IIN']=card_bin['IIN'].astype(float)


# ## Bambora Import

# In[6]:

bb_column_names=['TRANSACTION_REF','ADDITIONAL_REFERENCE_2','PAYMENTREFERENCE','BB_TRANSACTION_TYPE','MCC','CONTRACT_ID','IIN','BIN_DESC','ORDERID','PAYMENT_PROCESSOR','MONTH','DAY','YEAR','PERIOD'
              ,'ISSUER_COUNTRY','MERCHANT_COUNTRY','TRANSACTION_TYPE','CARD_SCHEME','CREDIT_DEBIT','CONSUMER_CORPORATE','SECURITY_LEVEL','REGIONALITY'
              ,'PRODUCT_CODE','SF_FIXED_FEE','SF_PERC_FEE','CON_COM_BIN','VOLUME','ROUNDED_TRXN_AMOUNT','SCHEME_TOTAL_FEE_EUR','FLOW','BB_IC_TOTAL','BB_IC_BPS','BB_SF_BPS']


# In[7]:

#import the file from local drives
#bb=pd.read_csv('d:\\djohnson\\Desktop\\aib_comp_pull_bb_data.csv',error_bad_lines=False,skiprows=32,sep=';',names=bb_column_names,index_col=False)
bb=pd.read_csv('d:\\djohnson\\Desktop\\aib_comp_pull_bb_data.csv',error_bad_lines=False,sep=';',skiprows=95,names=bb_column_names,index_col=False)


# In[8]:

bb['BB_TRANSACTION_TYPE']=bb['BB_TRANSACTION_TYPE'].str.strip()
bb['ISSUER_COUNTRY']=bb['ISSUER_COUNTRY'].str.strip()
bb['MERCHANT_COUNTRY']=bb['MERCHANT_COUNTRY'].str.strip()
bb['CARD_SCHEME']=bb['CARD_SCHEME'].str.strip()
bb['CREDIT_DEBIT']=bb['CREDIT_DEBIT'].str.strip()
bb['CONSUMER_CORPORATE']=bb['CONSUMER_CORPORATE'].str.strip()
bb['REGIONALITY']=bb['REGIONALITY'].str.strip()
bb['BIN_DESC']=bb['BIN_DESC'].str.strip()


# In[9]:

#create a new copy and safe old in memory for working purposes and to prevent repeated import from local drive
bb1=bb.copy()
bb1=bb1.dropna()
bb1=bb1.drop(['CON_COM_BIN'],axis=1)


# In[10]:

bb1['SECURITY_LEVEL'].unique()


# In[11]:

bb1['SECURITY_LEVEL']=bb1['SECURITY_LEVEL'].apply(lambda x:'NON-SECURE' if (7 == x) or (0 == x) or (6 == x) else 'SECURE')


# In[12]:

bb1=bb1[(bb1['BB_TRANSACTION_TYPE']=='Sale')]
bb1=bb1.rename({'ROUNDED_TRXN_AMOUNT':'FLOW'})
bb1.head()


# In[13]:

bb1.info()


# In[14]:

bb1_contracts=bb1[['CONTRACT_ID','ISSUER_COUNTRY','MERCHANT_COUNTRY','CARD_SCHEME','CREDIT_DEBIT','CONSUMER_CORPORATE','SECURITY_LEVEL','IIN','BIN_DESC']]


# In[15]:

bb1=bb1[(bb1['BIN_DESC']!='')]


# In[16]:

bb1_contracts.head()


# In[17]:

bb1_contracts=bb1_contracts.drop_duplicates()


# In[18]:

bb1_contracts.info()


# In[20]:

bb1_contracts.to_csv('d:\\djohnson\\Desktop\\bb1_contracts.csv')


# ## AIB Import

# In[49]:

#name the columns
#all monetary is in euros
ab_column_names=['TRANSACTION_DATE','CONTRACT_ID','ISSUER_COUNTRY','IIN','BIN_DESC','CARD_SCHEME','MERCHANT_COUNTRY','TRANSACTION_TYPE','SECURITY_LEVEL','CARD_TYPE','IC_DESCRIPTION','FLOW','AIB_SF_RATE_AMOUNT','AIB_SF_PERC','AIB_SF_TOTAL','AIB_IC_RATE','AIB_IC_PERC','AIB_IC_TOTAL','AIB_SF_BPS','AIB_IC_BPS','CREDIT_DEBIT','CONSUMER_CORPORATE']


# In[50]:

#import the file from local drives
ab=pd.read_csv('d:\\djohnson\\Desktop\\aib_comp_pull_aib_data.csv',error_bad_lines=False,skiprows=40,names=ab_column_names,sep=';',index_col=False)


# In[51]:

ab['ISSUER_COUNTRY']=ab['ISSUER_COUNTRY'].str.strip()
ab['CARD_SCHEME']=ab['CARD_SCHEME'].str.strip()
ab['MERCHANT_COUNTRY']=ab['MERCHANT_COUNTRY'].str.strip()
ab['TRANSACTION_TYPE']=ab['TRANSACTION_TYPE'].str.strip()
ab['SECURITY_LEVEL']=ab['SECURITY_LEVEL'].str.strip()
ab['CARD_TYPE']=ab['CARD_TYPE'].str.strip()
ab['IC_DESCRIPTION']=ab['IC_DESCRIPTION'].str.strip()
ab['CREDIT_DEBIT']=ab['CREDIT_DEBIT'].str.strip()
ab['CONSUMER_CORPORATE']=ab['CONSUMER_CORPORATE'].str.strip()
ab['SECURITY_LEVEL']=ab['SECURITY_LEVEL'].str.strip()
ab['CONTRACT_ID']=ab['CONTRACT_ID'].astype(float)
ab['BIN_DESC']=ab['BIN_DESC'].str.strip()


# In[52]:

#create a new copy and safe old in memory for working purposes and to prevent repeated import from local drive
ab1=ab.copy()


# In[53]:

ab1['SECURITY_LEVEL'].unique()


# In[54]:

ab1['SECURITY_LEVEL']=ab['SECURITY_LEVEL'].apply(lambda x:'NON-SECURE' if ('Not authenticated security transaction at a merchant who supports Verified-by-VISA - 3D-Secure' == x) or ('Not authenticated security transaction at a merchant who supports MasterCard SecureCode - UCAF' == x) or ('Channel encrypted' == x) or ('Not relevant' == x) else 'SECURE')


# In[55]:

ab1['CREDIT_DEBIT']=ab['CREDIT_DEBIT'].apply(lambda x:'Debit' if ('Prepaid' == x) or ('Debit'== x) else 'Credit')


# In[56]:

ab1.head()


# In[57]:

ab2=ab1[['CONTRACT_ID','ISSUER_COUNTRY','MERCHANT_COUNTRY','CARD_SCHEME','CREDIT_DEBIT','CONSUMER_CORPORATE','SECURITY_LEVEL','BIN_DESC']].drop_duplicates()


# In[58]:

ab2.to_csv('d:\\djohnson\\Desktop\\ab2.csv')


# In[59]:

ab1.info()


# In[60]:

ab1=ab1[['CONTRACT_ID','ISSUER_COUNTRY','MERCHANT_COUNTRY','BIN_DESC','SECURITY_LEVEL','CARD_SCHEME','CREDIT_DEBIT','CONSUMER_CORPORATE','FLOW','AIB_IC_RATE','AIB_IC_PERC','AIB_IC_TOTAL','AIB_IC_BPS']]


# ## Attach AIB Lanes to Active Bambora Lanes 
# This is a left join that will show all active Bambora lanes on only those AIB lanes where there is congruence.

# In[61]:

#ab_bb_combo=pd.merge(bb1_contracts,ab1,on=['CONTRACT_ID','ISSUER_COUNTRY','MERCHANT_COUNTRY','CARD_SCHEME','CREDIT_DEBIT','CONSUMER_CORPORATE','SECURITY_LEVEL','IIN'],how='left')
ab_bb_combo=pd.merge(bb1_contracts,ab1,on=['CONTRACT_ID','ISSUER_COUNTRY','MERCHANT_COUNTRY','CARD_SCHEME','CREDIT_DEBIT','CONSUMER_CORPORATE','SECURITY_LEVEL','BIN_DESC'],how='left')


# In[62]:

ab_bb_combo.head()


# ### Only show those lanes where there is activity for AIB and Bambora
# This is done but filtering to only those results that have scheme fee information

# In[63]:

ab_bb_combo=ab_bb_combo[(ab_bb_combo['AIB_IC_BPS'].notnull())].drop_duplicates()


# In[64]:

ab_bb_combo.head()


# ### Only Show the Median aggregated by lane, contract ID, Credit/Debit and Card type, Flow

# In[65]:

#ab_bb_combo=ab_bb_combo.groupby(['CONTRACT_ID','ISSUER_COUNTRY','CARD_SCHEME','MERCHANT_COUNTRY','CREDIT_DEBIT','CONSUMER_CORPORATE','FLOW','SECURITY_LEVEL','IIN'],as_index=False)[['AIB_IC_BPS','AIB_SF_BPS']].median()
ab_bb_combo=ab_bb_combo.groupby(['CONTRACT_ID','ISSUER_COUNTRY','CARD_SCHEME','MERCHANT_COUNTRY','CREDIT_DEBIT','CONSUMER_CORPORATE','FLOW','SECURITY_LEVEL','BIN_DESC'],as_index=False)[['AIB_IC_BPS']].median()


# In[66]:

print ab_bb_combo.head()


# In[67]:

ab_bb_combo.to_csv('d:\\djohnson\\Desktop\\ab_bb_comp.csv')


# In[68]:

ab_bb_combo.info()


# ## Setup the Bambora Baseline Lanes, Flows, and SFs

# In[69]:

base=ab_bb_combo.drop(['FLOW','AIB_IC_BPS'],axis=1).drop_duplicates()


# In[70]:

bbbase=pd.merge(base,bb1,on=['CONTRACT_ID','ISSUER_COUNTRY','MERCHANT_COUNTRY','CARD_SCHEME','CREDIT_DEBIT','CONSUMER_CORPORATE','SECURITY_LEVEL'],how='left')


# In[71]:

bbbase=bbbase.rename(columns={'ROUNDED_TRXN_AMOUNT':'FLOW','FLOW':'FLOW_2'})


# In[72]:

bbbase.head()


# In[73]:

bbbase=bbbase.drop('BIN_DESC_y',axis=1)


# In[74]:

bbbase=bbbase.rename(columns={'BIN_DESC_x':'BIN_DESC'})


# In[75]:

bbbase.info()


# ### Link AIB and Bambora

# In[76]:

#ab_bb_combo=pd.merge(bbbase,ab_bb_combo,on=['CONTRACT_ID','ISSUER_COUNTRY','CARD_SCHEME','MERCHANT_COUNTRY','CREDIT_DEBIT','CONSUMER_CORPORATE','FLOW','SECURITY_LEVEL','IIN'],how='left')
ab_bb_combo=pd.merge(bbbase,ab_bb_combo,on=['CONTRACT_ID','ISSUER_COUNTRY','CARD_SCHEME','MERCHANT_COUNTRY','CREDIT_DEBIT','CONSUMER_CORPORATE','FLOW','SECURITY_LEVEL','BIN_DESC'],how='left')


# In[77]:

ab_bb_combo.head()


# ## Insert the Signal logic

# In[78]:

ab_bb_combo['IC_DIFF_%']=(ab_bb_combo['BB_IC_BPS']-ab_bb_combo['AIB_IC_BPS'])/ab_bb_combo['AIB_IC_BPS']


# In[79]:

ab_bb_combo['IC_SIGNAL']=''
ab_bb_combo['IC_SIGNAL']=ab_bb_combo['IC_DIFF_%'].apply(lambda x:'Signal' if (x>=.05) else '')


# ### Final Output

# In[80]:

ab_bb_combo=ab_bb_combo[['PERIOD'
                         ,'TRANSACTION_REF'
                         ,'TRANSACTION_TYPE'
                         ,'CONTRACT_ID'
                         ,'BIN_DESC'
                         ,'ISSUER_COUNTRY'
                         ,'MERCHANT_COUNTRY'
                         ,'REGIONALITY'
                         ,'CARD_SCHEME'
                         ,'CONSUMER_CORPORATE'
                         ,'CREDIT_DEBIT'
                         ,'SECURITY_LEVEL'
                         ,'VOLUME'
                         ,'FLOW'
                         ,'SF_FIXED_FEE'
                         ,'SF_PERC_FEE'
                         ,'SCHEME_TOTAL_FEE_EUR'
                         ,'BB_IC_TOTAL'
                         ,'BB_SF_BPS'
                         ,'BB_IC_BPS'
                         ,'AIB_IC_BPS'
                         ,'IC_DIFF_%'
                         ,'IC_SIGNAL']]


# In[81]:

ab_bb_combo.head()


# In[82]:

print 'total transactions'
print ab_bb_combo['TRANSACTION_REF'].count()
print 'total signals'
print ab_bb_combo['TRANSACTION_REF'][(ab_bb_combo['IC_SIGNAL']=='Signal')].count()


# In[83]:

ab_bb_combo.to_csv('d:\\djohnson\\Desktop\\aib to bambora comparison.csv')

