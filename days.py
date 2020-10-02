class Dates:
    def __init__(self, day, month, year, weekday, day_type, nr_positions, min_proficient, max_proficient):
        self.__day = day
        self.__month = month
        self.__year = year
        self.__weekday = weekday
        self.__day_type = day_type
        self.__nr_required_interns = nr_positions
        self.__nr_required_proficient_interns = min_proficient
        self.__nr_required_non_proficient_interns = nr_positions - max_proficient
        self.__nr_available_interns = 0
        self.__nr_available_proficient_interns = 0
        self.__nr_available_non_proficient_interns = 0
        self.__available_proficient_interns = []
        self.__available_non_proficient_interns = []
        self.__unavailable_proficient_interns = []
        self.__unavailable_non_proficient_interns = []
        self.__allocated_proficient_interns = []
        self.__allocated_non_proficient_interns = []
        self.__changes_to_other_dates = {}


    #################################   Get methods #################################
    def get_day(self):
        return self.__day

    def get_weekday(self):
        return self.__weekday

    def get_day_type(self):
        return self.__day_type

    def get_nr_required_interns(self):
        return self.__nr_required_interns

    def get_nr_required_proficient_interns(self):
        return self.__nr_required_proficient_interns

    def get_nr_required_non_proficient_interns(self):
        return self.__nr_required_non_proficient_interns

    def get_nr_available_interns(self):
        return self.__nr_available_interns

    def get_nr_available_proficient_interns(self):
        return self.__nr_available_proficient_interns

    def get_nr_available_non_proficient_interns(self):
        return self.__nr_available_non_proficient_interns

    def get_available_proficient_interns(self):
        return self.__available_proficient_interns

    def get_available_non_proficient_interns(self):
        return self.__available_non_proficient_interns

    def get_available_interns(self):
        return self.get_available_proficient_interns() + self.get_available_non_proficient_interns()

    def get_allocated_proficient_interns(self):
        return self.__allocated_proficient_interns

    def get_allocated_non_proficient_interns(self):
        return self.__allocated_non_proficient_interns

    def get_changes_to_other_dates(self):
        return self.__changes_to_other_dates

    def get_allocated_interns(self):
        return self.get_allocated_proficient_interns() + self.get_allocated_non_proficient_interns()

    def get_nr_allocated_interns(self):
        return len(self.get_allocated_interns())

    #################################   Change methods #################################
    def add_available_proficient_intern(self, intern):
        self.__available_proficient_interns.append(intern)
        self.__nr_available_interns += 1
        self.__nr_available_proficient_interns += 1

    def add_available_non_proficient_intern(self, intern):
        self.__available_non_proficient_interns.append(intern)
        self.__nr_available_interns += 1
        self.__nr_available_non_proficient_interns += 1

    def remove_available_proficient_intern(self, intern):
        self.__available_proficient_interns.remove(intern)
        self.__nr_available_interns -= 1
        self.__nr_available_proficient_interns -= 1

    def remove_available_non_proficient_intern(self, intern):
        self.__available_non_proficient_interns.remove(intern)
        self.__nr_available_interns -= 1
        self.__nr_available_non_proficient_interns -= 1

    def make_unavailable_proficient_intern(self, intern):
        self.remove_available_proficient_intern(intern)
        self.__unavailable_proficient_interns.append(intern)

    def make_unavailable_non_proficient_intern(self, intern):
        self.remove_available_non_proficient_intern(intern)
        self.__unavailable_non_proficient_interns.append(intern)

    def make_available_proficient_intern(self, intern):
        self.add_available_proficient_intern(intern)
        self.__unavailable_proficient_interns.remove(intern)

    def make_available_non_proficient_intern(self, intern):
        self.add_available_non_proficient_intern(intern)
        self.__unavailable_non_proficient_interns.remove(intern)

    def allocate_proficient_intern(self, intern):
        self.__allocated_proficient_interns.append(intern)
        self.__nr_required_interns -= 1
        self.__nr_required_proficient_interns -= 1

    def allocate_non_proficient_intern(self, intern):
        self.__allocated_non_proficient_interns.append(intern)
        self.__nr_required_interns -= 1
        self.__nr_required_non_proficient_interns -= 1

    def remove_allocation_proficient_intern(self, intern):
        self.__allocated_proficient_interns.remove(intern)
        self.__nr_required_interns += 1
        self.__nr_required_proficient_interns += 1

    def remove_allocation_non_proficient_intern(self, intern):
        self.__allocated_non_proficient_interns.remove(intern)
        self.__nr_required_interns += 1
        self.__nr_required_non_proficient_interns += 1

    def record_changes(self, intern, days_list):
        self.__changes_to_other_dates.update({intern: days_list})

    def remove_changes(self, intern):
        del self.__changes_to_other_dates[intern]

    def is_weekend(self):
        return self.__day_type == 'Weekend'