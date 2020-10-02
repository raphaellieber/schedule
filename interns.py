class Interns:
    def __init__(self, name, proficiency, nr_asked, pos_dates, req_dates, mand_dates, nr_weekends):
        self.__name = name
        self.__proficiency = proficiency
        self.__nr_asked = nr_asked
        self.__dates_possible = pos_dates
        self.__dates_requested = req_dates
        self.__dates_mandatory = mand_dates
        self.__nr_required_weekends = nr_weekends[0]
        self.__nr_permitted_weekends = nr_weekends[1]
        self.__dates_allocated = []
        self.__nr_allocated = 0
        self.__available = True
        self.__score = 0

    def get_name(self):
        return self.__name

    def get_proficiency(self):
        return self.__proficiency

    def get_nr_asked(self):
        return self.__nr_asked

    def get_possible_dates(self):
        return self.__dates_possible

    def get_requested_dates(self):
        return self.__dates_requested

    def get_mandatory_dates(self):
        return self.__dates_mandatory

    def get_allocated_dates(self):
        return self.__dates_allocated

    def get_nr_required_weekend_days(self):
        return self.__nr_required_weekends

    def get_nr_allocated(self):
        return self.__nr_allocated

    def get_score(self):
        return self.__score

    def allocate(self, date):
        self.__dates_allocated.append(date)
        self.__nr_allocated += 1

    def remove_last_allocation(self):
        del self.__dates_allocated[-1]
        self.__nr_allocated -= 1

    def weekend_allocated(self):
        self.__nr_required_weekends -= 1
        self.__nr_permitted_weekends -= 1

    def removed_weekend_allocation(self):
        self.__nr_required_weekends += 1
        self.__nr_permitted_weekends += 1

    def weekend_allocation_required(self):
        return self.__nr_required_weekends > 0

    def weekend_allocation_permitted(self):
        return self.__nr_permitted_weekends > 0