#######################  DASHBOARD 2: Number of average credit score for per pool #######################
import matplotlib.pyplot as plt
 

conn = p1.connect(r'Driver={SQL Server}; Server=DESKTOP-R6USKL7\MSSQL_DNST; Database=MortgageData; Trusted_Connection=yes;')
cursor2 = conn.cursor()
sqlQuery2 =  """\
        SELECT Agency, COUNT(*) COUNT_OF_POOLS
        FROM
        (
            SELECT Pool_Option_j, Pool_Type, Agency, Pool_Balance_Type, Servicer,
                SUM(HIGH_BAL_Y) HIGH_BAL_Y, 
                SUM(HIGH_BAL_N) HIGH_BAL_N,
                ( SUM(HIGH_BAL_Y)  * 100 ) / (SUM(HIGH_BAL_Y) + SUM(HIGH_BAL_N)) PERCENTAGE
            FROM
            (
                SELECT P1.Pool_Option_j, P1.Pool_Type, P1.Agency, P1.Pool_Balance_Type, P1.Servicer,
                    CASE WHEN L1.HighBalFlag = 'Y' THEN COUNT(*) ELSE 0 END HIGH_BAL_Y,
                    CASE WHEN L1.HighBalFlag = 'N' THEN COUNT(*) ELSE 0 END HIGH_BAL_N
                FROM EligiblePriceComb AS E1 
                    LEFT JOIN LoanData AS L1
                        ON E1.LoanID = L1.LoanID
                    LEFT JOIN PoolOptionData AS P1
                        ON E1.Pool_Opton_j = P1.Pool_Option_j
                WHERE P1.Pool_Balance_Type = 'Standard Balance'
                GROUP BY P1.Pool_Option_j, P1.Pool_Type, P1.Agency, P1.Pool_Balance_Type, P1.Servicer, L1.HighBalFlag
            ) AS P2
            GROUP BY Pool_Option_j, Pool_Type, Agency, Pool_Balance_Type, Servicer
            HAVING (( SUM(HIGH_BAL_Y)  * 100 ) / (SUM(HIGH_BAL_Y) + SUM(HIGH_BAL_N)) >=10)
        ) AS A1
        GROUP BY AGENCY
"""

cursor2.execute(sqlQuery2)
df3 = cursor2.fetchall()
cursor2.close()
conn.close()

names=[str(df3[i][0]) + '=> ' + str(df3[i][1]) for i in range(0, len(df3))]
size=[df3[i][1] for i in range(0, len(df3))]
 
# Create a circle for the center of the plot
my_circle=plt.Circle( (0,0), 0.7, color='white')
plt.pie(size, labels=names, wedgeprops = { 'linewidth' : 2, 'edgecolor' : 'white' })
plt.title('Number of pools which has high balanced loans more than 10% for each agency')
p=plt.gcf()
p.gca().add_artist(my_circle)
plt.show()




#######################  Showing all list of pools which has high balanced loans more than 10% for each agency #######################  

import plotly.graph_objects as go
from plotly.subplots import make_subplots

conn = p1.connect(r'Driver={SQL Server}; Server=DESKTOP-R6USKL7\MSSQL_DNST; Database=MortgageData; Trusted_Connection=yes;')
cursor1 = conn.cursor()
sqlQuery2 =  """\
       SELECT Pool_Option_j, Pool_Type, Agency, Pool_Balance_Type, Servicer,
            SUM(HIGH_BAL_Y) HIGH_BAL_Y, 
            ( SUM(HIGH_BAL_Y)  * 100 ) / (SUM(HIGH_BAL_Y) + SUM(HIGH_BAL_N)) PERCENTAGE
        FROM
        (
            SELECT P1.Pool_Option_j, P1.Pool_Type, P1.Agency, P1.Pool_Balance_Type, P1.Servicer,
                CASE WHEN L1.HighBalFlag = 'Y' THEN COUNT(*) ELSE 0 END HIGH_BAL_Y,
                CASE WHEN L1.HighBalFlag = 'N' THEN COUNT(*) ELSE 0 END HIGH_BAL_N
            FROM EligiblePriceComb AS E1 
                LEFT JOIN LoanData AS L1
                    ON E1.LoanID = L1.LoanID
                LEFT JOIN PoolOptionData AS P1
                    ON E1.Pool_Opton_j = P1.Pool_Option_j
            WHERE P1.Pool_Balance_Type = 'Standard Balance'
            GROUP BY P1.Pool_Option_j, P1.Pool_Type, P1.Agency, P1.Pool_Balance_Type, P1.Servicer, L1.HighBalFlag
        ) AS P2
        GROUP BY Pool_Option_j, Pool_Type, Agency, Pool_Balance_Type, Servicer
        HAVING (( SUM(HIGH_BAL_Y)  * 100 ) / (SUM(HIGH_BAL_Y) + SUM(HIGH_BAL_N)) >=10)
"""

cursor1.execute(sqlQuery2)
df2 = cursor1.fetchall()
cursor1.close()
conn.close()

fig = make_subplots(
    rows=1, cols=1,
    shared_xaxes=True,
    vertical_spacing=0.03,
    specs=[[{"type": "table"}]]
)

columns2 = ['Pool Id', 'Pool type', 'Agency', 'Pool Balance Type', 'Servicer', 'Number of HB Loans','Percentage of HB Loans']

fig.add_trace(
    go.Table(
        header=dict(
            values = columns2,
            font = dict(size=12),
            align="left"
        ),
        cells=dict(
            values=[[df2[i][j] for i in range (0,len(df2))] for j in range(0, len(columns2)) ] ,
            align = "left")
    ),
    row=1, col=1
)

fig.update_layout(
    height=450,
    showlegend=False,
    title_text="List of pools which has high balanced loans more than 10%",
)

fig.show()


