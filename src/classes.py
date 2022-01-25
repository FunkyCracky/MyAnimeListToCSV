from abc import ABC, abstractmethod
import requests

class Data(ABC):
    
    def request(self, username):
        return requests.get("https://api.jikan.moe/v4/users/{}/{}".format(username, self.keys["API"]), timeout = 6)

    def write_to_csv(self, csv_writer, content, key):
        csv_writer.writerow(self.header)
        for entry in json.loads(content)[self.keys["content"]]:
            csv_writer.writerow(self.get_element(entry))

    def get_header(self):
        return self.header 

    def get_genres(self, entry):
        genres = ""
        for genre in entry["genres"]:
            genres += genre["name"] + ", "
        return genres[:-2]

class AnimeData(Data):
    def __init__(self) -> None:
        self.status = {1: "Watching", 2: "Completed", 3: "On Hold", 4: "Dropped", 6: "PTW"}
        self.header = ["Title", "Status", "Score", "Eps. watched", "Start date", "End date", "Season", "Year", "Genres"]
        self.keys = {"content": "anime", "API": "animelist"}

    def get_element(self, entry):
        return [entry["title"],
                self.status[entry["watching_status"]],
                entry["score"] if entry["score"] != 0 else "",
                entry["watched_episodes"],
                entry["watch_start_date"][:10] if entry["watch_start_date"] != None else "", 
                entry["watch_end_date"][:10] if entry["watch_end_date"] != None else "",
                "{} {}".format(entry["season_name"], entry["season_year"]) if entry["season_year"] != None else "",
                entry["season_year"] if entry["season_year"] != None else "",
                self.get_genres(entry)]

class MangaData(Data):
    def __init__(self) -> None:
        self.status = {1: "Reading", 2: "Completed", 3: "On Hold", 4: "Dropped", 6: "PTR"}
        self.header = ["Title", "Status", "Score", "Chaps. read", "Vols. read", "Start date", "End date", "Type", "Genres"]
        self.keys = {"content": "manga", "API": "mangalist"}

    def get_element(self, entry):
        return [entry["title"],
                self.status[entry["reading_status"]],
                entry["score"] if entry["score"] != 0 else "",
                entry["read_chapters"],
                entry["read_volumes"],
                entry["start_date"][:10] if entry["start_date"] != None else "", 
                entry["end_date"][:10] if entry["end_date"] != None else "",
                entry["type"],
                self.get_genres(entry)]