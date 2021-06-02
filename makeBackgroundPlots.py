import copy
import csv

from utils import eliminate_unknown_from_matrix, convert_string_to_int, get_column_values, get_column_nonempty_values, \
    get_sizes_within_ranges, count_by_values, create_pie_chart, create_bar_chart, convert_string_to_float


def make_background_plots():
    filename = "results.csv"
    users = []
    with open(filename, 'r') as data:
        for line in csv.DictReader(data):
            users.append(line)

    # get satisfaction
    satisfaction = eliminate_unknown_from_matrix([list(map(convert_string_to_int, get_column_values(users, 'Are you in general satisfied with the final resulting game??')))])[0]


    # ages
    age_ranges = [(0, 20), (20, 30), (30, 40), (40, 50), (50, 60), (60, 100)]
    age_ranges_labels = ['<20', '20-29', '30-39', '40-49', '50-59', '>=60']
    ages = list(map(convert_string_to_int, get_column_nonempty_values(users, 'What is your age?')))
    create_bar_chart(get_sizes_within_ranges(age_ranges, ages), age_ranges_labels, 'background/ages', 'What is your age?' )

    # nationality

    nationalities = get_column_nonempty_values(users, 'What is your nationality?')
    [labels, sizes] = (count_by_values(nationalities))
    create_pie_chart(sizes, labels, 'background/nationalities', 'What is your nationality?' )

    # gender
    genders = get_column_nonempty_values(users, 'What is your gender?')
    [labels, sizes] = (count_by_values(genders))
    create_pie_chart(sizes, labels, 'background/genders', 'What is your gender?')

    # education
    educations = get_column_nonempty_values(users, 'What is your education?')
    [labels, sizes] = (count_by_values(educations))
    create_pie_chart(sizes, labels, 'background/educations', 'What is your education?')

    # companies
    companies_sizes = get_column_nonempty_values(users,
                                                 'What is the approximate size of your company (if no company, skip)?')
    create_pie_chart([len(companies_sizes), len(users) - len(companies_sizes)], ['has company', 'has no company'],
                     'background/companies', "Companies' affiliation chart" )
    [labels, sizes] = count_by_values(companies_sizes)
    create_pie_chart(sizes, labels, 'background/companies_sizes', 'What is the approximate size of your company?')

    #num of games made

    num_of_games_made = get_column_nonempty_values(users,
                                                 'How many games you worked on were released?')

    [labels, sizes] = count_by_values(sorted(list(filter(lambda x: x != None, map(convert_string_to_float, num_of_games_made)))))
    new_sizes = copy.deepcopy(sizes)
    new_labels = copy.deepcopy(labels)
    create_bar_chart(new_sizes, new_labels, 'background/num_of_games_made', 'How many games you worked on were released?')

    # experience in game development
    experience = get_column_nonempty_values(users, 'For how long have/had you been working on the game development?')
    [labels, sizes] = count_by_values(sorted(list(filter(lambda x: x != None, map(convert_string_to_float, experience)))))
    create_bar_chart(sizes, labels, 'background/experience', 'For how long have/had you been working on the game development?', labels)
