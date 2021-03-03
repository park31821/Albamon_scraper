import csv


def save_to_file(title, jobs):
    file = open(f"{title}.csv", mode="w")
    writer = csv.writer(file)
    writer.writerow(["location", "title", "time", "pay", "last registerd"])
    for job in jobs:
        writer.writerow(list(job.values()))
