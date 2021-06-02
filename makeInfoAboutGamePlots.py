import csv
from functools import reduce

import matplotlib.pyplot as plt
import statistics

from constants.methodologiesShortNames import methodologies_short_names
from constants.problemsShortNames import problems_short_names
from utils import get_column_nonempty_values, count_by_values, create_pie_chart, make_horizontal_bar_chart, \
    convert_string_to_float, create_bar_chart, get_basic_statistics, get_column_values


def make_info_about_game_plots():
    # INFO ABOUT GAME
    # role
    respondents = []
    filename = "results.csv"
    with open(filename, 'r') as data:
        for line in csv.DictReader(data):
            respondents.append(line)

    role_q = 'What was/were your position/positions?'
    roles = get_column_nonempty_values(respondents, role_q)
    new_roles = []
    for role in roles:
        for new_role in role.split(','):
            new_roles.append(new_role)
    [labels, sizes] = count_by_values(new_roles)
    zipped = list(zip(labels, sizes))
    zipped.sort(key=lambda x: x[1])
    sorted_labels = list(map(lambda x: x[0], zipped))
    sorted_sizes = list(map(lambda x: x[1], zipped))
    make_horizontal_bar_chart(sorted_sizes, sorted_labels, 'infoAboutGame/roles', role_q + ' (number of people)')

    # team size
    team_size_q = ' What was the team size (approximately)?'
    team_size = get_column_nonempty_values(respondents, team_size_q)
    [labels, sizes] = count_by_values(
        sorted(list(filter(lambda x: x != None, map(convert_string_to_float, team_size)))))
    create_bar_chart(sizes, labels, 'infoAboutGame/team_size',
                     team_size_q, labels)

    # target platform
    target_platform_q = 'What was the target platform?'
    target_platforms = get_column_nonempty_values(respondents, target_platform_q)
    results = []
    for target_platform in target_platforms:
        for target_platform_split in target_platform.split('/'):
            results.append(target_platform_split)

    [labels, sizes] = (count_by_values(results))
    create_pie_chart(sizes, labels, 'infoAboutGame/target_platform', target_platform_q)


    # hours per week
    hours_per_week_q = 'How many hours did you usually spend on game development in a week?'
    hours_per_week = list(map(convert_string_to_float, get_column_nonempty_values(respondents, hours_per_week_q)))
    print('hours_per_week -------')
    get_basic_statistics(hours_per_week)

    # weeks
    weeks_q = 'For how many weeks have you been developing the game?'
    weeks = list(map(convert_string_to_float, get_column_nonempty_values(respondents, weeks_q)))
    print('weeks --------')
    get_basic_statistics(weeks)

    # hours spent per game
    hours_per_week_q = 'How many hours did you usually spend on game development in a week?'
    hours_per_week = list(map(convert_string_to_float, get_column_values(respondents, hours_per_week_q)))
    weeks_q = 'For how many weeks have you been developing the game?'
    weeks = list(map(convert_string_to_float, get_column_values(respondents, weeks_q)))
    time_overall = []
    for data in zip(hours_per_week, weeks):
        if data[0] is not None and data[1] is not None:
            time_overall.append(data[0] * data[1])
    print('overall hours ------')
    get_basic_statistics(time_overall)

    # rating of used methodologies

    columns = list(respondents[0].keys())
    first_methodologies_index = columns.index(
        '1) We used the 𝗽𝗿𝗼𝗱𝘂𝗰𝘁 𝗯𝗮𝗰𝗸𝗹𝗼𝗴 (a prioritized features list, containing short descriptions of all functionality we wanted)')
    last_methodologies_index = columns.index('16) We used 𝗰𝗼𝗱𝗶𝗻𝗴 𝘀𝘁𝗮𝗻𝗱𝗮𝗿𝗱𝘀.')

    labels = methodologies_short_names

    # Remove headers
    methodologies_questions = columns[first_methodologies_index: last_methodologies_index + 1]
    data = {}
    for [index, methodologies_question] in enumerate(methodologies_questions):
        data[labels[index]] = get_column_nonempty_values(respondents, methodologies_question)



    usage = {}
    for methodology_q in data:
        counter = 0
        for answer in data[methodology_q]:
            if not 'Never' in answer:
                counter = counter + 1

        usage[methodology_q] = round((counter/24) *100)

    labels = sorted(usage,  key=usage.get)
    sizes = list(map(lambda x: usage[x], labels))
    make_horizontal_bar_chart(sizes, labels, 'infoAboutGame/methodologies_rating', 'Methodologies rating (percent)')

    # distribution for each methodolofy

    for data_label in data:
        [labels, sizes] = (count_by_values(data[data_label]))
        create_pie_chart(sizes, labels, 'infoAboutGame/methodologies/'+data_label, data_label)


    first_problems_index = columns.index(
        '1.  We realized that our project was 𝘂𝗻𝗿𝗲𝗮𝗹𝗶𝘀𝘁𝗶𝗰 𝗼𝗿 𝗲𝘅𝘁𝗿𝗲𝗺𝗲𝗹𝘆 𝗮𝗺𝗯𝗶𝘁𝗶𝗼𝘂𝘀 in scope.')
    last_problems_index = columns.index(
        '15.  Our 𝗳𝗶𝗻𝗮𝗹 𝗯𝘂𝗱𝗴𝗲𝘁 𝘄𝗮𝘀 𝗰𝗼𝗻𝘀𝗶𝗱𝗲𝗿𝗮𝗯𝗹𝘆 𝗺𝗼𝗿𝗲 than the original one.')
    # rating of problems met

    labels = problems_short_names


    # Remove headers
    problems_questions = columns[first_problems_index : last_problems_index+ 1]
    data = {}
    for [index, problems_questions] in enumerate(problems_questions):
        data[labels[index]] = get_column_nonempty_values(respondents, problems_questions)


    usage = {}
    for problem_q in data:
        counter = 0
        for answer in data[problem_q]:

            if not 'Never' in answer:
                counter = counter + 1

        usage[problem_q] = round((counter/24) *100)

    labels = sorted(usage,  key=usage.get)
    sizes = list(map(lambda x: usage[x], labels))
    make_horizontal_bar_chart(sizes, labels, 'infoAboutGame/problems_rating', 'Problems rating (percent)')

    # distribution for each methodolofy

    for data_label in data:
        [labels, sizes] = (count_by_values(data[data_label]))
        create_pie_chart(sizes, labels, 'infoAboutGame/problems/'+data_label, data_label)


    # distribution for each stage

    first_stage_index = 33
    last_stage_index = 38
    stages = ['Initiation', 'Team building', 'Pre-production', 'Production', 'Testing', 'Release']
    print(columns[38])
    for i in range (first_stage_index, last_stage_index + 1):
        results = []
        column_values = get_column_nonempty_values(respondents, columns[i])
        for column_value in column_values:
            for split_value in column_value.split(', '):
                results.append(split_value)
        [labels, sizes] = count_by_values(results)
        sorted_zip = sorted(zip(labels, sizes), key=lambda x: x[1])
        labels = list(map(lambda x: x[0], sorted_zip))
        sizes = list(map(lambda x: round(x[1]/len(respondents) * 100), sorted_zip))
        make_horizontal_bar_chart(sizes, labels, 'infoAboutGame/stages/'+stages[i-first_stage_index], stages[i-first_stage_index] + ' (%)')
        print([labels, sizes])

    stages_order__index = 39
    column_values = get_column_nonempty_values(respondents, columns[stages_order__index])
    [labels, sizes] = count_by_values(column_values)
    sorted_zip = sorted(zip(labels, sizes), key=lambda x: x[1])
    labels = list(map(lambda x: x[0], sorted_zip))
    sizes = list(map(lambda x: round(x[1]), sorted_zip))
    make_horizontal_bar_chart(sizes, labels, 'infoAboutGame/stages/order',
                              'Order of stages distribution' + ' (%)')
