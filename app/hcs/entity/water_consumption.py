from ..models import WaterMeterLog


class WaterConsumption:
    def __init__(self, water_meter_id, curr_year, curr_month):
        self.water_meter_id = water_meter_id
        self.curr_year = curr_year
        self.curr_month = curr_month

    def count(self):
        """Count the difference between water consumption of the current and
        the previous month."""
        previous_water_meter_consumption = self.__get_previous_water_meter_consumption()
        current_water_meter_log = WaterMeterLog.objects.filter(water_meter_id=self.water_meter_id, year=self.curr_year, month=self.curr_month).first()
        return current_water_meter_log.consumed - previous_water_meter_consumption

    def __get_previous_year_n_month(self):
        """Find out which was the previous year and month based on the 
        current year and month values."""
        previous_month = self.curr_month - 1
        previous_year = self.curr_year
        is_previous_month_out_of_range = previous_month == 0
        if is_previous_month_out_of_range:
            previous_month = 12
            previous_year -= 1
        return (previous_year, previous_month)

    def __get_previous_water_meter_consumption(self):
        """Get consumption based on the water meter from the previous month.
        If it doesn't exist, return 0 instead."""
        previous_year, previous_month = self.__get_previous_year_n_month()
        entry = WaterMeterLog.objects.filter(water_meter_id=self.water_meter_id, year=previous_year, month=previous_month).first()
        return entry.consumed if entry else 0
