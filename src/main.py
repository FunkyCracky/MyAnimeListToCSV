from time import sleep
from classes import AnimeData, MangaData
import requests, csv, json, os

def write_to_csv(data, csv_writer):
    csv_writer.writerow(data.get_header())
    for i in range(data.get_size()):
        csv_writer.writerow(data.get_element(i))

def fetch_and_write_data(out, data, csv_writer, page, username, c, m_type):
    r = requests.get("https://api.jikan.moe/v3/user/{}/{}?page={}".format(username, m_type, page), timeout=6)
    if r.status_code != 200:
        print("Something went wrong. Code: " + str(r.status_code))
        out.close()
        return main()
    table = json.loads(r.content)["anime" if c == "A" else "manga"]
    data.set_table(table)
    write_to_csv(data, csv_writer)

def get_type():
    c = str(input("Anime (A) or manga (M)? ")).upper()
    info = {"A": ("animelist", AnimeData()), "M": ("mangalist", MangaData())}
    if c in ("A", "M"):
        return c, info[c]
    else:
        print("The input is incorrect. Try again!")
        return get_type()

def main():
    username = str(input("MyAnimeList username: "))
    c, (m_type, data) = get_type()
    page = 1
    out_name = str(input("File output name: "))
    out_path = os.path.join(os.path.dirname( __file__ ), "..", out_name)
    out = open(out_path + ".csv", "w", newline = "")
    csv_writer = csv.writer(out, delimiter =";")
    while True:
        try:
            fetch_and_write_data(out, data, csv_writer, page, username, c, m_type)
            if data.get_size() < 300:
                break
            page += 1
        except requests.exceptions.Timeout:
            for i in range(4, 1, -1):
                print("The API didn't respond. Trying again in " + str(i) + " seconds...", end = "\r")
                sleep(1)
            print("The API didn't respond. Trying again in 1 second...", end = "\r")
            sleep(1)
            print("\nLet's try again!")
    print("Done! Go to the main folder and check the file " + out_name + ".csv!")
    out.close()

if __name__ == "__main__":
    main()