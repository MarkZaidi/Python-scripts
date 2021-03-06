# -*- coding: utf-8 -*-
"""
Created on Wed Apr  7 15:25:04 2021

@author: Mark Zaidi
"""

#%% load libraries
import pandas
import math
import matplotlib
import matplotlib.pyplot as plt
import os
import numpy as np
import seaborn as sns
#%% Read data
data=pandas.read_csv(r'C:\Users\Mark Zaidi\Documents\QuPath\PIMO GBM related projects\Feb 2021 IMC\cell_measurements.csv')
annotation_data=pandas.read_csv(r'C:\Users\Mark Zaidi\Documents\QuPath\PIMO GBM related projects\Feb 2021 IMC\annotation_measurements.csv')
#%% set constants (currently unused)
param_Name='Name'
param_Parent='Parent'
param_UnusedClass='PathCellObject'
param_pos_kwd='pimo positive'
param_neg_kwd='pimo negative'
#%% get baseline measurements
cells_in_pimo_pos=sum(data.apply(lambda x: 1 if x['Parent'] == "pimo positive" else 0 , axis=1))
cells_in_pimo_neg=sum(data.apply(lambda x: 1 if x['Parent'] == "pimo negative" else 0 , axis=1))
#%% lets try getting percent positive for 1 marker in 1 region
marker="Tb(159)_159Tb-CD68"
cond1= data['Name'].str.contains(marker,regex=False)
cond2= data['Parent'].str.contains('pimo positive',regex=False)
percent_marker_pos_in_pimo_pos=(cond1&cond2).sum()/cond2.sum()*100
#%% get unique IHC marker names
df2=data["Name"].str.split(':',expand=True)
df3=pandas.unique(df2[df2.columns].values.ravel('K'))
df3=df3[(df3 != 'PathCellObject')]
marker_list = [x for x in df3 if x != None]
marker_list=[x.strip(' ') for x in marker_list]
marker_list=list(set(marker_list))
annotation_list=data["Parent"].unique().tolist()
marker_short=[i.split('-', 1)[1] for i in marker_list]
#%% iteratively get percent positive scores
count=0
pct_name=list()
marker_count=0
pct_pos=[]
pos_in_pimo_neg=[]
pos_in_pimo_pos=[]
for marker in marker_short:
    full_marker=marker_list[marker_count]
    marker_count=marker_count+1
    for annotation in annotation_list:
        pct_name.append(['Percent ' + marker + ' positive in ' + annotation])
        cond1= data['Name'].str.contains(full_marker,regex=False)
        cond2= data['Parent'].str.contains(annotation,regex=False)
        pct_pos.append((cond1&cond2).sum()/cond2.sum()*100)
        if 'positive' in annotation:
            pos_in_pimo_pos.append((cond1&cond2).sum()/cond2.sum()*100)
        elif 'negative' in annotation:
            pos_in_pimo_neg.append((cond1&cond2).sum()/cond2.sum()*100)

        count=count+1
#%% visualize percent positive as clustered bar chart
pct_pos_df=pandas.DataFrame([marker_short,pos_in_pimo_pos,pos_in_pimo_neg,[i / j for i, j in zip(pos_in_pimo_pos, pos_in_pimo_neg)]]).transpose().sort_values(3,ascending=False)
#labels = marker_short
#neg_bar = pos_in_pimo_pos
#pos_bar = pos_in_pimo_neg
labels=pct_pos_df[0]
pos_bar=pct_pos_df[1]
neg_bar=pct_pos_df[2]

x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
plt.xticks(rotation=90)
rects1 = ax.bar(x - width/2, neg_bar, width, label='PIMO Negative')
rects2 = ax.bar(x + width/2, pos_bar, width, label='PIMO Positive')

#add data labels
ratios = pct_pos_df[3]
for rect1, rect2, ratio in zip(rects1, rects2, ratios):
    ratio="{:.2f}".format(ratio)
    #height = rect2.get_height()
    height=(max(rect1.get_height(),rect2.get_height()))
    ax.text(rect2.get_x() + rect2.get_width() / 2, height + 5, ratio,
            ha='center', va='bottom',rotation='vertical')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Percent Positive')
ax.set_title('Percent positive scores in PIMO +/- regions')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

plt.ylim([0,125])
#ax.bar_label(rects1, padding=3)
#ax.bar_label(rects2, padding=3)

#fig.tight_layout()
plt.savefig(r'C:\Users\Mark Zaidi\Documents\Python Scripts\GBM IMC percent postive\Percent positive scores in PIMO + vs - regions.png',dpi=800,pad_inches=0.1,bbox_inches='tight')

# Make some labels.
#ratios = ["label%d" % i for i in xrange(len(rects))]
#%% Visualize IHC marker in PIMO positive vs negative as a violin plot
#Identify cells belonging to pos or neg Parent annotations
pos_data= data[data['Parent'].str.contains('pimo positive',regex=False)]
neg_data= data[data['Parent'].str.contains('pimo negative',regex=False)]
# Pair up marker names with measurement (not all are cell mean, some are nucleus median, etc.)
#maybe made dataframe with columns: marker, measurement, and hmmmmmmmm
col_names=data.columns
#%% create a clustered violin plot
ax = sns.violinplot( x='Parent',y="Gd(155)_155Gd-PIMO: Cell: Mean",data=data[data['Gd(155)_155Gd-PIMO: Cell: Mean']<0.9*data['Gd(155)_155Gd-PIMO: Cell: Mean'].max()], palette="muted",scale='width',cut=0)
#%% now do the above, but iteratively
measurements_of_interest=['Pr(141)_141Pr-aSMA: Cell: Mean','Nd(143)_143Nd-GFAP: Cell: Median','Nd(145)_145Nd-CD31: Cell: Mean','Nd(150)_150Nd-SOX2: Nucleus: Median','Eu(151)_151Eu-CA9: Cell: Mean','Sm(152)_152Sm-CD45: Cell: Mean','Eu(153)_153Eu-VCAM: Cell: Mean','Gd(155)_155Gd-PIMO: Cell: Mean','Tb(159)_159Tb-CD68: Cell: Mean','Gd(160)_160Gd-GLUT1: Cell: Mean','Dy(163)_163Dy-HK2: Cell: Mean','Dy(164)_164Dy-LDHA: Cell: Mean','Er(168)_168Er-Ki67: Nucleus: Mean','Er(170)_170Er-IBA1: Cell: Mean','Yb(173)_173Yb-TMHistone: Nucleus: Mean','Yb(174)_174Yb-ICAM: Cell: Mean','Ir(191)_191Ir-DNA191: Nucleus: Mean','Ir(193)_193Ir-DNA193: Nucleus: Mean']
#2 lines below are violin code
# fig = plt.figure(figsize=(30, 30))
# gs = fig.add_gridspec(3, 6)

#fig = plt.figure(figsize=(6, 6))
count=0
index=0,0
figpath=r'C:\Users\Mark Zaidi\Documents\Python Scripts\GBM IMC percent postive\figures'
measure_short=[i.split(':', 1)[0] for i in measurements_of_interest]
for measure in measurements_of_interest:
    
    #ax = sns.violinplot( x='Parent',y=measure,data=data[data[measure]<0.9*data[measure].max()], palette="muted",scale='width',cut=0)
    ax = sns.violinplot( x='Parent',y=measure,data=data[data[measure]<(data[measure].mean()+2*data[measure].std())], palette="muted",scale='width',cut=0,inner="box")
    plt.savefig(os.path.join(figpath,measure_short[count]+'.png'),dpi=800,pad_inches=0.1,bbox_inches='tight')
    count=count+1
    plt.close()
    ##Violin subplot code below
    # print(count)
    # if count<6:
    #     index=0,count
    # elif (count>=6)&(count<12):
    #     index=1,count-6
    # elif (count>=12)&(count<18):
    #     index=2,count-12
    # ax = fig.add_subplot(gs[index])

    # ax = sns.violinplot( x='Parent',y=measure,data=data[data[measure]<(data[measure].mean()+2*data[measure].std())], palette="muted",scale='width',cut=0,inner="box")

    # count=count+1

#plt.savefig(r'C:\Users\Mark Zaidi\Documents\Python Scripts\GBM IMC percent postive\violin_plot.png',dpi=800,pad_inches=0.1,bbox_inches='tight')
#%% create overall violinplot figure
fig = plt.figure(figsize=(30, 30))
gs = fig.add_gridspec(3, 6)
count=0
index=0,0
figpath=r'C:\Users\Mark Zaidi\Documents\Python Scripts\GBM IMC percent postive\figures'
for measure in measurements_of_interest:
    
    #ax = sns.violinplot( x='Parent',y=measure,data=data[data[measure]<0.9*data[measure].max()], palette="muted",scale='width',cut=0)
    # ax = sns.violinplot( x='Parent',y=measure,data=data[data[measure]<(data[measure].mean()+2*data[measure].std())], palette="muted",scale='width',cut=0,inner="box")
    # plt.savefig(os.path.join(figpath,measure_short[count]+'.png'),dpi=800,pad_inches=0.1,bbox_inches='tight')
    # count=count+1
    # plt.close()
    ##Violin subplot code below
    print(count)
    if count<6:
        index=0,count
    elif (count>=6)&(count<12):
        index=1,count-6
    elif (count>=12)&(count<18):
        index=2,count-12
    ax = fig.add_subplot(gs[index])

    ax = sns.violinplot( x='Parent',y=measure,data=data[data[measure]<(data[measure].mean()+2*data[measure].std())], palette="muted",scale='width',cut=0,inner="box")

    count=count+1
plt.savefig(os.path.join(figpath,'Overall.png'),dpi=800,pad_inches=0.1,bbox_inches='tight')