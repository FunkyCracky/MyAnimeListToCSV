from abc import ABC, abstractmethod
import requests

class Data(ABC):
    
    def request(self, username, list_type):
        return requests.get("https://api.jikan.moe/v4/users/{}/{}".format(username, list_type), timeout = 6)

    def set_table(self, content, key):
        self.table = json.loads(content)[key]

    def get_header(self):
        return self.header

    def get_size(self):
        return len(self.table)   

    def get_genres(self, i):
        genres = ""
        for genre in self.table[i]["genres"]:
            genres += genre["name"] + ", "
        return genres[:-2]

class AnimeData(Data):
    def __init__(self) -> None:
        self.status = {1: "Watching", 2: "Completed", 3: "On Hold", 4: "Dropped", 6: "PTW"}
        self.header = ["Title", "Status", "Score", "Eps. watched", "Start date", "End date", "Season", "Year", "Genres"]

    def request(self, username):
        return super().request(username, "animelist")

    def set_table(self, content):
        set_table(self, content, "anime")

    def get_element(self, i):
        entry = self.table[i]
        return [entry["title"],
                self.status[entry["watching_status"]],
                entry["score"] if entry["score"] != 0 else "",
                entry["watched_episodes"],
                entry["watch_start_date"][:10] if entry["watch_start_date"] != None else "", 
                entry["watch_end_date"][:10] if entry["watch_end_date"] != None else "",
                str(entry["season_name"]) + " " + str(entry["season_year"]) if entry["season_year"] != None else "",
                entry["season_year"] if entry["season_year"] != None else "",
                self.get_genres(i)]

class MangaData(Data):
    def __init__(self) -> None:
        self.status = {1: "Reading", 2: "Completed", 3: "On Hold", 4: "Dropped", 6: "PTR"}
        self.header = ["Title", "Status", "Score", "Chaps. read", "Vols. read", "Start date", "End date", "Type", "Genres"]

    def request(self, username):
        return super().request(username, "mangalist")

    def set_table(self, content):
        set_table(self, content, "manga")

    def get_element(self, i):
        entry = self.table[i]
        return [entry["title"],
                self.status[entry["reading_status"]],
                entry["score"] if entry["score"] != 0 else "",
                entry["read_chapters"],
                entry["read_volumes"],
                entry["start_date"][:10] if entry["start_date"] != None else "", 
                entry["end_date"][:10] if entry["end_date"] != None else "",
                entry["type"],
                self.get_genres(entry)]