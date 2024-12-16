class PConfig:

    def calculate_training_time(self, data_training_time: dict) -> int:
        days = data_training_time["days"]
        hours = data_training_time["hours"]
        minutes = data_training_time["minutes"]
        seconds = data_training_time["seconds"]
        return days * 24 * 60 * 60 + hours * 60 * 60 + minutes * 60 + seconds