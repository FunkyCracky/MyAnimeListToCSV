from abc import ABC, abstractmethod
import json, requests

class Data(ABC):
    
    def request(self, username):
        return requests.get("https://api.jikan.moe/v4/users/{}/{}".format(username, self.info["list"]), timeout = 6)

    def write_to_csv(self, csv_writer, content):
        csv_writer.writerow(self.header)
        for entry in json.loads(content)["data"]:
            csv_writer.writerow(self.get_element(entry))

    def get_header(self):
        return self.header 

    def get_genres(self, entry):
        genres = ""
        for genre in entry[self.info["type"]]["genres"]:
            genres += genre["name"] + ", "
        return genres[:-2]

class AnimeData(Data):
    def __init__(self) -> None:
        self.status = {1: "Watching", 2: "Completed", 3: "On Hold", 4: "Dropped", 6: "PTW"}
        self.header = ["Title", "Status", "Score", "Eps. watched", "Start date", "End date", "Season", "Year", "Genres"]
        self.info = {"type": "anime", "list": "animelist"}

    def get_element(self, entry):
        year = entry["anime"]["year"] if entry["anime"]["year"] != None else ""
        season = "{} {}".format(entry["anime"]["season"].capitalize(), year) if year != None else ""
        return [entry["anime"]["title"],
                self.status[entry["watching_status"]],
                entry["score"] if entry["score"] != 0 else "",
                entry["episodes_watched"],
                entry["watch_start_date"][:10] if entry["watch_start_date"] != None else "", 
                entry["watch_end_date"][:10] if entry["watch_end_date"] != None else "",
                season,
                year,
                self.get_genres(entry)]

class MangaData(Data):
    def __init__(self) -> None:
        self.status = {1: "Reading", 2: "Completed", 3: "On Hold", 4: "Dropped", 6: "PTR"}
        self.header = ["Title", "Status", "Score", "Chaps. read", "Vols. read", "Start date", "End date", "Type", "Genres"]
        self.info = {"type": "manga", "list": "mangalist"}

    def get_element(self, entry):
        return [entry["manga"]["title"],
                self.status[entry["reading_status"]],
                entry["score"] if entry["score"] != 0 else "",
                entry["chapters_read"],
                entry["volumes_read"],
                entry["read_start_date"][:10] if entry["read_start_date"] != None else "", 
                entry["read_end_date"][:10] if entry["read_end_date"] != None else "",
                entry["manga"]["type"],
                self.get_genres(entry)]