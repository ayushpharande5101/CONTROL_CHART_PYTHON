import pandas as pd
import streamlit as st
from PIL import Image
import pyodbc
import matplotlib.pyplot as plt

# creating a Dashboard
st.set_page_config(page_title="SPC chart", layout='wide')

# inserting an image as a logo
dash_logo = "CTPL2.png"  # need changes
l_width = 200
l_height = 200
img = Image.open(dash_logo)
img.thumbnail((l_width, l_height))

def connection():  # sql server connection changes needed
    conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                          'Server= AYUSHP-DELL\\SQLEXPRESS03;'
                          'Trusted_Connection=yes;')

    cursor = conn.cursor()
    return cursor

def chart():
    global point_color
    plt.figure(figsize=(10, 5))
    if selected_chart_type == 'SPC Chart':
        sql1 = "SELECT SR_NO,DATETIME,BATCH,FINAL_WEIGHT,UCL,LCL,CL FROM Control_chart.dbo.SOLO_CHART "
        curs1 = connection().execute(sql1)
        rows1 = curs1.fetchall()
        columns1 = [column[0] for column in curs1.description]
        ds = pd.DataFrame.from_records(rows1, columns=columns1)
        curs1.close()
        UCL = ds['UCL'].iloc[-1]
        LCL = ds['LCL'].iloc[-1]
        CL = ds['CL'].iloc[-1]
        plot_data = []
        for i in range(2):

            last_row = ds.iloc[-(i + 1)]
            plt.text(last_row['SR_NO'], last_row['FINAL_WEIGHT'],
                     f'{last_row["FINAL_WEIGHT"]:.2f}', fontsize=8, ha='center', va='bottom')
            point_color = 'red' if selected_chart_type == 'SOLO Chart' and (
                    last_row['FINAL_WEIGHT'] > UCL or last_row['FINAL_WEIGHT'] < LCL) else '#1476b8'
            plt.axhline(y=CL, color='g', linestyle='-', label='CL')
            plt.axhline(y=UCL, color='r', linestyle='--', label='UCL')
            plt.axhline(y=LCL, color='r', linestyle='--', label='LCL')
            for label, value in [('UCL', UCL), ('LCL', LCL), ('CL', CL)]:
                plt.annotate(label, xy=(ds['SR_NO'].iloc[-1], value), xytext=(ds['SR_NO'].iloc[-1] + 1, value),
                             color='black', fontsize=10, ha='left', va='center')

            plot_data.append((last_row['SR_NO'], last_row['FINAL_WEIGHT']))
        # Plot all points at once

        plt.plot(*zip(*plot_data), marker='o', linestyle='-', color=point_color)
        plt.title('SPC Chart')
        plt.xlabel('Part Id In Integer')
        plt.ylabel('Coating Difference In Real Format')

    elif selected_chart_type == 'X Chart':
        sql1 = ("SELECT SR_NO,DATETIME,BATCH,1,2,3,4,5,X_MAX,X_MIN,AVERAGE,RANGE,OVERALL_AVERAGE,OVERALL_RANGE,UCL_X,"
                " LCL_X FROM Control_chart.dbo.X_CHART")
        curs1 = connection().execute(sql1)
        rows1 = curs1.fetchall()
        columns1 = [column[0] for column in curs1.description]
        ds = pd.DataFrame.from_records(rows1, columns=columns1)
        curs1.close()
        plot_data = []
        UCL_X = ds['UCL_X'].iloc[-1]
        LCL_X = ds['LCL_X'].iloc[-1]
        CL = 117
        for i in range(13):
            if len(ds) > (i + 1):  # Check if enough rows are available
                last_row = ds.iloc[-(i + 1)]
                plt.text(last_row['SR_NO'], last_row['AVERAGE'],
                         f'{last_row["AVERAGE"]:.2f}', fontsize=8, ha='center', va='bottom')
                plt.axhline(y=CL, color='g', linestyle='-', label='CL')
                plt.axhline(y=UCL_X, color='r', linestyle='--', label='UCL')
                plt.axhline(y=LCL_X, color='r', linestyle='--', label='LCL')
                for label, value in [('UCL', UCL_X), ('LCL', LCL_X), ('CL', CL)]:
                    plt.annotate(label, xy=(ds['SR_NO'].iloc[-1], value), xytext=(ds['SR_NO'].iloc[-1] + 0.5, value),
                                 color='black', fontsize=10, ha='left', va='center')
                point_color = 'red' if selected_chart_type == 'R Chart' and (last_row['AVERAGE'] > UCL_X or
                                                                             last_row['AVERAGE'] < LCL_X) else '#1476b8'
                plot_data.append((last_row['SR_NO'], last_row['AVERAGE']))

            # Plot all points at once
        plt.plot(*zip(*plot_data), marker='o', linestyle='-', color=point_color)
        plt.title('SPC-X Chart')
        plt.xlabel('Part Id In Integer')
        plt.ylabel('Coating Difference In Real Format')

    elif selected_chart_type == 'Histogram':
        sql = "SELECT SR_NO,DATETIME,BATCH,OC_POINTS FROM Control_chart.dbo.Histogram "
        curs1 = connection().execute(sql)
        rows1 = curs1.fetchall()
        columns1 = [column[0] for column in curs1.description]
        ds = pd.DataFrame.from_records(rows1, columns=columns1)
        curs1.close()
        plt.hist(ds['OC_POINTS'], bins=30, edgecolor='black')  # Adjust the number of bins as needed
        # Add labels and title
        plt.xlabel('Interval')
        plt.ylabel('Frequency')
        plt.title('Histogram')

    elif selected_chart_type == 'R Chart':
        sql1 = ("SELECT SR_NO,DATETIME,BATCH,1,2,3,4,5,X_MAX,X_MIN,RANGE,OVERALL_RANGE,UCL_R,LCL_R"
                " FROM Control_chart.dbo.R_CHART ")
        curs1 = connection().execute(sql1)
        rows1 = curs1.fetchall()
        columns1 = [column[0] for column in curs1.description]
        ds = pd.DataFrame.from_records(rows1, columns=columns1)
        curs1.close()
        plot_data = []
        UCL_R = ds['UCL_R'].iloc[-1]
        LCL_R = ds['LCL_R'].iloc[-1]
        CL = 117
        for i in range(13):
            last_row = ds.iloc[-(i + 1)]
            plt.text(last_row['SR_NO'], last_row['RANGE'],
                     f'{last_row["RANGE"]:.2f}', fontsize=8, ha='center', va='bottom')
            point_color = 'red' if selected_chart_type == 'R Chart' and (
                    last_row['RANGE'] > UCL_R or last_row['RANGE'] < LCL_R) else '#1476b8'

            plt.axhline(y=CL, color='g', linestyle='-', label='CL')
            plt.axhline(y=UCL_R, color='r', linestyle='--', label='UCL')
            plt.axhline(y=LCL_R, color='r', linestyle='--', label='LCL')
            for label, value in [('UCL', UCL_R), ('LCL', LCL_R), ('CL', CL)]:
                plt.annotate(label, xy=(ds['SR_NO'].iloc[-1], value), xytext=(ds['SR_NO'].iloc[-1] + 1, value),
                             color='black', fontsize=10, ha='left', va='center')

            plot_data.append((last_row['SR_NO'], last_row['RANGE']))
        # Plot all points at once
        plt.plot(*zip(*plot_data), marker='o', linestyle='-', color=point_color)
        plt.title('SPC-R Chart')
        plt.xlabel('Part Id In Integer')
        plt.ylabel('Coating Difference In Real Format')

l_w = 1.5
la_w = 0.5
dd_w = 5
m_w = 2
r_w = 1
# creating columns to create image, chart selection,clear button
l_side, la, dd, m_side, r_side = st.columns([l_w, la_w, dd_w, m_w, r_w])
with l_side:
    st.image(img, use_column_width=False)
with la:
    st.markdown('Date:')
with dd:
    left, mid, right = st.columns(3)
    with left:
        From_date = st.date_input('From :', value=pd.to_datetime('today').date())
    with mid:
        To_date = st.date_input('To :', value=pd.to_datetime('today').date())
    with right:
        Batch = ['1', '2', '3']
        s_option = st.selectbox('Batch:', Batch)
with m_side:
    f_date = str(From_date)
    t_date = str(To_date)
    batch_n = s_option
    batch = int(batch_n.replace('Batch ', ''))
    chart_types = ['SPC Chart','R Chart', 'X Chart', 'Histogram']
    selected_chart_type = st.selectbox('Select Chart Type:', chart_types)
    chart()

with r_side:
    if st.button('Clear Chart', help='Click to clear the chart'):
        # Clear the chart by updating the placeholder with an empty figure
        chart_placeholder = st.empty()
        fig, ax = plt.subplots(figsize=(10, 5))

# columns to create date, batch select box, table and to plot the selected chart on dashboard
left_w = 8
right_w = 2
left_s, right_s = st.columns([left_w, right_w])
with left_s:
    with st.container(border=True):
        st.pyplot(plt)

with right_s:
    if selected_chart_type == 'R Chart':
        sql = ("SELECT SR_NO, DATETIME, BATCH, RANGE, UCL_R, LCL_R,CpK,Cp"
               " FROM Control_chart.dbo.R_CHART")
        curs = connection().execute(sql)
        # Fetch all rows and create a DataFrame
        rows = curs.fetchall()
        columns = [column[0] for column in curs.description]
        ds = pd.DataFrame.from_records(rows, columns=columns)
        # Close cursor and connection
        curs.close()
        cpk_cp_table = pd.DataFrame({'Parameter': ['CpK', 'Cp'],
                                     'Value': [ds['CpK'].iloc[0], ds['Cp'].iloc[0]]})
        st.table(cpk_cp_table)
    elif selected_chart_type == 'X Chart':
        sql = ("SELECT SR_NO, DATETIME, BATCH, AVERAGE, UCL_X, LCL_X,CpK,Cp"
               " FROM Control_chart.dbo.X_CHART")
        curs = connection().execute(sql)
        # Fetch all rows and create a DataFrame
        rows = curs.fetchall()
        columns = [column[0] for column in curs.description]
        ds = pd.DataFrame.from_records(rows, columns=columns)
        # Close cursor and connection
        curs.close()
        cpk_cp_table = pd.DataFrame({'Parameter': ['CpK', 'Cp'],
                                     'Value': [ds['CpK'].iloc[0], ds['Cp'].iloc[0]]})
        st.table(cpk_cp_table)

