import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class ComputerLabBookingSystem:
    def __init__(self, lab_capacity, lab_name):
        self.lab_capacity = lab_capacity
        self.lab_schedule = {}
        self.lab_name = lab_name

    def book_lab(self, user_name, id_value, date, time_slot, faculty_code):
        if user_name not in self.lab_schedule:
            self.lab_schedule[user_name] = {}
        if id_value not in self.lab_schedule[user_name]:
            self.lab_schedule[user_name][id_value] = {}
        if date not in self.lab_schedule[user_name][id_value]:
            self.lab_schedule[user_name][id_value][date] = {'time_slot': time_slot, 'faculty_code': faculty_code}
            return True
        else:
            return False

    def update_booking(self, user_name, id_value, date, new_time_slot):
        formatted_date = datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d")

        if user_name in self.lab_schedule and id_value in self.lab_schedule[user_name]:
            user_bookings = self.lab_schedule[user_name][id_value]

            if formatted_date in user_bookings:
                print(f"Updating booking for {user_name}, ID: {id_value}, Date: {formatted_date}, New Time Slot: {new_time_slot}")

                # Update the time slot
                user_bookings[formatted_date]['time_slot'] = new_time_slot

                print("Lab Schedule after update:")
                print(self.lab_schedule)

                return True
            else:
                print(f"Date {formatted_date} not found for user {user_name}, ID: {id_value}")
        else:
            print(f"User {user_name}, ID: {id_value} not found in lab schedule")

        return False

    def delete_booking(self, user_name, id_value, date):
        if user_name in self.lab_schedule and id_value in self.lab_schedule[user_name] and date in self.lab_schedule[user_name][id_value]:
            del self.lab_schedule[user_name][id_value][date]
            if not self.lab_schedule[user_name][id_value]:
                del self.lab_schedule[user_name][id_value]
                if not self.lab_schedule[user_name]:
                    del self.lab_schedule[user_name]
            return True
        else:
            return False

    def get_bookings(self):
        return self.lab_schedule

def book_lab_callback():
    user_name = user_entry.get()
    id_value = id_entry.get()
    date = date_entry.get()
    time_slot = selected_time.get()
    faculty_code = faculty_entry.get()

    if not user_name or not id_value or not date or not time_slot or not faculty_code:
        messagebox.showerror("Error", "Please fill in all fields.")
        return

    success = lab_system.book_lab(user_name, id_value, date, time_slot, faculty_code)

    if success:
        outcome_label.config(text=f"Booking successful for {user_name}, ID: {id_value} on {date} at {time_slot}.")
    else:
        outcome_label.config(text=f"Sorry, the time slot {time_slot} on {date} is already booked.")

def update_booking_callback():
    selected_item = tree.selection()

    if not selected_item:
        messagebox.showinfo("Info", "Please select a booking to update.")
        return

    # Extract information from the selected item
    values = tree.item(selected_item, 'values')
    user_name, id_value, date_str, time_slot, faculty_code = values

    # Convert date to the expected format
    try:
        date = datetime.strptime(date_str, "%d %B %Y").strftime("%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Error", "Invalid date format. Please select a valid date.")
        return

    # Prompt user for new time slot using dropdown
    new_time_slot = show_time_slot_dropdown()

    if new_time_slot:
        success = lab_system.update_booking(user_name, id_value, date, new_time_slot)

        if success:
            messagebox.showinfo("Success", f"Booking updated for {user_name}, ID: {id_value} on {date}. New time slot: {new_time_slot}")
            open_bookings_window()  # Refresh the bookings window
        else:
            messagebox.showerror("Error", "Failed to update booking. Please try again.")

def open_bookings_window():
    bookings_window = tk.Toplevel(root)
    bookings_window.title("List of Bookings")

    # Set the size of the window
    bookings_window.geometry("900x600")

    # Set the background color for the window
    bookings_window.configure(background='#283747')

    bookings_label = tk.Label(bookings_window, text="List of Bookings", font=("Helvetica", 16))
    bookings_label.pack(pady=10)

    # Create a Treeview widget
    global tree  # Ensure 'tree' is a global variable
    tree = ttk.Treeview(bookings_window, columns=('User', 'ID', 'Date', 'Time Slot', 'Faculty Code'), show='headings')

    # Set column headings
    tree.heading('User', text='User')
    tree.heading('ID', text='ID')
    tree.heading('Faculty Code', text='Faculty Code')
    tree.heading('Date', text='Date')
    tree.heading('Time Slot', text='Time Slot')

    # Get bookings and sort them
    bookings = lab_system.get_bookings()

    if not bookings:
        print("No bookings available")  # Debugging line
    else:
        for user_name, user_bookings in bookings.items():
            for id_value, id_bookings in user_bookings.items():
                for date, data in id_bookings.items():
                    time_slot = data.get('time_slot', 'N/A')
                    faculty_code = data.get('faculty_code', 'N/A')
                    tree.insert('', 'end', values=(user_name, id_value, date, time_slot, faculty_code))

    # Pack the Treeview
    tree.pack(expand=True, fill='both')

    # Add Update and Delete buttons
    update_button = tk.Button(bookings_window, text="Update Booking", command=update_booking_callback)
    update_button.pack(pady=10)

    delete_button = tk.Button(bookings_window, text="Delete Booking", command=delete_booking_callback)
    delete_button.pack(pady=10)

# ... (rest of your code remains unchanged)

def delete_booking_callback():
    global tree
    selected_item = tree.selection()

    if not selected_item:
        messagebox.showinfo("Info", "Please select a booking to delete.")
        return

    # Extract information from the selected item
    values = tree.item(selected_item, 'values')
    user_name, id_value, date, time_slot, faculty_code = values

    # Confirm deletion with the user
    confirm_delete = messagebox.askyesno("Confirm Deletion", f"Do you really want to delete the booking for {user_name}, ID: {id_value} on {date}?")

    if confirm_delete:
        success = lab_system.delete_booking(user_name, id_value, date)

        if success:
            messagebox.showinfo("Success", f"Booking deleted for {user_name}, ID: {id_value} on {date}.")
            open_bookings_window()  # Refresh the bookings window
        else:
            messagebox.showerror("Error", "Failed to delete booking. Please try again.")

def show_time_slot_dropdown():
    # Prompt user for new time slot using dropdown
    new_time_slot_window = tk.Toplevel(root)
    new_time_slot_window.title("Select New Time Slot")

    # Set the size of the window
    new_time_slot_window.geometry("400x200")

    # Set the background color for the window
    new_time_slot_window.configure(background='#283747')

    new_time_label = tk.Label(new_time_slot_window, text="Update Time Slot:", font=("Helvetica", 16), background='#283747', fg='BLACK')
    new_time_label.pack(pady=10)

    new_time_options = ["9:00 AM - 10:00 AM", "10:00 AM - 11:00 AM", "11:00 AM - 12:00 PM", "12:00 PM - 1:00 PM", "1:00 PM - 2:00 PM", "2:00 PM - 3:00 PM", "3:00 PM - 4:00 PM", "4:00 PM - 5:00 PM"]
    selected_new_time = tk.StringVar()
    new_time_dropdown = ttk.Combobox(new_time_slot_window, textvariable=selected_new_time, values=new_time_options)
    new_time_dropdown.set("Select New Time Slot")
    new_time_dropdown.pack(pady=10)

    def confirm_update():
        new_time_slot = selected_new_time.get()
        new_time_slot_window.destroy()
        return new_time_slot

    confirm_button = tk.Button(new_time_slot_window, text="Confirm", command=confirm_update, background='#2ecc71', fg='white', font=("Helvetica", 12))
    confirm_button.pack(pady=10)

# GUI setup
root = tk.Tk()
root.title("COMPUTER LAB BOOKING SYSTEM")

# Set the initial size of the window
root.geometry("900x600")

# Set the background color for the entire root window
root.configure(background='#283747')

# Widgets for the main window
user_label = tk.Label(root, text="NAME:")
user_entry = tk.Entry(root)

id_label = tk.Label(root, text=" ID STUDENT / STAFF:")
id_entry = tk.Entry(root)

faculty_label = tk.Label(root, text="FACULTY CODE:")
faculty_entry = tk.Entry(root)

date_label = tk.Label(root, text="DATE:")
date_entry = tk.Entry(root)

time_label = tk.Label(root, text="TIME SLOT:")
time_options = ["9:00 AM - 10:00 AM", "10:00 AM - 11:00 AM", "11:00 AM - 12:00 PM", "12:00 PM - 1:00 PM", "1:00 PM - 2:00 PM", "2:00 PM - 3:00 PM", "3:00 PM - 4:00 PM", "4:00 PM - 5:00 PM"]
selected_time = tk.StringVar()
time_dropdown = ttk.Combobox(root, textvariable=selected_time, values=time_options)
time_dropdown.set("Select Time Slot")

outcome_label = tk.Label(root, text="", font=("Helvetica", 12), fg="black", background='#AED6F1')

# Dropdown for selecting the computer lab
lab_options = ["Computer Lab 1", "Computer Lab 2", "Computer Lab 3", "Computer Lab 4", "Computer Lab 5"]
selected_lab = tk.StringVar()
lab_dropdown = ttk.Combobox(root, textvariable=selected_lab, values=lab_options)
lab_dropdown.set("Select Computer Lab")

# Buttons for the main window
book_button = tk.Button(root, text="Book Lab", command=book_lab_callback)
check_bookings_button = tk.Button(root, text="Check Bookings", command=open_bookings_window)

# Grid layout for the main window
user_label.grid(row=0, column=0, padx=10, pady=10)
user_entry.grid(row=0, column=1, padx=10, pady=10)

id_label.grid(row=1, column=0, padx=10, pady=10)
id_entry.grid(row=1, column=1, padx=10, pady=10)

faculty_label.grid(row=2, column=0, padx=10, pady=10)
faculty_entry.grid(row=2, column=1, padx=10, pady=10)

date_label.grid(row=3, column=0, padx=10, pady=10)
date_entry.grid(row=3, column=1, padx=10, pady=10)

time_label.grid(row=4, column=0, padx=10, pady=10)
time_dropdown.grid(row=4, column=1, padx=10, pady=10)

lab_dropdown.grid(row=5, column=0, columnspan=2, pady=10)
book_button.grid(row=6, column=0, columnspan=2, pady=10)
check_bookings_button.grid(row=7, column=0, columnspan=2, pady=10)
outcome_label.grid(row=8, column=0, columnspan=2, pady=10)

# Create an instance of LabBookingSystem
lab_system = ComputerLabBookingSystem(lab_capacity=10, lab_name="Computer Lab")

# Start the GUI event loop
root.mainloop()