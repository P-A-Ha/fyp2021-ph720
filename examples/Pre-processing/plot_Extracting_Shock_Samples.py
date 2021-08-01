"""
Extracting Shock Data for Feature Extraction (UNFINISHED)
=========================================================

Fetching shock instances (including symptoms that indicate severe dengue) and structuring the data

"""
#%%
## Importing Libraries

# Generic
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import glob
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio

Terminal = True

SQI_clinical_file = r'..\..\..\..\OUCRU\Outputs\Complete_SQIs_with_Clinical.csv'
Raw_signals = r'..\..\..\..\OUCRU\Outputs\Raw_signals.csv'


#Loading SQI Matched with clinitcal to the Dataframe
SQI_C = pd.read_csv(SQI_clinical_file)
Raw = pd.read_csv(Raw_signals)

if Terminal:
    print("\n SQI with Clinical Match:")
    print(SQI_C)
    print("\n Raw Signals")
    print(Raw)


# %%

event = ['event_shock', 'reshock24','diagnosis_admission',\
     'ascites', 'respiratory_distress', 'ventilation_cannula', \
     'ventilation_mechanical', 'ventilation_ncpap', 'bleeding_severe', \
     'cns_abnormal', 'liver_mild', 'pleural_effusion', 'skidney']

event_shock = 'shock_admission'

SQI_C['keep'] = False
for i in range(len(event)):
    event_s = event[i]
    SQI_C['keep'][SQI_C[event_s] == True] = True
    print("\n Total ", event[i], " events:")

SQI_C.to_csv(r'..\..\..\..\OUCRU\Outputs\Complete_SQIs_with_Clinical_keep.csv')


patient_list = ['003-2009', '003-2012','003-2023','003-2028','003-2103','003-2104','003-2109', '003-2110', '003-2162']
    
# %%
for i in range(len(patient_list)):
    #fig = make_subplots(rows=2, cols=1)
    title_str = 'IR_ADC over Time for patient ' + str(patient_list[i])
    fig = go.Figure(layout_title_text = title_str)
    fig.add_trace(go.Scatter(x = Raw.PPG_Datetime[Raw.study_no == patient_list[i]], y =  Raw.IR_ADC[Raw.study_no == patient_list[i]], name='IR_ADC'))#,),row=1,col=1)
    for index, row in SQI_C[(SQI_C.study_no == patient_list[i]) & (SQI_C.keep == True)].iterrows():
        fig.add_vline(x = row.PPG_w_s, line_width=3, line_dash="dot", line_color="red")# annotation_text="Shock")#, annotation_position="top left", annotation_font_size=20, annotation_font_color="red")
        if not row.empty:
            fig.add_trace( go.Scatter(mode='markers', x=[row.PPG_w_s], y=[Raw['PLETH'][(Raw.study_no == patient_list[i]) & (Raw.PPG_Datetime >= row.PPG_w_s) & (Raw.PPG_Datetime < row.PPG_w_f)]], marker=dict(color='red', opacity=1), name = "Shock" ))
    if not SQI_C[(SQI_C.study_no == patient_list[i]) & (SQI_C.shock_admission == True)].empty:
        fig.add_annotation(
        xref="x domain",
        yref="y domain",
        # The arrow head will be 25% along the x axis, starting from the left
        x=0.01,
        # The arrow head will be 40% along the y axis, starting from the bottom
        y=0.01,
        text="Admitted with Shock",
        showarrow=False,
        font=dict(
            family="Courier New, monospace",
            size=20,
            color="RED"
            )
                        )
    

    fig.update_xaxes(rangeslider_visible=True)
    fig.update_xaxes(title_text="Date")
    fig.update_yaxes(title_text="IR_ADC")
    fig.update_layout(showlegend=True)

    imagepath1 = "D:\FILES\Desktop\Dissertation ICL\OUCRU\Outputs\Images\PNG"
    imagepath2 = "D:\FILES\Desktop\Dissertation ICL\OUCRU\Outputs\Images\SVG"
    imagepath3 = "D:\FILES\Desktop\Dissertation ICL\OUCRU\Outputs\Images\HTML"
    img_title1 = os.path.join(imagepath1,title_str)
    img_title2 = os.path.join(imagepath2,title_str)
    img_title3 = os.path.join(imagepath3,title_str)
    img_s1 = img_title1 + ".png"
    img_s2 = img_title2 + ".svg"
    img_s3 = img_title3 + ".html"
    fig.write_image(img_s1)
    fig.write_image(img_s2)
    fig.write_html(img_s3)

    fig.show()

    

    #fig = make_subplots(rows=2, cols=1)
    title_str2 = 'PLETH over Time for patient ' + str(patient_list[i])
    fig2 = go.Figure(layout_title_text = title_str2)
    fig2.add_trace(go.Scatter(x = Raw.PPG_Datetime[Raw.study_no == patient_list[i]], y =  Raw.PLETH[Raw.study_no == patient_list[i]], name='PLETH'))#,),row=1,col=1)
    for index, row in SQI_C[(SQI_C.study_no == patient_list[i]) & (SQI_C.keep == True)].iterrows():
        fig2.add_vline(x = row.PPG_w_s, line_width=3, line_dash="dot", line_color="red")#, annotation_text="Shock")#, annotation_position="top left", annotation_font_size=20, annotation_font_color="red")
        if not row.empty:
            fig.add_trace( go.Scatter(mode='markers', x=[row.PPG_w_s], y=[Raw['PLETH'][(Raw.study_no == patient_list[i]) & (Raw.PPG_Datetime >= row.PPG_w_s) & (Raw.PPG_Datetime < row.PPG_w_f)]], marker=dict(color='red', opacity=1), name = "Shock" ))
    if not SQI_C[(SQI_C.study_no == patient_list[i]) & (SQI_C.shock_admission == True)].empty:
        fig2.add_annotation(
        xref="x domain",
        yref="y domain",
        # The arrow head will be 25% along the x axis, starting from the left
        x=0.01,
        # The arrow head will be 40% along the y axis, starting from the bottom
        y=0.01,
        text="Admitted with Shock",
        showarrow=False,
        font=dict(
            family="Courier New, monospace",
            size=20,
            color="RED"
            )
                        )


    fig2.update_xaxes(rangeslider_visible=True)
    fig2.update_xaxes(title_text="Date")
    fig2.update_yaxes(title_text="PLETH")
    fig2.update_layout(showlegend=True)


    img_title4 = os.path.join(imagepath1,title_str2)
    img_title5 = os.path.join(imagepath2,title_str2)
    img_title6 = os.path.join(imagepath3,title_str2)
    img_s4 = img_title4 + ".png"
    img_s5 = img_title5 + ".svg"
    img_s6 = img_title6 + ".html"
    fig2.write_image(img_s4)
    fig2.write_image(img_s5)
    fig2.write_html(img_s6)

    fig2.show()
    



#MULTIPLE plots same figure 

#fig.append_trace(go.Scatter(x = Raw.PPG_Datetime[Raw.study_no == '003-2009'], y =  Raw.PLETH[Raw.study_no == '003-2009'], name='Pleth'), row=2, col=1)
#for index, row in SQI_C[(SQI_C.study_no == '003-2009') & (SQI_C.keep == True)].iterrows():
#    fig.add_vline(x = row.PPG_w_s, line_width=3, line_dash="dash", line_color="red", row=2, col=1)


#fig.update_yaxes(title_text="Infrared", row=1, col=1)
#fig.update_yaxes(title_text="Pleth", row=2, col=1)

# fig.update_xaxes(rangeslider_visible=True, row=1, col=1)
# fig.update_xaxes(title_text="Date", row=1, col=1)
# fig.update_xaxes(rangeslider_visible=True, row=2, col=1)
# fig.update_xaxes(title_text="Date", row=2, col=1)

#fig.update_layout(height=1000, width=1000, title_text=" IR_ADC and PLETH Plots for Patient 003-2009")
# %%
