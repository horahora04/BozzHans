import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.database import database

test_data = {"_id": "test123", "title": "Produk Tes", "price_max": 10000}
database.insert_data(test_data)
