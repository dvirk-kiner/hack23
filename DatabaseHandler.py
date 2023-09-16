import sqlite3
import csv, math
from datetime import datetime

from distances import get_distances
#  lat , lon
class DatabaseHandler:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        
    def select(self, query, to_fetch_all=False):
        self.cursor.execute(query)
        if to_fetch_all:
            return self.cursor.fetchall()
        
    def insert(self, query):
        print("_"*20)
        print(query)
        print(self.cursor.execute(query))
        print("_"*20)
        self.conn.commit()
    
    def update(self, query):
        self.cursor.execute(query)
        self.conn.commit()
        
    def delete(self, query):
        self.cursor.execute(query)
        self.conn.commit()
    
    def insert_csv_to_db(self, csv_path, table_name="routes"):
        print(csv_path)
        with open(csv_path, 'r') as f:
            # self.cursor.execute(f"DELETE FROM {table_name}")
            dr = csv.DictReader(f)
            to_db = []
            for i in dr:
                plant_lat = i["Plant Latitude"]
                plant_lon = i["Plant Longitude"]
                client_lat = i["Client Latitude"]
                client_lon = i["Client Longitude"]
                
                q = f"INSERT INTO locations (lat, lon) VALUES ({plant_lat}, {plant_lon})"
                self.insert(q)
                res = self.select(f"SELECT id FROM locations WHERE lat={plant_lat} AND lon={plant_lon}")
                
                a_id = res[0][0]
                
                q = f"INSERT INTO locations (lat, lon) VALUES ({client_lat}, {client_lon})"
                self.insert(q)
                res = self.select(f"SELECT id FROM locations WHERE lat={client_lat} AND lon={client_lon}")
                b_id = res[0][0]
                
                start_date = datetime.strptime(i["Date"], "%d-%m-%Y")
                distance =get_distances((plant_lat, plant_lon),(client_lat, client_lon))
                end_date = distance / 50 / 10
                end_date = math.ceil(distance / 50 / 10 ) if end_date >= 1 else 0
                to_db.append((a_id, b_id, start_date, end_date, distance, "Holcin", 0))
                
            self.cursor.executemany(f"INSERT INTO {table_name} \
                (id_starting_point, id_ending_point, delivery_start_date, delivery_end_date, distance, company, is_deleted) \
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?);", to_db)
            
            self.conn.commit()
            
    def create_db_schemas(self):
        table_1 = "routes"
        table_2 = "distances"
        table_3 = "locations"

        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_1} ( \
            id INT AUTO_INCREMENT PRIMARY KEY, \
            id_starting_point DOUBLE, \
            id_ending_point DOUBLE, \
            delivery_start_date DATE, \
            delivery_end_date DATE, \
            distance DOUBLE, \
            company VARCHAR(255), \
            is_deleted BOOLEAN \
            )")
        # id	id_point_A	id_point_A	distance
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_2} ( \
            id INT AUTO_INCREMENT PRIMARY KEY, \
            id_point_a INT, \
            id_point_b INT, \
            distance DOUBLE, \
            UNIQUE (id_point_a, id_point_b) \
            )")
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_3} ( \
            id INT AUTO_INCREMENT PRIMARY KEY, \
            lon DOUBLE, \
            lat DOUBLE, \
            UNIQUE (lon, lat)\
            )")
        
        self.conn.commit()
        
    def close(self):
        self.conn.close()
        
if __name__ == "__main__":
    
    db = DatabaseHandler(r"/Users/Bar/Desktop/hackZurich_2023/hack23/db/hack23_db.db")
    db.create_db_schemas()
    db.insert_csv_to_db(r"/Users/Bar/Desktop/hackZurich_2023/hack23/data/out_bound.csv")
    db.close()