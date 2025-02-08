import connectdb
import logging
import pandas as pd
import time

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO 
)

def sqlexample(excel_filename, sql_file) -> None:
    db_cursor, connection = connectdb.connect()
    try:
        db_cursor.execute("DROP TABLE IF EXISTS procedurehistory;")
        connection.commit()

        # Read the SQL file and create the table
        with open(sql_file, "r") as create_file:
            create_command = create_file.read()
            db_cursor.execute(create_command)
            connection.commit()
            logging.info("Created table successfully")

        # Read the Excel file into a pandas dataframe
        sheet = pd.read_excel(excel_filename)

        column_map = {col: col.lower().replace(" ", "_") for col in sheet.columns}

        # Apply the mapping to the dataframe's column names
        sheet.rename(columns=column_map, inplace=True)

        columns = sheet.columns.tolist()

        insert_query = f"""
            INSERT INTO procedurehistory ({', '.join(columns)}) 
            VALUES ({', '.join(['%s'] * len(columns))})
        """

        start_time = time.time()

        # Iterate through each row of the Excel sheet and insert values into the table
        for index, row in sheet.iterrows():
            values = []

            # Iterate over the columns and collect the values
            for column in columns:
                value = row[column]
                if pd.isna(value):
                    value = None
                values.append(value)

            # Execute the insert query with the current values
            db_cursor.execute(insert_query, values)
            connection.commit()
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Time taken to insert records : {elapsed_time:.2f} seconds")

    except Exception as error:
        logging.error(error)

    finally:
        if db_cursor is not None:
            db_cursor.close()  # Closing the cursor
            logging.info("\nCursor closed ...")

        if connection is not None:
            connection.close()  # Closing the connection
            logging.info("\nDatabase connection terminated")

excel_file = "Excel file path"
sql_file = "DDL.sql file path"
sqlexample(excel_file, sql_file)