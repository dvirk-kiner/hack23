# this file contains the algorithm for optimizing joint drives
# There is a database table contains all the needed drives and there is another table contains all the distances between different locations
# The algorithm will find combinations of 2 drives that reduces the amount of empty trucks going back

import datetime
import sqlite3


class Optimizer:
    def __init__(self, db_path) -> None:
        self.db = sqlite3.connect(db_path)
        self.cur = self.db.cursor()
        self.parameters = {
            "max_distance_between_routes": 500,
        }

    def execute_query(self, query):
        res = self.db.execute(query)
        self.db.commit()
        return res

    def mark_route_as_deleted(self, route_id):
        query = f"UPDATE routes SET is_deleted=1 WHERE id={route_id}"
        self.execute_query(query)

    def optimize_route(self, ab_id, ab_distance, start_point_id, end_point_id, delivery_end_day):
        max_distance = self.parameters["max_distance_between_routes"]
        possible_date_start = delivery_end_day.strftime("%d/%m/%Y")
        possible_date_end = (delivery_end_day + datetime.timedelta(days=1)).strftime("%d/%m/%Y")

        query = f"""
        SELECT p.id as id, d.distance as ad, d2.distance as cd, d3.distance as bc FROM (
	        SELECT * FROM routes WHERE
            is_deleted=0 AND
            id_starting_point IN (
                SELECT id_point_b from distances WHERE
                (id_point_a={start_point_id}) AND
                (distance <= {max_distance})) AND
                (delivery_start_date BETWEEN '{possible_date_start}' AND '{possible_date_end}')
            ) AS p
        JOIN distances d ON p.id_ending_point = d.id_point_a AND d.id_point_b = {start_point_id}
        JOIN distances d2 ON p.id_starting_point = d2.id_point_a AND p.id_ending_point = d2.id_point_b
        JOIN distances d3 ON d3.id_point_a = p.id_starting_point AND d3.id_point_b = {end_point_id}
        WHERE ad <= {max_distance} AND ({ab_distance} + cd > bc + ad);
        """
        query = query.replace("\n", " ")
        self.cur.execute(query)

        record = self.cur.fetchone()

        if record is None:
            return ab_id, 0 # no optimization

        optimized_route_id, ad_distance, cd_distance, bc_distance = record

        empty_distance_utilization = 100.0 * (bc_distance + ad_distance) / (ab_distance + cd_distance)

        self.mark_route_as_deleted(ab_id)
        self.mark_route_as_deleted(optimized_route_id)
        return optimized_route_id, empty_distance_utilization

    def optimize_routes(self, company="HOLCIM"):
        tomorrow_date = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%d/%m/%Y")

        query = f"SELECT id FROM routes WHERE is_deleted=0 AND company=\"{company}\" AND delivery_start_date=\"{tomorrow_date}\""
        self.cur.execute(query)
        routes_records_to_optimize = self.cur.fetchall()


        for idx, route_record in enumerate(routes_records_to_optimize):
            route_id = route_record[0]
            query = f"SELECT * FROM routes WHERE id={route_id}"
            self.cur.execute(query)
            route_data = self.cur.fetchone()

            (
                route_id,
                id_starting_point,
                id_ending_point,
                delivery_start_date,
                delivery_end_date,
                distance,
                company,
                is_deleted,
            ) = route_data

            if is_deleted:
                print(f"Route {route_id} is already deleted. Skipping")
                continue
            
            # if idx == 0:
            #     delivery_end_date != (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%d/%m/%Y")

            opt_out = self.optimize_route(route_id, distance, id_starting_point, id_ending_point, delivery_end_date)

            if opt_out is None:
                print(f"Route {route_id} cannot be optimized. Continuing")
                continue

            optimization_route_id, empty_distance_utilization = opt_out

            print(f"Optimized route {route_id} to {optimization_route_id}. Utilization: {empty_distance_utilization:.2f}%")

            # routes_optimization.append((route_id, optimization_route_id))
            routes_optimization = []
            routes_optimization_ptrs = []
            routes_optimization_ptrs.append(tomorrow_date)
            if route_id == optimization_route_id:
                q = f"SELECT id_starting_point, id_ending_point FROM routes WHERE id={route_id}"
                self.cur.execute(q)
                route_data_start,  route_data_end = self.cur.fetchone()
                routes_optimization.append(route_data_start)
                routes_optimization.append(route_data_end)
                routes_optimization.append(route_data_end)
                routes_optimization.append(route_data_start)
            else:
                for route_idx in [route_id, optimization_route_id]:
                    q = f"SELECT id_starting_point, id_ending_point FROM routes WHERE id={route_idx}"
                    self.cur.execute(q)
                    route_data_start,  route_data_end = self.cur.fetchone()
                    routes_optimization.append(route_data_start)
                    routes_optimization.append(route_data_end)
            for r_o in routes_optimization:
                q = f"SELECT lon, lat FROM locations WHERE id={r_o}"
                self.cur.execute(q)
                lot_p,  lat_p = self.cur.fetchone()
                routes_optimization_ptrs.append(lot_p)
                routes_optimization_ptrs.append(lat_p)
            
            q = f"INSERT INTO routes_optimization \
                (delivery_start_date, lot_A, lat_A,lot_B, lat_B,lot_C, lat_C,lot_D, lat_D) VALUES \
                    (?,?,?,?,?,?,?,?,?);"
            
            self.cur.executemany(q, routes_optimization_ptrs)

        # return routes_optimization

    def __del__(self):
        self.db.close()
