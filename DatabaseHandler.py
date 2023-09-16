import datetime
import math
import sqlite3
from distances import get_all_distances

import pandas as pd
from tqdm.auto import tqdm

# from distances import get_distances


#  lat , lon
class DatabaseHandler:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def select(self, query, to_fetch_all=False):
        query = query.replace("\n", " ")
        self.cursor.execute(query)
        if to_fetch_all:
            return self.cursor.fetchall()

    @staticmethod
    def remove_whitespaces(query):
        return " ".join(query.split())

    def insert(self, query):
        query = self.remove_whitespaces(query)
        self.cursor.execute(query)
        self.conn.commit()
        return self.cursor.lastrowid

    def update(self, query):
        query = self.remove_whitespaces(query)
        self.cursor.execute(query)
        self.conn.commit()

    def delete(self, query):
        query = self.remove_whitespaces(query)
        self.cursor.execute(query)
        self.conn.commit()

    def excel_to_db(self, excel_path, sheet_name=0):
        dr = pd.read_excel(excel_path, sheet_name=sheet_name)
        dr.dropna(axis="index", how="any", inplace=True)
        distances_to_db = []
        routes_to_db = []
        for i, row in tqdm(list(dr.iterrows())):
            plant_lat = row["Plant Latitude"]
            plant_lon = row["Plant Longitude"]
            client_lat = row["Client Latitude"]
            client_lon = row["Client Longitude"]

            q = f"INSERT OR IGNORE INTO locations (lat, lon) VALUES ({plant_lat}, {plant_lon})"
            self.insert(q)
            a_id = self.select(
                f"SELECT id FROM locations WHERE (lat={plant_lat}) AND (lon={plant_lon})", to_fetch_all=True
            )
            a_id = a_id[0][0]

            q = f"INSERT OR IGNORE INTO locations (lat, lon) VALUES ({client_lat}, {client_lon})"
            self.insert(q)
            b_id = self.select(
                f"SELECT id FROM locations WHERE (lat={client_lat}) AND (lon={client_lon})", to_fetch_all=True
            )
            b_id = b_id[0][0]

            start_date = row["Date"].date().strftime("%d/%m/%Y")
            # distances = get_distances([(plant_lat, plant_lon)], [(client_lat, client_lon)])
            # distance = distances[0]
            distance = row["Distance [km]"]
            end_date = (row["Date"].date() + datetime.timedelta(days=distance // 500)).strftime("%d/%m/%Y")
            routes_to_db.append((a_id, b_id, start_date, end_date, distance, "HOLCIM", 0))
            distances_to_db.append((a_id, b_id, distance))
            distances_to_db.append((b_id, a_id, distance))

            if len(distances_to_db) > 1_000:
                self.cursor.executemany(
                    """
                    INSERT OR IGNORE INTO distances
                    (id_point_a, id_point_b, distance)
                    VALUES (?, ?, ?);
                    """,
                    distances_to_db,
                )
                distances_to_db = []

            if len(routes_to_db) > 1_000:
                self.cursor.executemany(
                    """
                    INSERT INTO routes
                    (id_starting_point, id_ending_point, delivery_start_date, delivery_end_date, distance, company, is_deleted)
                    VALUES (?, ?, ?, ?, ?, ?, ?);
                    """,
                    routes_to_db,
                )
                routes_to_db = []

        self.conn.commit()

    def create_db_schemas(self):
        table_1 = "routes"
        table_2 = "distances"
        table_3 = "locations"
        table_4 = "optimizations"

        self.cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {table_1} (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            id_starting_point INTEGER,
            id_ending_point INTEGER,
            delivery_start_date DATE,
            delivery_end_date DATE,
            distance DOUBLE,
            company VARCHAR(255),
            is_deleted BOOLEAN
            );"""
        )

        self.cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {table_2} (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            id_point_a INTEGER,
            id_point_b INTEGER,
            distance DOUBLE,
            UNIQUE (id_point_a, id_point_b)
            );"""
        )

        self.cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {table_3} (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            lon DOUBLE,
            lat DOUBLE,
            UNIQUE (lon, lat)
            );"""
        )
        
        self.cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {table_4} (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            delivery_start_date DATE,
            lot_A DOUBLE,
            lat_A DOUBLE,
            lot_B DOUBLE,
            lat_B DOUBLE,
            lot_C DOUBLE,
            lat_C DOUBLE,
            lot_D DOUBLE,
            lat_D DOUBLE
            );"""
        )

        self.conn.commit()

    def location_exists(self, lon, lat):
        q = f"SELECT id FROM locations WHERE (lat={lat}) AND (lon={lon})"
        res = self.select(q, to_fetch_all=True)

        if len(res) == 0:
            return None

        return res[0][0]

    def add_new_location(self, lon, lat):
        loc = self.location_exists(lon, lat)

        # if location already exists, return its id
        if loc is not None:
            return loc

        q = f"INSERT INTO locations (lat, lon) VALUES ({lat}, {lon})"
        self.insert(q)
        loc_id = self.cursor.lastrowid

        # compute distances to all other locations
        q = f"SELECT id, lat, lon FROM locations WHERE id != {loc_id}"
        res = self.select(q, to_fetch_all=True)

        origins = [(lat, lon)]
        destinations = [(l[1], l[2]) for l in res]

        distances = get_all_distances(origins, destinations)[0]

        distances_to_add = [(loc_id, res[i][0], distances[i]) for i in range(len(res))]
        distances_to_add += [(res[i][0], loc_id, distances[i]) for i in range(len(res))]

        self.cursor.executemany(
            """
            INSERT INTO distances
            (id_point_a, id_point_b, distance)
            VALUES (?, ?, ?);
            """,
            distances_to_add,
        )
        self.conn.commit()

        return loc_id

    def add_new_route(self, a_lon, a_lot, b_lon, b_lot, end_date, company):
        # Add new locations
        a_id = self.add_new_location(a_lon, a_lot)
        b_id = self.add_new_location(b_lon, b_lot)

        # Add new route
        distance = self.select(
            f"SELECT distance FROM distances WHERE (id_point_a={a_id}) AND (id_point_b={b_id})", to_fetch_all=True
        )[0][0]
        distance_to_days = distance // 500
        end_date_str = end_date.strftime("%d/%m/%Y")
        start_date_str = (end_date - datetime.timedelta(days=distance_to_days)).strftime("%d/%m/%Y")

        self.insert(
            f"""
            INSERT INTO routes
            (id_starting_point, id_ending_point, delivery_start_date, delivery_end_date, distance, company, is_deleted)
            VALUES ({a_id}, {b_id}, '{start_date_str}', '{end_date_str}', {distance}, '{company}', 0);
            """
        )

    def close(self):
        self.conn.close()


if __name__ == "__main__":
    table_4 = "optimizations"
    db = DatabaseHandler(r"./db/hack23_db.db")
    db.cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {table_4} (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            delivery_start_date DATE,
            lot_A DOUBLE,
            lat_A DOUBLE,
            lot_B DOUBLE,
            lat_B DOUBLE,
            lot_C DOUBLE,
            lat_C DOUBLE,
            lot_D DOUBLE,
            lat_D DOUBLE
            );"""
        )
    # db.create_db_schemas()
    # db.excel_to_db(r"./data/out_bound.csv")
    db.close()
