from tkinter import * 
from tkinter import ttk 
from tkinter import messagebox
from mysql.connector import connection
import db_connection
import re

# removing all grid elements from screen
class Remove:
     def __init__(self, master):
          super(Remove, self).__init__()
          self.master = master
          self.available_slot = 0

     def remove_all_widgets(self):
          for widgets in self.master.winfo_children():  # this is used only for grid system.
               widgets.grid_remove()
        


class MainWindow:

     def __init__(self, root):
          self.master = root
          self.font = "verdana 12 bold"
          self.color = "yellow"
          self.__username = ""
          self.__password = ""

     def loginWindow(self):
          heading = Label(self.master, text="Vehicle Parking Management System", font="verdana 22 bold", bg=self.color)
          heading.grid(row=0, column=0, padx=(300,0), pady=20)

          
          self.loginFrame = LabelFrame(self.master, text="")
          self.loginFrame.grid(row=1, column=0, padx=(300,0), pady=50)

          self.username_label = Label(self.loginFrame, text="Username", font=self.font, bg="#f2f2f2")
          self.username_label.grid(row=0, column=0, padx=30, pady=(40,20))

          self.username_entry = Entry(self.loginFrame, textvariable=self.__username, width=20, font="verdana 12")
          self.username_entry.grid(row=0, column=1, padx=(10, 30), pady=(40,20), ipady=3)

          self.password_label = Label(self.loginFrame, text="Password", font=self.font, bg="#f2f2f2")
          self.password_label.grid(row=1, column=0, padx=30, pady=20)

          self.password_entry = Entry(self.loginFrame, textvariable=self.__password, width=20, show="*", font="verdana 12")
          self.password_entry.grid(row=1, column=1, padx=(10,30), pady=20, ipady=3)

          self.login_button = Button(self.loginFrame, text="Login", width="20", font="verdana 12 bold", bg="#00a5aa", fg="#fff", cursor="hand2", command=lambda: self.authenticate())
          self.login_button.grid(row=2, column=0, columnspan=2, padx=30, pady=30)

          pass


     def authenticate(self):
          self.__username = self.username_entry.get()
          self.__password = self.password_entry.get()

          if len(self.__username) <= 0:
               messagebox.showerror("Invalid Credentials", "Please enter the username", parent=self.master)
               self.username_entry.delete(0, END)
               self.username_entry.focus()
               return
          if len(self.__password) <= 0:
               messagebox.showerror("Invalid Credentials", "Please enter the password", parent=self.master)
               self.password_entry.delete(0, END)
               self.password_entry.focus()
               return
          
          connection = db_connection.connect()

          cursor = connection.cursor()
          try:
               cursor.execute("SELECT * from users where username='{}'".format(self.__username))
               data = cursor.fetchone()
               print(data)
               if data == None or data[2] != self.__password:
                    messagebox.showerror("Invalid Credentials", "Your credentials are invalid. Please try again.")
                    self.username_entry.delete(0, END)
                    self.password_entry.delete(0, END)
                    self.username_entry.focus()
                    return
               connection.close()

          except Exception as e:
               connection.rollback()
               messagebox.showerror("Error", e, parent=self.master)
               print(e)
               return
          
          print("Username", self.__username, "is logged in into the system..")
          Remove.remove_all_widgets(self.loginFrame)
          self.homePortal()


     def homePortal(self):
          heading = Label(self.master, text="Vehicle Parking Management System", font="verdana 22 bold", bg=self.color)
          heading.grid(row=0, column=0, padx=(250,0), pady=20)

          self.navFrame = LabelFrame(self.master, text="")
          self.navFrame.grid(row=1, column=0, padx=(250,0), pady=50)

          self.vehicle_entry_portal_btn = Button(self.navFrame, text="Vehicle Entry", font=self.font , bg="#ff55ff", fg="#fff", command=lambda: self.vehicle_entry())
          self.vehicle_entry_portal_btn.grid(row=0, column=0, padx=20, pady=20)

          self.veiw_slot_portal_btn = Button(self.navFrame, text="View Available Slots", font=self.font , bg="#ff55ff", fg="#fff")
          self.veiw_slot_portal_btn.grid(row=0, column=1, padx=20, pady=20)

          self.logout_btn = Button(self.navFrame, text="Logout", bg="#ff55ff", font=self.font , fg="#fff", command= lambda: self.logout())
          self.logout_btn.grid(row=0, column=2, padx=20, pady=20)
          
          self.tableFrame = LabelFrame(self.master, text="", bg="#5a9bad")
          self.tableFrame.grid(row=2, column=0, padx=(200, 0), sticky="nsew")

          self.heading = Label(self.tableFrame, text="Today's Records", bg="#5a9bad", fg="#fff", font="Verdana 14 bold")
          self.heading.grid(row=0, column=0, pady=10, columnspan=2)

          self.tv = ttk.Treeview(self.tableFrame, style="mystyle.Treeview", columns=(1, 2, 3, 4, 5), show="headings",height=25, selectmode="none")
          self.tv.grid(row=1, column=0)

          # changing font size of heading and body of tree view
          self.style = ttk.Style()
          self.style.configure('Treeview.Heading', font=("verdana bold", 12))
          self.style.configure("mystyle.Treeview", highlightthickness=1, bd=1, font=('verdana', 11))  # Modify the font of the body
          self.style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])  # Remove the borders

          self.verscrlbar = ttk.Scrollbar(self.tableFrame, orient="vertical", command=self.tv.yview)
          self.verscrlbar.grid(row=1, column=1, rowspan=30, sticky='ns')
          self.tv.configure(yscrollcommand=self.verscrlbar.set)

          self.tv.column(1, width=100, anchor='c')
          self.tv.column(2, width=400)
          self.tv.column(3, width=200, anchor='c')
          self.tv.column(4, width=250, anchor='c')
          self.tv.column(5, width=150, anchor='c')

          self.tv.heading(1, text="ID")
          self.tv.heading(2, text="Owner's Name")
          self.tv.heading(3, text="Car Number")
          self.tv.heading(4, text="Date")
          self.tv.heading(5, text="Booked Slot")


     def vehicle_entry(self):

          self.availabel_slot = self.check_availabel_slot()

          self.bgcolor = "#66ffff"
          self.toplevel = Toplevel(self.master)
          self.toplevel.geometry("800x800")
          self.toplevel.resizable(height=0, width=0)
          self.toplevel.title("Vehicle Entry")
          self.toplevel.config(bg=self.bgcolor)

          self.heading = Label(self.toplevel, text="Vehicle Entry Form", bg=self.bgcolor, font="Verdana 20 bold")
          self.heading.grid(row=0, column=0, columnspan=3, padx=(100,0), pady=30, sticky='nesw')

          self.label = Label(self.toplevel, text="First Name", bg=self.bgcolor, font=self.font)
          self.label.grid(row=1, column=0, padx=(100,20), pady=10)

          self.fnameEntry = Entry(self.toplevel, font="verdana 12")
          self.fnameEntry.grid(row=1, column=1, padx=10, pady=10)

          self.label = Label(self.toplevel, text="Last Name", bg=self.bgcolor, font=self.font)
          self.label.grid(row=2, column=0, padx=(100,20), pady=10)

          self.lnameEntry = Entry(self.toplevel, font="verdana 12")
          self.lnameEntry.grid(row=2, column=1, padx=10, pady=10)

          self.label = Label(self.toplevel, text="Vehicle Number", bg=self.bgcolor, font=self.font)
          self.label.grid(row=3, column=0, padx=(100,20), pady=10)

          self.velicle_num_Entry = Entry(self.toplevel, font="verdana 12")
          self.velicle_num_Entry.grid(row=3, column=1, padx=10, pady=10)

          self.label = Label(self.toplevel, text="Contact No", bg=self.bgcolor, font=self.font)
          self.label.grid(row=5, column=0, padx=(100,20), pady=10)

          self.telnumEntry = Entry(self.toplevel, font="verdana 12")
          self.telnumEntry.grid(row=5, column=1, padx=10, pady=10)

          self.label = Label(self.toplevel, text="Slot", bg=self.bgcolor, font=self.font)
          self.label.grid(row=6, column=0, padx=(100,20), pady=10)

          if self.available_slot > 0:
               self.label = Label(self.toplevel, text= self.available_slot, bg=self.bgcolor, font="verdana 12")
               self.label.grid(row=6, column=1, padx=(100,20), pady=10)
          else:
               self.label = Label(self.toplevel, text="No slot is available." , bg=self.bgcolor, font="verdana 12")
               self.label.grid(row=6, column=1, padx=(100,20), pady=10)

          self.label = Label(self.toplevel, text="Gender", bg=self.bgcolor, font=self.font)
          self.label.grid(row=7, column=0, padx=(100,20), pady=10)

          self.genderOptions = ['Male', 'Female']
          self.gender = StringVar()
          self.gender.set(self.genderOptions[0])

          self.genderEntry = OptionMenu(self.toplevel, self.gender, *self.genderOptions)
          self.genderEntry.config(font="verdana 12")
          self.genderEntry.grid(row=7, column=1, padx=10, pady=10)

          self.save = Button(self.toplevel, text="Save", bg="#0000cc", cursor="hand2", fg="#fff", font="verdana 12", width=20, command=lambda: self.validateForm())
          self.save.grid(row=11, column=0, padx=(50, 0), pady=(30,0))

          self.reset = Button(self.toplevel, text="Reset", bg="#ff6600", cursor="hand2", font="verdana 12", width=20, command=lambda: self.resetForm())
          self.reset.grid(row=11, column=1, padx=(10, 0), pady=(30, 0))
          pass 

     
     def validateForm(self):
          if self.fnameEntry.get() == '':
               messagebox.showerror('Error', "Please enter your first name.", parent=self.toplevel)
               self.fnameEntry.focus()
               return

          if self.lnameEntry.get() == '':
               messagebox.showerror('Error', "Please enter your Last name.", parent=self.toplevel)
               self.lnameEntry.focus()
               return

          if self.velicle_num_Entry.get() == '':
               messagebox.showerror('Error', "Please enter your address.", parent=self.toplevel)
               self.addrEntry.focus()
               return

          if self.telnumEntry.get() == '':
               messagebox.showerror('Error', "Please enter your phone number.", parent=self.toplevel)
               self.telnumEntry.focus()
               return

          if not self.valid_tel_num():
               messagebox.showerror('Error', "Please enter valid Number", parent=self.toplevel)
               self.telnumEntry.focus()
               return

          self.save_form_data()
          pass


     def check_availabel_slot(self):
          connection = db_connection.connect()
          cursor = connection.cursor()
          try:
               cursor.execute("select * from slot where booked_status='Available'")
               data = cursor.fetchall()
               if data == None or len(data) <= 0:
                    messagebox.showerror("Error", "No slots available right now. Please try after some time.")
                    return 0
               else:
                    return int(data[0][0])

          except Exception as e:
               connection.rollback()
               print(e)
          
          return 0


     def save_form_data(self):
          connection = db_connection.connect()
          cursor = connection.cursor()

          try:
               cursor.execute("insert into vehicle_details(full_name, vehicle_number, phone_number, gender, slot) values ('{}', '{}', {}, '{}', '{}')".format((self.fnameEntry.get()+" "+ self.lnameEntry.get()), self.velicle_num_Entry.get(), int(self.telnumEntry.get()), self.gender.get(), self.available_slot))
               connection.commit()

               messagebox.showinfo("Successful", "Slot Booked successfully..", parent=self.toplevel)

          except Exception as e:
               connection.rollback()
               messagebox.showerror("Error", e, parent=self.toplevel)
               print(e)

          connection.close()
          self.resetForm()


     def valid_tel_num(self):
          if len(re.findall("[a-bA-Z]", self.telnumEntry.get())) > 0:
               return False

          if len(self.telnumEntry.get()) != 10:
               return False
          return True


     def resetForm(self):
          self.availabel_slot = self.check_availabel_slot()
          self.fnameEntry.delete(0, END)
          self.lnameEntry.delete(0, END)
          self.velicle_num_Entry.delete(0, END)
          self.telnumEntry.delete(0, END)
          self.gender.set("--Select--")
          self.fnameEntry.focus()
          pass


     def logout(self):
          Remove.remove_all_widgets(self.navFrame)
          self.loginWindow()



if __name__ == '__main__':
     root = Tk()
     root.geometry("1500x900")
     root.title("Vehicle Parking Management System")
     root.config(background="yellow")
     root.resizable(height=0, width=0)

     main_obj = MainWindow(root)
     main_obj.loginWindow()

     root.mainloop()