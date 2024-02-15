import time
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
                plt.annotate(label, xy=(ds['SR_NO'].iloc[-1], value), xytext=(ds['SR_NO'].iloc[-1] + 0.09, value),
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
        UCL_X = 550
        LCL_X = ds['LCL_X'].iloc[-1]
        CL = 117
        for i in range(7):
            last_row = ds.iloc[-(i + 1)]
            plt.text(last_row['SR_NO'], last_row['AVERAGE'],
                     f'{last_row["AVERAGE"]:.2f}', fontsize=8, ha='center', va='bottom')
            point_color = 'red' if selected_chart_type == 'X Chart' and (
                    last_row['AVERAGE'] > UCL_X or last_row['AVERAGE'] < LCL_X) else '#1476b8'

            plt.axhline(y=CL, color='g', linestyle='-', label='CL')
            plt.axhline(y=UCL_X, color='r', linestyle='--', label='UCL')
            plt.axhline(y=LCL_X, color='r', linestyle='--', label='LCL')
            for label, value in [('UCL', UCL_X), ('LCL', LCL_X), ('CL', CL)]:
                plt.annotate(label, xy=(ds['SR_NO'].iloc[-1], value), xytext=(ds['SR_NO'].iloc[-1] + 0.5, value),
                             color='black', fontsize=10, ha='left', va='center')

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
        ds1 = pd.DataFrame.from_records(rows1, columns=columns1)
        curs1.close()
        plot_data = []
        UCL_R = ds1['UCL_R'].iloc[-1]
        LCL_R = ds1['LCL_R'].iloc[-1]
        CL = 117
        for i in range(13):
            last_row = ds1.iloc[-(i + 1)]
            plt.text(last_row['SR_NO'], last_row['RANGE'],
                     f'{last_row["RANGE"]:.2f}', fontsize=8, ha='center', va='bottom')
            point_color = 'red' if selected_chart_type == 'R Chart' and (
                    last_row['RANGE'] > UCL_R or last_row['RANGE'] < LCL_R) else '#1476b8'

            plt.axhline(y=CL, color='g', linestyle='-', label='CL')
            plt.axhline(y=UCL_R, color='r', linestyle='--', label='UCL')
            plt.axhline(y=LCL_R, color='r', linestyle='--', label='LCL')
            for label, value in [('UCL', UCL_R), ('LCL', LCL_R), ('CL', CL)]:
                plt.annotate(label, xy=(ds1['SR_NO'].iloc[-1], value), xytext=(ds1['SR_NO'].iloc[-1] + 1, value),
                             color='black', fontsize=10, ha='left', va='center')

            plot_data.append((last_row['SR_NO'], last_row['RANGE']))
        # Plot all points at once
        plt.plot(*zip(*plot_data), marker='o', linestyle='-', color=point_color)
        plt.title('SPC-R Chart')
        plt.xlabel('Part Id In Integer')
        plt.ylabel('Coating Difference In Real Format')


def show_chart(f_date, t_date, batch):
    point_color = '#1476b8'
    plt.figure(figsize=(10, 5))
    # Construct the SQL query based on the selected chart type
    if selected_chart_type == 'SPC Chart':
        sql1 = "SELECT SR_NO,DATETIME,BATCH,FINAL_WEIGHT,UCL,LCL,CL,USL,LSL FROM Control_chart.dbo.SOLO_CHART "
        curs1 = connection().execute(sql1)
        rows1 = curs1.fetchall()
        columns1 = [column[0] for column in curs1.description]
        ds1 = pd.DataFrame.from_records(rows1, columns=columns1)
        curs1.close()

        USL = ds1['USL'].iloc[-1]
        LSL = ds1['LSL'].iloc[-1]
        UCL = ds1['UCL'].iloc[-1]
        LCL = ds1['LCL'].iloc[-1]
        CL = ds1['CL'].iloc[-1]
        for index, row in ds1.iterrows():
            plt.text(row['SR_NO'], row['FINAL_WEIGHT'], f'{row["FINAL_WEIGHT"]:.2f}', fontsize=8, ha='center',
                     va='bottom')
            if selected_chart_type == 'SPC Chart' and (row['FINAL_WEIGHT'] > UCL or row['FINAL_WEIGHT'] < LCL):
                plt.scatter(row['SR_NO'], row['FINAL_WEIGHT'], color='red', zorder=5)

        plt.axhline(y=CL, color='g', linestyle='-', label='CL')
        plt.axhline(y=UCL, color='r', linestyle='--', label='UCL')
        plt.axhline(y=LCL, color='r', linestyle='--', label='LCL')
        plt.axhline(y=USL, color='y', linestyle='--', label='USL')
        plt.axhline(y=LSL, color='y', linestyle='--', label='LSL')
        for label, value in [('UCL', UCL), ('LCL', LCL), ('CL', CL), ('USL', USL), ('LSL', LSL)]:
            plt.annotate(label, xy=(ds1['SR_NO'].iloc[-1], value), xytext=(ds1['SR_NO'].iloc[-1] + 0.11, value),
                         color='black', fontsize=10, ha='left', va='center')

        plt.plot(ds1['SR_NO'], ds1['FINAL_WEIGHT'], marker='o', linestyle='-')
        plt.title(f'SPC Chart')
        plt.xlabel('Part Id In Integer')
        plt.ylabel('Coating Difference In Real Format')

    elif selected_chart_type == 'X Chart':

        sql = ("SELECT SR_NO, DATETIME, BATCH, AVERAGE, UCL_X, LCL_X"
               " FROM Control_chart.dbo.X_CHART WHERE DATETIME BETWEEN ? AND ? OR BATCH = ?")
        curs = connection().execute(sql, (f_date, t_date, batch))
        rows = curs.fetchall()
        columns = [column[0] for column in curs.description]
        ds = pd.DataFrame.from_records(rows, columns=columns)
        curs.close()
        if ds.empty:
            st.warning("No data found for the selected criteria.")
            return
            # Plot the chart
        batch_c = ds['BATCH'].iloc[0]

        UCL = ds['UCL_X'].iloc[-1]
        LCL = ds['LCL_X'].iloc[-1]
        # CL = ds['CL'].iloc[-1]
        plt.figure(figsize=(10, 5))
        for index, row in ds.iterrows():
            plt.text(row['SR_NO'], row['AVERAGE'], f'{row["AVERAGE"]:.2f}', fontsize=8, ha='center',
                     va='bottom')
            if selected_chart_type == 'R Chart' and (row['AVERAGE'] > UCL or row['AVERAGE'] < LCL):
                plt.scatter(row['SR_NO'], row['AVERAGE'], color='red', zorder=5)

        # plt.axhline(y=CL, color='g', linestyle='-', label='CL')
        plt.axhline(y=UCL, color='r', linestyle='--', label='UCL')
        plt.axhline(y=LCL, color='r', linestyle='--', label='LCL')
        for label, value in [('UCL', UCL), ('LCL', LCL)]:
            plt.annotate(label, xy=(ds['SR_NO'].iloc[-1], value), xytext=(ds['SR_NO'].iloc[-1] + 0.11, value),
                         color='black', fontsize=10, ha='left', va='center')

        plt.xticks(ds['SR_NO'], ha='right')
        plt.plot(ds['SR_NO'], ds['AVERAGE'], marker='o', linestyle='-')
        plt.title(f'SPC-{selected_chart_type} Chart')
        plt.xlabel('Part Id In Integer')
        plt.ylabel('Coating Difference In Real Format')

    elif selected_chart_type == 'Histogram':
        sql_query = "SELECT SR_NO,DATETIME,OC_POINTS FROM Control_chart.dbo.Histogram "

        curs = connection().execute(sql_query)
        rows = curs.fetchall()
        columns = [column[0] for column in curs.description]
        ds = pd.DataFrame.from_records(rows, columns=columns)
        curs.close()
        plt.hist(ds['OC_POINTS'], bins=30, edgecolor='black')  # Adjust the number of bins as needed
        # Add labels and title
        plt.xlabel('Interval')
        plt.ylabel('Frequency')
        plt.title('Histogram')
        plt.title(f'SPC-{selected_chart_type} Chart')
        plt.xlabel('Part Id In Integer')
        plt.ylabel('Coating Difference In Real Format')

    elif selected_chart_type == 'R Chart':
        sql_query = ("SELECT SR_NO, DATETIME, BATCH, RANGE, UCL_R, LCL_R"
                     " FROM Control_chart.dbo.R_CHART WHERE DATETIME BETWEEN ? AND ? OR BATCH = ?")
        curs = connection().execute(sql_query, (f_date, t_date, batch))
        rows = curs.fetchall()
        columns = [column[0] for column in curs.description]
        ds = pd.DataFrame.from_records(rows, columns=columns)
        curs.close()
        if ds.empty:
            st.warning("No data found for the selected criteria.")
            return

        UCL = ds['UCL_R'].iloc[-1]
        LCL = ds['LCL_R'].iloc[-1]
        # CL = ds['CL'].iloc[-1]
        for index, row in ds.iterrows():
            plt.text(row['SR_NO'], row['RANGE'], f'{row["RANGE"]:.2f}', fontsize=8, ha='center',
                     va='bottom')
            if selected_chart_type == 'R Chart' and (row['RANGE'] > UCL or row['RANGE'] < LCL):
                plt.scatter(row['SR_NO'], row['RANGE'], color='red', zorder=5)

        # plt.axhline(y=CL, color='g', linestyle='-', label='CL')
        plt.axhline(y=UCL, color='r', linestyle='--', label='UCL')
        plt.axhline(y=LCL, color='r', linestyle='--', label='LCL')
        for label, value in [('UCL', UCL), ('LCL', LCL)]:
            plt.annotate(label, xy=(ds['SR_NO'].iloc[-1], value), xytext=(ds['SR_NO'].iloc[-1] + 0.11, value),
                         color='black', fontsize=10, ha='left', va='center')
        plt.xticks(ds['SR_NO'], ha='right')
        plt.plot(ds['SR_NO'], ds['RANGE'], marker='o', linestyle='-')
        plt.title(f'SPC-{selected_chart_type} Chart')
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
    left, mid,  right = st.columns(3)
    with left:
        From_date = st.date_input('From :', value=pd.to_datetime('today').date())
    with mid:
        To_date = st.date_input('To :', value=pd.to_datetime('today').date())
    with right:
        s_option = st.text_input('Batch :', value = 'A1356')
with m_side:
    f_date = str(From_date)
    t_date = str(To_date)
    batch = str(s_option)

    chart_types = ['SPC Chart', 'R Chart', 'X Chart', 'Histogram']
    selected_chart_type = st.selectbox('Select Chart Type:', chart_types)
    if f_date or t_date or batch:
        show_chart(f_date, t_date, batch)
    else:
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
               " FROM Control_chart.dbo.R_chart")
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
               " FROM Control_chart.dbo.X_chart")
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
if __name__ == '__main__':
    chart_placeholder = st.empty()

    # Run the chart in a loop
    while True:
        # Clear the previous chart


        # Generate and display the new chart
        if f_date or t_date or batch:
            show_chart(f_date, t_date, batch)
        else:
            chart()

        # Add a delay to control the update speed
        time.sleep(5)