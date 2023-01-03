import csv


def txt_read(path):
    with open(path, "r") as data:
        return data.read().replace("\n", "; ")


def txt_write(data, path):
    with open(path, "w") as file:
        file.write(data)


def csv_read(path):
    list = []
    with open(path, 'r') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            list.append(row[2])  # change the row depend on CSV
    list.pop(0)
    return "; ".join(list)


def main():
    # email_list = txt_read("data.txt")
    email_list = csv_read("data.csv")
    txt_write(email_list, "updated_data.txt")


main()
