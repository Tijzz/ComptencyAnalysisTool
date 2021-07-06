import os
import csv

bales_categories = ["Shows solidarity", "Shows tension release", "Agrees", "Gives suggestion", "Gives opinion", "Gives orientation", "Asks for orientation", "Asks for opinion", "Asks for suggestion", "Disagrees", "Shows tension", "Shows antagonism"]
players = ["Player 1", "Player 2", "Player 3", "Player 4", "Player 5"]


def format_bales_graph(results):
    text_folder_name = "dash-data"
    file_path = text_folder_name + "/bales-graph-data.csv"
    if not os.path.isdir(text_folder_name):
        os.mkdir(text_folder_name)
    if os.path.isfile(file_path):
        os.remove(file_path)
    if not os.path.isfile(file_path):
        open(file_path, "x")
    text_file = open(file_path, 'a', newline='')

    csv_writer = csv.writer(text_file)
    csv_writer.writerow(["Player", "Category", "Amount"])

    total_said = [0, 0, 0, 0, 0]
    player_counter = 0
    for i in results:
        total_categories_counter = 0
        for j in results.get(i):
            if total_categories_counter == 13:
                total_said[player_counter] = j
            total_categories_counter += 1
        player_counter += 1

    player_counter_2 = 0
    for i in results:
        category_counter = 0
        for j in results.get(i):
            if category_counter < 12:
                amount = j/total_said[player_counter_2]*100
                csv_writer.writerow([players[player_counter_2], bales_categories[category_counter], amount])
                category_counter += 1
            else:
                break
        player_counter_2 += 1
    return file_path


def format_pie_chart(results):
    text_folder_name = "dash-data"
    file_path = text_folder_name + "/pie-chart-data.csv"
    if not os.path.isdir(text_folder_name):
        os.mkdir(text_folder_name)
    if os.path.isfile(file_path):
        os.remove(file_path)
    if not os.path.isfile(file_path):
        open(file_path, "x")
    text_file = open(file_path, 'a', newline='')

    csv_writer = csv.writer(text_file)
    csv_writer.writerow(["Player", "Words", "Sentences", "Positive", "Negative"])

    player_counter = 0
    for i in results:
        csv_writer.writerow([players[player_counter], results.get(i)[12], results.get(i)[13], results.get(i)[14], results.get(i)[15]])
        player_counter += 1
    return file_path


def format_bar_chart(results):
    text_folder_name = "dash-data"
    file_path = text_folder_name + "/bar-chart-data.csv"
    if not os.path.isdir(text_folder_name):
        os.mkdir(text_folder_name)
    if os.path.isfile(file_path):
        os.remove(file_path)
    if not os.path.isfile(file_path):
        open(file_path, "x")
    text_file = open(file_path, 'a', newline='')

    csv_writer = csv.writer(text_file)
    csv_writer.writerow(["Player", "Polarity", "Amount"])

    player_counter = 0
    for i in results:
        category_counter = 0
        for j in results.get(i):
            if category_counter == 14:
                csv_writer.writerow([players[player_counter], "Positive", j])
            elif category_counter == 15:
                csv_writer.writerow([players[player_counter], "Negative", j])
            elif category_counter > 15:
                break
            category_counter += 1
        player_counter += 1
    return file_path


def format_leader_chart(results):
    text_folder_name = "dash-data"
    file_path = text_folder_name + "/leader-chart-data.csv"
    if not os.path.isdir(text_folder_name):
        os.mkdir(text_folder_name)
    if os.path.isfile(file_path):
        os.remove(file_path)
    if not os.path.isfile(file_path):
        open(file_path, "x")
    text_file = open(file_path, 'a', newline='')

    csv_writer = csv.writer(text_file)
    csv_writer.writerow(["Category", "Amount (%)"])

    player_total_score = [0, 0, 0, 0, 0]
    total_sentence_score = 0
    total_pos_score = 0
    total_neg_score = 0

    player_counter = 0
    for i in results:
        category_counter = 0
        for j in results.get(i):
            if category_counter == 13:
                player_total_score[player_counter] += j
                total_sentence_score += j
            elif category_counter == 14:
                player_total_score[player_counter] += j
                total_pos_score += j
            elif category_counter == 15:
                player_total_score[player_counter] += j
                total_neg_score += j
            elif category_counter > 15:
                break
            category_counter += 1
        player_counter += 1

    leader_score = max(player_total_score)
    player_counter_next = 0
    leader = 0

    for i in results:
        if player_total_score[player_counter_next] == leader_score:
            leader = player_counter_next + 1
            category_counter_next = 0
            for j in results.get(i):
                if category_counter_next == 13:
                    csv_writer.writerow(["Sentences", j/total_sentence_score*100])
                elif category_counter_next == 14:
                    csv_writer.writerow(["Positive", j/total_pos_score*100])
                elif category_counter_next == 15:
                    csv_writer.writerow(["Negative", j/total_neg_score*100])
                elif category_counter_next > 15:
                    break
                category_counter_next += 1
        player_counter_next += 1
    return file_path, leader


def format_leadership_type_chart(results):
    pass
