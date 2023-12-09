# imports used for program
from datetime import datetime
from tkinter import *
from tkinter import messagebox


# Vehicle Class
class Vehicle:
    def __init__(self, color, make, model, year, note=""):
        # uses lower and capitalize to make it both look need and all will be in the same case
        self.color = color.lower().capitalize()
        self.make = make.lower().capitalize()
        self.model = model.lower().capitalize()
        self.year = year
        self.note = note

    # Used for output and testing
    def __str__(self):
        return f"{self.color}, {self.year} {self.make} {self.model}"

    # Update's the vehicle's note variable
    def update_note(self, note_txt):
        self.note = note_txt


# Customer Class
class Customer:
    # Class initialization
    def __init__(self, fname, lname, phone, email, vehicle):

        self.fname = fname.lower().capitalize()
        self.lname = lname.lower().capitalize()
        self.phone = self.update_phone(phone)
        self.email = self.format_email(email)
        self.vehicle = vehicle
        self.next = None

    # Output used for testing
    def __str__(self):
        return f"Customer Name: {self.fname} {self.lname}, Phone Number: {self.phone}\n" \
               f"{self.vehicle}"

    # Formats the number string to show up like (xxx)xxx-xxxx
    def format_phone(self, phone_number):

        if len(phone_number) == 10:
            formatted_number = f"({phone_number[0:3]}){phone_number[3:6]}-{phone_number[6:]}"
            return formatted_number
        elif len(phone_number) == 13:
            return phone_number
        else:
            return "Cannot create, make sure your input is 10 digits and only numbers."

    # Checks if it has an @ sign to verify email (time crunch can update)
    def format_email(self, email):
        if email.__contains__("@"):
            formatted_email = email
            return formatted_email
        else:
            return f"Cannot create/update, incorrect email layout, makes sure you include the @ and web address."

    # Updates the phone with format, used with initialization
    def update_phone(self, phone_number):
        formatted_phone = self.format_phone(phone_number)
        self.phone = formatted_phone
        return formatted_phone

    # Updates the email after check, used with initialization
    def update_email(self, email):
        formatted_email = self.format_email(email)
        self.email = formatted_email
        return formatted_email


# Linked List Class
class CustomerList:
    # Creation
    def __init__(self):
        self.head = None

    # Adds customer to list, and will sort them in order by first name then last name
    def add_customer(self, fname, lname, phone, email, vehicle):

        new_customer = Customer(fname, lname, phone, email, vehicle)

        if not self.head:
            self.head = new_customer
            return
        # Sorting
        if fname.lower() < self.head.fname.lower() or (fname.lower() == self.head.fname.lower()
                                                   and lname.lower() < self.head.last_name.lower()):
            new_customer.next = self.head
            self.head = new_customer
            return

        current = self.head

        while current.next and (fname.lower() > current.next.fname.lower() or
                                (fname.lower() == current.next.fname.lower() and
                                lname.lower() > current.next.lname.lower())):
            current = current.next

        new_customer.next = current.next
        current.next = new_customer

    # Find's customer using first name last name
    def find_customer(self, first_name, last_name):

        current = self.head
        # Searching linked list
        while current:

            if current.fname.lower() == first_name.lower() and current.lname.lower() == last_name.lower():
                return current

            current = current.next

        return None

    # Outputs each Customer and their information
    def display_customers(self):

        current = self.head
        all_customers = []

        # Goes through linked list outputting formatted information
        while current:

            customer_info = (f"Name: {current.fname} {current.lname},\n"
                             f"Phone: {current.phone}, Email: {current.email},\n"
                             f"Vehicle Info: {current.vehicle}\n")

            all_customers.append(customer_info)
            current = current.next

        return all_customers


# Appointment Class
class Appointment:
    # Appointment Creation
    def __init__(self, customer, date, time):

        self.customer = customer
        self.date = date
        self.time = time

    # Output for information and testing
    def __str__(self):

        return f"Appointment for {self.customer.fname} {self.customer.lname} at " \
               f"{self.time.strftime('%I:%M %p')} on {self.date.strftime('%Y-%m-%d')}"


# Node used for linked list
class Node:
    def __init__(self, appointment):

        self.appointment = appointment
        self.next = None


# Appointment Queue Class
class AppointmentQueue:
    def __init__(self, customer_list):

        self.head = None
        self.customer_list = customer_list

    def get_length(self):

        current = self.head
        length = 0

        while current:

            length += 1
            current = current.next

        return length

    # Adds appointment to queue by date then time
    def add_appointment(self, new_appointment):

        new_node = Node(new_appointment)

        if not self.head:

            self.head = new_node

        else:

            current = self.head
            prev = None

            while current and (current.appointment.date < new_appointment.date or
                               (current.appointment.date == new_appointment.date and
                                current.appointment.time < new_appointment.time)):
                prev = current
                current = current.next

            if prev:

                prev.next = new_node
                new_node.next = current

            else:

                new_node.next = self.head
                self.head = new_node

        customer = new_appointment.customer
        self.customer_list.add_customer(customer.lname, customer.lname, customer.phone, customer.email, customer.vehicle)

    # Finds first name last name combination then deletes it from queue
    def remove_appointment_by_name(self, first_name, last_name):

        current = self.head
        prev = None
        found_appointment = False

        # Looking for name
        while current:

            customer = current.appointment.customer

            if(customer.fname.lower() == first_name.lower() and
                    customer.lname.lower() == last_name.lower()):

                found_appointment = True

                if prev:
                    prev.next = current.next
                else:
                    self.head = current.next
                break

            prev = current
            current = current.next

        if found_appointment:

            print(f"Appointment for {first_name} {last_name} removed.")
            return True

        else:

            print(f"No appointment found for {first_name} {last_name}.")
            return False

    # Outputs Appointment info
    def display_customer_appointments(self):

        current = self.head

        while current:

            print(current.appointment)
            current = current.next


# GUI Class
class GUI:
    # Main Menu
    def __init__(self, master):

        self.customer_list = CustomerList()
        self.appointment_queue = AppointmentQueue(self.customer_list)

        self.master = master
        self.master.title("Appointment System")
        self.master.geometry("400x200")

        self.home_frame = Frame(master)
        self.home_frame.pack()

        self.home_label = Label(self.home_frame, text="Select which action you'd like to take:")
        self.home_label.pack()

        self.add_button = Button(self.home_frame, text="Add Appointment", command=self.open_add_appointment)
        self.add_button.pack()

        self.remove_button = Button(self.home_frame, text="Remove Appointment", command=self.open_remove_appointment)
        self.remove_button.pack()

        self.show_customers_button = Button(self.home_frame, text="Show All Customers", command=self.show_all_customers_info)
        self.show_customers_button.pack()

        self.show_all_button = Button(self.home_frame, text="Show All Appointments", command=self.show_all_appointments)
        self.show_all_button.pack()

        self.find_customer_button = Button(self.home_frame, text="Find Customer", command=self.search_customer)
        self.find_customer_button.pack()

        self.update_customer_button = Button(self.home_frame, text="Update Customer", command=self.update_customer_info)
        self.update_customer_button.pack()

        self.close_button = Button(self.home_frame, text="Close Program", command=master.quit)
        self.close_button.pack()

        self.appointment_queue = AppointmentQueue(self.customer_list)

    # Where the add appointment fields are
    def open_add_appointment(self):
        self.home_frame.pack_forget()

        add_frame = Frame(self.master)
        add_frame.pack()

        self.master.geometry("300x500")

        fname_label = Label(add_frame, text="First Name:")
        fname_label.pack()
        fname_entry = Entry(add_frame)
        fname_entry.pack()

        lname_label = Label(add_frame, text="Last Name:")
        lname_label.pack()
        lname_entry = Entry(add_frame)
        lname_entry.pack()

        phone_label = Label(add_frame, text="Phone:")
        phone_label.pack()
        phone_entry = Entry(add_frame)
        phone_entry.pack()

        email_label = Label(add_frame, text="Email:")
        email_label.pack()
        email_entry = Entry(add_frame)
        email_entry.pack()

        color_label = Label(add_frame, text="Color:")
        color_label.pack()
        color_entry = Entry(add_frame)
        color_entry.pack()

        make_label = Label(add_frame, text="Make:")
        make_label.pack()
        make_entry = Entry(add_frame)
        make_entry.pack()

        model_label = Label(add_frame, text="Model:")
        model_label.pack()
        model_entry = Entry(add_frame)
        model_entry.pack()

        year_label = Label(add_frame, text="Year:")
        year_label.pack()
        year_entry = Entry(add_frame)
        year_entry.pack()

        note_label = Label(add_frame, text="Reason for appointment:")
        note_label.pack()
        note_entry = Entry(add_frame)
        note_entry.pack()

        date_label = Label(add_frame, text="Date (YYYY-MM-DD):")
        date_label.pack()
        date_entry = Entry(add_frame)
        date_entry.pack()

        time_label = Label(add_frame, text="Time (HH:MM)")
        time_label.pack()
        time_entry = Entry(add_frame)
        time_entry.pack()

        # Action for button to add to queue
        def add_to_queue():

            fname = fname_entry.get()
            lname = lname_entry.get()
            phone = phone_entry.get()
            email = email_entry.get()
            color = color_entry.get()
            make = make_entry.get()
            model = model_entry.get()
            year = year_entry.get()
            note = note_entry.get()
            date = date_entry.get()
            time = time_entry.get()

            if not all((fname, lname, phone, email, color, make, model, year, date, time)):
                messagebox.showwarning("Warning", "One or more fields are empty, please fill them to continue.")
                return

            if note is not None:
                vehicle = Vehicle(color, make, model, year, note)
            else:
                vehicle = Vehicle(color, make, model, year)

            customer = Customer(fname, lname, phone, email, vehicle)

            try:
                appointment_date = datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Date Error", "Please enter date in YYYY-MM-DD format")
                return

            try:
                appointment_time = datetime.strptime(time, "%H:%M")
            except ValueError:
                messagebox.showerror("Time Error", "Please enter the time in HH:MM format")

            appointment = Appointment(customer, appointment_date, appointment_time)

            self.appointment_queue.add_appointment(appointment)

            success_message = f"Appointment for {fname} {lname} added to queue."
            messagebox.showinfo("Success", success_message)

            fname_entry.delete(0, END)
            lname_entry.delete(0, END)

            self.go_back(add_frame)

        add_button = Button(add_frame, text="Add to Queue", command=add_to_queue)
        add_button.pack()

        back_button = Button(add_frame, text="Go Back", command=lambda: self.go_back(add_frame))
        back_button.pack()

    # Action for button to remove appointment
    def open_remove_appointment(self):
        self.home_frame.pack_forget()
        remove_frame = Frame(self.master)
        remove_frame.pack()

        fname_label = Label(remove_frame, text="First Name:")
        fname_label.pack()
        fname_entry = Entry(remove_frame)
        fname_entry.pack()

        lname_label = Label(remove_frame, text="Last Name:")
        lname_label.pack()
        lname_entry = Entry(remove_frame)
        lname_entry.pack()

        result_label = Label(remove_frame, text="")
        result_label.pack()

        # Removes from queue
        def remove_from_queue():
            fname = fname_entry.get()
            lname = lname_entry.get()

            success = self.appointment_queue.remove_appointment_by_name(fname, lname)

            fname_entry.delete(0, END)
            lname_entry.delete(0, END)

            if success:
                result_label.config(text=f"Appointment for {fname} {lname} has been deleted.")
            else:
                result_label.config(text=f"No appointment found for {fname} {lname}")

        remove_button = Button(remove_frame, text="Remove Appointment", command=remove_from_queue)
        remove_button.pack()

        back_button = Button(remove_frame, text="Go Back", command=lambda: self.go_back(remove_frame))
        back_button.pack()

    # looks for customer to be deleted from appointments
    def search_customer(self):
        self.home_frame.pack_forget()

        search_frame = Frame(self.master)
        search_frame.pack()

        self.master.geometry("300x225")

        fname_label = Label(search_frame, text="First Name:")
        fname_label.pack()
        fname_entry = Entry(search_frame)
        fname_entry.pack()

        lname_label = Label(search_frame, text="Last Name:")
        lname_label.pack()
        lname_entry = Entry(search_frame)
        lname_entry.pack()

        result_label = Label(search_frame, text="")
        result_label.pack()

        # finds customer for customer information
        def find_customer():
            first_name = fname_entry.get().capitalize()
            last_name = lname_entry.get().capitalize()

            found_customer = self.appointment_queue.customer_list.find_customer(first_name, last_name)

            if found_customer:
                if found_customer.vehicle.note is not None:
                    result = (f"Customer Info:\n"
                              f"Name: {found_customer.fname} {found_customer.lname}\n"
                              f"Phone: {found_customer.phone}, Email: {found_customer.email}\n"
                              f"Vehicle Info: {found_customer.vehicle}\n"
                              f"Vehicle Note: {found_customer.vehicle.note}")
                else:
                    result = (f"Customer Info:\n"
                              f"Name: {found_customer.fname} {found_customer.lname}\n"
                              f"Phone: {found_customer.phone}, Email: {found_customer.email}\n"
                              f"Vehicle Info: {found_customer.vehicle}\n")

                result_label.config(text=result)
            else:
                result_label.config(text="Customer not found, either misspelled or not in list.")

        find_button = Button(search_frame, text="Find Customer", command=find_customer)
        find_button.pack()

        home_button = Button(search_frame, text="Go Back", command=lambda: self.go_back(search_frame))
        home_button.pack()

    # Shows all information for all customers in order
    def show_all_customers_info(self):
        all_customers = self.appointment_queue.customer_list.display_customers()

        all_customers_info_window = Toplevel(self.master)
        all_customers_info_window.title("All Customers Information")
        all_customers_info_window.geometry("400x600")

        all_customers_info_label = Label(all_customers_info_window, text="All Customers Information")
        all_customers_info_label.pack()

        customer_frame = Frame(all_customers_info_window)
        customer_frame.pack()

        for customer in all_customers:
            customer_label = Label(customer_frame, text=customer)
            customer_label.pack(anchor=W)

        back_button = Button(all_customers_info_window, text="Go Back", command=all_customers_info_window.withdraw)
        back_button.pack()

    # Shows all appointments in queue and their information
    def show_all_appointments(self):
        self.home_frame.pack_forget()

        show_all_frame = Toplevel(self.master)
        show_all_frame.title("All Appointments")

        show_all_frame.geometry("400x600")

        appointment_label = Label(show_all_frame, text="Customer and Their Appointment:")
        appointment_label.pack()

        appointments_frame = Frame(show_all_frame)
        appointments_frame.pack()

        # Gets appointment to output on GUI
        def grab_and_display_appointments():
            current = self.appointment_queue.head
            row = 0
            while current:
                appointments_label = Label(appointments_frame, text=str(current.appointment))
                appointments_label.grid(row=row, column=0, sticky=W)
                current = current.next
                row += 1

        grab_and_display_appointments()

        # Used to get back to home page
        def go_home():
            show_all_frame.withdraw()
            self.master.geometry("300x200")
            self.home_frame.pack()

        back_button = Button(show_all_frame, text="Go Back", command=go_home)
        back_button.pack()

    # Brings to search page to change information
    def update_customer_info(self):
        self.home_frame.pack_forget()

        search_frame = Frame(self.master)
        search_frame.pack()

        self.master.geometry("300x225")

        fname_label = Label(search_frame, text="First Name:")
        fname_label.pack()
        fname_entry = Entry(search_frame)
        fname_entry.pack()

        lname_label = Label(search_frame, text="Last Name:")
        lname_label.pack()
        lname_entry = Entry(search_frame)
        lname_entry.pack()

        # finds customer based on first name last name to update information
        def find_customer():

            first_name = fname_entry.get().capitalize()
            last_name = lname_entry.get().capitalize()

            found_customer = self.appointment_queue.customer_list.find_customer(first_name, last_name)

            if found_customer:
                messagebox.showinfo("Customer Found", f"Success! {first_name} {last_name} is a customer!")
                self.display_update_fields(search_frame, found_customer)
                fname_label.pack_forget()
                fname_entry.pack_forget()
                lname_label.pack_forget()
                lname_entry.pack_forget()
                remove_button.pack_forget()
                back_button.pack_forget()
            else:
                messagebox.showwarning("Customer Not Found", f"Failure! {first_name} {last_name} is not a customer, try again.")

        remove_button = Button(search_frame, text="Find Customer", command=find_customer)
        remove_button.pack()

        back_button = Button(search_frame, text="Go Back", command=lambda: self.go_back(search_frame))
        back_button.pack()

    # Fields that are grabbed from when asked for information
    def display_update_fields(self, frame, customer):

        update_frame = Frame(frame)
        update_frame.pack()

        update_label = Label(update_frame, text="Fill in what you would like to update:")
        update_label.pack()

        email_label = Label(update_frame, text=" New Email:")
        email_label.pack()
        email_entry = Entry(update_frame)
        email_entry.pack()

        phone_label = Label(update_frame, text="New Phone:")
        phone_label.pack()
        phone_entry = Entry(update_frame)
        phone_entry.pack()

        note_label = Label(update_frame, text="New Note:")
        note_label.pack()
        note_entry = Entry(update_frame)
        note_entry.pack()

        # Updates the Customer information
        def update_customer():

            email = email_entry.get()
            phone = phone_entry.get()
            note = note_entry.get()

            if email:
                update_email_result = customer.update_email(email)
                if update_email_result:
                    messagebox.showinfo("Email Update", f"Email updated to: {update_email_result}")
            if phone:
                customer.update_phone(phone)
                messagebox.showinfo("Phone Update", f"Phone number updated to: {phone}")
            if note:
                customer.vehicle.update_note(note)
                messagebox.showinfo("Note Update", f"Note updated to: {note}")

            if email or phone or note:
                self.go_back(update_frame)
                self.master.geometry("300x200")

                self.home_frame.pack()

            else:
                messagebox.showwarning("All Fields Empty", "You must enter in at least one field, otherwise, hit home")

        update_button = Button(update_frame, text="Update", command=update_customer)
        update_button.pack()

        home_button = Button(update_frame, text="Home", command=lambda: self.go_back(update_frame))
        home_button.pack()

     # Used to go to main menu
    def go_back(self, frame):
        frame.pack_forget()
        self.master.geometry("300x200")
        self.home_frame.pack()


# Commented out code was for driver testing
if __name__ == '__main__':

    root = Tk()
    app = GUI(root)
    root.mainloop()

    # appointment_queue = AppointmentQueue()
    # customer_list = []
    #
    # vehicle1 = Vehicle("red", "toyota", "corolla", 2013)
    # vehicle2 = Vehicle("silver", "honda", "civic", 2018)
    # vehicle3 = Vehicle("black", "nissan", "maxima", 2008)
    #
    # customer1 = Customer("john", "smith", "5153390000", "rando@gmail.com", vehicle1)
    # customer2 = Customer("jane", "doe", "5159993892", "rende@gmail.com", vehicle2)
    # customer3 = Customer("josh", "johnson", "5157775559", "srtram@me.com", vehicle3)
    #
    # customer_list.append(customer1)
    # customer_list.append(customer2)
    # customer_list.append(customer3)
    #
    # appointment_date1 = datetime(2023, 12, 12)
    # appointment_time1 = datetime.strptime("9:00", "%H:%M").time()
    #
    # appointment_date2 = datetime(2023, 12, 11)
    # appointment_time2 = datetime.strptime("11:30", "%H:%M").time()
    #
    # appointment_date3 = datetime(2023, 12, 11)
    # appointment_time3 = datetime.strptime("11:00", "%H:%M").time()
    #
    # appointment1 = Appointment(customer1, appointment_date1, appointment_time1)
    # appointment2 = Appointment(customer2, appointment_date2, appointment_time2)
    # appointment3 = Appointment(customer3, appointment_date3, appointment_time3)
    #
    # appointment_queue.add_appointment(appointment1)
    # appointment_queue.add_appointment(appointment2)
    # appointment_queue.add_appointment(appointment3)
    #
    # appointment_queue.display_customer_appointments()
    #
    # print(appointment_queue.get_length())
    #
    # appointment_queue.remove_appointment_by_name("Jane", "Doe")
    #
    # appointment_queue.display_customer_appointments()
    # print(appointment_queue.get_length())
