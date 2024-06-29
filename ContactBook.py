import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk

root = tk.Tk()
root.title("Contact Book")
root.geometry("800x600")
root.config(bg="#A9A9A9")  

title_font = ("Helvetica", 24, "bold")
label_font = ("Helvetica", 12)
entry_font = ("Helvetica", 12)
button_font = ("Helvetica", 12, "bold")
bg_color = "#A9A9A9" 
accent_color = "#FF6347"
button_color = "#4682B4" 

style = ttk.Style()
style.configure("Treeview.Heading", font=('Helvetica', 12, 'bold'), foreground="black", background="#D3D3D3", borderwidth=1)
style.configure("Treeview", font=('Helvetica', 12), rowheight=25, borderwidth=1, relief="solid", bordercolor="black")
style.map("Treeview.Heading", background=[('active', '#D3D3D3')], foreground=[('active', 'black')])
style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])  

style.element_create('Custom.Treeheading.separator', 'from', 'default')
style.layout('Treeview.Heading', [('Treeheading.cell', {'sticky': 'nswe'}),
                                  ('Treeheading.border', {'sticky': 'nswe', 'children': [
                                      ('Treeheading.padding', {'sticky': 'nswe', 'children': [
                                          ('Treeheading.image', {'side': 'right', 'sticky': ''}),
                                          ('Treeheading.text', {'sticky': 'we'})
                                      ]})
                                  ]}),
                                  ('Custom.Treeheading.separator', {'side': 'right', 'sticky': 'ns'})])
contacts = []

def add_contact():
    name = simpledialog.askstring("Input", "Enter contact name:")
    if name is None:
        return
    phone = simpledialog.askstring("Input", "Enter contact phone number:")
    if phone is None:
        return
    email = simpledialog.askstring("Input", "Enter contact email:")
    if email is None:
        return
    address = simpledialog.askstring("Input", "Enter contact address:")
    if address is None:
        return
    
    if not name.strip() or not phone.strip() or not email.strip() or not address.strip():
        messagebox.showerror("Error", "Please fill in all fields.")
        return
    
    contacts.append({"name": name, "phone": phone, "email": email, "address": address})
    update_contact_list()

def update_contact_list():
    contact_list.delete(*contact_list.get_children())
    for contact in contacts:
        contact_list.insert("", tk.END, values=(contact["name"], contact["phone"], contact["email"], contact["address"]))

def search_contact():
    search_term = simpledialog.askstring("Search", "Enter name or phone number to search:")
    if search_term is None:
        return
    found_contacts = []
    for contact in contacts:
        if search_term.lower() in contact["name"].lower() or search_term == contact["phone"]:
            found_contacts.append(contact)
    if found_contacts:
        show_search_results(found_contacts)
    else:
        messagebox.showinfo("Search", "No contacts found.")

def show_search_results(results):
    result_window = tk.Toplevel(root)
    result_window.title("Search Results")
    result_window.geometry("600x400")
    result_window.config(bg=bg_color)
    
    result_label = tk.Label(result_window, text="Search Results", font=title_font, bg=bg_color)
    result_label.pack(pady=10)
    
    result_list = ttk.Treeview(result_window, columns=("Name", "Phone Number", "Email", "Address"), show="headings")
    result_list.heading("Name", text="Name")
    result_list.heading("Phone Number", text="Phone Number")
    result_list.heading("Email", text="Email")
    result_list.heading("Address", text="Address")
    
    for contact in results:
        result_list.insert("", tk.END, values=(contact["name"], contact["phone"], contact["email"], contact["address"]))
    
    result_list.pack(pady=20, fill=tk.BOTH, expand=True)

def update_contact():
    selected_contact = contact_list.selection()
    if not selected_contact:
        messagebox.showerror("Error", "Please select a contact to update.")
        return
    
    contact_info = contact_list.item(selected_contact)["values"]
    name = contact_info[0]
    new_phone = simpledialog.askstring("Input", f"Enter new phone number for {name}:", initialvalue=contact_info[1])
    if new_phone is None:
        return
    new_email = simpledialog.askstring("Input", f"Enter new email for {name}:", initialvalue=contact_info[2])
    if new_email is None:
        return
    new_address = simpledialog.askstring("Input", f"Enter new address for {name}:", initialvalue=contact_info[3])
    if new_address is None:
        return
    
    for contact in contacts:
        if contact["name"] == name:
            contact["phone"] = new_phone
            contact["email"] = new_email
            contact["address"] = new_address
    
    update_contact_list()

def delete_contact():
    selected_contact = contact_list.selection()
    if not selected_contact:
        messagebox.showerror("Error", "Please select a contact to delete.")
        return
    
    contact_info = contact_list.item(selected_contact)["values"]
    name = contact_info[0]
    
    for contact in contacts:
        if contact["name"] == name:
            contacts.remove(contact)
            break
    
    update_contact_list()

title_label = tk.Label(root, text="Contact Book", font=title_font, bg=bg_color, fg="black")
title_label.pack(pady=10)

button_frame = tk.Frame(root, bg=bg_color)
button_frame.pack(pady=10)

add_button = tk.Button(button_frame, text="Add Contact", command=add_contact, font=button_font, bg=button_color, fg="white", padx=10, pady=5)
add_button.grid(row=0, column=0, padx=10, pady=5)

view_button = tk.Button(button_frame, text="View Contacts", command=update_contact_list, font=button_font, bg=button_color, fg="white", padx=10, pady=5)
view_button.grid(row=0, column=1, padx=10, pady=5)

search_button = tk.Button(button_frame, text="Search Contact", command=search_contact, font=button_font, bg=button_color, fg="white", padx=10, pady=5)
search_button.grid(row=0, column=2, padx=10, pady=5)

update_delete_frame = tk.Frame(root, bg=bg_color)
update_delete_frame.pack(pady=10)

update_button = tk.Button(update_delete_frame, text="Update Contact", command=update_contact, font=button_font, bg=button_color, fg="white", padx=10, pady=5)
update_button.pack(side=tk.LEFT, padx=20)

delete_button = tk.Button(update_delete_frame, text="Delete Contact", command=delete_contact, font=button_font, bg=button_color, fg="white", padx=10, pady=5)
delete_button.pack(side=tk.RIGHT, padx=20)

columns = ("Name", "Phone Number", "Email", "Address")
contact_list = ttk.Treeview(root, columns=columns, show="headings", height=15, style="Treeview")
contact_list.heading("Name", text="Name")
contact_list.heading("Phone Number", text="Phone Number")
contact_list.heading("Email", text="Email")
contact_list.heading("Address", text="Address")
contact_list.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

root.mainloop()