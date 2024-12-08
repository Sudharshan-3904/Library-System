#TODO - Add delete book records button only for admins
#TODO - Add a way to resiter new user


import customtkinter as ctk
from CTkTable import *
from CTkMessagebox import *
import library
from threading import Thread
import pandas as pd
import numpy as np

class Interface:
    def __init__(self) -> None:
        self.__LOGGED_IN = False
        self.__selected_mode = "System"
        self.__selected_theme = "dark-blue"
        self.__api_obj = library.API()
        
        self.__root = ctk.CTk()
        self.__root.title("Library Management System")
        self.__root._set_appearance_mode(self.__selected_mode)
        ctk.set_default_color_theme(self.__selected_theme)

        self.__book_title_str_var = ctk.StringVar(value="")
        self.__book_author_str_var = ctk.StringVar(value="")
        self.__book_publisher_str_var = ctk.StringVar(value="")
        self.__book_isbn_str_var = ctk.StringVar(value="")
        self.__book_status_str_var = ctk.StringVar(value="Reading List")
        self.__book_criteria_str_var = ctk.StringVar(value="Title")
        self.__book_target_str_var = ctk.StringVar(value="")
        self.__add_user_un_str_var = ctk.StringVar(value="")
        self.__add_user_pw_str_var = ctk.StringVar(value="")
        self.__user_auth_str_var = ctk.StringVar(value="Librarian")

        self.__username_entry_str_var = ctk.StringVar(value="")
        self.__password_entry_str_var = ctk.StringVar(value="")

        self.__search_key_entry_str_var = ctk.StringVar(value="ISBN")
        self.__search_value_entry_str_var = ctk.StringVar(value="")

        self.__current_user_auth_level = None

    # TODO - remove authorized after development
    def startApp(self,authorized=1, auth_level = "Admin"):
        if authorized==1:
            self.__LOGGED_IN = True
            self.__current_user_auth_level = auth_level
            self.updateSection("Home")
            self.create_main_layout()
            self.__root.mainloop()
        else:
            self.__LOGGED_IN = False
            self.updateSection("Login")
            self.__root.mainloop()
    
    def stopApp(self):
        if self.showConfirm("Would you like to close the program ?"):
            self.__LOGGED_IN = False
            self.__root.destroy()
        else:
            return
    
    def create_main_layout(self):
        self.__title_label.grid(row=0, column=0, rowspan=1, columnspan=16, padx=5, pady=5)
        self.__navbar_frame.grid(row=1, column=0, rowspan=32, columnspan=2, padx=5, pady=5)
        self.__section_parent_frame.grid(row=1, column=2, rowspan=32, columnspan=2, padx=5, pady=5)

    def showConfirm(self, message=""):
        msg = CTkMessagebox(title="Exit?", message=message, icon="question", option_1="Cancel", option_2="No", option_3="Yes")
        response = msg.get()
    
        if response=="Yes":
            return True
        else:
            return False
    
    def showInfo(self, message=""):
        CTkMessagebox(title="Info", message=message)

    def check_credentials(self):
        self.__current_user_auth_level = self.__api_obj.validate_credentials(ip_un=self.__username_entry_str_var.get(), ip_pwd=self.__password_entry_str_var.get())
        if (self.__current_user_auth_level is not None):
            if (self.__current_user_auth_level) != "":
                self.__LOGGED_IN = True
                self.__login_frame.destroy()
                self.updateSection("Home")
                self.create_main_layout()
                self.__root.update()
            else:
                self.__login_info_label.configure(text="Incorrect Username or Password! Try Again.")
                self.__LOGGED_IN = False
        else:
            self.__api_obj.update_log("Non-Existing Credentials entered.")
            self.__login_info_label.configure(text="Credentials Do Not Exists. PLease Contact Admin.")
            self.__LOGGED_IN = False
    
    def clear_login_fields(self) -> None:
        self.__username_entry_str_var.set("")
        self.__password_entry_str_var.set("")
    
    def update_book_list(self) -> None:
        add_list = []
        add_list.append(self.__book_title_str_var.get())
        add_list.append(self.__book_author_str_var.get())
        add_list.append(self.__book_publisher_str_var.get())
        add_list.append(self.__book_isbn_str_var.get())
        add_list.append(self.__book_status_str_var.get())
        self.__api_obj.write_books_data(add_list)
    
    def clear_book_data(self) -> None:
        self.__book_title_str_var.set("")
        self.__book_author_str_var.set("")
        self.__book_publisher_str_var.set("")
        self.__book_isbn_str_var.set("")
        self.__book_status_str_var.set("Reading List")
        self.__book_target_str_var.set("")

    def edit_book_data(self):
        add_list = []
        add_list.append(self.__book_title_str_var.get())
        add_list.append(self.__book_author_str_var.get())
        add_list.append(self.__book_publisher_str_var.get())
        add_list.append(self.__book_isbn_str_var.get())
        add_list.append(self.__book_status_str_var.get())
        self.__api_obj.update_book_data(add_list[0], add_list)
    
    def add_new_user(self):
        self.__api_obj.add_new_credentials(self.__add_user_un_str_var.get(), self.__add_user_pw_str_var.get(), self.__user_auth_str_var.get())
    
    def get_isbn_data(self) -> None:
        book_isbn_data = self.__api_obj.get_data_from_isbn(self.__book_isbn_str_var.get())
        self.__book_title_str_var.set(book_isbn_data["Title"])
        self.__book_author_str_var.set(book_isbn_data["Authors"])
        self.__book_publisher_str_var.set(book_isbn_data["Publisher"])
        self.__section_parent_frame.update()

    def search_book_data(self) -> list:
        ipKey = self.__search_key_entry_str_var.get()
        ipVal = self.__search_value_entry_str_var.get()

        if ipKey == "ISBN":
            ipVal = int(ipVal)
        
        searchResultDict = self.__api_obj.search_books_data(key=ipKey, value=ipVal)
        if searchResultDict['found']:
            for _ in range(len(self.__results_display_table.get()) - 1):
                self.__results_display_table.delete_row(_+1)
            for dataRow in searchResultDict['data']:
                self.__results_display_table.add_row(dataRow)
            self.__results_display_table.grid(row=3, column=0, columnspan=10, rowspan=(len(searchResultDict["data"]) + 1))
        else:
            self.__search_result_label = ctk.CTkLabel(master=self.__section_parent_frame, text="No Record(s) Found")
            self.__search_result_label.grid(row=3, column=0, columnspan=10, rowspan=1)
    
    def updateSection(self, section=""):
        def clearFrame(input_frame=self.__root):
            for widget in input_frame.winfo_children():
                widget.destroy()

        match section:
            case "Login":
                if self.__LOGGED_IN:
                    self.updateSection("Home")
                clearFrame()
                self.__login_frame = ctk.CTkFrame(master=self.__root)
                
                self.__login_info_label = ctk.CTkLabel(master=self.__login_frame, text="Enter Username and Password")
                self.__login_info_label.grid(row=0, column=0, rowspan=1, columnspan=5, padx=5, pady=2)
                
                self.__login_username_label = ctk.CTkLabel(master=self.__login_frame, text="Username")
                self.__login_username_label.grid(row=1, column=0, rowspan=1, columnspan=2, padx=5, pady=2)                
                self.__login_entry_username = ctk.CTkEntry(master=self.__login_frame, textvariable=self.__username_entry_str_var, placeholder_text="Username", placeholder_text_color="white")
                self.__login_entry_username.grid(row=1, column=2, rowspan=1, columnspan=3, padx=5, pady=2)
                
                self.__login_password_label = ctk.CTkLabel(master=self.__login_frame, text="Password")
                self.__login_password_label.grid(row=2, column=0, rowspan=1, columnspan=2, padx=5, pady=2)                
                self.__login_entry_password = ctk.CTkEntry(master=self.__login_frame, textvariable=self.__password_entry_str_var, placeholder_text="Password", placeholder_text_color="white")
                self.__login_entry_password.grid(row=2, column=2, rowspan=1, columnspan=3, padx=5, pady=2)
                
                self.__login_button_submit = ctk.CTkButton(master=self.__login_frame, text="Login", command=self.check_credentials)
                self.__login_button_submit.grid(row=3, column=0, rowspan=1, columnspan=2, padx=5, pady=2)                
                self.__login_button_clear = ctk.CTkButton(master=self.__login_frame, text="Clear", command=self.clear_login_fields)
                self.__login_button_clear.grid(row=3, column=2, rowspan=1, columnspan=2, padx=5, pady=2)
                
                self.__login_frame.pack()
                self.__root.update()

            case "Home":
                if not self.__LOGGED_IN:
                    self.updateSection("Login")
                clearFrame()
                self.__title_label = ctk.CTkLabel(master=self.__root, text="Library Management System")
                self.__navbar_frame = ctk.CTkFrame(master=self.__root)
                self.__section_parent_frame = ctk.CTkFrame(master=self.__root)
                self.create_main_layout()

                # Navbar Items
                self.__home_page_nav_option = ctk.CTkButton(master=self.__navbar_frame, text="Home", command=lambda: self.updateSection("Home"))
                self.__home_page_nav_option.grid(row=0, column=0, rowspan=1, columnspan=2, padx=5, pady=2)
                self.__search_book_nav_option = ctk.CTkButton(master=self.__navbar_frame, text="Search", command=lambda: self.updateSection("Search"))
                self.__search_book_nav_option.grid(row=1, column=0, rowspan=1, columnspan=2, padx=5, pady=2)
                self.__add_book_nav_option = ctk.CTkButton(master=self.__navbar_frame, text="Add Book", command=lambda: self.updateSection("Add New"))
                self.__add_book_nav_option.grid(row=2, column=0, rowspan=1, columnspan=2, padx=5, pady=2)
                self.__edit_book_nav_option = ctk.CTkButton(master=self.__navbar_frame, text="Edit Data", command=lambda: self.updateSection("Edit Record"))
                self.__edit_book_nav_option.grid(row=3, column=0, rowspan=1, columnspan=2, padx=5, pady=2)

                if self.__current_user_auth_level == "Admin":
                    self.__add_user_option = ctk.CTkButton(master=self.__navbar_frame, text="Add User", command=lambda: self.updateSection("Add User"))
                    self.__add_user_option.grid(row=4, column=0, rowspan=1, columnspan=2, padx=5, pady=2)

                self.__quit_nav_option = ctk.CTkButton(master=self.__navbar_frame, text="Quit", command=self.stopApp)
                self.__quit_nav_option.grid(row=5, column=0, rowspan=1, columnspan=2, padx=5, pady=2)
                
                # Book List
                self.__books_display_table = CTkTable(master=self.__section_parent_frame, values=self.__api_obj.read_books_data())
                # for data in self.__api_obj.read_books_data():
                #     "print(data)"
                #     self.__books_display_table.add_row(data)
                self.__books_display_table.pack()

            case "Add New":
                if not self.__LOGGED_IN:
                    self.updateSection("Login")
                clearFrame(self.__section_parent_frame)
                
                self.__add_new_title_label = ctk.CTkLabel(master=self.__section_parent_frame, text="Add a new Book to Library")
                self.__add_new_title_label.grid(row=0, column=0, rowspan=1, columnspan=10, padx=5, pady=2)

                self.__add_new_book_isbn_label = ctk.CTkLabel(master=self.__section_parent_frame, text="Book ISBN")
                self.__add_new_book_isbn_label.grid(row=1, column=0, rowspan=1, columnspan=2, padx=5, pady=2)
                self.__add_new_book_isbn_entry = ctk.CTkEntry(master=self.__section_parent_frame, textvariable=self.__book_isbn_str_var)
                self.__add_new_book_isbn_entry.grid(row=1, column=2, rowspan=1, columnspan=6, padx=5, pady=2)
                self.__get_isbn_data_btn = ctk.CTkButton(master=self.__section_parent_frame, text="Get Info", command=self.get_isbn_data)
                self.__get_isbn_data_btn.grid(row=2, column=2, rowspan=1, columnspan=4, padx=5, pady=2)

                self.__add_new_book_title_label = ctk.CTkLabel(master=self.__section_parent_frame, text="Book Title")
                self.__add_new_book_title_label.grid(row=3, column=0, rowspan=1, columnspan=2, padx=5, pady=2)
                self.__add_new_book_title_entry = ctk.CTkEntry(master=self.__section_parent_frame, textvariable=self.__book_title_str_var)
                self.__add_new_book_title_entry.grid(row=3, column=2, rowspan=1, columnspan=6, padx=5, pady=2)

                self.__add_new_book_author_label = ctk.CTkLabel(master=self.__section_parent_frame, text="Book Author")
                self.__add_new_book_author_label.grid(row=4, column=0, rowspan=1, columnspan=2, padx=5, pady=2)
                self.__add_new_book_author_entry = ctk.CTkEntry(master=self.__section_parent_frame, textvariable=self.__book_author_str_var)
                self.__add_new_book_author_entry.grid(row=4, column=2, rowspan=1, columnspan=6, padx=5, pady=2)

                self.__add_new_book_publisher_label = ctk.CTkLabel(master=self.__section_parent_frame, text="Book Publisher")
                self.__add_new_book_publisher_label.grid(row=5, column=0, rowspan=1, columnspan=2, padx=5, pady=2)
                self.__add_new_book_publisher_entry = ctk.CTkEntry(master=self.__section_parent_frame, textvariable=self.__book_publisher_str_var)
                self.__add_new_book_publisher_entry.grid(row=5, column=2, rowspan=1, columnspan=6, padx=5, pady=2)

                self.__add_new_book_status_label = ctk.CTkLabel(master=self.__section_parent_frame, text="Book Status")
                self.__add_new_book_status_label.grid(row=6, column=0, rowspan=1, columnspan=2, padx=5, pady=2)
                self.__add_new_book_status_entry = ctk.CTkOptionMenu(master=self.__section_parent_frame, values=["Reading List", "Started", "Finished", "DNF", "Halfway"], variable=self.__book_status_str_var)
                self.__add_new_book_status_entry.grid(row=6, column=2, rowspan=1, columnspan=6, padx=5, pady=2)

                self.__add_new_submit_button = ctk.CTkButton(master=self.__section_parent_frame, text="Add", command=self.update_book_list)
                self.__add_new_submit_button.grid(row=7, column=0, rowspan=1, columnspan=4, padx=5, pady=2)
                self.__add_new_clear_data_button = ctk.CTkButton(master=self.__section_parent_frame, text="Clear", command=self.clear_book_data)
                self.__add_new_clear_data_button.grid(row=7, column=4, rowspan=1, columnspan=4, padx=5, pady=2)

            case "Edit Record":
                if not self.__LOGGED_IN:
                    self.updateSection("Login")
                clearFrame(self.__section_parent_frame)
                
                self.__edit_record_title_label = ctk.CTkLabel(master=self.__section_parent_frame, text="Search By")
                self.__edit_record_title_label.grid(row=0, column=0, rowspan=1, columnspan=2, padx=5, pady=2)
                self.__criteria_book_title_radio = ctk.CTkRadioButton(master=self.__section_parent_frame, variable=self.__book_criteria_str_var, value="Title", text="Title")
                self.__criteria_book_title_radio.grid(row=1, column=0, rowspan=1, columnspan=2, padx=5, pady=2)
                self.__criteria_book_author_radio = ctk.CTkRadioButton(master=self.__section_parent_frame, variable=self.__book_criteria_str_var, value="Author", text="Author")
                self.__criteria_book_author_radio.grid(row=1, column=2, rowspan=1, columnspan=2, padx=5, pady=2)
                self.__criteria_book_publisher_radio = ctk.CTkRadioButton(master=self.__section_parent_frame, variable=self.__book_criteria_str_var, value="Publisher", text="Publisher")
                self.__criteria_book_publisher_radio.grid(row=1, column=4, rowspan=1, columnspan=2, padx=5, pady=2)
                self.__criteria_book_isbn_radio = ctk.CTkRadioButton(master=self.__section_parent_frame, variable=self.__book_criteria_str_var, value="ISBN", text="ISBN")
                self.__criteria_book_isbn_radio.grid(row=1, column=6, rowspan=1, columnspan=2, padx=5, pady=2)
                self.__criteria_book_isbn_radio = ctk.CTkRadioButton(master=self.__section_parent_frame, variable=self.__book_criteria_str_var, value="Status", text="Status")
                self.__criteria_book_isbn_radio.grid(row=1, column=8, rowspan=1, columnspan=2, padx=5, pady=2)

                self.__edit_search_criteria_label = ctk.CTkLabel(master=self.__section_parent_frame, text=f"Old {self.__book_criteria_str_var.get()}")
                self.__edit_search_criteria_label.grid(row=2, column=0, rowspan=1, columnspan=2, padx=5, pady=2)
                self.__edit_search_target_entry = ctk.CTkEntry(master=self.__section_parent_frame, textvariable=self.__book_target_str_var)
                self.__edit_search_target_entry.grid(row=2, column=2, rowspan=1, columnspan=6, padx=5, pady=2)

                self.__edit_record_book_title_label = ctk.CTkLabel(master=self.__section_parent_frame, text="Book Title")
                self.__edit_record_book_title_label.grid(row=3, column=0, rowspan=1, columnspan=2, padx=5, pady=2)
                self.__edit_record_book_title_entry = ctk.CTkEntry(master=self.__section_parent_frame, textvariable=self.__book_title_str_var)
                self.__edit_record_book_title_entry.grid(row=3, column=2, rowspan=1, columnspan=6, padx=5, pady=2)

                self.__edit_record_book_author_label = ctk.CTkLabel(master=self.__section_parent_frame, text="Book Author")
                self.__edit_record_book_author_label.grid(row=4, column=0, rowspan=1, columnspan=2, padx=5, pady=2)
                self.__edit_record_book_author_entry = ctk.CTkEntry(master=self.__section_parent_frame, textvariable=self.__book_author_str_var)
                self.__edit_record_book_author_entry.grid(row=4, column=2, rowspan=1, columnspan=6, padx=5, pady=2)

                self.__edit_record_book_publisher_label = ctk.CTkLabel(master=self.__section_parent_frame, text="Book Publisher")
                self.__edit_record_book_publisher_label.grid(row=5, column=0, rowspan=1, columnspan=2, padx=5, pady=2)
                self.__edit_record_book_publisher_entry = ctk.CTkEntry(master=self.__section_parent_frame, textvariable=self.__book_publisher_str_var)
                self.__edit_record_book_publisher_entry.grid(row=5, column=2, rowspan=1, columnspan=6, padx=5, pady=2)

                self.__edit_record_book_isbn_label = ctk.CTkLabel(master=self.__section_parent_frame, text="Book ISBN")
                self.__edit_record_book_isbn_label.grid(row=6, column=0, rowspan=1, columnspan=2, padx=5, pady=2)
                self.__edit_record_book_isbn_entry = ctk.CTkEntry(master=self.__section_parent_frame, textvariable=self.__book_isbn_str_var)
                self.__edit_record_book_isbn_entry.grid(row=6, column=2, rowspan=1, columnspan=6, padx=5, pady=2)

                self.__add_new_book_status_label = ctk.CTkLabel(master=self.__section_parent_frame, text="Book Status")
                self.__add_new_book_status_label.grid(row=7, column=0, rowspan=1, columnspan=2, padx=5, pady=2)
                self.__add_new_book_status_entry = ctk.CTkOptionMenu(master=self.__section_parent_frame, values=["Reading List", "Started", "Finished", "DNF", "Halfway"], variable=self.__book_status_str_var)
                self.__add_new_book_status_entry.grid(row=7, column=2, rowspan=1, columnspan=6, padx=5, pady=2)

                self.__edit_record_submit_button = ctk.CTkButton(master=self.__section_parent_frame, text="Update", command=self.edit_book_data)
                self.__edit_record_submit_button.grid(row=8, column=0, rowspan=1, columnspan=4, padx=5, pady=2)
                self.__edit_record_clear_data_button = ctk.CTkButton(master=self.__section_parent_frame, text="Clear", command=self.clear_book_data)
                self.__edit_record_clear_data_button.grid(row=8, column=4, rowspan=1, columnspan=4, padx=5, pady=2)

            case "Search":
                if not self.__LOGGED_IN:
                    self.updateSection("Login")
                clearFrame(self.__section_parent_frame)
                
                self.__search_title_label = ctk.CTkLabel(master=self.__section_parent_frame, text="Search a Book in the Library")
                self.__search_title_label.grid(row=0, column=0, rowspan=1, columnspan=10, padx=5, pady=2)
                
                self.__results_display_table = CTkTable(master=self.__section_parent_frame, values=[["Title", "Author", "Publisher", "ISBN", "Status"]])
                self.__results_display_table.grid(row=3, column=0, columnspan=10, rowspan=1)

                self.__search_book_key_entry = ctk.CTkOptionMenu(master=self.__section_parent_frame, values=["Title", "ISBN", "Author", "Publisher", "Status"], variable=self.__search_key_entry_str_var)
                self.__search_book_key_entry.grid(row=1, column=0, rowspan=1, columnspan=4, padx=5, pady=2)
                self.__search_book_value_entry = ctk.CTkEntry(master=self.__section_parent_frame, textvariable=self.__search_value_entry_str_var)
                self.__search_book_value_entry.grid(row=1, column=4, rowspan=1, columnspan=6, padx=5, pady=2)
                self.__get_isbn_data_btn = ctk.CTkButton(master=self.__section_parent_frame, text="Get Info", command=lambda: self.search_book_data())
                self.__get_isbn_data_btn.grid(row=2, column=4, rowspan=1, columnspan=6, padx=5, pady=2)


            case "Add User":
                if not self.__LOGGED_IN:
                    self.updateSection("Login")

                if self.__current_user_auth_level != "Admin":
                    self.updateSection("Home")
                clearFrame(self.__section_parent_frame)

                self.__add_user_frame = ctk.CTkFrame(master=self.__section_parent_frame)
                
                self.__add_user_info_label = ctk.CTkLabel(master=self.__add_user_frame, text="Enter New Username and Password")
                self.__add_user_info_label.grid(row=0, column=0, rowspan=1, columnspan=5, padx=5, pady=2)
                
                self.__add_user_username_label = ctk.CTkLabel(master=self.__add_user_frame, text="Username")
                self.__add_user_username_label.grid(row=1, column=0, rowspan=1, columnspan=2, padx=5, pady=2)                
                self.__add_user_entry_username = ctk.CTkEntry(master=self.__add_user_frame, textvariable=self.__add_user_un_str_var, placeholder_text="Username", placeholder_text_color="white")
                self.__add_user_entry_username.grid(row=1, column=2, rowspan=1, columnspan=3, padx=5, pady=2)
                
                self.__add_user_password_label = ctk.CTkLabel(master=self.__add_user_frame, text="Password")
                self.__add_user_password_label.grid(row=2, column=0, rowspan=1, columnspan=2, padx=5, pady=2)                
                self.__add_user_entry_password = ctk.CTkEntry(master=self.__add_user_frame, textvariable=self.__add_user_pw_str_var, placeholder_text="Password", placeholder_text_color="white")
                self.__add_user_entry_password.grid(row=2, column=2, rowspan=1, columnspan=3, padx=5, pady=2)
                
                # TODO - Change the string variable
                self.__add_user_auth_level_label = ctk.CTkLabel(master=self.__add_user_frame, text="Type")
                self.__add_user_auth_level_label.grid(row=3, column=0, rowspan=1, columnspan=2, padx=5, pady=2)                
                self.__add_user_menu_auth_level = ctk.CTkOptionMenu(master=self.__add_user_frame, values=["Admin", "Librarian"], variable=self.__user_auth_str_var)
                self.__add_user_menu_auth_level.grid(row=3, column=2, rowspan=1, columnspan=3, padx=5, pady=2)

                self.__add_user_button_submit = ctk.CTkButton(master=self.__add_user_frame, text="Add User", command=self.add_new_user)
                self.__add_user_button_submit.grid(row=4, column=0, rowspan=1, columnspan=2, padx=5, pady=2)                
                self.__add_user_button_clear = ctk.CTkButton(master=self.__add_user_frame, text="Clear", command=self.clear_login_fields)
                self.__add_user_button_clear.grid(row=4, column=2, rowspan=1, columnspan=2, padx=5, pady=2)
                
                self.__add_user_frame.pack()

            case _:              # Default Case
                clearFrame()
                if self.__LOGGED_IN:
                    self.updateSection(section="Home")
                else:
                    self.updateSection(section="Login")
            
        self.__root.update()

runner_main = Thread(target=Interface().startApp(authorized=0, auth_level="Admin"), daemon=True)
runner_main.start()
runner_main.join()
