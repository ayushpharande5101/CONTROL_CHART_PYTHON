import datetime
import random
import statistics
import time
import pyodbc
from pylogix import PLC

connection = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                           'Server= AYUSHP-DELL\\SQLEXPRESS03;'
                           'Trusted_Connection=yes;')

if connection:
    print("Connected Successfully")
else:
    print("Failed to connect")

cursor = connection.cursor()

def insert_data_X_Chart(cursor, values):
    table_name = 'Control_chart.dbo.[X_CHART]'

    columns = ['SR_NO','DATETIME','BATCH','[1]', '[2]', '[3]', '[4]', '[5]','X_MAX','X_MIN','AVERAGE','RANGE','OVERALL_AVERAGE','OVERALL_RANGE','UCL_X','LCL_X','STD_LONGTERM','STD_SHORTTERM','Cp','CpK']

    SQLCommand = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES (?, ? ,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

    cursor.execute(SQLCommand, values)
    connection.commit()  # Commit changes to the database

def insert_data_R_Chart(cursor, values):
    table_name = 'Control_chart.dbo.[R_CHART]'

    columns = ['SR_NO','DATETIME','BATCH', '[1]', '[2]', '[3]', '[4]', '[5]','X_MAX','X_MIN','RANGE','OVERALL_RANGE','UCL_R','LCL_R','STD_LONGTERM','STD_SHORTTERM','CpK','Cp']

    SQLCommand = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES (?, ? , ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

    cursor.execute(SQLCommand, values)
    connection.commit()  # Commit changes to the database

def insert_data_ind(cursor, values):
    table_name = 'Control_chart.dbo.[SOLO_CHART]'

    columns = ['SR_NO','DATETIME','BATCH','FINAL_WEIGHT','UCL','LCL','USL','LSL','CL']

    SQLCommand = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES (?, ?, ?, ?, ? ,?, ?, ?, ?)"

    cursor.execute(SQLCommand, values)
    connection.commit()  # Commit changes to the database

def insert_data_histogram(cursor, values):
    table_name = 'Control_chart.dbo.[Histogram]'
    columns = ['SR_NO','DATETIME', '[VALUES]', 'OC_POINTS']
    SQLCommand = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES (?, ?, ?, ?)"
    cursor.execute(SQLCommand, values)
    connection.commit()  # Commit changes to the database



DATA = []
AVG = []
RNG = []
STANDARD_DEVIATION = []
i = 0
j = 1
r = 1
count = 0
while True:
    with PLC() as comm:

        comm.IPAddress = '192.168.10.30'
        print("TRUE")

        START_BIT = comm.Read('SPC_Trigget_Bit')

        if START_BIT.Value == True:
            Z1 = comm.Read('SPC_Batch_No')
            Z2 = comm.Read('SPC_Dosing_Wt')
            Z3 = comm.Read('SPC_Dosing_Wt_CL')
            Z4 = comm.Read('SPC_Dosing_Wt_LCL')
            Z5 = comm.Read('SPC_Dosing_Wt_UCL')
            Z6 = comm.Read('SPC_Psrt_ID')

            Dosing_Weight = Z2.Value

            BATCH1 = Z1.Value
            PART_ID1 = Z6.Value

            start_index = 4
            end_index = BATCH1.index(b'\x00', start_index)

            BATCH = BATCH1[start_index:end_index].decode('utf-8')
            PART_ID = PART_ID1.decode("utf-8")

            time.sleep(2)

            DATA.append(Dosing_Weight)
            STANDARD_DEVIATION.append(Dosing_Weight)

            if len(STANDARD_DEVIATION) <= 2:
                STD_Long_term = 0
            else:
                STD_Long_term = statistics.stdev(STANDARD_DEVIATION)
            if len(DATA) <= 2:
                STD_short_term = 0
            else:
                STD_short_term = statistics.stdev(DATA)

            print(STD_Long_term)

            if len(DATA) >= 5:
                print(f"DATA: ",DATA)
                AVERAGE = statistics.mean(DATA)
                AVG.append(AVERAGE)

                X_MAX = max(DATA)
                print(f"MAXIMUM:",X_MAX)

                X_MIN = min(DATA)
                print(f"MINIMUM:",X_MIN)

                RANGE = max(DATA) - min(DATA)
                RNG.append(RANGE)

                if len(AVG) >= 2:
                    OVERALL_AVERAGE = statistics.mean(AVG)
                else:
                    OVERALL_AVERAGE = 0

                if len(RNG) >= 2:
                    OVERALL_RANGE = statistics.mean(RNG)
                else:
                    OVERALL_RANGE = 0

                if OVERALL_AVERAGE == 0 and OVERALL_RANGE == 0:
                    UCL_X_CHART = 0
                    LCL_X_CHART = 0
                else:
                    UCL_X_CHART = OVERALL_AVERAGE + (0.577 * OVERALL_RANGE)
                    LCL_X_CHART = OVERALL_AVERAGE - (0.577 * OVERALL_RANGE)

                if STD_short_term == 0:
                    Cp = 0
                else :
                    Cp = (UCL_X_CHART - LCL_X_CHART)/(6 * STD_short_term)
                print(Cp)

                if STD_Long_term == 0:
                    CpK = 0
                else:
                    CpK_Lower = (OVERALL_AVERAGE - LCL_X_CHART) / (3 * STD_Long_term)
                    CpK_Upper = (UCL_X_CHART - OVERALL_AVERAGE) / (3 * STD_Long_term)
                    CpK = min(CpK_Upper, CpK_Lower)
                print(f"CpK: ",CpK)
                DATETIME = datetime.datetime.now()

                values = (j/5,DATETIME,BATCH, DATA[0], DATA[1], DATA[2], DATA[3], DATA[4], X_MAX, X_MIN, AVERAGE,RANGE,OVERALL_AVERAGE,OVERALL_RANGE,UCL_X_CHART, LCL_X_CHART,STD_Long_term,STD_short_term,Cp,CpK)
                print(values)
                insert_data_X_Chart(cursor, values)

                print("DATA INSERTED IN X_CHART")

                #==============================================#=====R-CHART=====#===============================================================

                if OVERALL_AVERAGE == 0 and OVERALL_RANGE == 0:
                    UCL_R_CHART = 0
                    LCL_R_CHART = 0
                else:
                    UCL_R_CHART = 2.114 * OVERALL_RANGE
                    LCL_R_CHART = 0 * OVERALL_RANGE

                if STD_short_term == 0:
                    Cp_R = 0
                else :
                    Cp_R = (UCL_R_CHART - LCL_R_CHART)/(6 * STD_short_term)
                print(Cp_R)

                if STD_Long_term == 0:
                    CpK_R = 0
                else:
                    CpK_Lower = (OVERALL_AVERAGE - LCL_R_CHART) / (3 * STD_Long_term)
                    CpK_Upper = (UCL_R_CHART - OVERALL_AVERAGE) / (3 * STD_Long_term)
                    CpK_R = min(CpK_Upper, CpK_Lower)
                print(f"CpK: ",CpK_R)
                DATETIME = datetime.datetime.now()

                values = (j/5, DATETIME, BATCH, DATA[0], DATA[1], DATA[2], DATA[3], DATA[4], X_MAX, X_MIN, RANGE,
                            OVERALL_RANGE, UCL_R_CHART, LCL_R_CHART, STD_Long_term, STD_short_term, Cp_R, CpK_R)

                insert_data_R_Chart(cursor,values)
                print("DATA INSERTED IN R_CHART")

                DATA.clear()
                time.sleep(1)

            else:
                print("Updating Values")
            j = j + 1

        if START_BIT.Value == True:
            Z1 = comm.Read('SPC_Batch_No')
            Z2 = comm.Read('SPC_Dosing_Wt')
            Z3 = comm.Read('SPC_Dosing_Wt_CL')
            Z4 = comm.Read('SPC_Dosing_Wt_LCL')
            Z5 = comm.Read('SPC_Dosing_Wt_UCL')
            Z6 = comm.Read('SPC_Psrt_ID')

            BATCH1 = Z1.Value
            PART_ID1 = Z6.Value

            start_index = 4
            end_index = BATCH1.index(b'\x00', start_index)

            BATCH = BATCH1[start_index:end_index].decode('utf-8')
            PART_ID = PART_ID1.decode("utf-8")

            Dosing_Weight = Z2.Value
            CL = Z3.Value
            Positive_Tolerence = Z5.Value
            Negative_Tolerence = Z4.Value
            LSL = CL - Negative_Tolerence
            USL = CL + Positive_Tolerence
            UCL = CL + 2
            LCL = CL - 2
            DATETIME = datetime.datetime.now()
            values = (i, DATETIME, BATCH, Dosing_Weight,UCL,LCL, USL, LSL,CL)

            insert_data_ind(cursor, values)
            i = i + 1
            time.sleep(1)

            if Dosing_Weight > USL or Dosing_Weight < LSL:
                count = count + 1
                Dateandtime = datetime.datetime.now()
                if i % 10 == 0:
                    values = (r, Dateandtime, i, count)
                    r = r + 1
                    insert_data_histogram(cursor, values)
                    count = 0
            comm.Write('SPC_Trigget_Bit', False)

        else:
            print("Waiting for Weight value")
            time.sleep(1)

