import numpy as np
import sklearn.metrics
import csv
import seaborn as sns
import matplotlib.pyplot as plt
from constants.methodologiesShortNames import methodologies_short_names
from constants.problemsShortNames import problems_short_names
from utils import convert_string_to_int, eliminate_unknown_from_matrix, get_column_values, get_freq_to_num_matrix, \
    inverse_freq_values

def make_matrix_plot():
    filename = "results.csv"
    users = []
    with open(filename, 'r') as data:
        for line in csv.DictReader(data):
            users.append(line)

    satisfaction = eliminate_unknown_from_matrix([list(map(convert_string_to_int, get_column_values(users,
                                        'Are you in general satisfied with the final resulting game??')))])[0]
    users = []
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            users.append(row)

    columns = users[0]
    first_methodologies_index = columns.index(
        '1) We used the 𝗽𝗿𝗼𝗱𝘂𝗰𝘁 𝗯𝗮𝗰𝗸𝗹𝗼𝗴 (a prioritized features list, containing short descriptions of all functionality we wanted)')
    last_methodologies_index = columns.index('16) We used 𝗰𝗼𝗱𝗶𝗻𝗴 𝘀𝘁𝗮𝗻𝗱𝗮𝗿𝗱𝘀.')

    first_problems_index = columns.index(
        '1.  We realized that our project was 𝘂𝗻𝗿𝗲𝗮𝗹𝗶𝘀𝘁𝗶𝗰 𝗼𝗿 𝗲𝘅𝘁𝗿𝗲𝗺𝗲𝗹𝘆 𝗮𝗺𝗯𝗶𝘁𝗶𝗼𝘂𝘀 in scope.')
    last_problems_index = columns.index(
        '15.  Our 𝗳𝗶𝗻𝗮𝗹 𝗯𝘂𝗱𝗴𝗲𝘁 𝘄𝗮𝘀 𝗰𝗼𝗻𝘀𝗶𝗱𝗲𝗿𝗮𝗯𝗹𝘆 𝗺𝗼𝗿𝗲 than the original one.')
    users = users[1:]


    methodologies_matrix_words = list(map(lambda user: user[first_methodologies_index: last_methodologies_index + 1], users))
    problems_matrix_words = list(map(lambda user: user[first_problems_index: last_problems_index + 1], users))
    methodologies_matrix_num  = (get_freq_to_num_matrix(methodologies_matrix_words))
    problems_matrix_num = get_freq_to_num_matrix(problems_matrix_words)

    #add satisfaction to the problems matrix
    for respondent_problems_vector, respondent_satisfation in zip(problems_matrix_num, satisfaction):
        respondent_problems_vector.append(respondent_satisfation)

    similarity = np.array(sklearn.metrics.pairwise.cosine_similarity(np.array(methodologies_matrix_num).T, np.array(problems_matrix_num).T))

    for i in range(similarity.shape[0]):
        similarity[i] -= similarity[i].mean()
    similarity *= -1

    sns.set()
    fig, ax = plt.subplots()

    y_axis_labels = methodologies_short_names

    x_axis_labels = problems_short_names
    sns.heatmap(
        similarity,
        center=0,
        cmap=sns.diverging_palette(20, 220, n=200),
        square=True,
        ax=ax,
        xticklabels=x_axis_labels,
        yticklabels=y_axis_labels
    )
    plt.title("Similarity matrix")
    fig.savefig('background/similarity_matrix' + '.png', bbox_inches='tight')