import sys
import pandas as pd
from datetime import datetime, timedelta


class CitesteCSV:
    def __init__(self, file_path):
        self.file_path = file_path
        self.dataframe = None

    def citeste_csv(self):
        try:
            self.dataframe = pd.read_csv(self.file_path)
            self.dataframe = self.dataframe.dropna()
        except Exception as e:
            print(f"Error reading CSV file: {e}")
        return self.dataframe


class CurrencyConverter:
    def __init__(self, dataframe, val_eur_to_ron, val_gbp_to_ron):
        self.dataframe = dataframe
        self.val_eur_to_ron = val_eur_to_ron
        self.val_gbp_to_ron = val_gbp_to_ron

    def convert_to_ron(self):
        def converteste_in_ron(linie_df):
            try:
                if linie_df['Fare Currency'] == 'EUR':
                    return float(linie_df['Fare Amount']) * self.val_eur_to_ron
                elif linie_df['Fare Currency'] == 'GBP':
                    return float(linie_df['Fare Amount']) * self.val_gbp_to_ron
                else:
                    return float(linie_df['Fare Amount'])
            except ValueError:
                print(f"Valoarea {linie_df['Fare Amount']} nu este un numar. Va fi inlocuit cu 0!")
                return 0

        self.dataframe['Fare Amount RON'] = self.dataframe.apply(converteste_in_ron, axis=1)
        return self.dataframe

class Statistica:
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def afiseaza_coloane(self):
        print(self.dataframe.columns)

    def total_bani_cheltuiti(self):
        total_cheltuit = self.dataframe['Fare Amount RON'].sum()
        print(f'Total bani cheltuiti: {total_cheltuit:.2f} Ron')

    def total_curse(self):
        tip_curse = list(set(self.dataframe['Trip or Order Status']))
        statusuri_curse = list(self.dataframe['Trip or Order Status'])
        total_curse = len(statusuri_curse)
        print(f'Total curse: {total_curse}')

        for tip_cursa in tip_curse:
            total_tip_curse = statusuri_curse.count(tip_cursa)
            print(f'Curse {tip_cursa}: {total_tip_curse}')

    def total_curse_pe_an(self):
        """
        data, ora este sub forma: 2024-05-30 14:38:07 +0000 UTC
        :return:
        extragem doar anii din string
        """
        # extrag data/ora de incheiere a fiecarei curse 'COMPLETED'
        status_curse = list(self.dataframe['Trip or Order Status'])
        date_curse_terminate = list(self.dataframe['Dropoff Time'])

        ani_curse = []
        for i in range(len(status_curse)):
            if status_curse[i] == 'COMPLETED':
                ani_curse.append(date_curse_terminate[i].split('-')[0])
        ani_unici = list(set(ani_curse))

        for an in ani_unici:
            print(f'In anul {an} au fost efectuate {ani_curse.count(an)} curse complete')

    def total_curse_pe_oras(self):
        """
        Afiseaza in terminal cate curse complete au fost efectuate in fiecare oras
        """
        status_curse = list(self.dataframe['Trip or Order Status'])
        orase = list(self.dataframe['City'])

        orase_curse_complete = []
        for i in range(len(status_curse)):
            if status_curse[i] == 'COMPLETED':
                orase_curse_complete.append(orase[i])

        orase_unice = list(set(orase_curse_complete))

        for oras in orase_unice:
            print(f'In {oras} au fost efectuate {orase_curse_complete.count(oras)} curse')

    def total_curse_pe_luna(self):
        """
        Afiseaza in terminal cate curse complete au fost efectuate in fiecare luna din fiecare oras
        """
        status_curse = list(self.dataframe['Trip or Order Status'])
        date_curse_terminate = list(self.dataframe['Dropoff Time'])

        date_an_luna = []
        # adaugam anii, lunile in o lista de tupluri similar cu [('2022', '08'), ('2023', '01'), ('2022', '06')]
        # la o lista de tupluri putem aplica set ca sa obtinem valori unice
        for i in range(len(status_curse)):
            if status_curse[i] == 'COMPLETED':
                date_an_luna.append(tuple(date_curse_terminate[i].split('-')[:2]))

        date_an_luna_unice = list(set(date_an_luna))
        #sortam lista de tupluri in functie de an si luna
        date_an_luna_unice.sort(key=lambda x: (x[0], x[1]))
        for an_luna in date_an_luna_unice:
            print(f'In anul {an_luna[0]} luna {an_luna[1]} au fost efectuate {date_an_luna.count(an_luna)} curse.')

    def distanta_totala(self):
        """Se va afisa in terminal distanta totala parcursa in km"""

        mile_to_km = 1.609344
        distante = list(self.dataframe['Distance (miles)'])
        statusuri_curse = list(self.dataframe['Trip or Order Status'])

        distante_mile_curse_complete = []

        for i in range(len(statusuri_curse)):
            if statusuri_curse[i] == 'COMPLETED':
                distante_mile_curse_complete.append(float(distante[i]))

        distanta_totala_km = sum(distante_mile_curse_complete) * mile_to_km
        #print(len(distante), len(statusuri_curse),len(distante_mile_curse_complete))
        print(f'Distanta totala parcursa este de {distanta_totala_km:.2f} km.')

    def total_curse_per_produs(self):
        """Va afisa in terminal numarul de curse parcurse cu fiecare tip de serviciu uber"""
        tip_uber = list(self.dataframe['Product Type'])
        statusuri_curse = list(self.dataframe['Trip or Order Status'])

        curse_complete_tip_uber = []

        for i in range(len(statusuri_curse)):
            if statusuri_curse[i] == 'COMPLETED':
                curse_complete_tip_uber.append(tip_uber[i])

        for tip_uber in (list(set(curse_complete_tip_uber))):
            print(f'Au fost efectuate {curse_complete_tip_uber.count(tip_uber)} cu {tip_uber}.')

    def transforma_in_datetime(self, data_str):
        # stergem '+0000 UTC' si pastram formatul '2024-05-30 14:38:07'
        data_str = data_str.split(' +')[0]
        return datetime.strptime(data_str, '%Y-%m-%d %H:%M:%S')

    def calculeaza_timp_total(self):
        timp_total = timedelta()
        lst_timpi_trafic = []

        lst_begin_time = list(self.dataframe['Begin Trip Time'])
        lst_dropoff_time = list(self.dataframe['Dropoff Time'])

        statusuri_curse = list(self.dataframe['Trip or Order Status'])

        for i in range(len(statusuri_curse)):
            if statusuri_curse[i] == 'COMPLETED':
                begin_time = self.transforma_in_datetime(lst_begin_time[i])
                dropoff_time = self.transforma_in_datetime(lst_dropoff_time[i])
                trip_duration = dropoff_time - begin_time
                lst_timpi_trafic.append(str(trip_duration))
                timp_total += trip_duration
        return timp_total, lst_timpi_trafic

    def perioada_totala_curse(self):
        timp_total = self.calculeaza_timp_total()[0]
        total_secunde = timp_total.total_seconds()

        zile = timp_total.days
        ore, remainder = divmod(total_secunde, 3600)
        minute, seconds = divmod(remainder, 60)

        print(f'Timpul total petrecut in trafic cu Uber este {zile}zile, {ore}ore, {minute}minute, {seconds}secunde')

    def convert_to_timedelta(self, duration_str):
        hours, minutes, seconds = map(int, duration_str.split(':'))
        return timedelta(hours=hours, minutes=minutes, seconds=seconds)

    def timpi_curse(self):
        """Va afisa in terminal cea mai scurta cursa in minute"""

        durata_deplasari = self.calculeaza_timp_total()[1]
        durata_timp = [self.convert_to_timedelta(d) for d in durata_deplasari]
        return durata_timp

    def format_timedelta(self, td):
        total_seconds = int(td.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        min_from_hours = hours * 60
        minutes = minutes + min_from_hours
        return minutes, seconds

    def cea_mai_scurta_cursa(self):
        # print(min(self.timpi_curse()))
        print(f'Cea mai scurta cursa a durat {self.format_timedelta(min(self.timpi_curse()))[0]} minute si {self.format_timedelta(min(self.timpi_curse()))[1]} secunde')


    def cea_mai_lunga_cursa(self):
        # print(max(self.timpi_curse()))
        print(f'Cea mai scurta cursa a durat {self.format_timedelta(max(self.timpi_curse()))[0]} minute si {self.format_timedelta(max(self.timpi_curse()))[1]} secunde')


if __name__ =='__main__':
    if len(sys.argv) != 2:
        sys.exit("Trebuie sa specifici un argument")

    file_path = sys.argv[1]
    csv_citit = CitesteCSV(file_path)
    df_csv = csv_citit.citeste_csv()

    if df_csv is not None:
        transformare_ron = CurrencyConverter(dataframe=df_csv, val_eur_to_ron=4.9763, val_gbp_to_ron=5.85)
        df_csv_ron = transformare_ron.convert_to_ron()

        statistici = Statistica(df_csv_ron)
        statistici.total_bani_cheltuiti()
        statistici.total_curse()
        statistici.total_curse_pe_an()
        statistici.total_curse_pe_oras()
        statistici.total_curse_pe_luna()
        statistici.distanta_totala()
        statistici.total_curse_per_produs()
        statistici.calculeaza_timp_total()
        statistici.perioada_totala_curse()
        statistici.cea_mai_scurta_cursa()
        statistici.cea_mai_lunga_cursa()
