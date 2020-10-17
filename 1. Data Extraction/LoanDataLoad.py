
import pyodbc as p1
import os
import json

##### connect to the SQL Server DB and insert data
def insertIntoSQL(allDicts, LoadIndicator):
    #preparing conection string for SQL Server connection
    conn = p1.connect(r'Driver={SQL Server}; Server=DESKTOP-R6USKL7\MSSQL_DNST; Database=MortgageData; Trusted_Connection=yes;')
    cursor = conn.cursor()
    cursor.fast_executemany = True
    for dicts in allDicts:
        # preparing SQL Query for each type of files
        if LoadIndicator == 1:
            insertQuery = "INSERT INTO dbo.LoanData (LoanID , Amount, FICO, DTI, HighBalFlag, PropOcc, PropState, PropType, Purpose) " \
                      "VALUES ( '" + str(dicts["LoanID"]) + "' , " \
                          + str(dicts["Amount"]) + " , " \
                          + str(dicts["FICO"]) + ", " \
                          + str(dicts["DTI"]) + ", '" \
                          + str(dicts["HighBalFlag"]) + "', '" \
                          + str(dicts["PropOcc"]) + "' , '" \
                          + str(dicts["PropState"]) + "' , '" \
                          + str(dicts["PropType"]) + "' , '" \
                          + str(dicts["Purpose"]) + "' )"
        elif LoadIndicator == 2:
            insertQuery = "INSERT INTO dbo.PoolOptionData (Pool_Option_j, Pool_Type, Pool_Balance_Type, Agency, Servicer) " \
                          "VALUES ( '" + str(dicts["Pool Option, j"]) + "' , '" \
                          + str(dicts["Pool Type"]) + "' , '" \
                          + str(dicts["Pool Balance Type"]) + "', '" \
                          + str(dicts["Agency"]) + "', '" \
                          + str(dicts["Servicer"]) + "' )"
        elif LoadIndicator == 3:
            insertQuery = "INSERT INTO dbo.EligiblePriceComb (LoanID, Price_P_ijk, Pool_Opton_j, Servicer_k) " \
                          "VALUES ( '" + str(dicts["LoanID"]) + "' , " \
                          + str(dicts["Price, P_ijk"]) + " , '" \
                          + str(dicts["Pool Opton, j"]) + "', '" \
                          + str(dicts["Servicer, k"]) + "' )"
        elif LoadIndicator == 4:
            insertQuery = "INSERT INTO dbo.BaseLine (LoanID, Price, Selected_Pool_ID, Servicer) " \
                          "VALUES ( '" + str(dicts["Loan ID"]) + "' , " \
                          + str(dicts["Price"]) + " , '" \
                          + str(dicts["Selected Pool ID"]) + "', '" \
                          + str(dicts["Servicer"]) + "' )"
        cursor.execute(insertQuery)
    cursor.commit()
    cursor.close()
    conn.close()

######################################### Main Function ###############################################
def main(arg, LoadIndic):
    allDicts = []
    source_folder = arg

    #iterating through all the files in folder
    for file in os.listdir(source_folder):
        #concataneting foler and file name for each file
        full_filename = "%s/%s" % (source_folder, file)
        with open(full_filename, 'r') as fi:
            dict = json.load(fi)
            # collecting records of each JSON file into the list
            allDicts.append(dict)
        fi.close()
    #calling a function to insert all records of JSON file
    insertIntoSQL(allDicts, LoadIndic)

if __name__ == "__main__":
    #set the name of folder which includes all JSON files of Loan data

    DataFolder = "Pool Optimization Data for TC v5/Loan Data"
    print('Data extraction step is started here ... ')
    main(DataFolder, 1)
    print('Successfully extracted data from Loan Data JSON file')

    DataFolder = "Pool Optimization Data for TC v5/Pool Option Data"
    main(DataFolder, 2)
    print('Successfully extracted data from Pool option Data JSON file')

    DataFolder = "Pool Optimization Data for TC v5/Eligible Pricing Combinations"
    main(DataFolder, 3)
    print('Successfully extracted data from Eligible Pricing Combinations Data JSON file')

    DataFolder = "Pool Optimization Data for TC v5/Baseline (Constraints Set B)"
    main(DataFolder, 4)
    print('Successfully extracted data from Baseline (Constraints Set B) Data JSON file')


