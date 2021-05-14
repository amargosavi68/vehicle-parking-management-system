from tkinter import *   

class MainWindow:

     def __init__(self, root):
          self.master = root
          self.font = "verdana 12 bold"
          self.color = "yellow"
          self.__username = ""
          self.__password = ""

     def loginWindow(self):
          heading = Label(self.master, text="Vehicle Parking Management System", font="verdana 22 bold", bg=self.color)
          heading.pack(pady=20)

          self.loginFrame = LabelFrame(self.master, text="")
          self.loginFrame.pack(padx=50, pady=50)

          self.username_label = Label(self.loginFrame, text="Username", font=self.font, bg="#f2f2f2")
          self.username_label.grid(row=0, column=0, padx=30, pady=(40,20))

          self.username_entry = Entry(self.loginFrame, textvariable=self.__username, width=20, font="verdana 12")
          self.username_entry.grid(row=0, column=1, padx=(10, 30), pady=(40,20), ipady=3)

          self.password_label = Label(self.loginFrame, text="Password", font=self.font, bg="#f2f2f2")
          self.password_label.grid(row=1, column=0, padx=30, pady=20)

          self.password_entry = Entry(self.loginFrame, textvariable=self.__password, width=20, font="verdana 12")
          self.password_entry.grid(row=1, column=1, padx=(10,30), pady=20, ipady=3)

          self.login_button = Button(self.loginFrame, text="Login", width="20", font="verdana 12 bold", bg="#00a5aa", fg="#fff", cursor="hand2")
          self.login_button.grid(row=2, column=0, columnspan=2, padx=30, pady=30)

          pass


if __name__ == '__main__':
     root = Tk()
     root.geometry("1300x800")
     root.title("Vehicle Parking Management System")
     root.config(background="yellow")

     main_obj = MainWindow(root)
     main_obj.loginWindow()

     root.mainloop()