from flask import Flask, jsonify, json
import psycopg2
import os
import logging

from psycopg2 import OperationalError

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',  # Log message format
                    handlers=[logging.StreamHandler()])
app = Flask(__name__)
logger = logging.getLogger(__name__)

# PostgreSQL connection parameters
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_NAME = os.getenv('DB_NAME', 'pyserver')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')


# Connect to PostgreSQL database
def get_db_connection():
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, host=DB_HOST, password=DB_PASSWORD)
        return conn
    except OperationalError as e:
        logger.error(f"Error while connecting to PostgreSQL: {e}")
        return None


@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Python Web Server!"})


@app.route('/products')
def products():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Error connecting to database"}), 500

    try:
        cursor = conn.cursor()
        logger.debug("Fetching all products from the database.")
        cursor.execute("SELECT * FROM products;")  # Assuming 'products' is your table
        products = cursor.fetchall()
        cursor.close()

        if products:
            product_list = [{"id": product[0], "name": product[1], "price": product[2]} for product in products]
            logger.info(f"Retrieved {len(product_list)} products: {json.dumps(product_list, indent=2)}")

            return jsonify(product_list)
        else:
            logger.info("No products found.")
            return jsonify({"message": "No products found"}), 404
    except Exception as e:
        logger.error(f"Error retrieving products: {str(e)}")
        return f"Error retrieving products: {str(e)}"


# Start the web server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
