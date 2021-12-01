from bs4 import BeautifulSoup
import requests
import csv
import json

def write_to_csv(table):
    def get_genres(el):
        genres = ""
        for genre in el["genres"]:
            genres += genre["name"] + ", "
        return genres[:-2]
    new_status = {1: "Watching", 2: "Completed", 3: "On Hold", 4: "Dropped", 6: "PTW"}
    out = open("out.csv", "w", newline="")
    csv_writer = csv.writer(out, delimiter =";")
    csv_writer.writerow(["Name", "Status", "Score", "Eps watched", "Start date", "Finish date", "Season", "Year", "Genres"])
    for el in table:
        csv_writer.writerow([el["anime_title"],
                             new_status[el["status"]],
                             el["score"] if el["score"] != 0 else "",
                             el["num_watched_episodes"],
                             el["start_date_string"] if el["start_date_string"] != None else "", 
                             el["finish_date_string"] if el["finish_date_string"] != None else "",
                             str(el["anime_season"]["season"]) + " " + str(el["anime_season"]["year"]) if el["anime_season"] != None else "",
                             str(el["anime_season"]["year"]) if el["anime_season"] != None else "",
                             get_genres(el)])

def main():
    username = str(input("MyAnimeList username: "))
    r = requests.get("https://myanimelist.net/animelist/" + username + "?status=7")
    if r.status_code == 200:
        soup = BeautifulSoup(r.content)
        table = soup.find_all(attrs={"class" : "list-table"})[0]['data-items']
        table = json.loads(table)
        write_to_csv(table)
    else:
        print("Something went wrong. Code: " + r.status_code)

if __name__ == "__main__":
    main()