from Point import Point

class Order:
    def __init__(self, start_point:Point, end_point:Point, company, delivery_date):
        self.starning_point = start_point
        self.ending_point = end_point
        self.company = company
        self.delivery_date = delivery_date