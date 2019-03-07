from __future__ import division
from numpy import pi
import pandas as pd
pd.set_option('display.float_format', lambda x: '%.3f' % x)
import numpy as np


# In[3]:


from bokeh.models.callbacks import CustomJS
from bokeh.plotting import figure, output_file, show
from bokeh.models import DatetimeTickFormatter
from bokeh.io import output_file, show
from bokeh.layouts import gridplot,column,row,widgetbox
from bokeh.models import Button
from bokeh.palettes import RdYlBu6,GnBu6, OrRd6
from bokeh.plotting import figure, curdoc
from bokeh.models.widgets import MultiSelect,DataTable,TableColumn,NumberFormatter,Slider,Panel,Tabs,Paragraph,Div
from bokeh.models.glyphs import VBar
from bokeh.models import LinearAxis,Range1d,FactorRange,ColumnDataSource
from bokeh.transform import cumsum
from bokeh.palettes import Category20c #colors for the pie chart


# In[4]:


from bokeh import __version__ as bokeh_version
from bokeh.io import output_notebook, show
from bokeh.plotting import figure

output_notebook()


# In[5]:


columns=['STATUSID','RECEIVEDDATE','DATEAUTHORISATION','SENDDATE','PAYMENTDATE','STATUSDATE'
         ,'MERCHANTID','MERCHANTNAME','ORDERID','CREDITCARDCOMPANY','CREDITDEBITINDICATOR'
         ,'CVVINDICATOR','CVVRESULT','CVVSERVICEINDICATOR','AVSINDICATOR','AVSRESULT','FRAUDCODE'
         ,'FRAUDINDICATOR','FRAUDRESULT','STTINDICATOR','MERCHANTREFERENCE','PAYMENTREFERENCE'
         ,'CUSTOMERID','COUNTRYCODE','AUTHORISEDCURRENCYCODE','AUTHORISEDAMOUNT','AMOUNT','SURNAME'
         ,'CITY','PREFIXSURNAME','STREET','ZIP','STATE','PROVIDERNAME','PAYMENTPROCESSOR','SERVICEPROVIDERID'
         ,'PAYMENTMETHODID','PAYMENTPRODUCTID','IIN','CVVINDICATOR','CVVDESC','AVSDESC','AVS_RESPONSE','CONS_CORP_BIN'
         ,'INTERCHANGE_RATE','INTERCHANGE_PERCENT_RATE','INTERCHANGE_FLAT_RATE','TRANSACTION_FLOW','ISSUING_BANK','CARD_SCHEME_BIN'
         ,'CRED_DEB_BIN','ipaddressmerchant']


# In[6]:


df=pd.read_csv('d:\\djohnson\\Desktop\\ctrip2.txt',skiprows=82,sep=';',error_bad_lines=False,warn_bad_lines=False,names=columns)


# In[7]:


dg_df=pd.read_csv('d:\\djohnson\\Desktop\\vantiv_downgrades.csv',error_bad_lines=False,warn_bad_lines=False)


# In[8]:


df=df.drop(len(df)-1)


# In[9]:


df['AMOUNT']=df['AMOUNT'].astype(float)
df['STATUSID']=df['STATUSID'].astype(float)
df['INTERCHANGE_RATE']=df['INTERCHANGE_RATE'].str.strip()
df['AVS_RESPONSE']=df['AVS_RESPONSE'].str.strip()
df['CREDITDEBITINDICATOR']=df['CREDITDEBITINDICATOR'].str.strip()
df['CARD_SCHEME_BIN']=df['CARD_SCHEME_BIN'].str.strip()
df['CRED_DEB_BIN']=df['CRED_DEB_BIN'].str.strip()
df['ipaddressmerchant']=df['ipaddressmerchant'].str.strip()
df['AVSDESC']=df['AVSDESC'].str.strip()
df['RECEIVEDDATE']=pd.to_datetime(df['RECEIVEDDATE'])
df['DATEAUTHORISATION']=pd.to_datetime(df['DATEAUTHORISATION'])
df['SENDDATE']=pd.to_datetime(df['SENDDATE'])
df['PAYMENTDATE']=pd.to_datetime(df['PAYMENTDATE'])
df['STATUSDATE']=pd.to_datetime(df['STATUSDATE'])


# In[10]:


df['RECEIVEDDATE']=df['RECEIVEDDATE'].dt.strftime('%Y/%m')
df['DATEAUTHORISATION']=df['DATEAUTHORISATION'].dt.strftime('%Y/%m')
df['SENDDATE']=df['SENDDATE'].dt.strftime('%Y/%m')
df['PAYMENTDATE']=df['PAYMENTDATE'].dt.strftime('%Y/%m')
df['STATUSDATE']=df['STATUSDATE'].dt.strftime('%Y/%m')


# In[11]:


#df.info()


# In[12]:


dg_df.head()


# In[13]:


df.head()


# In[14]:


df=pd.merge(df,dg_df,on='INTERCHANGE_RATE',how='left')


# ## Total Downgrades

# In[65]:


count=df[['RECEIVEDDATE','DOWNGRADE']]
count=count.groupby(['RECEIVEDDATE'],as_index=False).sum()
orders=df[['RECEIVEDDATE','ORDERID']]
orders=orders.groupby(['RECEIVEDDATE'],as_index=False).count()
count=pd.merge(count,orders,how='left',on=['RECEIVEDDATE'])
count['DOWNGRADE_PERCENTAGE']=count['DOWNGRADE']/count['ORDERID']

#in order to feed the information from the dataframe into the bar chart we will need to convert the infromation into lists
date=count['RECEIVEDDATE'].values.tolist() #x
dg_count=count['DOWNGRADE_PERCENTAGE'].values.tolist() #y
dg_orders=count['ORDERID'].values.tolist() #y2

#let's review our dataframe variables now converted to lists
#print date
#print dg_count
#print dg_orders

#let's have a look at the results in Bokeh
output_file("downgrades.html")

x=date
y=dg_count
y2=dg_orders
TOOLS="hover,save,wheel_zoom,pan,reset"

#create a figure
p1 = figure(x_range=x,plot_height=700, title="Ctrip Downgrade Percentages and Volumes",toolbar_location="above",tools=TOOLS,tooltips=[('Perctage', '@top{0.00%}')])
#fill the plot with the array information within the created figure
p1.vbar(x=date, top=y, width=0.9, legend='Downgrade Percentage')
#establish the range of the left y-axis
p1.y_range = Range1d(0,1) 

#title size
p1.title.text_font_size = '13pt'

#format the color and size of the border around the graphs
p1.border_fill_color = "whitesmoke"
p1.min_border_left = 80

#add in the axis lables
p1.xaxis.axis_label = "Date"
p1.yaxis.axis_label = "Downgrade Percentage"

#axis font size
p1.yaxis.axis_label_text_font_style='normal'
p1.yaxis.axis_label_text_font_size='12pt'

p1.xaxis.axis_label_text_font_style='normal'
p1.xaxis.axis_label_text_font_size='12pt'

#tick font size
p1.xaxis.major_label_text_font_size='9pt'
p1.yaxis.major_label_text_font_size='9pt'

p1.extra_y_ranges={"y2":Range1d(start=0,end=15000)}
p1.line(x,y2,color="red",y_range_name="y2",line_width=3,legend='Volume')
#p1.circle(x,y2,color="black",y_range_name="y2")
p1.add_layout(LinearAxis(y_range_name="y2"),'right')

#show(p1)


# ## Visa

# In[16]:


#visa
visa_sum=df[['RECEIVEDDATE','DOWNGRADE']][(df['CARD_SCHEME_BIN']=='VISA')]
visa_sum=visa_sum.groupby(['RECEIVEDDATE'],as_index=False).sum()
visa_count=df[['RECEIVEDDATE','ORDERID']][(df['CARD_SCHEME_BIN']=='VISA')]
visa_count=visa_count.groupby(['RECEIVEDDATE'],as_index=False).count()
visa_count=pd.merge(visa_count,visa_sum,how='left',on=['RECEIVEDDATE'])
visa_count['DOWNGRADE_PERCENTAGE']=visa_count['DOWNGRADE']/visa_count['ORDERID']

#in order to feed the information from the dataframe into the bar chart we will need to convert the infromation into lists
date=visa_count['RECEIVEDDATE'].values.tolist() #x
dg_count=visa_count['DOWNGRADE_PERCENTAGE'].values.tolist() #y
dg_orders=visa_count['ORDERID'].values.tolist() #y2

#let's review our dataframe variables now converted to lists
#print date
#print dg_count
#print dg_orders

#let's have a look at the results in Bokeh
output_file("downgrades.html")

x=date
y=dg_count
y2=dg_orders
TOOLS="hover,save,wheel_zoom,pan,reset"


p2 = figure(plot_height=700, title="Visa Ctrip Downgrade Percentages and Volumes", toolbar_location="above"            ,tools=TOOLS,tooltips=[('Perctage', '@top{0.00%}')]            ,x_range=p1.x_range, y_range=p1.y_range,extra_y_ranges=p1.extra_y_ranges)
p2.vbar(x=date, top=y, width=0.9, legend='Downgrade Percentage')
p2.y_range = Range1d(0,1)

#title size
p2.title.text_font_size = '13pt'

#format the color and size of the border around the graphs
p2.border_fill_color = "whitesmoke"
p2.min_border_left = 80

#add in the axis lables
p2.xaxis.axis_label = "Date"
p2.yaxis.axis_label = "Downgrade Percentage"

#axis font size
p2.yaxis.axis_label_text_font_style='normal'
p2.yaxis.axis_label_text_font_size='12pt'

p2.xaxis.axis_label_text_font_style='normal'
p2.xaxis.axis_label_text_font_size='12pt'

#tick font size
p2.xaxis.major_label_text_font_size='9pt'
p2.yaxis.major_label_text_font_size='9pt'

p2.extra_y_ranges={"y2":Range1d(start=0,end=15000)}
p2.line(x,y2,color="red",y_range_name="y2",line_width=3, legend='Volume')
p2.circle(x,y2,color="black",y_range_name="y2")
p2.add_layout(LinearAxis(y_range_name="y2"),'right')

#show(p2)


# ## MasterCard

# In[17]:


#masterCard
mc_sum=df[['RECEIVEDDATE','DOWNGRADE']][(df['CARD_SCHEME_BIN']=='MASTERCARD')]
mc_sum=mc_sum.groupby(['RECEIVEDDATE'],as_index=False).sum()
mc_count=df[['RECEIVEDDATE','ORDERID']][(df['CARD_SCHEME_BIN']=='MASTERCARD')]
mc_count=mc_count.groupby(['RECEIVEDDATE'],as_index=False).count()
mc_count=pd.merge(mc_count,mc_sum,how='left',on=['RECEIVEDDATE'])
mc_count['DOWNGRADE_PERCENTAGE']=mc_count['DOWNGRADE']/mc_count['ORDERID']

#in order to feed the information from the dataframe into the bar chart we will need to convert the infromation into lists
date=mc_count['RECEIVEDDATE'].values.tolist() #x
dg_count=mc_count['DOWNGRADE_PERCENTAGE'].values.tolist() #y
dg_orders=mc_count['ORDERID'].values.tolist() #y2

#let's review our dataframe variables now converted to lists
#print date
#print dg_count
#print dg_orders

#let's have a look at the results in Bokeh
output_file("downgrades.html")

x=date
y=dg_count
y2=dg_orders
TOOLS="hover,save,wheel_zoom,pan,reset"


p3 = figure(plot_height=700, title="MasterCard Ctrip Downgrade Percentages and Volumes", toolbar_location="above"            ,tools=TOOLS,tooltips=[('Perctage', '@top{0.00%}')]            ,x_range=p1.x_range, y_range=p1.y_range,extra_y_ranges=p1.extra_y_ranges)
p3.vbar(x=date, top=y, width=0.9, legend='Downgrade Percentage')
p3.y_range = Range1d(0,1)

#title size
p3.title.text_font_size = '13pt'

p3.border_fill_color = "whitesmoke"
p3.min_border_left = 80

#add in the axis lables
p3.xaxis.axis_label = "Date"
p3.yaxis.axis_label = "Downgrade Percentage"

#axis font size
p3.yaxis.axis_label_text_font_style='normal'
p3.yaxis.axis_label_text_font_size='12pt'

p3.xaxis.axis_label_text_font_style='normal'
p3.xaxis.axis_label_text_font_size='12pt'

#tick font size
p3.xaxis.major_label_text_font_size='9pt'
p3.yaxis.major_label_text_font_size='9pt'

p3.extra_y_ranges={"y2":Range1d(start=0,end=15000)}
p3.line(x,y2,color="red",y_range_name="y2",line_width=3l,legend='Volume')
p3.circle(x,y2,color="black",y_range_name="y2")
p3.add_layout(LinearAxis(y_range_name="y2"),'right')

#show(p3)


# ## Total No EIRF

# In[18]:


count_eirf=df[['RECEIVEDDATE','DOWNGRADE']][(df['EIRF']==0)]
count_eirf=count_eirf.groupby(['RECEIVEDDATE'],as_index=False).sum()
orders_eirf=df[['RECEIVEDDATE','ORDERID']][(df['EIRF']==0)]
orders_eirf=orders_eirf.groupby(['RECEIVEDDATE'],as_index=False).count()
count_eirf=pd.merge(count_eirf,orders_eirf,how='left',on=['RECEIVEDDATE'])
count_eirf['DOWNGRADE_PERCENTAGE']=count_eirf['DOWNGRADE']/count['ORDERID']

#in order to feed the information from the dataframe into the bar chart we will need to convert the infromation into lists
date=count_eirf['RECEIVEDDATE'].values.tolist() #x
dg_count=count_eirf['DOWNGRADE_PERCENTAGE'].values.tolist() #y
dg_orders=count_eirf['ORDERID'].values.tolist() #y2

#let's review our dataframe variables now converted to lists
#print date
#print dg_count
#print dg_orders

#let's have a look at the results in Bokeh
output_file("downgrades.html")

x=date
y=dg_count
y2=dg_orders
TOOLS="hover,save,wheel_zoom,pan,reset"


p4 = figure(plot_height=700, title="Ctrip Downgrade Percentages and Volumes", toolbar_location="above"            ,tools=TOOLS,tooltips=[('Perctage', '@top{0.00%}')]            ,x_range=p1.x_range, y_range=p1.y_range,extra_y_ranges=p1.extra_y_ranges)
p4.vbar(x=date, top=y, width=0.9,legend='Downgrade Percentage')
p4.y_range = Range1d(0,1)

#title size
p4.title.text_font_size = '13pt'

p4.border_fill_color = "whitesmoke"
p4.min_border_left = 80

#add in the axis lables
p4.xaxis.axis_label = "Date"
p4.yaxis.axis_label = "Downgrade Percentage"

#axis font size
p4.yaxis.axis_label_text_font_style='normal'
p4.yaxis.axis_label_text_font_size='12pt'

p4.xaxis.axis_label_text_font_style='normal'
p4.xaxis.axis_label_text_font_size='12pt'

#tick font size
p4.xaxis.major_label_text_font_size='9pt'
p4.yaxis.major_label_text_font_size='9pt'

p4.extra_y_ranges={"y2":Range1d(start=0,end=15000)}
p4.line(x,y2,color="red",y_range_name="y2",line_width=3,legend='Volume')
p4.circle(x,y2,color="black",y_range_name="y2")
p4.add_layout(LinearAxis(y_range_name="y2"),'right')

#show(p4)


# ## Visa No EIRF

# In[19]:


#visa
visa_sum_eirf=df[['RECEIVEDDATE','DOWNGRADE']][(df['CARD_SCHEME_BIN']=='VISA')&(df['EIRF']==0)]
visa_sum_eirf=visa_sum_eirf.groupby(['RECEIVEDDATE'],as_index=False).sum()
visa_count_eirf=df[['RECEIVEDDATE','ORDERID']][(df['CARD_SCHEME_BIN']=='VISA')&(df['EIRF']==0)]
visa_count_eirf=visa_count_eirf.groupby(['RECEIVEDDATE'],as_index=False).count()
visa_count_eirf=pd.merge(visa_count_eirf,visa_sum_eirf,how='left',on=['RECEIVEDDATE'])
visa_count_eirf['DOWNGRADE_PERCENTAGE']=visa_count_eirf['DOWNGRADE']/visa_count_eirf['ORDERID']

#in order to feed the information from the dataframe into the bar chart we will need to convert the infromation into lists
date=visa_count_eirf['RECEIVEDDATE'].values.tolist() #x
dg_count=visa_count_eirf['DOWNGRADE_PERCENTAGE'].values.tolist() #y
dg_orders=visa_count_eirf['ORDERID'].values.tolist() #y2

#let's review our dataframe variables now converted to lists
#print date
#print dg_count
#print dg_orders

#let's have a look at the results in Bokeh
output_file("downgrades.html")

x=date
y=dg_count
y2=dg_orders
TOOLS="hover,save,wheel_zoom,pan,reset"


p5 = figure(plot_height=700, title="Visa Ctrip Downgrade Percentages Volume", toolbar_location="above"            ,tools=TOOLS,tooltips=[('Perctage', '@top{0.00%}')]            ,x_range=p1.x_range, y_range=p1.y_range,extra_y_ranges=p1.extra_y_ranges)
p5.vbar(x=date, top=y, width=0.9,legend='Downgrade Percentage')
p5.y_range = Range1d(0,1)

#title size
p5.title.text_font_size = '13pt'

p5.border_fill_color = "whitesmoke"
p5.min_border_left = 80

#axis font size
p5.yaxis.axis_label_text_font_style='normal'
p5.yaxis.axis_label_text_font_size='12pt'

p5.xaxis.axis_label_text_font_style='normal'
p5.xaxis.axis_label_text_font_size='12pt'

#tick font size
p5.xaxis.major_label_text_font_size='9pt'
p5.yaxis.major_label_text_font_size='9pt'

p5.extra_y_ranges={"y2":Range1d(start=0,end=15000)}
p5.line(x,y2,color="red",y_range_name="y2",line_width=3,legend='Volume')
p5.circle(x,y2,color="black",y_range_name="y2")
p5.add_layout(LinearAxis(y_range_name="y2"),'right')

#show(p5)


# ## MasterCard No EIRF

# In[20]:


#visa
mc_sum_eirf=df[['RECEIVEDDATE','DOWNGRADE']][(df['CARD_SCHEME_BIN']=='MASTERCARD')&(df['EIRF']==0)]
mc_sum_eirf=mc_sum_eirf.groupby(['RECEIVEDDATE'],as_index=False).sum()
mc_count_eirf=df[['RECEIVEDDATE','ORDERID']][(df['CARD_SCHEME_BIN']=='MASTERCARD')&(df['EIRF']==0)]
mc_count_eirf=mc_count_eirf.groupby(['RECEIVEDDATE'],as_index=False).count()
mc_count_eirf=pd.merge(mc_count_eirf,mc_sum_eirf,how='left',on=['RECEIVEDDATE'])
mc_count_eirf['DOWNGRADE_PERCENTAGE']=mc_count_eirf['DOWNGRADE']/mc_count_eirf['ORDERID']

#in order to feed the information from the dataframe into the bar chart we will need to convert the infromation into lists
date=mc_count_eirf['RECEIVEDDATE'].values.tolist() #x
dg_count=mc_count_eirf['DOWNGRADE_PERCENTAGE'].values.tolist() #y
dg_orders=mc_count_eirf['ORDERID'].values.tolist() #y2

#let's review our dataframe variables now converted to lists
print date
print dg_count
print dg_orders

#let's have a look at the results in Bokeh
output_file("downgrades.html")

x=date
y=dg_count
y2=dg_orders
TOOLS="hover,save,wheel_zoom,pan,reset"

p6 = figure(plot_height=700, title="MasterCard Ctrip Downgrade Percentages and Volumes", toolbar_location="above"            ,tools=TOOLS,tooltips=[('Perctage', '@top{0.00%}')]            ,x_range=p1.x_range, y_range=p1.y_range,extra_y_ranges=p1.extra_y_ranges)
p6.vbar(x=date, top=y, width=0.9,legend='Downgrade Percentage')
p6.y_range = Range1d(0,1)

#title size
p6.title.text_font_size = '13pt'

p6.border_fill_color = "whitesmoke"
p6.min_border_left = 80

#axis font size
p6.yaxis.axis_label_text_font_style='normal'
p6.yaxis.axis_label_text_font_size='12pt'

p6.xaxis.axis_label_text_font_style='normal'
p6.xaxis.axis_label_text_font_size='12pt'

#tick font size
p6.xaxis.major_label_text_font_size='9pt'
p6.yaxis.major_label_text_font_size='9pt'

p6.extra_y_ranges={"y2":Range1d(start=0,end=15000)}
p6.line(x,y2,color="red",y_range_name="y2",line_width=3,legend='Volume')
p6.circle(x,y2,color="black",y_range_name="y2")
p6.add_layout(LinearAxis(y_range_name="y2"),'right')

#show(p5)


# ## Total AVS Particpation %

# In[21]:


'''lets declare the lists we will need to populate the axes of these bar charts ultimately what 
    we want to see is the percentage each avs description category makes up within each time period
    using the hbar chart and a for loop I've developed or generated a method to doing this
'''

#lets establish the lists. Please note that over time these lists will need to be updated with additional fields this just happens with time. Nothing stays the same forever.
avs_desc=['AVS Not Performed','Full AVS','Partial AVS','Neither ZIP nor address match','Unsupp/Inconc AVS','CVV Match']
dates=['2017/07','2017/08','2017/12','2018/01','2018/02','2018/03','2018/04','2018/05','2018/06']

'''Since the avs_desacription categories is te variable that will be broken out percentage wise we will need to create six lists each with a date that corresponds to te description
    for example we will want to see what percentage to the avs downgrade participation percentage was AVS not performed. This can range between 0 and 100%
    since these lists have to act as varaibles in one step of the process I created this rubric to helo keep track of what each variable is

    #a=AVS Not Performed
    #b=Full AVS
    #c=Partial AVS
    #d=Neither ZIP nor address match
    #e=Unsupp/Inconc AVS
    #f=CVV Match
'''

#create each list and then put them into one master list. The master lists is a lists with six lists that can be called and updated accordingly in the for loop
a=[];b=[];c=[];d=[];e=[];f=[]
master_list=[a,b,c,d,e,f]

'''The for loop created basically goes into each lists and enters in the downgrade percentage for a coresponding date
    for example we will see on one date AVS not perfomred was 80% on another day it was 17% and so on until the last date is called
    each result is then appended into the whatever master lists sublist has been called in this case we have 6 list and 9 dates
    therefore each avs description should have 9 figures in their corresponding lists'''

for ml in range(0,len(master_list)): #this calls the six lists basically calling one at a time
    master=master_list[ml]
    avs_selection=avs_desc[ml] #this calls one of the six descriptions one at a time in line with the masterlist for loop count and applies this variable in the equation below
    for dt in range(0,len(dates)): #This for calls the 9 dates and is a sub for-loop under the master which dictates that for each of the six categories nine dates will be applied
        date_selection=dates[dt]
        try:
            percentage=round(float(df['ORDERID'][(df['RECEIVEDDATE']==date_selection)&(df['DOWNGRADE']==1)&(df['AVSDESC']==avs_selection)].count())/float(df['ORDERID'][(df['RECEIVEDDATE']==date_selection)&(df['DOWNGRADE']==1)].count()),3)
        except ZeroDivisionError:
            percentage=0
        master.append(percentage) #apply one of the nine results from the equations to the master list 
        
#Build the dictionary that will be used to generate the chart
avs_participation={
    'dt' : dates,
    'AVS Not Performed':a,
    'Full AVS':b,
    'Partial AVS':c,
    'Neither ZIP nor address match':d,
    'Unsupp/Inconc AVS':e,
    'CVV Match':f
}
#create the hbar figure we want to see. The end result should be a 100% stacked bar chart
p7 = figure(y_range=dates, plot_height=700, x_range=(0,1), title="Ctrip Downgrade AVS Performance Metrics",
           toolbar_location=None,tools=TOOLS,tooltips="$name @dt: @$name{0.00%}")
p7.hbar_stack(avs_desc, y='dt', height=0.4, color=GnBu6,source=ColumnDataSource(avs_participation))

#title size
p7.title.text_font_size = '13pt'

p7.border_fill_color = "whitesmoke"
p7.min_border_left = 80

#add in the axis lables
p7.yaxis.axis_label = "Date"
p7.xaxis.axis_label = "AVS Downgrade Reason Percentage"

#axis font size
p7.yaxis.axis_label_text_font_style='normal'
p7.yaxis.axis_label_text_font_size='12pt'

p7.xaxis.axis_label_text_font_style='normal'
p7.xaxis.axis_label_text_font_size='12pt'

#tick font size
p7.xaxis.major_label_text_font_size='9pt'
p7.yaxis.major_label_text_font_size='9pt'


#show(p7)


# ## Visa AVS Particpation %

# In[22]:


'''lets declare the lists we will need to populate the axes of these bar charts ultimately what 
    we want to see is the percentage each avs description category makes up within each time period
    using the hbar chart and a for loop I've developed or generated a method to doing this
'''

#lets establish the lists. Please note that over time these lists will need to be updated with additional fields this just happens with time. Nothing stays the same forever.
avs_desc=['AVS Not Performed','Full AVS','Partial AVS','Neither ZIP nor address match','Unsupp/Inconc AVS','CVV Match']
dates=['2017/07','2017/08','2017/12','2018/01','2018/02','2018/03','2018/04','2018/05','2018/06']

'''Since the avs_desacription categories is te variable that will be broken out percentage wise we will need to create six lists each with a date that corresponds to te description
    for example we will want to see what percentage to the avs downgrade participation percentage was AVS not performed. This can range between 0 and 100%
    since these lists have to act as varaibles in one step of the process I created this rubric to helo keep track of what each variable is

    #a=AVS Not Performed
    #b=Full AVS
    #c=Partial AVS
    #d=Neither ZIP nor address match
    #e=Unsupp/Inconc AVS
    #f=CVV Match
'''

#create each list and then put them into one master list. The master lists is a lists with six lists that can be called and updated accordingly in the for loop
a=[];b=[];c=[];d=[];e=[];f=[]
master_list=[a,b,c,d,e,f]

'''The for loop created basically goes into each lists and enters in the downgrade percentage for a coresponding date
    for example we will see on one date AVS not perfomred was 80% on another day it was 17% and so on until the last date is called
    each result is then appended into the whatever master lists sublist has been called in this case we have 6 list and 9 dates
    therefore each avs description should have 9 figures in their corresponding lists'''

for ml in range(0,len(master_list)): #this calls the six lists basically calling one at a time
    master=master_list[ml]
    avs_selection=avs_desc[ml] #this calls one of the six descriptions one at a time in line with the masterlist for loop count and applies this variable in the equation below
    for dt in range(0,len(dates)): #This for calls the 9 dates and is a sub for-loop under the master which dictates that for each of the six categories nine dates will be applied
        date_selection=dates[dt]
        try:
            percentage=round(float(df['ORDERID'][(df['RECEIVEDDATE']==date_selection)&(df['DOWNGRADE']==1)&(df['AVSDESC']==avs_selection)&(df['CARD_SCHEME_BIN']=='VISA')].count())/                             float(df['ORDERID'][(df['RECEIVEDDATE']==date_selection)&(df['DOWNGRADE']==1)&(df['CARD_SCHEME_BIN']=='VISA')].count()),3)
        except ZeroDivisionError:
            percentage=0
        master.append(percentage) #apply one of the nine results from the equations to the master list 
        
#Build the dictionary that will be used to generate the chart
avs_participation={
    'dt' : dates,
    'AVS Not Performed':a,
    'Full AVS':b,
    'Partial AVS':c,
    'Neither ZIP nor address match':d,
    'Unsupp/Inconc AVS':e,
    'CVV Match':f
}
#create the hbar figure we want to see. The end result should be a 100% stacked bar chart
p8 = figure(y_range=dates, plot_height=700, x_range=(0,1), title="Visa Ctrip Downgrade AVS Performance Metrics",
           toolbar_location=None,tooltips="$name @dt: @$name{0.00%}")
p8.hbar_stack(avs_desc, y='dt', height=0.4, color=GnBu6, source=ColumnDataSource(avs_participation))

#title size
p8.title.text_font_size = '13pt'

p8.border_fill_color = "whitesmoke"
p8.min_border_left = 80

#add in the axis lables
p8.yaxis.axis_label = "Date"
p8.xaxis.axis_label = "AVS Downgrade Reason Percentage"

#axis font size
p8.yaxis.axis_label_text_font_style='normal'
p8.yaxis.axis_label_text_font_size='12pt'

p8.xaxis.axis_label_text_font_style='normal'
p8.xaxis.axis_label_text_font_size='12pt'

#tick font size
p8.xaxis.major_label_text_font_size='9pt'
p8.yaxis.major_label_text_font_size='9pt'


#show(p8)


# ## MasterCard AVS Particpation %

# In[23]:


'''lets declare the lists we will need to populate the axes of these bar charts ultimately what 
    we want to see is the percentage each avs description category makes up within each time period
    using the hbar chart and a for loop I've developed or generated a method to doing this
'''

#lets establish the lists. Please note that over time these lists will need to be updated with additional fields this just happens with time. Nothing stays the same forever.
avs_desc=['AVS Not Performed','Full AVS','Partial AVS','Neither ZIP nor address match','Unsupp/Inconc AVS','CVV Match']
dates=['2017/07','2017/08','2017/12','2018/01','2018/02','2018/03','2018/04','2018/05','2018/06']

'''Since the avs_desacription categories is te variable that will be broken out percentage wise we will need to create six lists each with a date that corresponds to te description
    for example we will want to see what percentage to the avs downgrade participation percentage was AVS not performed. This can range between 0 and 100%
    since these lists have to act as varaibles in one step of the process I created this rubric to helo keep track of what each variable is

    #a=AVS Not Performed
    #b=Full AVS
    #c=Partial AVS
    #d=Neither ZIP nor address match
    #e=Unsupp/Inconc AVS
    #f=CVV Match
'''

#create each list and then put them into one master list. The master lists is a lists with six lists that can be called and updated accordingly in the for loop
a=[];b=[];c=[];d=[];e=[];f=[]
master_list=[a,b,c,d,e,f]

'''The for loop created basically goes into each lists and enters in the downgrade percentage for a coresponding date
    for example we will see on one date AVS not perfomred was 80% on another day it was 17% and so on until the last date is called
    each result is then appended into the whatever master lists sublist has been called in this case we have 6 list and 9 dates
    therefore each avs description should have 9 figures in their corresponding lists'''

for ml in range(0,len(master_list)): #this calls the six lists basically calling one at a time
    master=master_list[ml]
    avs_selection=avs_desc[ml] #this calls one of the six descriptions one at a time in line with the masterlist for loop count and applies this variable in the equation below
    for dt in range(0,len(dates)): #This for calls the 9 dates and is a sub for-loop under the master which dictates that for each of the six categories nine dates will be applied
        date_selection=dates[dt]
        try:
            percentage=round(float(df['ORDERID'][(df['RECEIVEDDATE']==date_selection)&(df['DOWNGRADE']==1)&(df['AVSDESC']==avs_selection)&(df['CARD_SCHEME_BIN']=='MASTERCARD')].count())/                             float(df['ORDERID'][(df['RECEIVEDDATE']==date_selection)&(df['DOWNGRADE']==1)&(df['CARD_SCHEME_BIN']=='MASTERCARD')].count()),3)
        except ZeroDivisionError:
            percentage=0
        master.append(percentage) #apply one of the nine results from the equations to the master list 
        
#Build the dictionary that will be used to generate the chart
avs_participation={
    'dt' : dates,
    'AVS Not Performed':a,
    'Full AVS':b,
    'Partial AVS':c,
    'Neither ZIP nor address match':d,
    'Unsupp/Inconc AVS':e,
    'CVV Match':f
}
#create the hbar figure we want to see. The end result should be a 100% stacked bar chart
p9 = figure(y_range=dates, plot_height=700, x_range=(0,1), title="MasterCard Ctrip Downgrade AVS Performance Metrics",
           toolbar_location=None,tooltips="$name @dt: @$name{0.00%}")
p9.hbar_stack(avs_desc, y='dt', height=0.4, color=GnBu6, source=ColumnDataSource(avs_participation))

#title size
p9.title.text_font_size = '13pt'

p9.border_fill_color = "whitesmoke"
p9.min_border_left = 80

#add in the axis lables
p9.yaxis.axis_label = "Date"
p9.xaxis.axis_label = "AVS Downgrade Reason Percentage"

#axis font size
p9.yaxis.axis_label_text_font_style='normal'
p9.yaxis.axis_label_text_font_size='12pt'

p9.xaxis.axis_label_text_font_style='normal'
p9.xaxis.axis_label_text_font_size='12pt'

#tick font size
p9.xaxis.major_label_text_font_size='9pt'
p9.yaxis.major_label_text_font_size='9pt'

#show(p9)


# ## Total AVS Particpation % No EIRF

# In[24]:


'''lets declare the lists we will need to populate the axes of these bar charts ultimately what 
    we want to see is the percentage each avs description category makes up within each time period
    using the hbar chart and a for loop I've developed or generated a method to doing this
'''

#lets establish the lists. Please note that over time these lists will need to be updated with additional fields this just happens with time. Nothing stays the same forever.
avs_desc=['AVS Not Performed','Full AVS','Partial AVS','Neither ZIP nor address match','Unsupp/Inconc AVS','CVV Match']
dates=['2017/07','2017/08','2017/12','2018/01','2018/02','2018/03','2018/04','2018/05','2018/06']

'''Since the avs_desacription categories is te variable that will be broken out percentage wise we will need to create six lists each with a date that corresponds to te description
    for example we will want to see what percentage to the avs downgrade participation percentage was AVS not performed. This can range between 0 and 100%
    since these lists have to act as varaibles in one step of the process I created this rubric to helo keep track of what each variable is

    #a=AVS Not Performed
    #b=Full AVS
    #c=Partial AVS
    #d=Neither ZIP nor address match
    #e=Unsupp/Inconc AVS
    #f=CVV Match
'''

#create each list and then put them into one master list. The master lists is a lists with six lists that can be called and updated accordingly in the for loop
a=[];b=[];c=[];d=[];e=[];f=[]
master_list=[a,b,c,d,e,f]

'''The for loop created basically goes into each lists and enters in the downgrade percentage for a coresponding date
    for example we will see on one date AVS not perfomred was 80% on another day it was 17% and so on until the last date is called
    each result is then appended into the whatever master lists sublist has been called in this case we have 6 list and 9 dates
    therefore each avs description should have 9 figures in their corresponding lists'''

for ml in range(0,len(master_list)): #this calls the six lists basically calling one at a time
    master=master_list[ml]
    avs_selection=avs_desc[ml] #this calls one of the six descriptions one at a time in line with the masterlist for loop count and applies this variable in the equation below
    for dt in range(0,len(dates)): #This for calls the 9 dates and is a sub for-loop under the master which dictates that for each of the six categories nine dates will be applied
        date_selection=dates[dt]
        try:
            percentage=round(float(df['ORDERID'][(df['RECEIVEDDATE']==date_selection)&(df['DOWNGRADE']==1)&(df['AVSDESC']==avs_selection)&(df['EIRF']==0)].count())                             /float(df['ORDERID'][(df['RECEIVEDDATE']==date_selection)&(df['DOWNGRADE']==1)&(df['EIRF']==0)].count()),3)
        except ZeroDivisionError:
            percentage=0
        master.append(percentage) #apply one of the nine results from the equations to the master list 
        
#Build the dictionary that will be used to generate the chart
avs_participation={
    'dt' : dates,
    'AVS Not Performed':a,
    'Full AVS':b,
    'Partial AVS':c,
    'Neither ZIP nor address match':d,
    'Unsupp/Inconc AVS':e,
    'CVV Match':f
}
#create the hbar figure we want to see. The end result should be a 100% stacked bar chart
p10 = figure(y_range=dates, plot_height=700, x_range=(0,1), title="Ctrip Downgrade AVS Performance Metrics",
           toolbar_location=None,tooltips="$name @dt: @$name{0.00%}")
p10.hbar_stack(avs_desc, y='dt', height=0.4, color=GnBu6, source=ColumnDataSource(avs_participation))

#title size
p10.title.text_font_size = '13pt'

p10.border_fill_color = "whitesmoke"
p10.min_border_left = 80

#add in the axis lables
p10.yaxis.axis_label = "Date"
p10.xaxis.axis_label = "AVS Downgrade Reason Percentage"

#axis font size
p10.yaxis.axis_label_text_font_style='normal'
p10.yaxis.axis_label_text_font_size='12pt'

p10.xaxis.axis_label_text_font_style='normal'
p10.xaxis.axis_label_text_font_size='12pt'

#tick font size
p10.xaxis.major_label_text_font_size='9pt'
p10.yaxis.major_label_text_font_size='9pt'

#show(p10)


# ## Visa AVS Particpation % No EIRF

# In[25]:


'''lets declare the lists we will need to populate the axes of these bar charts ultimately what 
    we want to see is the percentage each avs description category makes up within each time period
    using the hbar chart and a for loop I've developed or generated a method to doing this
'''

#lets establish the lists. Please note that over time these lists will need to be updated with additional fields this just happens with time. Nothing stays the same forever.
avs_desc=['AVS Not Performed','Full AVS','Partial AVS','Neither ZIP nor address match','Unsupp/Inconc AVS','CVV Match']
dates=['2017/07','2017/08','2017/12','2018/01','2018/02','2018/03','2018/04','2018/05','2018/06']

'''Since the avs_desacription categories is te variable that will be broken out percentage wise we will need to create six lists each with a date that corresponds to te description
    for example we will want to see what percentage to the avs downgrade participation percentage was AVS not performed. This can range between 0 and 100%
    since these lists have to act as varaibles in one step of the process I created this rubric to helo keep track of what each variable is

    #a=AVS Not Performed
    #b=Full AVS
    #c=Partial AVS
    #d=Neither ZIP nor address match
    #e=Unsupp/Inconc AVS
    #f=CVV Match
'''

#create each list and then put them into one master list. The master lists is a lists with six lists that can be called and updated accordingly in the for loop
a=[];b=[];c=[];d=[];e=[];f=[]
master_list=[a,b,c,d,e,f]

'''The for loop created basically goes into each lists and enters in the downgrade percentage for a coresponding date
    for example we will see on one date AVS not perfomred was 80% on another day it was 17% and so on until the last date is called
    each result is then appended into the whatever master lists sublist has been called in this case we have 6 list and 9 dates
    therefore each avs description should have 9 figures in their corresponding lists'''

for ml in range(0,len(master_list)): #this calls the six lists basically calling one at a time
    master=master_list[ml]
    avs_selection=avs_desc[ml] #this calls one of the six descriptions one at a time in line with the masterlist for loop count and applies this variable in the equation below
    for dt in range(0,len(dates)): #This for calls the 9 dates and is a sub for-loop under the master which dictates that for each of the six categories nine dates will be applied
        date_selection=dates[dt]
        try:
            percentage=round(float(df['ORDERID'][(df['RECEIVEDDATE']==date_selection)&(df['DOWNGRADE']==1)&(df['AVSDESC']==avs_selection)&(df['EIRF']==0)&(df['CARD_SCHEME_BIN']=='VISA')].count())                             /float(df['ORDERID'][(df['RECEIVEDDATE']==date_selection)&(df['DOWNGRADE']==1)&(df['EIRF']==0)&(df['CARD_SCHEME_BIN']=='VISA')].count()),3)
        except ZeroDivisionError:
            percentage=0
        master.append(percentage) #apply one of the nine results from the equations to the master list 
        
#Build the dictionary that will be used to generate the chart
avs_participation={
    'dt' : dates,
    'AVS Not Performed':a,
    'Full AVS':b,
    'Partial AVS':c,
    'Neither ZIP nor address match':d,
    'Unsupp/Inconc AVS':e,
    'CVV Match':f
}
#create the hbar figure we want to see. The end result should be a 100% stacked bar chart
p11 = figure(y_range=dates, plot_height=700, x_range=(0,1), title="Visa Ctrip Downgrade AVS Performance Metrics",
           toolbar_location=None,tooltips="$name @dt: @$name{0.00%}")
p11.hbar_stack(avs_desc, y='dt', height=0.4, color=GnBu6, source=ColumnDataSource(avs_participation))

#title size
p11.title.text_font_size = '13pt'

p11.border_fill_color = "whitesmoke"
p11.min_border_left = 80

#add in the axis lables
p11.yaxis.axis_label = "Date"
p11.xaxis.axis_label = "AVS Downgrade Reason Percentage"

#axis font size
p11.yaxis.axis_label_text_font_style='normal'
p11.yaxis.axis_label_text_font_size='12pt'

p11.xaxis.axis_label_text_font_style='normal'
p11.xaxis.axis_label_text_font_size='12pt'

#tick font size
p11.xaxis.major_label_text_font_size='9pt'
p11.yaxis.major_label_text_font_size='9pt'

#show(p11)


# ## MasterCard AVS Particpation % No EIRF

# In[26]:


'''lets declare the lists we will need to populate the axes of these bar charts ultimately what 
    we want to see is the percentage each avs description category makes up within each time period
    using the hbar chart and a for loop I've developed or generated a method to doing this
'''

#lets establish the lists. Please note that over time these lists will need to be updated with additional fields this just happens with time. Nothing stays the same forever.
avs_desc=['AVS Not Performed','Full AVS','Partial AVS','Neither ZIP nor address match','Unsupp/Inconc AVS','CVV Match']
dates=['2017/07','2017/08','2017/12','2018/01','2018/02','2018/03','2018/04','2018/05','2018/06']

'''Since the avs_desacription categories is te variable that will be broken out percentage wise we will need to create six lists each with a date that corresponds to te description
    for example we will want to see what percentage to the avs downgrade participation percentage was AVS not performed. This can range between 0 and 100%
    since these lists have to act as varaibles in one step of the process I created this rubric to helo keep track of what each variable is

    #a=AVS Not Performed
    #b=Full AVS
    #c=Partial AVS
    #d=Neither ZIP nor address match
    #e=Unsupp/Inconc AVS
    #f=CVV Match
'''

#create each list and then put them into one master list. The master lists is a lists with six lists that can be called and updated accordingly in the for loop
a=[];b=[];c=[];d=[];e=[];f=[]
master_list=[a,b,c,d,e,f]

'''The for loop created basically goes into each lists and enters in the downgrade percentage for a coresponding date
    for example we will see on one date AVS not perfomred was 80% on another day it was 17% and so on until the last date is called
    each result is then appended into the whatever master lists sublist has been called in this case we have 6 list and 9 dates
    therefore each avs description should have 9 figures in their corresponding lists'''

for ml in range(0,len(master_list)): #this calls the six lists basically calling one at a time
    master=master_list[ml]
    avs_selection=avs_desc[ml] #this calls one of the six descriptions one at a time in line with the masterlist for loop count and applies this variable in the equation below
    for dt in range(0,len(dates)): #This for calls the 9 dates and is a sub for-loop under the master which dictates that for each of the six categories nine dates will be applied
        date_selection=dates[dt]
        try:
            percentage=round(float(df['ORDERID'][(df['RECEIVEDDATE']==date_selection)&(df['DOWNGRADE']==1)&(df['AVSDESC']==avs_selection)&(df['EIRF']==0)&(df['CARD_SCHEME_BIN']=='MASTERCARD')].count())                             /float(df['ORDERID'][(df['RECEIVEDDATE']==date_selection)&(df['DOWNGRADE']==1)&(df['EIRF']==0)&(df['CARD_SCHEME_BIN']=='MASTERCARD')].count()),3)
        except ZeroDivisionError:
            percentage=0
        master.append(percentage) #apply one of the nine results from the equations to the master list 
        
#Build the dictionary that will be used to generate the chart
avs_participation={
    'dt' : dates,
    'AVS Not Performed':a,
    'Full AVS':b,
    'Partial AVS':c,
    'Neither ZIP nor address match':d,
    'Unsupp/Inconc AVS':e,
    'CVV Match':f
}
#create the hbar figure we want to see. The end result should be a 100% stacked bar chart
p12 = figure(y_range=dates, plot_height=700, x_range=(0,1), title="MasterCard Ctrip Downgrade AVS Performance Metrics",
           toolbar_location=None,tooltips="$name @dt: @$name{0.00%}")
p12.hbar_stack(avs_desc, y='dt', height=0.4, color=GnBu6, source=ColumnDataSource(avs_participation))

#title size
p12.title.text_font_size = '13pt'

p12.border_fill_color = "whitesmoke"
p12.min_border_left = 80

#add in the axis lables
p12.yaxis.axis_label = "Date"
p12.xaxis.axis_label = "AVS Downgrade Reason Percentage"

#axis font size
p12.yaxis.axis_label_text_font_style='normal'
p12.yaxis.axis_label_text_font_size='12pt'

p12.xaxis.axis_label_text_font_style='normal'
p12.xaxis.axis_label_text_font_size='12pt'

#tick font size
p12.xaxis.major_label_text_font_size='9pt'
p12.yaxis.major_label_text_font_size='9pt'


#show(p12)


# ## Credit Debit Pie Chart

# In[27]:


deb_credit_perc=df[['CRED_DEB_BIN','ORDERID']][(df['DOWNGRADE']==1)&(df['CRED_DEB_BIN']!='')]
deb_credit_perc=deb_credit_perc.groupby (['CRED_DEB_BIN'],as_index=False).count()
deb_credit_perc_total=deb_credit_perc['ORDERID'].sum()
deb_credit_perc['PERCENTAGE']=(deb_credit_perc['ORDERID']/deb_credit_perc_total)* 2*pi
deb_credit_perc['PERCENTAGE_LABEL']=(deb_credit_perc['ORDERID']/deb_credit_perc_total)

deb_credit_perc['color']=''
deb_credit_perc['color'][(deb_credit_perc['CRED_DEB_BIN']=='CREDIT')] ='blue'
deb_credit_perc['color'][(deb_credit_perc['CRED_DEB_BIN']=='DEBIT')] ='red'

#print deb_credit_perc

p13 = figure(plot_height=700, title="Ctrip Downgrade Credit Debit Breakdown",             toolbar_location=None,tools="hover"            ,tooltips=[('Perctage', '@PERCENTAGE_LABEL{0.00%}')])

p13.wedge(x=0, y=0, radius=0.7,
        start_angle=cumsum('PERCENTAGE', include_zero=True), end_angle=cumsum('PERCENTAGE'),
        line_color="white", fill_color='color', source=deb_credit_perc,legend='CRED_DEB_BIN')

#title size
p13.title.text_font_size = '13pt'

p13.border_fill_color = "whitesmoke"
p13.min_border_left = 80

#show(p13)


# ## Visa and MasterCard Pie Chart

# In[28]:


card_type_perc=df[['CARD_SCHEME_BIN','ORDERID']][(df['DOWNGRADE']==1)&(df['CARD_SCHEME_BIN']!='')]
card_type_perc=card_type_perc.groupby (['CARD_SCHEME_BIN'],as_index=False).count()
card_type_perc_total=card_type_perc['ORDERID'].sum()
card_type_perc['PERCENTAGE']=(card_type_perc['ORDERID']/card_type_perc_total)* 2*pi
card_type_perc['PERCENTAGE_LABEL']=(card_type_perc['ORDERID']/card_type_perc_total)

card_type_perc['color']=''
card_type_perc['color'][(card_type_perc['CARD_SCHEME_BIN']=='VISA')] ='blue'
card_type_perc['color'][(card_type_perc['CARD_SCHEME_BIN']=='MASTERCARD')] ='red'

#print card_type_perc

p14 = figure(plot_height=700, title="Visa and MasterCard Ctrip Downgrade Credit Debit Breakdown",             toolbar_location=None,tools="hover"             ,tooltips=[('Perctage', '@PERCENTAGE_LABEL{0.00%}')])           

p14.wedge(x=0, y=0, radius=0.7,
        start_angle=cumsum('PERCENTAGE', include_zero=True), end_angle=cumsum('PERCENTAGE'),
        line_color="white", fill_color='color', source=card_type_perc,legend='CARD_SCHEME_BIN')

p14.title.text_font_size = '13pt'

p14.border_fill_color = "whitesmoke"
p14.min_border_left = 80

#show(p14)


# ## Credit Debit Pie Chart Excluding EIRF

# In[29]:


deb_credit_perc=df[['CRED_DEB_BIN','ORDERID']][(df['DOWNGRADE']==1)&(df['CRED_DEB_BIN']!='')&(df['EIRF']==0)]
deb_credit_perc=deb_credit_perc.groupby (['CRED_DEB_BIN'],as_index=False).count()
deb_credit_perc_total=deb_credit_perc['ORDERID'].sum()
deb_credit_perc['PERCENTAGE']=(deb_credit_perc['ORDERID']/deb_credit_perc_total)* 2*pi
deb_credit_perc['PERCENTAGE_LABEL']=(deb_credit_perc['ORDERID']/deb_credit_perc_total)

deb_credit_perc['color']=''
deb_credit_perc['color'][(deb_credit_perc['CRED_DEB_BIN']=='CREDIT')] ='blue'
deb_credit_perc['color'][(deb_credit_perc['CRED_DEB_BIN']=='DEBIT')] ='red'

#print deb_credit_perc

p15 = figure(plot_height=700, title="Ctrip Downgrade Credit Debit Breakdown",             toolbar_location=None,tools="hover"             ,tooltips=[('Perctage', '@PERCENTAGE_LABEL{0.00%}')])  

p15.wedge(x=0, y=0, radius=0.7,
        start_angle=cumsum('PERCENTAGE', include_zero=True), end_angle=cumsum('PERCENTAGE'),
        line_color="white", fill_color='color', source=deb_credit_perc,legend='CRED_DEB_BIN')

p15.title.text_font_size = '13pt'

p15.border_fill_color = "whitesmoke"
p15.min_border_left = 80

#show(p15)


# ## Visa and MasterCard Pie Chart Excluding EIRF

# In[30]:


card_type_perc=df[['CARD_SCHEME_BIN','ORDERID']][(df['DOWNGRADE']==1)&(df['CARD_SCHEME_BIN']!='')&(df['EIRF']==0)]
card_type_perc=card_type_perc.groupby (['CARD_SCHEME_BIN'],as_index=False).count()
card_type_perc_total=card_type_perc['ORDERID'].sum()
card_type_perc['PERCENTAGE']=(card_type_perc['ORDERID']/card_type_perc_total)* 2*pi
card_type_perc['PERCENTAGE_LABEL']=(card_type_perc['ORDERID']/card_type_perc_total)

card_type_perc['color']=''
card_type_perc['color'][(card_type_perc['CARD_SCHEME_BIN']=='VISA')] ='blue'
card_type_perc['color'][(card_type_perc['CARD_SCHEME_BIN']=='MASTERCARD')] ='red'

#print card_type_perc

p16 = figure(plot_height=700, title="Visa and MasterCard Ctrip Downgrade Credit Debit Breakdown",             toolbar_location=None,tools="hover"             ,tooltips=[('Perctage', '@PERCENTAGE_LABEL{0.00%}')]) 

p16.wedge(x=0, y=0, radius=0.7,
        start_angle=cumsum('PERCENTAGE', include_zero=True), end_angle=cumsum('PERCENTAGE'),
        line_color="white", fill_color='color', source=card_type_perc,legend='CARD_SCHEME_BIN')

#title size
p16.title.text_font_size = '13pt'

p16.border_fill_color = "whitesmoke"
p16.min_border_left = 80

#show(p16)


# ## Updateable Data Table

# In[31]:


df_tbl_1=df[['RECEIVEDDATE','AMOUNT','INTERCHANGE_PERCENT_RATE_y','INTERCHANGE_FLAT_RATE_y']][(df['DOWNGRADE']==1)&(df['EIRF']==0)]
df_tbl_1['DOWNGRADED_COST']=df_tbl_1['AMOUNT']*df_tbl_1['INTERCHANGE_PERCENT_RATE_y']
df_tbl_2=df_tbl_1[['RECEIVEDDATE','DOWNGRADED_COST']]
df_tbl_2=df_tbl_2.groupby(['RECEIVEDDATE'],as_index=False).sum()

df_tbl_2['OPTIMIZED_COST']=df_tbl_2['DOWNGRADED_COST']
df_tbl_2['OPTIMIZED_COST_%']=0
df_tbl_2['OPTIMIZATION_VARIANCE']=0

data = df_tbl_2
source = ColumnDataSource(data)

columns = [
        TableColumn(field="RECEIVEDDATE", title="Date"),
        TableColumn(field="DOWNGRADED_COST", title="Un-Optimized Costs", formatter=NumberFormatter(format="$0,0")),
        TableColumn(field="OPTIMIZED_COST", title="Optimized Costs", formatter=NumberFormatter(format="$0,0")),
        TableColumn(field="OPTIMIZED_COST_%", title="Optimized Costs %", formatter=NumberFormatter(format="$0,0")),
        TableColumn(field="OPTIMIZATION_VARIANCE", title="Optimization Variance", formatter=NumberFormatter(format="$0,0")),
]

data_table = DataTable(source=source, columns=columns, width=800)
widgetbox(data_table)

callback = CustomJS(args=dict(source=source), code="""
    var data = source.data;
    var A = perc.value;
    var x = source.data['OPTIMIZED_COST'];
    var y = source.data['OPTIMIZED_COST_%'];
    var z = source.data['OPTIMIZATION_VARIANCE'];
    for (var i=0; i < x.length; i++) {y[i]=x[i]*A;}
    for (var i=0; i < x.length; i++) {z[i]=x[i]-y[i];}
    source.change.emit();
""")

perc_slider = Slider(start=0.1, end=1, value=1, step=.1,
                    title="Percent", callback=callback)
callback.args["perc"] = perc_slider

p17 = column(
    widgetbox(perc_slider),
    widgetbox(data_table),
)


# In[66]:



# ## Lets Explore the IP Addresses

# In[33]:

'''
#EIRF Included
#clean-up the data to ensure only IP addresses are being accounted
ip=df[['ipaddressmerchant','ORDERID','DOWNGRADE']][(df['ipaddressmerchant']!='CREDIT')&(df['ipaddressmerchant']!='DEBIT')&(df['ipaddressmerchant']!='(null)')]
#group the data together in a pivot format to do deeper analysis of the transactional data
ip=ip.groupby(['ipaddressmerchant'],as_index=False).agg({'ORDERID':'count','DOWNGRADE':'sum'})
ip['DOWNGRADE_PERC']=ip['DOWNGRADE']/ip['ORDERID']
#print ip.head()


# In[34]:


#EIRF Excluded
#clean-up the data to ensure only IP addresses are being accounted
ip=df[['ipaddressmerchant','ORDERID','DOWNGRADE']][(df['ipaddressmerchant']!='CREDIT')&(df['ipaddressmerchant']!='DEBIT')&(df['ipaddressmerchant']!='(null)')&(df['EIRF']==0)]
#group the data together in a pivot format to do deeper analysis of the transactional data
ip=ip.groupby(['ipaddressmerchant'],as_index=False).agg({'ORDERID':'count','DOWNGRADE':'sum'})
ip['DOWNGRADE_PERC']=ip['DOWNGRADE']/ip['ORDERID']
#print ip.head()


# In[35]:


#EIRF Excluded
#clean-up the data to ensure only IP addresses are being accounted
ip=df[['ipaddressmerchant','RECEIVEDDATE','ORDERID','DOWNGRADE']][(df['ipaddressmerchant']!='CREDIT')&(df['ipaddressmerchant']!='DEBIT')&(df['ipaddressmerchant']!='(null)')&(df['EIRF']==0)]
#group the data together in a pivot format to do deeper analysis of the transactional data
ip=ip.groupby(['ipaddressmerchant','RECEIVEDDATE'],as_index=False).agg({'ORDERID':'count','DOWNGRADE':'sum'})
ip['DOWNGRADE_PERC']=ip['DOWNGRADE']/ip['ORDERID']
#print ip.head()
'''

# In[36]:


#we need to ask ourselves how much of this is skyscanner?


# In[37]:


#lets have a look at the skyscanner breakdown by IP


# In[38]:
#df.to_csv('d:\\djohnson\\Desktop\\ctrip_output.txt',sep=';')

curdoc().clear() #since running script in Jupyter and asking to run in html the sessions can duplicate since it's not on a server but in the test environment this script clears the cache clears the document and prevents the duplication error

grid1 = gridplot([[p1,p2,p3],[p13,p14],[p7,p8,p9]])
grid2 = gridplot([[p4,p5,p6],[p15,p16],[p10,p11,p12]])
grid3 = p17

tab1=Panel(child=grid1,title='Downgrades, Including EIRF')
tab2=Panel(child=grid2,title='Downgrades, Excluding EIRF')
tab3=Panel(child=grid3,title='Optimization')

tabs = Tabs(tabs=[tab1,tab2,tab3])

show(tabs)

