import logging
import pandas as pd
import connectdb
import time

logging.basicConfig(level=logging.INFO)

def get_column_data_types(df):
    column_data_types = {}
    for column in df.columns:
        if pd.api.types.is_numeric_dtype(df[column]):
            column_data_types[column] = "DECIMAL(10,0)" 
        else:
            column_data_types[column] = "TEXT"  
    return column_data_types

db_cursor, connection = connectdb.connect()

try:
    dataset_link = "csv file path"
    df = pd.read_csv(dataset_link)

    table_name = dataset_link.split("/")[-1].replace(".csv","")
    # print(table_name)

    db_cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
    connection.commit()

    column_data_types = get_column_data_types(df)

    columns_with_types = ', '.join([f'"{column}" {data_type}' for column, data_type in column_data_types.items()])
    create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_with_types});"

    db_cursor.execute(create_table_query)
    connection.commit()
    logging.info(f"{table_name} has been created successfully !")

    # Insert data into the table
    insert_query = f"""INSERT INTO {table_name} ({', '.join([f'{column}' for column in df.columns])}) 
                        VALUES ({', '.join(['%s' for _ in df.columns])})"""
    
    start_time = time.time()
    # Insert each row in the dataframe into the table
    for index, row in df.iterrows():
        db_cursor.execute(insert_query, tuple(row))  
        if index % 100 == 0:
            connection.commit()
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    logging.info(f"Time taken to insert records : {elapsed_time:.2f} seconds")
    # Final commit after all rows are inserted
    connection.commit()
    logging.info(f"Data has been inserted successfully into '{table_name}' table.")

    alter_query = f"ALTER TABLE {table_name} ALTER COLUMN timestamp TYPE TIMESTAMP USING timestamp::TIMESTAMP;"
    db_cursor.execute(alter_query)
    connection.commit()
    logging.info(f"Column 'timestamp' has been updated to DATETIME.")

    group_by_query = f"""
                            SELECT extract(year from timestamp) as year, count(*) as video_count
                            FROM {table_name}
                            GROUP BY year
                            ORDER BY year;
                    """
    db_cursor.execute(group_by_query)
    result = db_cursor.fetchall()
    logging.info(f"Grouped data by timestamp: {result}")

except Exception as error:
    logging.error(error)

finally:
    if db_cursor is not None:
        db_cursor.close()  # Closing the cursor
        logging.info("\nCursor closed ...")

    if connection is not None:
        connection.close()  # Closing the connection
        logging.info("\nDatabase connection terminated ...")