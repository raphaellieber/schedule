import pandas as pd
from interns import *
from days import *
from tkinter import *

###################################     Constants    ###################################
NR_INTERNS_PER_DAY = 5
NR_PROFICIENT_PER_DAY = [2, 3]
NR_OF_WEEKEND_DAYS = [0, 5]


###################################     Initiation    ###################################
def pos_dates(req_list, days_list):
    return [days_list[i] for i in range(len(req_list)) if req_list[i] != 'no']


def req_dates(req_list, days_list):
    return [days_list[i] for i in range(len(req_list)) if req_list[i] == 'required']


def mand_dates(req_list, days_list):
    return [days_list[i] for i in range(len(req_list)) if req_list[i] == 'mandatory']


def allocate_mandatory(list_of_interns):
    for intern in list_of_interns:
        for date in intern.get_mandatory_dates():
            if intern.get_proficiency():
                allocate_proficient_intern(date, intern)
            else:
                allocate_non_proficient_intern(date, intern)


def create_intern_list_for_each_day(list_of_interns):
    for intern in list_of_interns:
        if intern.get_proficiency():
            for date in intern.get_possible_dates():
                date.add_available_proficient_intern(intern)
        else:
            for date in intern.get_possible_dates():
                date.add_available_non_proficient_intern(intern)


###################################     Legality    ###################################
def more_than_enough_proficient_interns(day, proficient_intern_index, non_proficient_intern_index):
    remaining_proficient_interns = day.get_nr_available_proficient_interns() - proficient_intern_index
    remaining_non_proficient_interns = day.get_nr_available_non_proficient_interns() - non_proficient_intern_index
    return remaining_proficient_interns > day.get_nr_required_proficient_interns() and \
           remaining_proficient_interns + remaining_non_proficient_interns > day.get_nr_required_interns()


def more_than_enough_non_proficient_interns(day, proficient_intern_index, non_proficient_intern_index):
    remaining_proficient_interns = day.get_nr_available_proficient_interns() - proficient_intern_index
    remaining_non_proficient_interns = day.get_nr_available_non_proficient_interns() - non_proficient_intern_index
    return remaining_non_proficient_interns > day.get_nr_required_non_proficient_interns() and \
           remaining_proficient_interns + remaining_non_proficient_interns > day.get_nr_required_interns()


def last_intern_in_group(intern_index, group_size):
    return intern_index == group_size - 1

def legal_to_adapt_future_days(future_potential_dates, days_to_adapt, intern):
    """
    consider adding verification if there will remain enough available days for the intern.
    """
    nr_to_allocate = intern.get_nr_asked() - intern.get_nr_allocated()
    nr_available_currently = len(future_potential_dates) + 1
    if nr_to_allocate > nr_available_currently:
        return False

    if intern.get_proficiency():
        for day in days_to_adapt:
            if not more_than_enough_proficient_interns(day, 0, 0):
                return False
    else:
        for day in days_to_adapt:
            if not more_than_enough_non_proficient_interns(day, 0, 0):
                return False
    return True

def weekends_allocation_legal(intern, remaining_days):
    if not intern.weekend_allocation_required():
        return True
    else:
        remaining_weekend_days = [day.get_day() for day in remaining_days if day.is_weekend()]
        nr_relevant_remaining_weekend_days = len(remaining_weekend_days) - amount_of_proximal_days(remaining_weekend_days)
        return intern.get_nr_required_weekend_days() <= nr_relevant_remaining_weekend_days

def amount_of_proximal_days(days_list):
    if len(days_list) <= 1:
        return 0
    if days_list[1] - days_list[0] == 1:
        return 1 + amount_of_proximal_days(days_list[1:])
    else:
        return 0 + amount_of_proximal_days(days_list[1:])

###################################     Scheduling - Regular functions   ###################################
def allocate_proficient_intern(date, intern):
    intern.allocate(date)
    if date.is_weekend():
        intern.weekend_allocated()
    date.allocate_proficient_intern(intern)


def allocate_non_proficient_intern(date, intern):
    intern.allocate(date)
    if date.is_weekend():
        intern.weekend_allocated()
    date.allocate_non_proficient_intern(intern)


def remove_allocation(intern, date):
    intern.remove_last_allocation()
    if date.is_weekend():
        intern.removed_weekend_allocation()
    if intern.get_proficiency():
        date.remove_allocation_proficient_intern(intern)
    else:
        date.remove_allocation_non_proficient_intern(intern)


def adapt_more_than_1(days_list, day_index, intern, relevant_days_index_list):
    if intern.get_nr_asked() == intern.get_nr_allocated():
        relevant_days_index_list.extend([index for index in range(day_index + 2, len(days_list))])
    return [days_list[new_index] for new_index in relevant_days_index_list if
            intern in days_list[new_index].get_available_interns()]


def adapt_more_than_2(days_list, day_index, intern, relevant_days_index_list):
    if intern.get_nr_asked() == intern.get_nr_allocated():
        relevant_days_index_list.extend([index for index in range(day_index + 2, len(days_list))])
    else:
        relevant_days_index_list.append(day_index + 2)
    return [days_list[new_index] for new_index in relevant_days_index_list if
            intern in days_list[new_index].get_available_interns()]


def adapt_more_than_3(days_list, day_index, intern, relevant_days_index_list):
    if intern.get_nr_asked() == intern.get_nr_allocated():
        relevant_days_index_list.extend([index for index in range(day_index + 2, len(days_list))])
    else:
        relevant_days_index_list.extend([day_index + 2, day_index + 3])
    return [days_list[new_index] for new_index in relevant_days_index_list if
            intern in days_list[new_index].get_available_interns()]


def adapt_more_than_7(days_list, day_index, intern, relevant_days_index_list):
    if intern.get_nr_asked() == intern.get_nr_allocated():
        relevant_days_index_list.extend([index for index in range(day_index + 2, len(days_list))])
    else:
        relevant_days_index_list.extend([day_index + 2, day_index + 3])
        if days_list[day_index].get_weekday() in ['Wed', 'Thu']:
            relevant_days_index_list.extend([index for index in range(day_index + 7, len(days_list), 7)])
        elif days_list[day_index].is_weekend() and not intern.weekend_allocation_permitted():
            relevant_days_index_list.extend([index for index in range(day_index + 7, len(days_list), 7)])
            if days_list[day_index].get_weekday() == 'Sat':
                relevant_days_index_list.extend([index - 1 for index in range(day_index + 7, len(days_list), 7)])
    return [days_list[new_index] for new_index in relevant_days_index_list if
            intern in days_list[new_index].get_available_interns()]


def adapt_more_than_8(days_list, day_index, intern, relevant_days_index_list):
    if intern.get_nr_asked() == intern.get_nr_allocated():
        relevant_days_index_list.extend([index for index in range(day_index + 2, len(days_list))])
    else:
        relevant_days_index_list.extend([day_index + 2, day_index + 3])
        if days_list[day_index].get_weekday() in ['Wed', 'Thu']:
            relevant_days_index_list.extend([index for index in range(day_index + 7, len(days_list), 7)])
        elif days_list[day_index].is_weekend() and not intern.weekend_allocation_permitted():
            relevant_days_index_list.extend([index for index in range(day_index + 7, len(days_list), 7)])
            if days_list[day_index].get_weekday() == 'Fri':
                relevant_days_index_list.extend([index + 1 for index in range(day_index + 7, len(days_list), 7)])
            elif days_list[day_index].get_weekday() == 'Sat':
                relevant_days_index_list.extend([index - 1 for index in range(day_index + 7, len(days_list), 7)])
    return [days_list[new_index] for new_index in relevant_days_index_list if
            intern in days_list[new_index].get_available_interns()]


def future_days_to_adapt(days_list, day_index, intern):
    relevant_days_index_list = [day_index + 1]
    remaining_days = len(days_list) - day_index
    # if remaining_days > 8:
    #     return adapt_more_than_8(days_list, day_index, intern, relevant_days_index_list)
    # elif remaining_days > 7:
    #     return adapt_more_than_7(days_list, day_index, intern, relevant_days_index_list)
    if remaining_days > 3:
        return adapt_more_than_3(days_list, day_index, intern, relevant_days_index_list)
    elif remaining_days > 2:
        return adapt_more_than_2(days_list, day_index, intern, relevant_days_index_list)
    elif remaining_days > 1:
        return adapt_more_than_1(days_list, day_index, intern, relevant_days_index_list)
    return []


def adapt_future_days(current_day, future_days_list, intern):
    if intern.get_proficiency():
        for day in future_days_list:
            day.make_unavailable_proficient_intern(intern)
    else:
        for day in future_days_list:
            day.make_unavailable_non_proficient_intern(intern)
    current_day.record_changes(intern, future_days_list)


def undo_future_adaptations(current_day, intern):
    days_list = current_day.get_changes_to_other_dates()[intern]
    if intern.get_proficiency():
        for day in days_list:
            day.make_available_proficient_intern(intern)
    else:
        for day in days_list:
            day.make_available_non_proficient_intern(intern)
    current_day.remove_changes(intern)






###################################     Scheduling - Recursive functions   ###################################
def schedule(list_of_days, day_index, proficient_intern_index, non_proficient_intern_index, solutions):
    if len(solutions) == 1:
        return

    if day_index == len(list_of_days):
        solutions.append(create_df_sched(list_of_days))
        return

    if list_of_days[day_index].get_nr_required_interns() == 0:
        schedule(list_of_days, day_index + 1, 0, 0, solutions)

    else:
        if list_of_days[day_index].get_nr_required_proficient_interns() > 0:
            schedule_proficient(list_of_days, day_index, proficient_intern_index, non_proficient_intern_index, solutions)

        elif list_of_days[day_index].get_nr_required_non_proficient_interns() > 0:
            schedule_non_proficient(list_of_days, day_index, proficient_intern_index, non_proficient_intern_index, solutions)

        else:
            if list_of_days[day_index].get_nr_available_proficient_interns() - proficient_intern_index > 0:
                schedule_proficient(list_of_days, day_index, proficient_intern_index, non_proficient_intern_index,
                                    solutions)
            if list_of_days[day_index].get_nr_available_non_proficient_interns() - non_proficient_intern_index > 0:
                schedule_non_proficient(list_of_days, day_index, proficient_intern_index, non_proficient_intern_index,
                                    solutions)
    return


def schedule_proficient(list_of_days, day_index, proficient_intern_index, non_proficient_intern_index, solutions):
    current_day = list_of_days[day_index]
    intern = current_day.get_available_proficient_interns()[proficient_intern_index]
    future_potential_days = [list_of_days[index] for index in range(day_index, len(list_of_days)) if
                             intern in list_of_days[index].get_available_proficient_interns()]
    affected_days = future_days_to_adapt(list_of_days, day_index, intern)
    # if legal_to_adapt_future_days(affected_days, intern) and weekends_allocation_legal(intern, [current_day] + affected_days):
    if legal_to_adapt_future_days(future_potential_days, affected_days, intern):
        allocate_proficient_intern(current_day, intern)
        adapt_future_days(current_day, affected_days, intern)
        schedule(list_of_days, day_index, proficient_intern_index + 1, non_proficient_intern_index, solutions)
        undo_future_adaptations(current_day, intern)
        remove_allocation(intern, current_day)
    if more_than_enough_proficient_interns(current_day, proficient_intern_index, non_proficient_intern_index) and not \
            last_intern_in_group(proficient_intern_index, current_day.get_nr_available_proficient_interns()):
        schedule_proficient(list_of_days, day_index, proficient_intern_index + 1, non_proficient_intern_index, solutions)
    return


def schedule_non_proficient(list_of_days, day_index, proficient_intern_index, non_proficient_intern_index, solutions):
    current_day = list_of_days[day_index]
    intern = current_day.get_available_non_proficient_interns()[non_proficient_intern_index]
    future_potential_days = [list_of_days[index] for index in range(day_index, len(list_of_days)) if
                             intern in list_of_days[index].get_available_non_proficient_interns()]
    affected_days = future_days_to_adapt(list_of_days, day_index, intern)
    # if legal_to_adapt_future_days(affected_days, intern) and weekends_allocation_legal(intern, [current_day] + affected_days):
    if legal_to_adapt_future_days(future_potential_days, affected_days, intern):
        allocate_non_proficient_intern(current_day, intern)
        adapt_future_days(current_day, affected_days, intern)
        schedule(list_of_days, day_index, proficient_intern_index, non_proficient_intern_index + 1, solutions)
        undo_future_adaptations(current_day, intern)
        remove_allocation(intern, current_day)
    if more_than_enough_non_proficient_interns(current_day, proficient_intern_index, non_proficient_intern_index) and \
            not last_intern_in_group(non_proficient_intern_index, current_day.get_nr_available_non_proficient_interns()):
        schedule_non_proficient(list_of_days, day_index, proficient_intern_index, non_proficient_intern_index + 1, solutions)
    return


###################################     Export    ###################################
def create_df_sched(list_of_days):
    dates = [date.get_day() for date in list_of_days]
    positions = [(i + 1) for i in range(list_of_days[0].get_nr_allocated_interns())]
    return pd.DataFrame([[intern.get_name() for intern in day.get_allocated_interns()] for day in list_of_days], index=dates,
                        columns=positions)


###################################     Main    ###################################
df_cal = pd.read_csv("dates.csv")
df_req = pd.read_csv("requests.csv")

list_of_days = [Dates(row['Day'], row['Month'], row['Year'], row['Weekday'],
                      row['Type'], NR_INTERNS_PER_DAY, NR_PROFICIENT_PER_DAY[0], NR_PROFICIENT_PER_DAY[1])
                for index, row in df_cal.iterrows()]
list_of_interns = [Interns(row['name'], row['proficiency'], row['amount'], pos_dates(row[3:], list_of_days),
                           req_dates(row[3:], list_of_days), mand_dates(row[3:], list_of_days), NR_OF_WEEKEND_DAYS)
                   for index, row in df_req.iterrows()]

allocate_mandatory(list_of_interns)

create_intern_list_for_each_day(list_of_interns)
sol = []


root_sched = Tk()
root_sched.title('Schedule')
column_labels = ['Day', 'intern_01', 'intern_02', 'intern_03', 'intern_04', 'intern_05']
for i in range(len(column_labels)):
    column_label = Label(root_sched, text = column_labels[i]).grid(row = 1, column = i)
for i in range(len(list_of_days)):
    row_label = Label(root_sched, text = list_of_days[i].get_day()).grid(row = i + 2, column = 0)
    for j in range(len(list_of_days[i].get_allocated_interns())):
        name = Label(root_sched, text = list_of_days[i].get_allocated_interns()[j].get_name()).grid(row = i + 2, column = j + 1)
    # available_interns = list_of_days[i].get_available_interns()
    # available_interns_str = available_interns[0].get_name()
    # if len(available_interns) > 1:
    #     for k in range(1, len(available_interns)):
    #         available_interns_str += ', '
    #         available_interns_str += available_interns[k].get_name()
    # available_interns = Label(root_sched, text = available_interns_str).grid(row = i + 1, column = 6)

my_button = Button(root_sched, text='Allocate', command = allocate_proficient_intern).grid(row=0)


root_sched.mainloop()
schedule(list_of_days, 0, 0, 0, sol)



# print(len(sol))
# print(sol[0])