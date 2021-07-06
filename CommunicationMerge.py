import csv
import ast
import os

text_dict = {}
sorted_text_dict = {}

# Reading CSV file
with open("text-translation/translation_file_changed.csv") as csv_reading_file:
    csv_reader = csv.reader(csv_reading_file, delimiter=',')
    last_row = None
    counter = 0
    for row in csv_reader:
        # print(row[1])
        # if not row[0] == last_row:
        text_dict[row[0]] = row[1]
        last_row = row[0]
        counter += 1
    # print(text_dict)

dict_values = text_dict.values()
timestamp_values = []
for i in dict_values:
    value_list = ast.literal_eval(i)
    timestamp_values.append(value_list[0][0])
sorted_timestamp_values = sorted(timestamp_values)

text_folder_name = "merged-text"
if not os.path.isdir(text_folder_name):
    os.mkdir(text_folder_name)
if not os.path.isfile("merged-text/merged-text-file.csv"):
    open("merged-text/merged-text-file.csv", "x")
text_file = open("merged-text/merged-text-file.csv", 'a', newline='')
csv_writer = csv.writer(text_file)

finished_keys = []
for j in sorted_timestamp_values:
    for k in text_dict.keys():
        # print(ast.literal_eval(text_dict[k])[0][0])
        if ast.literal_eval(text_dict[k])[0][0] == j and k not in finished_keys:
            csv_writer.writerow([k, ast.literal_eval(text_dict[k])[1]])
            finished_keys.append(k)

print("Done")
# with open("merged-text/merged-text-file.csv") as csv_merged:
#     csv_merged_reader = csv.reader(csv_merged, delimiter=',')
#     line_counter = 0
#     for row in csv_merged_reader:
#         print("ROW ZERO", row[0], "ROW ONE:", row[1])
