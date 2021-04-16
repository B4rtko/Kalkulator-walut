import requests, os
from bs4 import BeautifulSoup
import pandas as pd


class ExchangeData:
    """
    Class used for downloading currency rates from nbp website and calculate exchanges
    """
    def __init__(self):
        self.df = self.data()

    def data(self):
        """
        Main function to maintain data downloading process. If it's possible to connect to NBP website it runs functions
        which download and convert data into DataFrame and then save it to csv file; If it's impossible to connect,
        function reads data from file kursy.csv if such file exists. Otherwise df is marked as None
        :return: DataFrame
        """
        try:  # if online
            self.online = True
            nbp_url = "https://www.nbp.pl/home.aspx?f=/kursy/kursya.html"
            df = self.data_frame(self.data_get(nbp_url))
            df = self.comma_to_dot_dataframe(df)
            self.data_save(df)
            df = df.sort_index()
        except requests.exceptions.ConnectionError:  # if offline
            try:
                self.online = False
                df = pd.read_csv("kursy.csv", index_col=0)
                with open("tytuł.txt", "r") as file:
                    self.name = file.readline()
                df = df.sort_index()
            except FileNotFoundError:
                df = None
        return df

    def data_get(self, url):
        """
        function responsible for downloading and managing data from given website (converting to html and separating needed data)
        :param url: str
        :return: list of data from website
        """
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        rates = [soup.center.find("p")]
        rates.extend(soup.center.find_all("tr"))
        return rates

    def data_frame(self, rates):
        """
        function separates all <td> tags which contains needed data and then creates DataFrame with them
        :param rates: list of data
        :return: DataFrame
        """
        title = rates[0].string
        with open("tytuł.txt", "w") as file:
            file.write(title)

        currency_name = ['złoty']
        currency_code_amount = ['1 PLN']
        currency_code = ['PLN']
        currency_rate = ['1']
        for level in rates[2:-1]:
            info = level.find_all("td")
            currency_name.append(self.get_first_word(info[0].string))
            currency_code_amount.append(info[1].string)
            currency_code.append(self.amount_get(info[1].string, rest=True))
            currency_rate.append(info[2].string)

        data = {'Nazwa waluty': currency_name, 'Kurs średni': currency_rate, 'Symbol i wartość': currency_code_amount}
        df = pd.DataFrame(data, index=currency_code)
        self.name = title
        return df

    def data_save(self, df):
        """
        simple function to save DataFrame as csv file
        """
        df.to_csv(os.path.join(os.getcwd(), "kursy.csv"))
        return None

    def exchange(self, from_currency, to_currency, amount):
        """
        function responsible for calculating amount after exchange between currencies; it behaves properly against rates
        not calculated 1:1 with PLN (such us JPY)
        :param from_currency: uppercase string of currency code
        :param to_currency: uppercase string of currency code
        :param amount: not negative number
        :return: calculated result
        """
        from_rate = float(self.df.loc[from_currency, 'Kurs średni'])/self.amount_get(self.df.loc[from_currency, 'Symbol i wartość'])
        to_rate = float(self.df.loc[to_currency, 'Kurs średni'])/self.amount_get(self.df.loc[to_currency, 'Symbol i wartość'])
        result = amount*from_rate/to_rate
        return result

    def amount_get(self, string, amount=True, rest=False):
        """
        function separates number or string (changing any of the 'amount' or 'rest' parameters results string) from currency
        code
        :param string: currency code
        :param amount: bool
        :param rest: bool
        :return: separated part of string
        """
        num_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        if amount and not rest:
            num_index = [i for i in range(len(string)) if string[i] in num_list]
            num = [string[i] for i in num_index]
            map(lambda x: str(x), num)
            num = "".join(num)
            return float(num)
        else:
            rest_index = [i for i in range(len(string)) if string[i] not in num_list]
            rest_string = "".join([string[i] for i in rest_index])
            return rest_string[1:]  # bo pierwszy znak to spacja

    def comma_to_dot_dataframe(self, df):
        """
        changes comma into dot (due to data at NBP website uses comma)
        :return: string
        """
        df['Kurs średni'] = df['Kurs średni'].map(lambda rate: float(rate.replace(",", ".")))
        return df

    def get_first_word(self, string):
        """
        function for separating first word from currency name (more words may cause problems at displaying)
        :param string: currency name
        :return: str
        """
        result = ""
        for i in string:
            if i == " ":
                break
            else:
                result += i
        return result
