import copy
import statistics
from statistics import median
import matplotlib.pyplot as plt

freq_num_mapping = {
    '': None,
    'Always (90% of working time)': 8,
    'Always  (90% of working time)': 8,
    'Multiple times per day': 7,
    'Once per day': 6,
    'Multiple times per week, but less than once per day': 5,
    'Once per week': 4,
    'Multiple times per month, but less than once per week': 3,
    'Monthly': 2,
    'Less than monthly but it occurs the case that we do': 1,
    'Never': 0,
}


def groupByRange(ranges, items):
    result = []
    for _range in ranges:
        result.append([])
    for item in items:
        for index, _range in enumerate(ranges):
            if item in range(*_range):
                result[index].append(item)
    return result


def get_column_nonempty_values(users, column):
    result = []
    for user in users:
        value = user[column]
        if value != '':
            result.append(value)
    return result

def get_column_values(users, column):
    result = []
    for user in users:
        value = user[column]
        if value != '':
            result.append(value)
        else:
            result.append(None)
    return result



def map_freq_to_num(user_freq_vector):
    return list(map(lambda x: freq_num_mapping[x], user_freq_vector))


def get_freq_to_num_matrix(freq_matrix):
    return eliminate_unknown_from_matrix(list(map(map_freq_to_num, freq_matrix)))


def take_known_median(freq_matrix, index):
    all_users_values = []
    for freq_matrix_user in freq_matrix:
        value = freq_matrix_user[index]
        if value != None:
            all_users_values.append(value)
    return median(all_users_values)



def eliminate_unknown_from_matrix(matrix):
    respondents_matrix_copy = copy.deepcopy(matrix)
    length = len(respondents_matrix_copy[0])
    medians = []
    for i in range(length):
        medians.append(take_known_median(respondents_matrix_copy, i))
    for respondent_vector in respondents_matrix_copy:
        for i, respondent_value in enumerate(respondent_vector):
            if respondent_value == None:
                respondent_vector[i] = take_known_median(respondents_matrix_copy, i)
    return respondents_matrix_copy


def convert_string_to_int(string):
    try:
        return int(string)
    except:
        return None


def convert_string_to_float(string):
    try:
        return float(string)
    except:
        return None


def make_horizontal_bar_chart(sizes, labels, name, title):
    fig1, ax1 = plt.subplots()
    bar = ax1.barh(labels, sizes)

    for rect in bar:
        width = rect.get_width()
        ax1.text(width, rect.get_y() + rect.get_height()/2.0, '%d' % int(width), ha='left', va='center')
    plt.barh(labels, sizes)
    plt.title(title)
    fig1.savefig(name + '.png', bbox_inches='tight')


def get_basic_statistics(data):
    print('mean - ', statistics.mean(list(data)))
    print('median - ', statistics.median(list(data)))
    print('stdev - ', statistics.stdev(list(data)))


def create_pie_chart(sizes, labels, name, title, figsize=(6.4,4.8),  legend=False,):
    plt.tight_layout()
    fig1, ax1 = plt.subplots(figsize=figsize)
    if legend:
        patches, text, percent = ax1.pie(sizes, autopct='%1.1f%%',
                                         shadow=True, startangle=90)
        # sort_legend = True
        # if sort_legend:
        #     patches, labels, dummy = zip(*sorted(zip(patches, labels, [sizes]),
        #                                          key=lambda x: x[2],
        #                                          reverse=True))

        ax1.legend(patches, labels, loc='center left', bbox_to_anchor=(-0.1, 1.),
                   fontsize=8)
    else:
        patches, text, percent = ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
                                         shadow=True, startangle=90)

    ax1.axis('equal')
    plt.title(title)
    plt.savefig(name + '.png', bbox_inches='tight')


def create_bar_chart(sizes, labels, name, title, xticks=None):
    plt.tight_layout()
    fig, ax = plt.subplots()
    # for i, v in enumerate(sizes):
    #     ax.text(i - 0.1, v + 0.25, str(round(v, 3)), color='blue', fontweight='bold')
    bar = ax.bar(labels, sizes)

    for rect in bar:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2.0, height, '%d' % int(height), ha='center', va='bottom')
    plt.title(title)
    if xticks:
        ax.set_xticks(xticks)
    fig.savefig(name + '.png', bbox_inches='tight')

def get_sizes_within_ranges(ranges, data):
    grouped_by_ranges = groupByRange(ranges, data)
    result = []
    for group in grouped_by_ranges:
        result.append(len(group))
    return result


def count_by_values(data):
    values = []
    sizes = []
    for dataPiece in data:
        if (dataPiece not in values):
            values.append(dataPiece)
            sizes.append(data.count(dataPiece))
    return [values, sizes]

def inverse_freq_values(matrix):
    max_freq_value = 8
    matrix_copy = copy.deepcopy(matrix)
    for respondent_vector in matrix_copy:
        for index, respondent_value in enumerate(respondent_vector):
            respondent_vector[index] = max_freq_value - respondent_value
    return matrix_copy


def get_percents_within_ranges(ranges, data):
    grouped_by_ranges = groupByRange(ranges, data)
    result = []
    for group in grouped_by_ranges:
        result.append(len(group) / len(data) * 100)
    return result