from tkinter import *  
from tkinter import messagebox 
import db_connection

# removing all grid elements from screen
class Remove:
     def __init__(self, master):
          super(Remove, self).__init__()
          self.master = master

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

          self.password_entry = Entry(self.loginFrame, textvariable=self.__password, width=20, font="verdana 12")
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
          cursor.execute("SELECT * from users where username='{}'".format(self.__username))

          if cursor.fetchone() == None:
               messagebox.showerror("Invalid Credentials", "Your credentials are invalid. Please try again.")
               self.username_entry.delete(0, END)
               self.password_entry.delete(0, END)
               self.username_entry.focus()
               return

          print("Username", self.__username, "is logged in into the system..")
          Remove.remove_all_widgets(self.loginFrame)
          self.homePortal()


     def homePortal(self):
          heading = Label(self.master, text="Vehicle Parking Management System", font="verdana 22 bold", bg=self.color)
          heading.grid(row=0, column=0, padx=(300,0), pady=20)

          self.navFrame = LabelFrame(self.master, text="")
          self.navFrame.grid(row=1, column=0, padx=(300,0), pady=50)

          self.vehicle_entry_portal_btn = Button(self.navFrame, text="Vehicle Entry", font=self.font , bg="#ff55ff", fg="#fff")
          self.vehicle_entry_portal_btn.grid(row=0, column=0, padx=20, pady=20)

          self.veiw_slot_portal_btn = Button(self.navFrame, text="View Available Slots", font=self.font , bg="#ff55ff", fg="#fff")
          self.veiw_slot_portal_btn.grid(row=0, column=1, padx=20, pady=20)

          self.logout_btn = Button(self.navFrame, text="Logout", bg="#ff55ff", font=self.font , fg="#fff", command= lambda: self.logout())
          self.logout_btn.grid(row=0, column=2, padx=20, pady=20)


     def logout(self):
          Remove.remove_all_widgets(self.navFrame)
          self.loginWindow()



if __name__ == '__main__':
     root = Tk()
     root.geometry("1300x800")
     root.title("Vehicle Parking Management System")
     root.config(background="yellow")

     main_obj = MainWindow(root)
     main_obj.loginWindow()

     root.mainloop()