class Time(object):
    def __init__(self, start_year):
        self.time = 0

        self.start_year = start_year
        self.time_interval = 'months'  # Either days, weeks, months or years

        self.options = {'years': 1, 'months': 12, 'weeks': 52, 'days': 365}

        self.date = []
        self.total_days = 0
        self.decimal_time = 0

    def proceed(self):
        self.time += 1
        self.correct_formulation()

    def correct_formulation(self):
        options = {'years': 365, 'months': 30, 'weeks': 7, 'days': 1}
        date_list = [None] * len(options)
        remaining = self.time * options[self.time_interval]
        for index, option in enumerate(options): 
            date_list[index], remaining = self.divRem(remaining, options[option])
        # date_list = date_list[list(options.keys()).index(self.time_interval):] = None
        self.date = date_list
        self.total_days = self.divRem(self.time * options[self.time_interval], options['years'])[1]
        self.decimal_time = self.time * options[self.time_interval] / options['years'] + self.start_year

    @staticmethod
    def divRem(number, divider):
        return [int((number - (number % divider)) / divider), number % divider]
