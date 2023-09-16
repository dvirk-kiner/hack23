import datetime
import math
import sqlite3

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
        dr.dropna(axis='index', how='any', inplace=True)
        to_db = []
        for i, row in tqdm(list(dr.iterrows())):
            plant_lat = row["Plant Latitude"]
            plant_lon = row["Plant Longitude"]
            client_lat = row["Client Latitude"]
            client_lon = row["Client Longitude"]

            q = f"INSERT OR IGNORE INTO locations (lat, lon) VALUES ({plant_lat}, {plant_lon})"
            a_id = self.insert(q)

            q = f"INSERT OR IGNORE INTO locations (lat, lon) VALUES ({client_lat}, {client_lon})"
            b_id = self.insert(q)

            start_date = row["Date"].date().strftime("%d/%m/%Y")
            # distances = get_distances([(plant_lat, plant_lon)], [(client_lat, client_lon)])
            # distance = distances[0]
            distance = row["Distance [km]"]
            end_date = (row["Date"].date() + datetime.timedelta(days=distance // 500)).strftime("%d/%m/%Y")
            to_db.append((a_id, b_id, start_date, end_date, distance, "HOLCIM", 0))
            to_db.append((b_id, a_id, start_date, end_date, distance, "HOLCIM", 0))

            self.insert(
                f"""
                INSERT INTO routes
                (id_starting_point, id_ending_point, delivery_start_date, delivery_end_date, distance, company, is_deleted)
                VALUES ({a_id}, {b_id}, {start_date}, {end_date}, {distance}, "HOLCIM", 0);
                """
            )

        # self.cursor.executemany(
        #     """
        #     INSERT INTO routes
        #     (id_starting_point, id_ending_point, delivery_start_date, delivery_end_date, distance, company, is_deleted)
        #         VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        #     """,
        #     to_db,
        # )

        self.conn.commit()

    def create_db_schemas(self):
        table_1 = "routes"
        table_2 = "distances"
        table_3 = "locations"

        self.cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {table_1} (
            id INTEGER PRIMARY KEY NOT NULL,
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
            id INTEGER PRIMARY KEY NOT NULL,
            id_point_a INTEGER,
            id_point_b INTEGER,
            distance DOUBLE,
            UNIQUE (id_point_a, id_point_b)
            );"""
        )

        self.cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {table_3} (
            id INTEGER PRIMARY KEY NOT NULL,
            lon DOUBLE,
            lat DOUBLE,
            UNIQUE (lon, lat)
            );"""
        )

        self.conn.commit()

    def close(self):
        self.conn.close()


if __name__ == "__main__":
    db = DatabaseHandler(r"./db/hack23_db.db")
    db.create_db_schemas()
    db.excel_to_db(r"./data/out_bound.csv")
    db.close()
