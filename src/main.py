from time import sleep
from classes import AnimeData, MangaData
from requests.exceptions import Timeout
import csv, json, os

def fetch_and_write_data(data, csv_writer, username, m_type) -> bool:
    for i in range(3):
        try:
            r = data.request(username)
            if r.status_code == 200:
                data.write_to_csv(csv_writer, r.content)
                return True
            print("The API returned an error (Attempt #{}). Code: {}".format(i+1, r.status_code))
        except Timeout:
            print("The API didn't respond (Attempt #{}).".format(i+1))
        if i < 2:
            print("Trying again...")
            sleep(1)
    print("We couldn't fetch the data from the API after 3 tries. Please try again later!")
    return False  

def get_type():
    c = str(input("Anime (A) or manga (M)? ")).upper()
    info = {"A": ("animelist", AnimeData()), "M": ("mangalist", MangaData())}
    if c in ("A", "M"):
        return info[c]
    else:
        print("The input is incorrect. Try again!")
        return get_type()

def main() -> None:
    username = str(input("MyAnimeList username: "))
    (m_type, data) = get_type()
    out_name = str(input("File output name: "))
    out_path = os.path.join(os.path.dirname( __file__ ), "..", out_name)
    out_file = open(out_path + ".csv", "w", newline = "")
    csv_writer = csv.writer(out_file, delimiter =";")
    if fetch_and_write_data(data, csv_writer, username, m_type):
        print("Done! Go to the main folder and check the file " + out_name + ".csv!")
    out_file.close()

if __name__ == "__main__":
    main()