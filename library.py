from datetime import datetime
import pandas as pd
import numpy as np
import os
from isbnlib import *
import csv
from hashlib import sha256

class API:
    def __init__(self) -> None:
        self.__valid_credentials = []
        self.__credentials_filename = f"{os.path.dirname(os.path.realpath(__file__))}\\UserData.csv"
        self.__log_filename = f"{os.path.dirname(os.path.realpath(__file__))}\\logs.log"
        self.__book_datafile = f"{os.path.dirname(os.path.realpath(__file__))}\\Books.csv"
        self.__books_header = ["Title", "Author", "Publisher", "ISBN", "Status"]
        self.update_log()
        self.readCredentials()
    
    def readCredentials(self) -> bool:
        if not (os.path.isfile(self.__credentials_filename)):
            self.update_log("Credentials file does not exists.")
            return False

        with open(f"{self.__credentials_filename}", 'r') as dataFile:
            self.__valid_credentials = list(csv.reader(dataFile))
            if [] in self.__valid_credentials:
                self.__valid_credentials.remove([])
        return True

    def encrypt_item(self, input_item: any):
        return sha256(input_item.encode()).hexdigest()
    
    def update_log(self, log_msg="") -> None:
        if log_msg != "":
            with open(self.__log_filename, "a") as logFile:
                logFile.write(f"{datetime.now()} -- {str(log_msg)}\n")
                logFile.close()
        else:
            with open(self.__log_filename, "w") as logFile:
                logFile.write(f"{'-'*30}New File Created{'-'*30}\n")
                logFile.close()

    def add_new_credentials(self, username:str, password:str, auth_level: str) -> bool:
        try:
            with open(f"{self.__credentials_filename}", 'a') as dataFile:
                dataFile.write(str(username))
                dataFile.write(str(","))
                dataFile.write(str(self.encrypt_item(password)))
                dataFile.write(str(","))
                dataFile.write(str(auth_level))
                dataFile.write("\n")
            return True
        except:
            self.update_log("Could not add new credentials.")
            return False
        finally:
            self.readCredentials()
    
    def validate_credentials(self, ip_un:str, ip_pwd:str) -> str:
        if self.readCredentials():
            uns = (np.array(self.__valid_credentials).flatten().tolist())[::3]
            pws = (np.array(self.__valid_credentials).flatten().tolist())[1::3]
            als = (np.array(self.__valid_credentials).flatten().tolist())[2::3]

            if ip_un in uns:
                if self.encrypt_item(ip_pwd) == pws[uns.index(ip_un)]:
                    return str(als[uns.index(ip_un)])
                else:
                    return ""
        else:
            self.update_log("Unable to read file")
    
    def read_books_data(self) -> list:
        if os.path.isfile(self.__book_datafile):
            books_df = pd.read_csv(self.__book_datafile)
            return_list = np.array(books_df).tolist()
            return_list.insert(0, self.__books_header)
            return return_list
        else:
            return []
        
    def get_data_from_isbn(self, ip_isbn: str) -> dict:
        try:
            isbn_data = meta(ip_isbn, service='goob')
        
            if len(isbn_data) == 0 or isbn_data is None:
                self.update_log(f"No ISBN data was found for {ip_isbn}")
                return {}
            book_details = dict()
            x = ""
            if len(isbn_data['Authors']) != 0:
                for i in isbn_data['Authors']:
                    x += str(i)
                    if len(isbn_data['Authors']) > 1:
                        x += ", "
            else:
                x = ""
            
            book_details["Title"] = isbn_data['Title']
            book_details["Authors"] = x
            book_details["Publisher"] = isbn_data['Publisher']
            book_details["ISBN"] = isbn_data['ISBN-13']
            return book_details
        except ISBNLibException as error:
            self.update_log(error)
    
    def write_books_data(self, new_data:list) -> None:
        data_list = [new_data.copy()]
        if not os.path.isfile(self.__book_datafile):
            data_list.insert(0, self.__books_header)
        books_df = pd.DataFrame(data_list)
        books_df.to_csv(self.__book_datafile, header=None, mode='a', index=None)

    def search_books_data(self, key: str, value) -> dict:
        returnDict = {'found' : False, 'data': ["Title", "Author", "Publisher", "ISBN", "Status"]}
        all_books_df = pd.DataFrame(self.read_books_data()[1:], columns=self.read_books_data()[0])
        returnDict['found'] = True in np.where(all_books_df[key] == value, True, False);
        if returnDict['found']:
            returnDict['data'] = np.array(all_books_df[all_books_df[key] == value]).tolist()
        return returnDict
    
    def update_book_data(self, search_key:str, new_values: list) -> bool:
        try:
            books = np.array(self.read_books_data())
            books[np.where(books == search_key)[0][0]] = new_values
            pd.DataFrame(books).to_csv(self.__book_datafile, index=False, header=False)
        except IndexError:
            self.update_log("No Record book data matching the criteria was found")
