import psycopg2 as pg

def product_exists(external_id, vendor_id):
    query = f"SELECT id FROM products WHERE external_id = '{external_id} and vendor_id = '{vendor_id}'"
    cursor.execute(query)
    return cursor.fetchone() is not None

def insert_new_product(external_id, name, vendor_id, category_id, subcategory_id, msrp, product_link, created_at, atc_link, combo):
    query = f"""
    INSERT INTO
        products (external_id, name, vendor_id, category_id, subcategory_id, msrp, product_link, created_at, atc_link, combo)
    VALUES
        ('{external_id}', '{name}', {vendor_id}, {category_id}, {subcategory_id}, {msrp}, '{product_link}', '{created_at}', '{atc_link}', {combo})
    """    
    cursor.execute(query)
    
    return True

def insert_new_drop(external_id, vendor_id, price, created_at):
    query = f"""
    INSERT INTO
        drops (product_id, price, created_at)
    VALUES
        ((SELECT id FROM products WHERE external_id = '{external_id}' and vendor_id = {vendor_id}), {price}, '{created_at}')
    """
    cursor.execute(query)

    return True

def process_drops(drops):
    for drop in drops:
        if not product_exists(drop[0], drop[2]):
            insert_new_product(drop[0], drop[1], drop[2], drop[3], drop[4], drop[5], drop[6], drop[7], drop[8], drop[9])

        insert_new_drop(drop[0], drop[2], drop[5], drop[7])

# Postgres info to connect
connection_args = {
    'host': '192.168.0.242',
    'dbname': 'tracker-network',
    'port': 5432
}

connection = pg.connect(**connection_args)
connection.autocommit = True

# make a cursor
cursor = connection.cursor()