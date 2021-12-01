from bs4 import BeautifulSoup
from time import sleep
import requests
import csv
import json

def write_to_csv(table, csv_writer):
    def get_genres(el):
        genres = ""
        for genre in el["genres"]:
            genres += genre["name"] + ", "
        return genres[:-2]
    new_status = {1: "Watching", 2: "Completed", 3: "On Hold", 4: "Dropped", 6: "PTW"}
    csv_writer.writerow(["Name", "Status", "Score", "Eps watched", "Start date", "Finish date", "Season", "Year", "Genres"])
    for el in table:
        csv_writer.writerow([el["title"],
                             new_status[el["watching_status"]],
                             el["score"] if el["score"] != 0 else "",
                             el["watched_episodes"],
                             el["watch_start_date"][:10] if el["watch_start_date"] != None else "", 
                             el["watch_end_date"][:10] if el["watch_end_date"] != None else "",
                             str(el["season_name"]) + " " + str(el["season_year"]) if el["season_year"] != None else "",
                             el["season_year"] if el["season_year"] != None else "",
                             get_genres(el)])

def main():
    username = str(input("MyAnimeList username: "))
    while True:
        c = str(input("Anime (A) or manga (M)? ")).upper()
        if c == "A":
            m_type = "animelist"
            break
        elif c == "M":
            print("Still working on it. Coming soon!")
            #m_type = "mangalist"
            #break
        else:
            print("The input is incorrect (must be A or M). Try again!")
    page = 1
    out = open("out.csv", "w", newline="")
    csv_writer = csv.writer(out, delimiter =";")
    while True:
        try:
            r = requests.get("https://api.jikan.moe/v3/user/{}/{}?page={}".format(username, m_type, page), timeout=6)
            if r.status_code != 200:
                print("Something went wrong. Code: " + str(r.status_code))
                break
            table = json.loads(r.content)["anime" if c == "A" else "manga"]
            print(table)
            write_to_csv(table, csv_writer)
            page += 1
            if len(table) < 300:
                break
        except requests.exceptions.Timeout:
            print("API didn't respond. Trying again in 4 seconds...")
            sleep(4)

if __name__ == "__main__":
    main()