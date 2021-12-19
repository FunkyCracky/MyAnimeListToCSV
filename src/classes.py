from abc import ABC, abstractmethod

class Data(ABC):
    def get_header(self):
        return self.header

    def get_size(self):
        return len(self.table)   

    def get_genres(self, i):
        genres = ""
        for genre in self.table[i]["genres"]:
            genres += genre["name"] + ", "
        return genres[:-2]

    def set_table(self, table):
        self.table = table

class AnimeData(Data):
    def __init__(self) -> None:
        self.status = {1: "Watching", 2: "Completed", 3: "On Hold", 4: "Dropped", 6: "PTW"}
        self.header = ["Title", "Status", "Score", "Eps. watched", "Start date", "End date", "Season", "Year", "Genres"]

    def get_element(self, i):
        return[self.table[i]["title"],
               self.status[self.table[i]["watching_status"]],
               self.table[i]["score"] if self.table[i]["score"] != 0 else "",
               self.table[i]["watched_episodes"],
               self.table[i]["watch_start_date"][:10] if self.table[i]["watch_start_date"] != None else "", 
               self.table[i]["watch_end_date"][:10] if self.table[i]["watch_end_date"] != None else "",
               str(self.table[i]["season_name"]) + " " + str(self.table[i]["season_year"]) if self.table[i]["season_year"] != None else "",
               self.table[i]["season_year"] if self.table[i]["season_year"] != None else "",
               self.get_genres(i)]

class MangaData(Data):
    def __init__(self) -> None:
        self.status = {1: "Reading", 2: "Completed", 3: "On Hold", 4: "Dropped", 6: "PTR"}
        self.header = ["Title", "Status", "Score", "Chaps. read", "Vols. read", "Start date", "End date", "Type", "Genres"]

    def get_element(self, i):
        return[self.table[i]["title"],
               self.status[self.table[i]["reading_status"]],
               self.table[i]["score"] if self.table[i]["score"] != 0 else "",
               self.table[i]["read_chapters"],
               self.table[i]["read_volumes"],
               self.table[i]["start_date"][:10] if self.table[i]["start_date"] != None else "", 
               self.table[i]["end_date"][:10] if self.table[i]["end_date"] != None else "",
               self.table[i]["type"],
               self.get_genres(self.table[i])]