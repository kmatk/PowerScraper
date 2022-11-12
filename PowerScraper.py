import pandas as pd
from bs4 import BeautifulSoup


def get_power(source):
    with open(source, 'r', errors='ignore') as file:
        page = BeautifulSoup(file, 'html.parser')
        results = page.find_all("div", class_="power-distribution-data")
        power, amt = [], []
        total_power = 0

        for element in results:
            power.append(element.get('data-power'))
            amt.append(element.get('data-count'))

        for i, _ in enumerate(power):
            total_power += (int(power[i]) * 5) * int(amt[i])

        return total_power


def get_t4_kills(source):
    with open(source, 'r', errors='ignore') as file:
        page = BeautifulSoup(file, 'html.parser')
        results = page.find_all("div", class_="t4kills-distribution-data")
        kills, amt = [], []
        t4_kills = 0

        for element in results:
            kills.append(element.get('data-kills'))
            amt.append(element.get('data-count'))

        for i, _ in enumerate(kills):
            t4_kills += ((int(kills[i]) * 2) + 2) * int(amt[i])

        return t4_kills


def get_t5_kills(source):
    with open(source, 'r', errors='ignore') as file:
        page = BeautifulSoup(file, 'html.parser')
        results = page.find_all("div", class_="t5kills-distribution-data")
        kills, amt = [], []
        t5_kills = 0

        for element in results:
            kills.append(element.get('data-kills'))
            amt.append(element.get('data-count'))

        for i, _ in enumerate(kills):
            t5_kills += ((int(kills[i]) * 2) + 2) * int(amt[i])

        return t5_kills


def get_deaths(source):
    with open(source, 'r', errors='ignore') as file:
        page = BeautifulSoup(file, 'html.parser')
        results = page.find_all("div", class_="death-distribution-data")
        deaths, amt = [], []
        total_deaths = 0

        for element in results:
            deaths.append(element.get('data-power'))
            amt.append(element.get('data-count'))

        for i, _ in enumerate(deaths):
            total_deaths += (int(deaths[i]) + 1) * int(amt[i])

        return total_deaths


def get_kd_data(kd_num):
    source = "source/kd" + str(kd_num) + ".html"
    t4_kills, t5_kills = get_t4_kills(source), get_t5_kills(source)
    total_kp = ((t4_kills * 10) + (t5_kills * 20)) / 1000
    return [get_power(source)/1000, total_kp, t4_kills, t5_kills, get_deaths(source)]


def main():
    csv = "kvk_data.csv"
    kd_list = [1195, 1394, 1584, 2051, 2429, 1515, 2257, 2400, 2363, 2431, 2536]  # KD 2525 not on RokBoard
    kd_data = {"POWER(B)": [], "KILL POINTS(B)": [], "T4 KILLS(M)": [], "T5 KILLS(M)": [], "DEATHS(M)": []}
    data = []

    for kd in kd_list:
        data.append(get_kd_data(kd))

    for i in data:
        kd_data["POWER(B)"].append(i[0])
        kd_data["KILL POINTS(B)"].append(i[1])
        kd_data["T4 KILLS(M)"].append(i[2])
        kd_data["T5 KILLS(M)"].append(i[3])
        kd_data["DEATHS(M)"].append(i[4])

    table = pd.DataFrame(data=kd_data, index=kd_list)
    table.to_csv(csv, sep="|")
    print("Successfully parsed data")
    print(table)


# Prevent program from being run if imported
if __name__ == '__main__':
    main()
