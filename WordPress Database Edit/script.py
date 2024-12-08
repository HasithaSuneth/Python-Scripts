from datetime import datetime
import mysql.connector
from db_config import db_config, table_prefix

 
# Establish database connection
def connect_to_database():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        return conn, cursor
    except mysql.connector.Error as err:
        print(f"Database Connection Error: {err}")
        exit(1)
    

def check_timestamps():
    sale_start_date = datetime(2024, 12, 1, 0, 0, 0)  # YYYY-MM-DD hh:mm:ss
    sale_end_date = datetime(2025, 1, 1, 23, 59, 59)
    sale_start_timestamp = int(sale_start_date.timestamp())
    sale_end_timestamp = int(sale_end_date.timestamp())
    print(sale_start_timestamp, sale_end_timestamp)
    
 
# Fetch all product IDs
def get_product_list(cursor):
    cursor.execute(f"SELECT ID FROM {table_prefix}posts WHERE post_type = 'product' AND post_status = 'publish'")
    return [row[0] for row in cursor.fetchall()]
     

# Check Current Sale Price Dates
def get_sale_dates(cursor):
    cursor.execute(
        f"SELECT post_id FROM {table_prefix}postmeta WHERE meta_key = %s OR meta_key = %s",
        ('_sale_price_dates_from', '_sale_price_dates_to')
    )
    return list(set([row[0] for row in cursor.fetchall()]))
 

# Add Sale Price Dates
def add_sale_dates(cursor, conn, product_ids, skip=True):
    sale_start_date = datetime(2024, 12, 1, 0, 0, 0)  # YYYY-MM-DD hh:mm:ss
    sale_end_date = datetime(2025, 1, 1, 23, 59, 59)

    # Convert to Unix timestamp
    sale_start_timestamp = int(sale_start_date.timestamp())
    sale_end_timestamp = int(sale_end_date.timestamp())

    # Add or update sale date metadata for each product
    for product_id in product_ids:
        try:
            # Check if _sale_price_dates_from exists
            cursor.execute(
                f"SELECT meta_id FROM {table_prefix}postmeta WHERE post_id = %s AND meta_key = %s",
                (product_id, '_sale_price_dates_from')
            )
            result_from = cursor.fetchone()

            if result_from:
                if not skip:
                    cursor.execute(
                        f"UPDATE {table_prefix}postmeta SET meta_value = %s WHERE meta_id = %s",
                        (sale_start_timestamp, result_from[0])
                    )
            else:
                cursor.execute(
                    f"INSERT INTO {table_prefix}postmeta (post_id, meta_key, meta_value) VALUES (%s, %s, %s)",
                    (product_id, '_sale_price_dates_from', sale_start_timestamp)
                )

            # Check if _sale_price_dates_to exists
            cursor.execute(
                f"SELECT meta_id FROM {table_prefix}postmeta WHERE post_id = %s AND meta_key = %s",
                (product_id, '_sale_price_dates_to')
            )
            result_to = cursor.fetchone()

            if result_to: 
                if not skip:
                    cursor.execute(
                        f"UPDATE {table_prefix}postmeta SET meta_value = %s WHERE meta_id = %s",
                        (sale_end_timestamp, result_to[0])
                    )
            else:
                cursor.execute(
                    f"INSERT INTO {table_prefix}postmeta (post_id, meta_key, meta_value) VALUES (%s, %s, %s)",
                    (product_id, '_sale_price_dates_to', sale_end_timestamp)
                )
                
            print(f'Product {product_id} processed.')

        except mysql.connector.Error as err:
            print(f"Error updating sale dates for product ID {product_id}: {err}")

    # Commit changes
    conn.commit()
    print(f"Sale dates processed for {len(product_ids)} products.")


# Remove Sale Price Dates
def remove_sale_dates(cursor, conn, product_ids):
    for product_id in product_ids:
        try:
            cursor.execute(
                f"DELETE FROM {table_prefix}postmeta WHERE post_id = %s AND meta_key IN ('_sale_price_dates_from', '_sale_price_dates_to')",
                (product_id,)
            )
        except mysql.connector.Error as err:
            print(f"Error removing sale dates for product ID {product_id}: {err}")
    
    # Commit changes
    conn.commit()
    print(f"Sale dates removed for {len(product_ids)} products.")

  
# Get Xstore Products Sale Counter Values 
def get_xstore_sale_counter(cursor):
    cursor.execute(f"SELECT post_id, meta_value FROM {table_prefix}postmeta WHERE meta_key = '_et_sale_counter'")
    return cursor.fetchall()
     
     
# Update Xstore Products Sale Counter Values 
def update_xstore_sale_counter(cursor, conn, product_ids, type):
    for product_id in product_ids:
        try:
            cursor.execute(
                f"UPDATE {table_prefix}postmeta SET meta_value = %s WHERE post_id = %s AND meta_key = %s",
                (type, product_id, '_et_sale_counter')
            )
            print(f'Product {product_id} processed.')
            
        except mysql.connector.Error as err:
            print(f"Error updating sale dates for product ID {product_id}: {err}")
    
    # Commit changes
    conn.commit()
    print(f"Xstore Sale counter update for {len(product_ids)} products.")


# Main function to run all processes
def main():
    conn, cursor = connect_to_database()
    print("Database connection established.")

    try:
        # Get product list
        product_ids = get_product_list(cursor)
        
        # ---------------- *** WARRNING *** ---------------------
        # ----------------      UPDATE      ---------------------
        # ------------ product_ids need to be a list ------------
        
        # add_sale_dates(cursor, conn, product_ids) # skip=False
        # add_sale_dates(cursor, conn, [4999], skip=False) # skip=False to update 
        # remove_sale_dates(cursor, conn, product_ids)
        # remove_sale_dates(cursor, conn, [4999])
        # update_xstore_sale_counter(cursor, conn, product_ids, 'single') 
        # update_xstore_sale_counter(cursor, conn, [4999], 'single') 
        
        # -------------------------------------------------------
        
        # ------------------      GET      ----------------------
        print(f"Found {len(product_ids)} products.")
        # print(product_ids)
        # check_timestamps()
        # print(get_sale_dates(cursor))
        # print(get_xstore_sale_counter(cursor))
        # -------------------------------------------------------
        
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("Database connection closed.")
         
         
if __name__ == "__main__":
    main()