import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
import mysql.connector
from tkcalendar import DateEntry
import re  

#for pdf view/create/print
import os
import platform
import subprocess
import fitz  # PyMuPDF
# import streamlit as st
from datetime import datetime
from tkinter import messagebox
from tkinter import PhotoImage
from PIL import Image, ImageTk
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
from reportlab.lib.pagesizes import letter

#for Date
from datetime import date
from tkcalendar import DateEntry
from datetime import date, datetime


class TransportManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Transport Management System")
        self.root.geometry("800x500")
        self.root.state('zoomed')

        self.create_topbar()  # Add top bar
        self.create_sidebar()  # Add side bar
        self.create_main_content()
        self.vehicle_submenu_visible = False
        self.driver_submenu_visible = False
        self.consignor_submenu_visible = False
        self.consignee_submenu_visible = False
        self.Destination_submenu_visible = False
        self.bill_submenu_visible = False
        self.tripsheet_submenu_visible = False
        

        # Save folders
        self.bill_folder = "F:/TMS_Bills"
        self.tripsheet_folder = "F:/TMS_Tripsheets"
        os.makedirs(self.bill_folder, exist_ok=True)
        os.makedirs(self.tripsheet_folder, exist_ok=True)

        #for view pdf
        self.current_pdf_doc = None
        self.current_page_index = 0
        self.current_pdf_image = None


    # database connection
    def connect_db(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Shivu@788197",
                database="demo_tms",
            )
            print("Database connected successfull!")
            return conn
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Error: {e}")
            return None
    
    #top bar
    def create_topbar(self):
        topbar = tk.Frame(self.root, bg="#1ABC9C", height=50)
        topbar.pack(side="top", fill="x")

        # Load and place the logo
        self.logo = PhotoImage(file="Logo BG5.png") 
        small_logo = self.logo.subsample(2, 2)
        logo_label = tk.Label(topbar, image=small_logo, bg="#1ABC9C")
        logo_label.image = small_logo
        logo_label.pack(side="left", padx=10, pady=5)

        # Transport company name
        transport_name = tk.Label(
            topbar,
            text="SHRI GURU TRANSPORT          ",
            font=("Bookman Old Style", 50, "bold"),
            fg="white",
            bg="#1ABC9C",
            anchor="center" )
        transport_name.place(y=10)
        transport_name.pack(pady=15)

        # || Shri Mahakooteshwar Prasanna ||
        god_name = tk.Label(topbar,
            text=" || Shri Mahakooteshwar Prasanna || ",
            font=("Georgia", 14, "bold"),fg="#730303",
            bg="#1ABC9C",anchor="center" )
        god_name.place(x=600, y=2) 
        

        god_name = tk.Label(topbar,
            text="H. O. : Moorusaviramath Compound,HUBBALLI-580028. \n Cell : 9916092013 / 9739050515 \n Subject to Hubli Jurisdiction ",
            font=("Georgia", 12, "bold"),fg="white",
            bg="#1ABC9C",anchor="center" )
        god_name.place(x=515, y=80)

        # Add GSTIN text below the main title
        gstin_label = tk.Label(
            topbar,
            text="GSTIN: 29AEDPH2195A1ZT",
            font=("Georgia", 14, "bold"),  # Smaller font size
            fg="Black",  # Same color as the main text
            bg="#1ABC9C")
        gstin_label.place(x=1200, y=110)  # Adjust the x and y values for proper positioning

    #side bar
    def create_sidebar(self):
        self.sidebar = tk.Frame(self.root, bg="#2C3E50", width=20000, height=50000)
        self.sidebar.pack(side="left", fill="y")


        title = tk.Label(self.sidebar, text="Transport\nManagement", font=("Georgia", 14, "bold"), fg="white", bg="#2C3E50")
        title.pack(pady=20)
        self.buttons = {}

        # Driver menu
        self.buttons["Driver"] = tk.Button(self.sidebar, text="🚚  Driver", font=("Georgia", 20), fg="white", bg="#34495E", relief="flat", anchor="w", padx=10, command=self.toggle_driver_submenu)
        self.buttons["Driver"].pack(fill="x", pady=5, padx=5)

        self.driver_submenu = tk.Frame(self.sidebar, bg="#34495E")
        self.driver_add_btn = tk.Button(self.driver_submenu, text="   ➕ Add Driver", font=("Georgia", 15), fg="white", bg="#2C3E50", relief="flat", anchor="w", padx=20, command=self.show_add_driver_section)
        self.driver_view_btn = tk.Button(self.driver_submenu, text="   📋 View Driver", font=("Georgia", 15), fg="white", bg="#2C3E50", relief="flat", anchor="w", padx=20, command=self.show_view_driver_section)

        # Vehicle menu
        self.buttons["Vehicle"] = tk.Button(self.sidebar, text="🚗  Vehicle", font=("Georgia", 20), fg="white", bg="#34495E", relief="flat", anchor="w", padx=10, command=self.toggle_vehicle_submenu)
        self.buttons["Vehicle"].pack(fill="x", pady=5, padx=5)

        self.vehicle_submenu = tk.Frame(self.sidebar, bg="#34495E")
        self.vehicle_add_btn = tk.Button(self.vehicle_submenu, text="   ➕ Add Vehicle", font=("Georgia", 15), fg="white", bg="#2C3E50", relief="flat", anchor="w", padx=20, command=self.show_add_vehicle_section)
        self.vehicle_view_btn = tk.Button(self.vehicle_submenu, text="   📋 View Vehicle", font=("Georgia", 15), fg="white", bg="#2C3E50", relief="flat", anchor="w", padx=20, command=self.show_view_vehicle_section)

        # Consignor menu
        self.buttons["Consignor"] = tk.Button(self.sidebar, text="📦  Consignor", font=("Georgia", 20), fg="white", bg="#34495E", relief="flat", anchor="w", padx=10, command=self.toggle_consignor_submenu)
        self.buttons["Consignor"].pack(fill="x", pady=5, padx=5)

        self.consignor_submenu = tk.Frame(self.sidebar, bg="#34495E")
        self.consignor_add_btn = tk.Button(self.consignor_submenu, text="   ➕ Add Consignor", font=("Georgia", 15), fg="white", bg="#2C3E50", relief="flat", anchor="w", padx=20, command=self.show_add_consignor_section)
        self.consignor_view_btn = tk.Button(self.consignor_submenu, text="   📋 View Consignor", font=("Georgia", 15), fg="white", bg="#2C3E50", relief="flat", anchor="w", padx=20, command=self.show_view_consignor_section)

        # Consignee menu
        self.buttons["Consignee"] = tk.Button(self.sidebar, text="📦  Consignee", font=("Georgia", 20), fg="white", bg="#34495E", relief="flat", anchor="w", padx=10, command=self.toggle_consignee_submenu)
        self.buttons["Consignee"].pack(fill="x", pady=5, padx=5)

        self.consignee_submenu = tk.Frame(self.sidebar, bg="#34495E")
        self.consignee_add_btn = tk.Button(self.consignee_submenu, text="   ➕ Add Consignee", font=("Georgia", 15), fg="white", bg="#2C3E50", relief="flat", anchor="w", padx=20, command=self.show_add_consignee_section)
        self.consignee_view_btn = tk.Button(self.consignee_submenu, text="   📋 View Consignee", font=("Georgia", 15), fg="white", bg="#2C3E50", relief="flat", anchor="w", padx=20, command=self.show_view_consignee_section)

        #Destination menu
        self.buttons["Destination"] = tk.Button(self.sidebar, text="⛳  Destination", font=("Georgia", 20), fg="white", bg="#34495E", relief="flat", anchor="w", padx=10, command=self.toggle_Destination_submenu)
        self.buttons["Destination"].pack(fill="x", pady=5, padx=5)

        self.Destination_submenu = tk.Frame(self.sidebar, bg="#34495E")
        self.Destination_add_btn = tk.Button(self.Destination_submenu, text="   ➕ Add Destination", font=("Georgia", 15), fg="white", bg="#2C3E50", relief="flat", anchor="w", padx=20, command=self.show_add_Destination_section)
        self.Destination_view_btn = tk.Button(self.Destination_submenu, text="   📋 View All Destination", font=("Georgia", 15), fg="white", bg="#2C3E50", relief="flat", anchor="w", padx=20, command=self.show_view_Destination_section)


        # Bill menu
        self.buttons["Bill"] = tk.Button(self.sidebar, text="🧾  Bill", font=("Georgia", 20), fg="white", bg="#34495E", relief="flat", anchor="w", padx=10, command=self.toggle_bill_submenu)
        self.buttons["Bill"].pack(fill="x", pady=5, padx=5)

        self.bill_submenu = tk.Frame(self.sidebar, bg="#34495E")
        self.bill_add_btn = tk.Button(self.bill_submenu, text="   ➕ Generate Bill", font=("Georgia", 15), fg="white", bg="#2C3E50", relief="flat", anchor="w", padx=20, command=self.show_add_bill_section)
        self.bill_view_btn = tk.Button(self.bill_submenu, text="   📋 View All Bills", font=("Georgia", 15), fg="white", bg="#2C3E50", relief="flat", anchor="w", padx=20, command=self.show_view_bill_section)
     
        # Add TripSheet button
        self.buttons["TripSheet"] = tk.Button(self.sidebar, text="📝  TripSheet", font=("Georgia", 20), fg="white", bg="#34495E", relief="flat", anchor="w", padx=10, command=self.toggle_tripsheet_submenu)
        self.buttons["TripSheet"].pack(fill="x", pady=5, padx=5)

        self.tripsheet_submenu = tk.Frame(self.sidebar, bg="#34495E")
        self.tripsheet_add_btn = tk.Button(self.tripsheet_submenu, text="   ➕ Create Trip", font=("Georgia", 15), fg="white", bg="#2C3E50", relief="flat", anchor="w", padx=20, command=self.show_add_tripsheet_section)
        self.tripsheet_view_btn = tk.Button(self.tripsheet_submenu, text="   📋 View All Trips", font=("Georgia", 15), fg="white", bg="#2C3E50", relief="flat", anchor="w", padx=20, command=self.show_view_tripsheet_section)
     
    #main content
    def create_main_content(self):
        self.main_frame = tk.Frame(self.root, bg="#ECF0F1")
        self.main_frame.pack(side="right", fill="both", expand=True)

        # Load and set the background image using Pillow
        try:
            self.background_image = Image.open("Logo BG5.png")  # Load the image
            self.background_image = ImageTk.PhotoImage(self.background_image)  # Convert to PhotoImage
        except Exception as e:
            print(f"Error loading image: {e}")
            return

        background_label = tk.Label(self.main_frame, image=self.background_image)
        background_label.place(relwidth=1, relheight=1)  
        
        self.welcome_label = tk.Label(self.main_frame, text="Welcome", font=("Times New Roman", 20, "bold"), bg="#ECF0F1")
        self.welcome_label.pack(pady=20)
        
        self.instruction_label = tk.Label(self.main_frame, text="🚀 Manage your transport operations with ease.\nChoose a module from the sidebar to get started.", font=("Georgia", 12), bg="white", padx=20, pady=10, relief="groove")
        self.instruction_label.pack(pady=10)

        # Footer Label
        footer_label = tk.Label(
            self.main_frame,
            text="© 2025 ——Developed by CBS Tech Squad",
            font=("Georgia", 9, "italic"),
            bg="#2C3E50",
            fg="white",
            pady=5
        )
        footer_label.pack(side="bottom", fill="x")

    def add_footer(self):
        footer_label = tk.Label(
            self.main_frame,
            text="© 2025  ——Developed by CBS Tech Squad",
            font=("Georgia", 9, "italic"),
            bg="#2C3E50",
            fg="white",
            pady=5
        )
        footer_label.pack(side="bottom", fill="x")

    # Toggle submenus starts!
    #Close all submenus.
    def close_all_submenus(self):
        if self.driver_submenu_visible:
            self.driver_submenu.pack_forget()
            self.driver_submenu_visible = False
        if self.vehicle_submenu_visible:
            self.vehicle_submenu.pack_forget()
            self.vehicle_submenu_visible = False
        if self.consignor_submenu_visible:
            self.consignor_submenu.pack_forget()
            self.consignor_submenu_visible = False
        if self.consignee_submenu_visible:
            self.consignee_submenu.pack_forget()
            self.consignee_submenu_visible = False
        if self.Destination_submenu_visible:
            self.Destination_submenu.pack_forget()
            self.Destination_submenu_visible = False
        if self.bill_submenu_visible:
            self.bill_submenu.pack_forget()
            self.bill_submenu_visible = False
        if self.tripsheet_submenu_visible:
            self.tripsheet_submenu.pack_forget()
            self.tripsheet_submenu_visible = False

    def toggle_driver_submenu(self):
        self.close_all_submenus()  # Close other submenus
        if not self.driver_submenu_visible:
            self.driver_submenu.pack(fill="x", padx=20, after=self.buttons["Driver"])
            self.driver_add_btn.pack(fill="x", pady=2)
            self.driver_view_btn.pack(fill="x", pady=2)
            self.driver_submenu_visible = True
       
    def toggle_vehicle_submenu(self):
        self.close_all_submenus()  # Close other submenus
        if not self.vehicle_submenu_visible:
            self.vehicle_submenu.pack(fill="x", padx=20, after=self.buttons["Vehicle"])
            self.vehicle_add_btn.pack(fill="x", pady=2)
            self.vehicle_view_btn.pack(fill="x", pady=2)
            self.vehicle_submenu_visible = True
        
    def toggle_consignor_submenu(self):
        self.close_all_submenus()  # Close other submenus
        if not self.consignor_submenu_visible:
            self.consignor_submenu.pack(fill="x", padx=20, after=self.buttons["Consignor"])
            self.consignor_add_btn.pack(fill="x", pady=2)
            self.consignor_view_btn.pack(fill="x", pady=2)
            self.consignor_submenu_visible = True

    def toggle_consignee_submenu(self):
        self.close_all_submenus()  # Close other submenus
        if not self.consignee_submenu_visible:
            self.consignee_submenu.pack(fill="x", padx=20, after=self.buttons["Consignee"])
            self.consignee_add_btn.pack(fill="x", pady=2)
            self.consignee_view_btn.pack(fill="x", pady=2)
            self.consignee_submenu_visible = True

    def toggle_Destination_submenu(self):
        self.close_all_submenus()  # Close other submenus
        if not self.Destination_submenu_visible:
            self.Destination_submenu.pack(fill="x", padx=20, after=self.buttons["Destination"])
            self.Destination_add_btn.pack(fill="x", pady=2)
            self.Destination_view_btn.pack(fill="x", pady=2)
            self.Destination_submenu_visible = True

    def toggle_bill_submenu(self):
        self.close_all_submenus()  # Close other submenus
        if not self.bill_submenu_visible:
            self.bill_submenu.pack(fill="x", padx=20, after=self.buttons["Bill"])
            self.bill_add_btn.pack(fill="x", pady=2)
            self.bill_view_btn.pack(fill="x", pady=2)
            self.bill_submenu_visible = True

    def toggle_tripsheet_submenu(self):
        self.close_all_submenus()  # Close other submenus
        if not self.tripsheet_submenu_visible:
            self.tripsheet_submenu.pack(fill="x", padx=20, after=self.buttons["TripSheet"])
            self.tripsheet_add_btn.pack(fill="x", pady=2)
            self.tripsheet_view_btn.pack(fill="x", pady=2)
            self.tripsheet_submenu_visible = True
    #Toggle submenus ends!


    # Driver section
    def show_add_driver_section(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        tk.Label(
            self.main_frame,
            text="👲  Add New Driver",
            font=("Georgia", 24, "bold"),
            bg="#ECF0F1",
            fg="#2C3E50"
        ).pack(pady=25)

        # Stylish card frame
        form_frame = tk.Frame(
            self.main_frame,
            bg="white",
            padx=40,
            pady=30,
            relief="ridge",
            bd=3
        )
        form_frame.pack(pady=10, padx=20)

        labels = ["Licence Number", "Name", "Contact Number", "Address"]
        entries = {}

        # Arrange in two columns
        for i, label in enumerate(labels):
            col = i % 2
            row = i // 2

            tk.Label(
                form_frame,
                text=label + " :",
                font=("Georgia", 13),
                bg="white",
                anchor="w"
            ).grid(row=row, column=col * 2, sticky="e", padx=(10, 5), pady=12)

            entry = tk.Entry(
                form_frame,
                font=("Georgia", 13),
                width=30,
                relief="groove",
                bd=2,
                highlightcolor="#1ABC9C",
                highlightthickness=1
            )
            entry.grid(row=row, column=col * 2 + 1, padx=(5, 15), pady=12)
            entries[label] = entry

        # Store entries as instance vars
        self.entry_L_no = entries["Licence Number"]
        self.entry_Name = entries["Name"]
        self.entry_C_no = entries["Contact Number"]
        self.entry_Address = entries["Address"]

        # Add button centered below
        button_frame = tk.Frame(self.main_frame, bg="#ECF0F1")
        button_frame.pack(pady=20)

        submit_btn = tk.Button(
            button_frame,
            text="➕ Add Driver",
            command=self.insert_into_driver,
            font=("Georgia", 14, "bold"),
            bg="#1ABC9C",
            fg="white",
            activebackground="#16A085",
            relief="raised",
            padx=25,
            pady=5
        )
        submit_btn.pack()
        self.add_footer()




    def insert_into_driver(self):
        Name = self.entry_Name.get().strip()
        L_no = self.entry_L_no.get().strip()
        C_no = self.entry_C_no.get().strip()
        Address = self.entry_Address.get().strip()

        if not all([Name, L_no, C_no, Address]):
            messagebox.showwarning("Input Error", "Please enter all fields.")
            return

        if len(L_no) != 16:
            messagebox.showwarning("Input Error", "Licence Number must be exactly 16 characters.")
            return

        if not C_no.startswith(('9', '8', '7', '6')):
            messagebox.showwarning("Input Error", "Contact number must start with 9, 8, 7, or 6.")
            return
        elif not C_no.isdigit() or len(C_no) != 10:
            messagebox.showwarning("Input Error", "Contact number must be exactly 10 digits.")
            return


        # Proceed to insert if validation passes
        conn = self.connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "INSERT INTO drivers (Driver_id, D_name, D_contact, D_address) VALUES (%s, %s, %s, %s)",
                    (L_no, Name, C_no, Address)
                )
                conn.commit()
                messagebox.showinfo("Success", "Driver added successfully!")
                self.clear_all_form_fields(self.main_frame)
                self.entry_L_no.focus_set()
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Error: {e}")
            finally:
                cursor.close()
                conn.close()


    def show_view_driver_section(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Title
        tk.Label(
            self.main_frame,
            text="📋 View All Registered Drivers",
            font=("Georgia", 26, "bold"),  # Increased font size
            bg="#ECF0F1",
            fg="#2C3E50"
        ).pack(pady=20)

        # Main card container
        card_frame = tk.Frame(self.main_frame, bg="white", bd=3, relief="ridge", padx=10, pady=10)
        card_frame.pack(padx=30, pady=10, fill="both", expand=True)

        # Left Panel — Table
        left_panel = tk.Frame(card_frame, bg="white")
        left_panel.pack(side="left", fill="both", expand=True)

        columns = ("Driver ID", "Name", "Contact", "Address")
        self.tree = ttk.Treeview(left_panel, columns=columns, show="headings")

        self.tree.heading("Driver ID", text="Driver ID")
        self.tree.column("Driver ID", anchor="center", width=220, stretch=tk.NO)
        self.tree.heading("Name", text="Name")
        self.tree.column("Name", anchor="center", width=250, stretch=tk.NO)
        self.tree.heading("Contact", text="Contact")
        self.tree.column("Contact", anchor="center", width=150, stretch=tk.NO)
        self.tree.heading("Address", text="Address")
        self.tree.column("Address", anchor="center", width=330, stretch=tk.NO)

        # Apply bigger row height and font
        style = ttk.Style()
        style.configure("Treeview", rowheight=28, font=("Georgia", 13))  # Increased font size
        style.configure("Treeview.Heading", font=("Georgia", 13, "bold"))

        scrollbar_y = ttk.Scrollbar(left_panel, orient="vertical", command=self.tree.yview)
        # scrollbar_x = ttk.Scrollbar(left_panel, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scrollbar_y.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar_y.pack(side="right", fill="y")
        # scrollbar_x.pack(side="bottom", fill="x")

        # Right Panel — Search
        right_panel = tk.Frame(card_frame, bg="white")
        right_panel.pack(side="right", fill="y", padx=20)

        tk.Label(right_panel, text="🔍 Search Drivers", font=("Georgia", 15, "bold"), bg="white").pack(pady=(5, 10))  # Bigger bold font

        self.search_var = tk.StringVar()
        search_entry = tk.Entry(right_panel, textvariable=self.search_var, font=("Georgia", 13), width=25, fg="gray")
        search_entry.insert(0, "Enter Name or License No")
        search_entry.pack()

        def on_focus_in(event):
            if search_entry.get() == "Enter Name or License No":
                search_entry.delete(0, tk.END)
                search_entry.config(fg="black")

        def on_focus_out(event):
            if not search_entry.get():
                search_entry.insert(0, "Enter Name or License No")
                search_entry.config(fg="gray")

        search_entry.bind("<FocusIn>", on_focus_in)
        search_entry.bind("<FocusOut>", on_focus_out)

        button_frame = tk.Frame(right_panel, bg="white")
        button_frame.pack(pady=15)

        tk.Button(button_frame, text="🔍 Search", font=("Georgia", 12), bg="#1ABC9C", fg="white", command=self.filter_driver_data).pack(pady=5, fill="x")
        tk.Button(button_frame, text="🔄 Reset", font=("Georgia", 12), bg="gray", fg="white", command=self.show_view_driver_section).pack(pady=5, fill="x")

        try:
            image = Image.open("Logo BG6.png")
            image = image.resize((180, 100), Image.Resampling.LANCZOS)
            logo_img = ImageTk.PhotoImage(image)
            logo_label = tk.Label(right_panel, image=logo_img, bg="white")
            logo_label.image = logo_img
            logo_label.pack(pady=10)
        except Exception as e:
            print(f"Error loading logo image: {e}")

        self.load_driver_data()
        self.add_footer()





    def load_driver_data(self):
        conn = self.connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM drivers")
            records = cursor.fetchall()
            cursor.close()
            conn.close()
    
            for row in self.tree.get_children():
                self.tree.delete(row)
    
            for row in records:
                self.tree.insert("", tk.END, values=row)
    
    def filter_driver_data(self):
        keyword = self.search_var.get().lower()
        conn = self.connect_db()
        if conn:
            cursor = conn.cursor()
            query = "SELECT * FROM drivers WHERE LOWER(Driver_id) LIKE %s OR LOWER(D_name) LIKE %s"
            cursor.execute(query, (f"%{keyword}%", f"%{keyword}%"))
            records = cursor.fetchall()
            cursor.close()
            conn.close()
    
            for row in self.tree.get_children():
                self.tree.delete(row)
    
            if records:
                for row in records:
                    self.tree.insert("", tk.END, values=row)
            else:
                messagebox.showinfo("No Results", "No matching drivers found.")


    # Vehicles section
    def show_add_vehicle_section(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Title
        tk.Label(
            self.main_frame,
            text="🚚  Add New Vehicle",
            font=("Georgia", 24, "bold"),
            bg="#ECF0F1",
            fg="#2C3E50"
        ).pack(pady=25)

        # Form container
        form_frame = tk.Frame(
            self.main_frame,
            bg="white",
            padx=40,
            pady=30,
            relief="ridge",
            bd=3
        )
        form_frame.pack(pady=10, padx=20)

        # Vehicle Number
        tk.Label(form_frame, text="Vehicle Number :", font=("Georgia", 13), bg="white").grid(row=0, column=0, sticky="e", padx=(10, 5), pady=12)
        self.entry_V_no = tk.Entry(form_frame, font=("Georgia", 13), width=30, relief="groove", bd=2, highlightcolor="#1ABC9C", highlightthickness=1)
        self.entry_V_no.grid(row=0, column=1, padx=(5, 15), pady=12)

        # Owner Name
        tk.Label(form_frame, text="Owner Name :", font=("Georgia", 13), bg="white").grid(row=0, column=2, sticky="e", padx=(10, 5), pady=12)
        self.entry_O_name = tk.Entry(form_frame, font=("Georgia", 13), width=30, relief="groove", bd=2, highlightcolor="#1ABC9C", highlightthickness=1)
        self.entry_O_name.grid(row=0, column=3, padx=(5, 15), pady=12)

        # Vehicle Type
        tk.Label(form_frame, text="Vehicle Type :", font=("Georgia", 13), bg="white").grid(row=1, column=0, sticky="e", padx=(10, 5), pady=12)
        self.vehicle_types = ["Select a Vehicle Type", "Intra", "Dost", "Bada Dost", "Mini Truck", "Lorry"]
        self.entry_V_type = ttk.Combobox(form_frame, values=self.vehicle_types, font=("Georgia", 13), width=28, state="readonly")
        self.entry_V_type.grid(row=1, column=1, padx=(5, 15), pady=12)
        self.entry_V_type.set(self.vehicle_types[0])

        # Add Button Centered
        button_frame = tk.Frame(self.main_frame, bg="#ECF0F1")
        button_frame.pack(pady=20)

        submit_btn = tk.Button(
            button_frame,
            text="➕ Add Vehicle",
            command=self.insert_into_vehicles,
            font=("Georgia", 14, "bold"),
            bg="#1ABC9C",
            fg="white",
            activebackground="#16A085",
            relief="raised",
            padx=25,
            pady=5
        )
        submit_btn.pack()
        self.add_footer()




    def insert_into_vehicles(self):
        V_no = self.entry_V_no.get().strip()
        O_name = self.entry_O_name.get().strip()
        V_type = self.entry_V_type.get().strip()

        if not all([V_no, O_name, V_type]):
            messagebox.showwarning("Input Error", "Please enter all fields.")
            return

        if len(V_no) != 10:
            messagebox.showwarning("Input Error", "Vehicle Number must be exactly 10 characters.")
            return

        if V_type == "Select a Vehicle Type":
            messagebox.showwarning("Input Error", "Please select a valid vehicle type.")
            return

        conn = self.connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO vehicles (vehicle_no, owner_name, vehicle_type) VALUES (%s, %s, %s)", 
                            (V_no, O_name, V_type))
                conn.commit()
                messagebox.showinfo("Success", "Vehicle added successfully!")
                self.clear_all_form_fields(self.main_frame)
                self.entry_V_no.focus_set()
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Error: {e}")
            finally:
                cursor.close()
                conn.close()



    def show_view_vehicle_section(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Title
        tk.Label(
            self.main_frame,
            text="🚗 List of All Registered Vehicles",
            font=("Georgia", 26, "bold"),
            bg="#ECF0F1",
            fg="#2C3E50"
        ).pack(pady=20)

        # Card-style container
        card_frame = tk.Frame(self.main_frame, bg="white", bd=3, relief="ridge", padx=15, pady=10)
        card_frame.pack(padx=30, pady=10, fill="both", expand=True)

        # Left Panel — Treeview
        # Left Panel — Treeview with scrollbars using grid (fixes alignment)
        left_panel = tk.Frame(card_frame, bg="white")
        left_panel.pack(side="left", fill="both", expand=True)

        # Treeview and Scrollbars (inside left_panel)
        columns = ("Vehicle Number", "Owner Name", "Vehicle Type")
        self.tree = ttk.Treeview(left_panel, columns=columns, show="headings", height=15)

        # Define column headers
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=180)

        # Apply style
        style = ttk.Style()
        style.configure("Treeview", font=("Georgia", 12), rowheight=28)
        style.configure("Treeview.Heading", font=("Georgia", 13, "bold"), background="#D5DBDB", foreground="black")

        # Scrollbars
        scrollbar_y = ttk.Scrollbar(left_panel, orient="vertical", command=self.tree.yview)
        # scrollbar_x = ttk.Scrollbar(left_panel, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scrollbar_y.set)

        # Pack Treeview and scrollbars (IMPORTANT: pack — not grid!)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar_y.pack(side="right", fill="y")
        # scrollbar_x.pack(side="bottom", fill="x")



        # Right Panel — Search + Image
        right_panel = tk.Frame(card_frame, bg="#F9F9F9", padx=10)
        right_panel.pack(side="right", fill="y")

        tk.Label(right_panel, text="🔍 Search Vehicles", font=("Georgia", 15, "bold"), bg="#F9F9F9").pack(pady=(5, 10))

        self.search_vehicle_var = tk.StringVar()
        search_entry = tk.Entry(right_panel, textvariable=self.search_vehicle_var, font=("Georgia", 13), width=25, fg="gray")
        search_entry.insert(0, "Enter Vehicle No or Owner Name")
        search_entry.pack()

        def on_focus_in(event):
            if search_entry.get() == "Enter Vehicle No or Owner Name":
                search_entry.delete(0, tk.END)
                search_entry.config(fg="black")

        def on_focus_out(event):
            if not search_entry.get():
                search_entry.insert(0, "Enter Vehicle No or Owner Name")
                search_entry.config(fg="gray")

        search_entry.bind("<FocusIn>", on_focus_in)
        search_entry.bind("<FocusOut>", on_focus_out)

        # Buttons
        button_frame = tk.Frame(right_panel, bg="#F9F9F9")
        button_frame.pack(pady=15)

        tk.Button(button_frame, text="🔍 Search", font=("Georgia", 12), bg="#1ABC9C", fg="white", command=self.filter_vehicle_data).pack(pady=5, fill="x")
        tk.Button(button_frame, text="🔄 Reset", font=("Georgia", 12), bg="gray", fg="white", command=self.show_view_vehicle_section).pack(pady=5, fill="x")

        # Image Below Search
        try:
            image = Image.open("Logo BG6.png")
            image = image.resize((180, 100), Image.Resampling.LANCZOS)
            logo_img = ImageTk.PhotoImage(image)
            logo_label = tk.Label(right_panel, image=logo_img, bg="#F9F9F9")
            logo_label.image = logo_img
            logo_label.pack(pady=10)
        except Exception as e:
            print(f"Error loading logo image: {e}")

        # Load data
        self.load_vehicle_data()
        self.add_footer()



    def load_vehicle_data(self):
        conn = self.connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM vehicles")
            records = cursor.fetchall()
            cursor.close()
            conn.close()

            for row in self.tree.get_children():
                self.tree.delete(row)

            for row in records:
                self.tree.insert("", tk.END, values=row)

    def filter_vehicle_data(self):
        keyword = self.search_vehicle_var.get().lower()
        conn = self.connect_db()
        if conn:
            cursor = conn.cursor()
            query = "SELECT * FROM vehicles WHERE LOWER(vehicle_no) LIKE %s OR LOWER(owner_name) LIKE %s"
            cursor.execute(query, (f"%{keyword}%", f"%{keyword}%"))
            records = cursor.fetchall()
            cursor.close()
            conn.close()

            for row in self.tree.get_children():
                self.tree.delete(row)

            if records:
                for row in records:
                    self.tree.insert("", tk.END, values=row)
            else:
                messagebox.showinfo("No Results", "No matching vehicles found.")


    # Consignor section
    def show_add_consignor_section(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Title
        tk.Label(
            self.main_frame,
            text="📦 Add New Consignor",
            font=("Georgia", 24, "bold"),
            bg="#ECF0F1",
            fg="#2C3E50"
        ).pack(pady=25)

        # Card-style form frame
        form_frame = tk.Frame(
            self.main_frame,
            bg="white",
            padx=40,
            pady=30,
            relief="ridge",
            bd=3
        )
        form_frame.pack(pady=10, padx=20)

        labels = ["Consignor Name", "Contact", "Address"]
        entries = {}

        for i, label in enumerate(labels):
            col = i % 2
            row = i // 2

            tk.Label(
                form_frame,
                text=label + " :",
                font=("Georgia", 13),
                bg="white",
                anchor="w"
            ).grid(row=row, column=col * 2, sticky="e", padx=(10, 5), pady=12)

            entry = tk.Entry(
                form_frame,
                font=("Georgia", 13),
                width=30,
                relief="groove",
                bd=2,
                highlightcolor="#1ABC9C",
                highlightthickness=1
            )
            entry.grid(row=row, column=col * 2 + 1, padx=(5, 15), pady=12)
            entries[label] = entry

        self.entry_Cnr_Name = entries["Consignor Name"]
        self.entry_C_no = entries["Contact"]

       # Fetch destination addresses in ascending order
        conn = self.connect_db()
        destinations = []
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT Destination FROM destination_p_rate ORDER BY Destination ASC")
            destinations = [row[0] for row in cursor.fetchall()]
            cursor.close()
            conn.close()

        # Row 1: Address : [Dropdown]
        tk.Label(form_frame, text="Address :", font=("Georgia", 13), bg="white").grid(
            row=1, column=0, sticky="e", padx=(10, 5), pady=12
        )
        address_combobox = ttk.Combobox(
            form_frame, values=destinations, font=("Georgia", 13), width=30, state="readonly"
        )
        address_combobox.grid(row=1, column=1, padx=(5, 15), pady=12)
        self.entry_address = address_combobox


        # Submit Button
        button_frame = tk.Frame(self.main_frame, bg="#ECF0F1")
        button_frame.pack(pady=20)

        submit_btn = tk.Button(
            button_frame,
            text="➕ Add Consignor",
            command=self.insert_into_consignor,
            font=("Georgia", 14, "bold"),
            bg="#1ABC9C",
            fg="white",
            activebackground="#16A085",
            relief="raised",
            padx=25,
            pady=5
        )
        submit_btn.pack()
        self.add_footer()


    def insert_into_consignor(self):
        Cnr_Name = self.entry_Cnr_Name.get().strip()
        C_no = self.entry_C_no.get().strip()
        Address = self.entry_address.get().strip()

        if not all([Cnr_Name, C_no, Address]):
            messagebox.showwarning("Input Error", "Please enter all fields.")
            return

        if not C_no.startswith(('9', '8', '7', '6')):
            messagebox.showwarning("Input Error", "Contact number must start with 9, 8, 7, or 6.")
            return
        elif not C_no.isdigit() or len(C_no) != 10:
            messagebox.showwarning("Input Error", "Contact number must be exactly 10 digits.")
            return


        conn = self.connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "INSERT INTO Consignor (consignor_name, contact, address) VALUES (%s, %s, %s)",
                    (Cnr_Name, C_no, Address)
                )
                conn.commit()
                messagebox.showinfo("Success", "Consignor added successfully!")
                self.clear_all_form_fields(self.main_frame)
                self.entry_Cnr_Name.focus_set()
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Error: {e}")
            finally:
                cursor.close()
                conn.close()


    def show_view_consignor_section(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        tk.Label(
            self.main_frame,
            text="📋 View All Registered Consignors",
            font=("Georgia", 26, "bold"),
            bg="#ECF0F1",
            fg="#2C3E50"
        ).pack(pady=20)

        card_frame = tk.Frame(self.main_frame, bg="white", bd=3, relief="ridge", padx=15, pady=10)
        card_frame.pack(padx=30, pady=10, fill="both", expand=True)

        # Left Panel — Table
        left_panel = tk.Frame(card_frame, bg="white")
        left_panel.pack(side="left", fill="both", expand=True)

        columns = ("Name", "Contact", "Address")
        self.tree = ttk.Treeview(left_panel, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=180)

        style = ttk.Style()
        style.configure("Treeview", font=("Georgia", 12), rowheight=28)
        style.configure("Treeview.Heading", font=("Georgia", 13, "bold"))

        scrollbar_y = ttk.Scrollbar(left_panel, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_y.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar_y.pack(side="right", fill="y")

        # Right Panel — Search & Image
        right_panel = tk.Frame(card_frame, bg="#F9F9F9", padx=10)
        right_panel.pack(side="right", fill="y")

        tk.Label(right_panel, text="🔍 Search Consignors", font=("Georgia", 15, "bold"), bg="#F9F9F9").pack(pady=(5, 10))

        self.search_consignor_var = tk.StringVar()
        search_entry = tk.Entry(right_panel, textvariable=self.search_consignor_var, font=("Georgia", 13), width=25, fg="gray")
        search_entry.insert(0, "Enter Name or Contact")
        search_entry.pack(pady=(0, 10))

        def on_focus_in(event):
            if search_entry.get() == "Enter Name or Contact":
                search_entry.delete(0, tk.END)
                search_entry.config(fg="black")

        def on_focus_out(event):
            if not search_entry.get():
                search_entry.insert(0, "Enter Name or Contact")
                search_entry.config(fg="gray")

        search_entry.bind("<FocusIn>", on_focus_in)
        search_entry.bind("<FocusOut>", on_focus_out)

        button_frame = tk.Frame(right_panel, bg="#F9F9F9")
        button_frame.pack(pady=(0, 15))

        tk.Button(button_frame, text="🔍 Search", font=("Georgia", 11), bg="#1ABC9C", fg="white", command=self.filter_consignor_data).pack(pady=3, fill="x")
        tk.Button(button_frame, text="🔄 Reset", font=("Georgia", 11), bg="gray", fg="white", command=self.show_view_consignor_section).pack(pady=3, fill="x")

        try:
            image = Image.open("Logo BG6.png")
            image = image.resize((180, 100), Image.Resampling.LANCZOS)
            logo_img = ImageTk.PhotoImage(image)
            logo_label = tk.Label(right_panel, image=logo_img, bg="#F9F9F9")
            logo_label.image = logo_img
            logo_label.pack(pady=5)
        except Exception as e:
            print(f"Error loading logo image: {e}")

        self.load_consignor_data()
        self.add_footer()



    def load_consignor_data(self):
        conn = self.connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM consignor")
            records = cursor.fetchall()
            cursor.close()
            conn.close()

            for row in self.tree.get_children():
                self.tree.delete(row)

            for row in records:
                self.tree.insert("", tk.END, values=row)

    def filter_consignor_data(self):
        keyword = self.search_consignor_var.get().lower()
        conn = self.connect_db()
        if conn:
            cursor = conn.cursor()
            query = "SELECT * FROM consignor WHERE LOWER(consignor_name) LIKE %s OR LOWER(contact) LIKE %s"
            cursor.execute(query, (f"%{keyword}%", f"%{keyword}%"))
            records = cursor.fetchall()
            cursor.close()
            conn.close()

            for row in self.tree.get_children():
                self.tree.delete(row)

            if records:
                for row in records:
                    self.tree.insert("", tk.END, values=row)
            else:
                messagebox.showinfo("No Results", "No matching consignors found.")


    # Consignee section
    def show_add_consignee_section(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Title
        tk.Label(
            self.main_frame,
            text="📦 Add New Consignee",
            font=("Georgia", 24, "bold"),
            bg="#ECF0F1",
            fg="#2C3E50"
        ).pack(pady=25)

        # Card-style frame
        form_frame = tk.Frame(
            self.main_frame,
            bg="white",
            padx=40,
            pady=30,
            relief="ridge",
            bd=3
        )
        form_frame.pack(pady=10, padx=20)

        labels = ["Consignee Name", "Contact"]
        entries = {}

        for i, label in enumerate(labels):
            col = i % 2
            row = i // 2

            tk.Label(
                form_frame,
                text=label + " :",
                font=("Georgia", 13),
                bg="white",
                anchor="w"
            ).grid(row=row, column=col * 2, sticky="e", padx=(10, 5), pady=12)

            entry = tk.Entry(
                form_frame,
                font=("Georgia", 13),
                width=30,
                relief="groove",
                bd=2,
                highlightcolor="#1ABC9C",
                highlightthickness=1
            )
            entry.grid(row=row, column=col * 2 + 1, padx=(5, 15), pady=12)
            entries[label] = entry

        # Store as instance variables
        self.entry_Cne_Name = entries["Consignee Name"]
        self.entry_C_no = entries["Contact"]

        # Fetch destination addresses in ascending order
        conn = self.connect_db()
        destinations = []
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT Destination FROM destination_p_rate ORDER BY Destination ASC")
            destinations = [row[0] for row in cursor.fetchall()]
            cursor.close()
            conn.close()

        # Row 1: Address in column 0, Dropdown in column 1
        tk.Label(form_frame, text="Address :", font=("Georgia", 13), bg="white").grid(
            row=1, column=0, sticky="e", padx=(10, 5), pady=12
        )
        address_combobox = ttk.Combobox(
            form_frame, values=destinations, font=("Georgia", 13), width=30, state="readonly"
        )
        address_combobox.grid(row=1, column=1, padx=(5, 15), pady=12)
        self.entry_address = address_combobox


        # Submit Button
        button_frame = tk.Frame(self.main_frame, bg="#ECF0F1")
        button_frame.pack(pady=20)

        submit_btn = tk.Button(
            button_frame,
            text="➕ Add Consignee",
            command=self.insert_into_consignee,
            font=("Georgia", 14, "bold"),
            bg="#1ABC9C",
            fg="white",
            activebackground="#16A085",
            relief="raised",
            padx=25,
            pady=5
        )
        submit_btn.pack()

        #Footer
        self.add_footer()


    def insert_into_consignee(self):
        Cne_Name = self.entry_Cne_Name.get().strip()
        C_no = self.entry_C_no.get().strip()
        Address = self.entry_address.get().strip()

        if not all([Cne_Name, C_no, Address]):
            messagebox.showwarning("Input Error", "Please enter all fields.")
            return

        if not C_no.startswith(('9', '8', '7', '6')):
            messagebox.showwarning("Input Error", "Contact number must start with 9, 8, 7, or 6.")
            return
        elif not C_no.isdigit() or len(C_no) != 10:
            messagebox.showwarning("Input Error", "Contact number must be exactly 10 digits.")
            return


        conn = self.connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "INSERT INTO Consignee (consignee_name, contact, address) VALUES (%s, %s, %s)",
                    (Cne_Name, C_no, Address)
                )
                conn.commit()
                messagebox.showinfo("Success", "Consignee added successfully!")
                self.clear_all_form_fields(self.main_frame)
                self.entry_Cne_Name.focus_set()
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Error: {e}")
            finally:
                cursor.close()
                conn.close()


    def show_view_consignee_section(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        tk.Label(
            self.main_frame,
            text="📋 View All Registered Consignees",
            font=("Georgia", 26, "bold"),
            bg="#ECF0F1",
            fg="#2C3E50"
        ).pack(pady=20)

        card_frame = tk.Frame(self.main_frame, bg="white", bd=3, relief="ridge", padx=15, pady=10)
        card_frame.pack(padx=30, pady=10, fill="both", expand=True)

        # Left Panel — Table
        left_panel = tk.Frame(card_frame, bg="white")
        left_panel.pack(side="left", fill="both", expand=True)

        columns = ("Name", "Contact", "Address")
        self.tree = ttk.Treeview(left_panel, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=180)

        style = ttk.Style()
        style.configure("Treeview", font=("Georgia", 12), rowheight=28)
        style.configure("Treeview.Heading", font=("Georgia", 13, "bold"))

        scrollbar_y = ttk.Scrollbar(left_panel, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_y.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar_y.pack(side="right", fill="y")

        # Right Panel — Search & Image
        right_panel = tk.Frame(card_frame, bg="#F9F9F9", padx=10)
        right_panel.pack(side="right", fill="y")

        tk.Label(right_panel, text="🔍 Search Consignees", font=("Georgia", 15, "bold"), bg="#F9F9F9").pack(pady=(5, 10))

        self.search_consignee_var = tk.StringVar()
        search_entry = tk.Entry(right_panel, textvariable=self.search_consignee_var, font=("Georgia", 13), width=25, fg="gray")
        search_entry.insert(0, "Enter Name or Contact")
        search_entry.pack(pady=(0, 10))

        def on_focus_in(event):
            if search_entry.get() == "Enter Name or Contact":
                search_entry.delete(0, tk.END)
                search_entry.config(fg="black")

        def on_focus_out(event):
            if not search_entry.get():
                search_entry.insert(0, "Enter Name or Contact")
                search_entry.config(fg="gray")

        search_entry.bind("<FocusIn>", on_focus_in)
        search_entry.bind("<FocusOut>", on_focus_out)

        button_frame = tk.Frame(right_panel, bg="#F9F9F9")
        button_frame.pack(pady=(0, 15))

        tk.Button(button_frame, text="🔍 Search", font=("Georgia", 11), bg="#1ABC9C", fg="white", command=self.filter_consignee_data).pack(pady=3, fill="x")
        tk.Button(button_frame, text="🔄 Reset", font=("Georgia", 11), bg="gray", fg="white", command=self.show_view_consignee_section).pack(pady=3, fill="x")

        try:
            image = Image.open("Logo BG6.png")
            image = image.resize((180, 100), Image.Resampling.LANCZOS)
            logo_img = ImageTk.PhotoImage(image)
            logo_label = tk.Label(right_panel, image=logo_img, bg="#F9F9F9")
            logo_label.image = logo_img
            logo_label.pack(pady=5)
        except Exception as e:
            print(f"Error loading logo image: {e}")

        self.load_consignee_data()
        self.add_footer()


    def load_consignee_data(self):
        conn = self.connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM consignee")
            records = cursor.fetchall()
            cursor.close()
            conn.close()

            for row in self.tree.get_children():
                self.tree.delete(row)

            for row in records:
                self.tree.insert("", tk.END, values=row)

    def filter_consignee_data(self):
        keyword = self.search_consignee_var.get().lower()
        conn = self.connect_db()
        if conn:
            cursor = conn.cursor()
            query = "SELECT * FROM consignee WHERE LOWER(consignee_name) LIKE %s OR LOWER(contact) LIKE %s"
            cursor.execute(query, (f"%{keyword}%", f"%{keyword}%"))
            records = cursor.fetchall()
            cursor.close()
            conn.close()

            for row in self.tree.get_children():
                self.tree.delete(row)

            if records:
                for row in records:
                    self.tree.insert("", tk.END, values=row)
            else:
                messagebox.showinfo("No Results", "No matching consignees found.")


    #Destination
    def show_add_Destination_section(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        tk.Label(self.main_frame,
                text="⛳ Add New Destination",
                font=("Georgia", 24, "bold"),
                bg="#ECF0F1",
                fg="#2C3E50").pack(pady=25)

        form_frame = tk.Frame(self.main_frame, bg="white", padx=40, pady=30, relief="ridge", bd=3)
        form_frame.pack(pady=10, padx=20)

        tk.Label(form_frame, text="Destination Name :", font=("Georgia", 13), bg="white").grid(row=0, column=0, sticky="e", padx=(10, 5), pady=12)
        self.entry_Dest_Name = tk.Entry(form_frame, font=("Georgia", 13), width=30, relief="groove", bd=2)
        self.entry_Dest_Name.grid(row=0, column=1, padx=(5, 15), pady=12)

        tk.Label(form_frame, text="Rate (₹/kg) :", font=("Georgia", 13), bg="white").grid(row=1, column=0, sticky="e", padx=(10, 5), pady=12)
        self.entry_Dest_Rate = tk.Entry(form_frame, font=("Georgia", 13), width=30, relief="groove", bd=2)
        self.entry_Dest_Rate.grid(row=1, column=1, padx=(5, 15), pady=12)

        button_frame = tk.Frame(self.main_frame, bg="#ECF0F1")
        button_frame.pack(pady=20)
        submit_btn = tk.Button(button_frame,
            text="➕ Add Destination",
            command=self.insert_into_Destination,
            font=("Georgia", 14, "bold"),
            bg="#1ABC9C",
            fg="white",
            padx=25,
            pady=5)
        
        submit_btn.pack()
        self.add_footer()
    


    def insert_into_Destination(self):
        dest = self.entry_Dest_Name.get().strip()
        rate = self.entry_Dest_Rate.get().strip()

        if not dest or not rate:
            messagebox.showwarning("Input Error", "Please enter all fields.")
            return

        try:
            rate = float(rate)
        except:
            messagebox.showwarning("Input Error", "Rate must be a number.")
            return

        conn = self.connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO destination_p_rate (Destination, Rate) VALUES (%s, %s)", (dest, rate))
                conn.commit()
                messagebox.showinfo("Success", "Destination added successfully!")
                self.clear_all_form_fields(self.main_frame)
                self.entry_Dest_Name.focus_set()
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Database Error: {e}")
            finally:
                cursor.close()
                conn.close()

    def show_view_Destination_section(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        tk.Label(
            self.main_frame,
            text="📋 View All Destinations",
            font=("Georgia", 26, "bold"),
            bg="#ECF0F1",
            fg="#2C3E50"
        ).pack(pady=20)

        # Card frame
        card_frame = tk.Frame(self.main_frame, bg="white", bd=3, relief="ridge", padx=15, pady=10)
        card_frame.pack(padx=30, pady=10, fill="both", expand=True)

        # Left Panel: Table
        left_panel = tk.Frame(card_frame, bg="white")
        left_panel.pack(side="left", fill="both", expand=True)

        columns = ("Destination", "Rate / 1Kg.")
        self.tree = ttk.Treeview(left_panel, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=200)

        style = ttk.Style()
        style.configure("Treeview", font=("Georgia", 12), rowheight=28)
        style.configure("Treeview.Heading", font=("Georgia", 13, "bold"))

        scrollbar_y = ttk.Scrollbar(left_panel, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_y.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar_y.pack(side="right", fill="y")

        # Right Panel: Search & Logo
        right_panel = tk.Frame(card_frame, bg="#F9F9F9", padx=10)
        right_panel.pack(side="right", fill="y")

        tk.Label(right_panel, text="🔍 Search Destinations", font=("Georgia", 15, "bold"), bg="#F9F9F9").pack(pady=(5, 10))

        self.search_destination_var = tk.StringVar()
        search_entry = tk.Entry(right_panel, textvariable=self.search_destination_var, font=("Georgia", 13), width=25, fg="gray")
        search_entry.insert(0, "Enter Destination Name")
        search_entry.pack(pady=(0, 10))

        def on_focus_in(event):
            if search_entry.get() == "Enter Destination Name":
                search_entry.delete(0, tk.END)
                search_entry.config(fg="black")

        def on_focus_out(event):
            if not search_entry.get():
                search_entry.insert(0, "Enter Destination Name")
                search_entry.config(fg="gray")

        search_entry.bind("<FocusIn>", on_focus_in)
        search_entry.bind("<FocusOut>", on_focus_out)

        button_frame = tk.Frame(right_panel, bg="#F9F9F9")
        button_frame.pack(pady=(0, 15))

        tk.Button(button_frame, text="🔍 Search", font=("Georgia", 11), bg="#1ABC9C", fg="white", command=self.filter_destination_data).pack(pady=3, fill="x")
        tk.Button(button_frame, text="🔄 Reset", font=("Georgia", 11), bg="gray", fg="white", command=self.show_view_Destination_section).pack(pady=3, fill="x")

        try:
            image = Image.open("Logo BG6.png")
            image = image.resize((180, 100), Image.Resampling.LANCZOS)
            logo_img = ImageTk.PhotoImage(image)
            logo_label = tk.Label(right_panel, image=logo_img, bg="#F9F9F9")
            logo_label.image = logo_img
            logo_label.pack(pady=5)
        except Exception as e:
            print(f"Error loading logo image: {e}")

        self.load_Destination_data()
        self.add_footer()

    def filter_destination_data(self):
        keyword = self.search_destination_var.get().lower()
        conn = self.connect_db()
        if conn:
            cursor = conn.cursor()
            query = "SELECT * FROM destination_p_rate WHERE LOWER(Destination) LIKE %s"
            cursor.execute(query, (f"%{keyword}%",))
            records = cursor.fetchall()
            cursor.close()
            conn.close()

            for row in self.tree.get_children():
                self.tree.delete(row)

            if records:
                for row in records:
                    self.tree.insert("", tk.END, values=row)
            else:
                messagebox.showinfo("No Results", "No matching destinations found.")


    def load_Destination_data(self):
        conn = self.connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT Destination, Rate FROM destination_p_rate")
            records = cursor.fetchall()
            cursor.close()
            conn.close()

            for row in self.tree.get_children():
                self.tree.delete(row)

            for row in records:
                self.tree.insert("", tk.END, values=row)


    # Bill section
    def show_add_bill_section(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        tk.Label(
            self.main_frame,
            text="🧾 Add New Bill",
            font=("Georgia", 24, "bold"),
            bg="#ECF0F1",
            fg="#2C3E50"
        ).pack(pady=25)

        form_frame = tk.Frame(self.main_frame, bg="white", padx=40, pady=30, relief="ridge", bd=3)
        form_frame.pack(pady=10, padx=20)

        # Date
        tk.Label(form_frame, text="Date :", font=("Georgia", 13), bg="white").grid(row=0, column=0, sticky="e", padx=(10, 5), pady=10)
        self.entry_Date = DateEntry(form_frame, font=("Georgia", 13), width=28, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy', maxdate=date.today())
        self.entry_Date.set_date(date.today())
        self.entry_Date.grid(row=0, column=1, padx=(5, 15), pady=10)

        # Consignor
        self.consignor_contact_name_map = {}
        self.consignee_contact_name_map = {}
        conn = self.connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT contact, consignor_name FROM consignor")
            for contact, name in cursor.fetchall():
                self.consignor_contact_name_map[contact] = name
            cursor.execute("SELECT contact, consignee_name FROM consignee")
            for contact, name in cursor.fetchall():
                self.consignee_contact_name_map[contact] = name
            cursor.close()
            conn.close()

        tk.Label(form_frame, text="Consignor Contact :", font=("Georgia", 13), bg="white").grid(row=1, column=0, sticky="e", padx=(10, 5), pady=10)
        self.entry_Cnr_no = ttk.Combobox(form_frame, font=("Georgia", 13), width=28, state="normal")
        self.entry_Cnr_no['values'] = list(self.consignor_contact_name_map.keys())
        self.entry_Cnr_no.grid(row=1, column=1, padx=(5, 15), pady=10)
        self.entry_Cnr_no.bind("<<ComboboxSelected>>", lambda e: self.fill_consignor_name(entries))
        self.entry_Cnr_no.bind("<FocusOut>", lambda e: self.fill_consignor_name(entries))

        tk.Label(form_frame, text="Consignor Name :", font=("Georgia", 13), bg="white").grid(row=1, column=2, sticky="e", padx=(10, 5), pady=10)
        self.entry_Cnr_Name = tk.Entry(form_frame, font=("Georgia", 13), width=30, relief="groove", bd=2)
        self.entry_Cnr_Name.grid(row=1, column=3, padx=(5, 15), pady=10)

        # Consignee
        tk.Label(form_frame, text="Consignee Contact :", font=("Georgia", 13), bg="white").grid(row=2, column=0, sticky="e", padx=(10, 5), pady=10)
        self.entry_Cne_no = ttk.Combobox(form_frame, font=("Georgia", 13), width=28, state="normal")
        self.entry_Cne_no['values'] = list(self.consignee_contact_name_map.keys())
        self.entry_Cne_no.grid(row=2, column=1, padx=(5, 15), pady=10)
        self.entry_Cne_no.bind("<<ComboboxSelected>>", lambda e: self.fill_consignee_name(entries))
        self.entry_Cne_no.bind("<FocusOut>", lambda e: self.fill_consignee_name(entries))

        tk.Label(form_frame, text="Consignee Name :", font=("Georgia", 13), bg="white").grid(row=2, column=2, sticky="e", padx=(10, 5), pady=10)
        self.entry_Cne_Name = tk.Entry(form_frame, font=("Georgia", 13), width=30, relief="groove", bd=2)
        self.entry_Cne_Name.grid(row=2, column=3, padx=(5, 15), pady=10)

        # Destination
        tk.Label(form_frame, text="Destination :", font=("Georgia", 13), bg="white").grid(row=3, column=0, sticky="e", padx=(10, 5), pady=10)
        destination_values = []
        conn = self.connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT Destination FROM destination_p_rate")
            destination_values = [row[0] for row in cursor.fetchall()]
            cursor.close()
            conn.close()
        self.entry_Destination = ttk.Combobox(form_frame, values=destination_values, font=("Georgia", 13), width=28, state="readonly")
        self.entry_Destination.grid(row=3, column=1, padx=(5, 15), pady=10)

        # No. of Article beside Destination
        tk.Label(form_frame, text="No. of Article :", font=("Georgia", 13), bg="white").grid(row=3, column=2, sticky="e", padx=(10, 5), pady=10)
        self.entry_No_Articl = tk.Entry(form_frame, font=("Georgia", 13), width=30, relief="groove", bd=2)
        self.entry_No_Articl.grid(row=3, column=3, padx=(5, 15), pady=10)

        # Weight below Destination
        tk.Label(form_frame, text="Weight :", font=("Georgia", 13), bg="white").grid(row=4, column=0, sticky="e", padx=(10, 5), pady=10)
        self.entry_Weight = tk.Entry(form_frame, font=("Georgia", 13), width=30, relief="groove", bd=2)
        self.entry_Weight.grid(row=4, column=1, padx=(5, 15), pady=10)

        # Payment Status below Weight
        tk.Label(form_frame, text="Payment Status :", font=("Georgia", 13), bg="white").grid(row=5, column=0, sticky="e", padx=(10, 5), pady=10)
        self.entry_P_Status = ttk.Combobox(form_frame, values=["Paid", "Unpaid"], font=("Georgia", 13), width=28, state="readonly")
        self.entry_P_Status.grid(row=5, column=1, padx=(5, 15), pady=10)

        # Set default weight to 50
        self.entry_Weight.insert(0, "50")

        # Bind events to auto-calculate
        self.entry_Weight.bind("<FocusOut>", lambda e: self.calculate_total_amount())
        self.entry_Destination.bind("<<ComboboxSelected>>", lambda e: self.calculate_total_amount())


        # Article & Total Amount side by side below Consignee
        tk.Label(form_frame, text="Article :", font=("Georgia", 13), bg="white").grid(row=4, column=2, sticky="e", padx=(10, 5), pady=10)
        self.entry_Articl = tk.Entry(form_frame, font=("Georgia", 13), width=30, relief="groove", bd=2)
        self.entry_Articl.grid(row=4, column=3, padx=(5, 15), pady=10)

        tk.Label(form_frame, text="Total Amount :", font=("Georgia", 13), bg="white").grid(row=5, column=2, sticky="e", padx=(10, 5), pady=10)
        self.entry_T_Amount = tk.Entry(form_frame, font=("Georgia", 13), width=30, relief="groove", bd=2)
        self.entry_T_Amount.grid(row=5, column=3, padx=(5, 15), pady=10)


        # Charges Breakdown (Read-only dropdown for display only)
        # Charges Applied (Display only)
        tk.Label(form_frame, text="Charges Applied :", font=("Georgia", 13), bg="white").grid(row=6, column=0, sticky="e", padx=(10, 5), pady=10)

        self.charges_applied = ttk.Combobox(form_frame, font=("Georgia", 13), width=50, state="readonly")
        self.charges_applied.grid(row=6, column=1, columnspan=3, padx=(5, 15), pady=10)
        self.charges_applied.set("Enter weight & destination to calculate")


        # Submit Button
        button_frame = tk.Frame(self.main_frame, bg="#ECF0F1")
        button_frame.pack(pady=20)
        submit_btn = tk.Button(
            button_frame,
            text="✅ Submit Bill",
            command=self.insert_into_bills,
            font=("Georgia", 14, "bold"),
            bg="#1ABC9C",
            fg="white",
            activebackground="#16A085",
            relief="raised",
            padx=30,
            pady=6
        )
        submit_btn.pack()

        self.add_footer()

        # Needed for name auto-fill
        entries = {
            "Consignor Name": self.entry_Cnr_Name,
            "Consignee Name": self.entry_Cne_Name
        }


    def calculate_total_amount(self):
        try:
            destination = self.entry_Destination.get()
            weight_str = self.entry_Weight.get()
            weight = float(weight_str)

            # Ensure minimum weight
            weight = max(weight, 50)

            conn = self.connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT Rate FROM destination_p_rate WHERE Destination = %s", (destination,))
                result = cursor.fetchone()
                cursor.close()
                conn.close()

                if result:
                    rate = float(result[0])
                    service_charge = 10.00
                    base_amount = weight * rate
                    total = base_amount + service_charge

                    # Set total amount field
                    self.entry_T_Amount.delete(0, tk.END)
                    self.entry_T_Amount.insert(0, f"{total:.2f}")

                    # Set charges display in correct format
                    self.charges_applied['values'] = [
                        f"{weight} KG × ₹{rate} = ₹{base_amount:.2f} + S.T. Charge (₹10) = ₹{total:.2f}"
                    ]
                    self.charges_applied.set(self.charges_applied['values'][0])
                else:
                    self.entry_T_Amount.delete(0, tk.END)
                    self.entry_T_Amount.insert(0, "0.00")
                    self.charges_applied.set("Rate not found for selected destination.")
        except Exception as e:
            print("Calculation error:", e)


    def fill_consignor_name(self, entries):
        contact = self.entry_Cnr_no.get().strip()
        name = self.consignor_contact_name_map.get(contact, "")
        if name:
            entries["Consignor Name"].delete(0, tk.END)
            entries["Consignor Name"].insert(0, name)

    def fill_consignee_name(self, entries):
        contact = self.entry_Cne_no.get().strip()
        name = self.consignee_contact_name_map.get(contact, "")
        if name:
            entries["Consignee Name"].delete(0, tk.END)
            entries["Consignee Name"].insert(0, name)


    def insert_into_bills(self):
        Date = self.entry_Date.get()
        Cnr_Name = self.entry_Cnr_Name.get()
        Cnr_no = self.entry_Cnr_no.get()
        Cne_Name = self.entry_Cne_Name.get()
        Cne_no = self.entry_Cne_no.get()
        No_Articl = self.entry_No_Articl.get()
        Articl = self.entry_Articl.get()
        Weight = self.entry_Weight.get()
        Destination = self.entry_Destination.get()
        T_Amount = self.entry_T_Amount.get()
        P_Status = self.entry_P_Status.get()
        
        try:
            Date_obj = datetime.strptime(Date, "%d/%m/%Y")
            Date = Date_obj.strftime("%Y-%m-%d")  # for DB
        except ValueError:
            messagebox.showerror("Invalid Date", "Please enter the date in dd/mm/yyyy format.")
            return


        if Date and Cnr_Name and Cnr_no and Cne_Name and Cne_no and No_Articl and Articl and Weight and Destination and T_Amount and P_Status:
            conn = self.connect_db()
            if conn:
                cursor = conn.cursor()
                try:
                    cursor.execute("INSERT INTO bill_details (date,consignor_name,consignor_contact,consignee_name,consignee_contact," \
                    "No_Articles,article,product_weight,destination,total_amount,payments) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                    (Date,Cnr_Name,Cnr_no,Cne_Name,Cne_no,No_Articl,Articl,Weight,Destination,T_Amount,P_Status))
                    conn.commit()
                    messagebox.showinfo("Success", "Bill Detailes added successfully!")
                    self.clear_all_form_fields(self.main_frame)
                    self.entry_Cnr_no.focus_set()
                    
                except mysql.connector.Error as e:
                    messagebox.showerror("Error", f"Error: {e}")
                finally:
                    cursor.close()
                    conn.close()
        else:
            messagebox.showwarning("Input Error", "Please enter all fields.")
            

    def clear_all_form_fields(self, parent_frame):
        for widget in parent_frame.winfo_children():
            if isinstance(widget, tk.Entry):
                widget.delete(0, tk.END)

            elif isinstance(widget, ttk.Combobox):
                try:
                    # Clear only the selection — values stay
                    widget.set("")
                except Exception as e:
                    print(f"Combobox clear failed: {e}")

            elif isinstance(widget, DateEntry):
                try:
                    widget.set_date(date.today())
                except Exception as e:
                    print(f"DateEntry reset failed: {e}")

            elif isinstance(widget, tk.Text):
                widget.delete("1.0", tk.END)

            elif isinstance(widget, tk.Frame):
                self.clear_all_form_fields(widget)



    def show_view_bill_section(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        top_frame = tk.Frame(self.main_frame, bg="#ECF0F1")
        top_frame.pack(fill="x", pady=10, padx=10)

        tk.Label(top_frame, text="🧾 List of All Bills", font=("Georgia", 24, "bold"), bg="#ECF0F1", fg="#2C3E50").pack(side="left", padx=10)

        search_frame = tk.Frame(top_frame, bg="#ECF0F1")
        search_frame.pack(side="right")

        self.search_bill_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.search_bill_var, font=("Georgia", 12), width=30, fg="gray")
        search_entry.insert(0, "Enter Bill No ")
        search_entry.grid(row=0, column=0, padx=(0, 5))

        search_entry.bind("<FocusIn>", lambda e: (search_entry.delete(0, tk.END), search_entry.config(fg="black")) if search_entry.get() == "Enter Bill No " else None)
        search_entry.bind("<FocusOut>", lambda e: (search_entry.insert(0, "Enter Bill No"), search_entry.config(fg="gray")) if not search_entry.get() else None)

        tk.Button(search_frame, text="🔍", font=("Georgia", 12), bg="#1ABC9C", fg="white", command=self.filter_bill_data).grid(row=0, column=1, padx=(0, 5))
        tk.Button(search_frame, text="Reset", font=("Georgia", 11), bg="gray", fg="white", command=self.show_view_bill_section).grid(row=0, column=2)

        tree_frame = tk.Frame(self.main_frame, bg="white")
        tree_frame.pack(padx=20, fill="both", expand=True)

        style = ttk.Style()
        style.configure("Bill.Treeview", font=("Georgia", 9), rowheight=28)
        style.configure("Bill.Treeview.Heading", font=("Georgia", 11, "bold"))

        columns = ("Bill No.", "Date", "Consignor", "Consignee","No. Article", "Article",
                    "Weight", "Destination","Total Amt", "Paid/ToPay", "Trip Status")


        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", style="Bill.Treeview")

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        tree.column("Bill No.", width=60)
        tree.column("Date", width=80)
        tree.column("Consignor", width=200)
        tree.column("Consignee", width=200)
        tree.column("No. Article", width=70)
        tree.column("Weight", width=70)
        tree.column("Total Amt", width=75)
        tree.column("Trip Status", width=90)
        tree.column("Paid/ToPay", width=90)

        scrollbar_y = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        scrollbar_x = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        tree.grid(row=0, column=0, sticky="nsew")
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        scrollbar_x.grid(row=1, column=0, sticky="ew")

        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        self.tree = tree  # if used by PDF/print functions
        self.load_bill_data()

        button_frame = tk.Frame(self.main_frame, bg="white")
        button_frame.pack(pady=10)

        # tk.Button(button_frame, text="Generate PDF for Selected", font=("Georgia", 12), bg="#1ABC9C", fg="white", command=self.generate_selected_pdf).pack(side="left", padx=10)
        tk.Button(button_frame, text="🖨️ Print Bill", font=("Georgia", 12), bg="#1ABC9C", fg="white", command=self.open_print_options).pack(side="left", padx=10)
        tk.Button(button_frame, text="👁️ View Bill", font=("Georgia", 12), bg="#1ABC9C", fg="white", command=self.open_selected_pdf_view).pack(side="left", padx=10)

        self.add_footer()


    def open_print_options(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Select Bill", "Please select a bill to print.")
            return

        values = self.tree.item(selected, 'values')
        bill_data = {
            "Bill_no": values[0],
            "Date": values[1],
            "Consignor": values[2],
            #"ConsignorContact": values[3],
            "Consignee": values[3],
            #"ConsigneeContact": values[5],
            "NoArticles": values[4],
            "Article": values[5],
            "Weight": values[6],
            "Destination": values[7],
            "Amount": values[8],
         }
        

        print_dialog = tk.Toplevel(self.root)
        print_dialog.title("Print Bill Copies")
        print_dialog.geometry("350x250")
        print_dialog.grab_set()
        print_dialog.configure(bg="#ECF0F1")

        tk.Label(print_dialog, text="Select the copies you want to print", font=("Georgia", 12, "bold"), bg="#ECF0F1", fg="#2C3E50").pack(pady=10)

        # Create checkbox variables
        self.print_driver_var = tk.BooleanVar(value=True)
        self.print_consignee_var = tk.BooleanVar(value=True)
        self.print_consignor_var = tk.BooleanVar()
        self.print_ho_var = tk.BooleanVar()

        # Add checkboxes
        tk.Checkbutton(print_dialog, text="Driver Copy", variable=self.print_driver_var, font=("Georgia", 11), bg="#ECF0F1").pack(anchor="w", padx=30)
        tk.Checkbutton(print_dialog, text="Consignee Copy", variable=self.print_consignee_var, font=("Georgia", 11), bg="#ECF0F1").pack(anchor="w", padx=30)
        tk.Checkbutton(print_dialog, text="Consignor Copy", variable=self.print_consignor_var, font=("Georgia", 11), bg="#ECF0F1").pack(anchor="w", padx=30)
        tk.Checkbutton(print_dialog, text="H.O. Copy", variable=self.print_ho_var, font=("Georgia", 11), bg="#ECF0F1").pack(anchor="w", padx=30)

        # Print button
        tk.Button(
            print_dialog,
            text="🖨️ Print Now",
            font=("Georgia", 12, "bold"),
            bg="#1ABC9C",
            fg="white",
            command=lambda: [print_dialog.destroy(), self.generate_bill_pdf(bill_data)]
        ).pack(pady=15)



    def load_bill_data(self):
        conn = self.connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                    SELECT 
                        bill_number,
                        date,
                        CONCAT(consignor_name, ' (', consignor_contact, ')') AS consignor,
                        CONCAT(consignee_name, ' (', consignee_contact, ')') AS consignee,
                        No_Articles,
                        article,
                        product_weight,
                        destination,
                        total_amount,
                        payments,
                        trip_status
                    FROM bill_details
                    ORDER BY 
                        CASE WHEN trip_status = 'Unplanned' THEN 0 ELSE 1 END,
                        bill_number DESC
                """)
            
            records = cursor.fetchall()
            cursor.close()
            conn.close()

            for row in self.tree.get_children():
                self.tree.delete(row)

            for row in records:
                self.tree.insert("", tk.END, values=row)

    def filter_bill_data(self):
        keyword = self.search_bill_var.get()

        if not keyword:
            messagebox.showwarning("Input Required", "Please enter a Bill Number to search.")
            return

        conn = self.connect_db()
        if conn:
            cursor = conn.cursor()
            query = "SELECT * FROM bill_details WHERE CAST(bill_number AS CHAR) LIKE %s"
            like_keyword = f"%{keyword}%"

            try:
                cursor.execute(query, (like_keyword,))
                records = cursor.fetchall()
                cursor.close()
                conn.close()

                for row in self.tree.get_children():
                    self.tree.delete(row)

                if records:
                    for row in records:
                        self.tree.insert("", tk.END, values=row)
                else:
                    messagebox.showinfo("No Results", f"No bill found with Bill No containing: {keyword}")

            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"MySQL error: {e}")

    def parse_bill_row_data(self, row_data):
        return [
            row_data[0],  # Bill No
            row_data[1],  # Date
            row_data[2].split(' (')[0],  # Consignor Name
            row_data[2].split(' (')[1][:-1],  # Consignor Contact
            row_data[3].split(' (')[0],  # Consignee Name
            row_data[3].split(' (')[1][:-1],  # Consignee Contact
            row_data[4],  # No. of Articles
            row_data[5],  # Article
            row_data[6],  # Weight
            row_data[7],  # Destination
            row_data[8],  # Total Amount
            row_data[9],  # Payment Status
            row_data[10]  # Trip Status
        ]


    def generate_bill_pdf(self, bill_data):
        bill_number = bill_data['Bill_no']
        date = datetime.strptime(bill_data['Date'], "%Y-%m-%d").strftime("%d/%m/%Y")
        
        filename = os.path.join(self.bill_folder, f"Bill_{bill_number}.pdf")

        logo_filename = "Logo balck.png"
        pdf_path = os.path.join(os.getcwd(), filename)
        c = canvas.Canvas(pdf_path, pagesize=letter)
        width, height = letter

        def draw_single_copy(c, logo_filename, label, y_offset):
            top = height - y_offset

            # Logo
            try:
                c.drawImage(logo_filename, 0.3 * inch, top - 0.8 * inch - 0.5 * inch, width=1.5 * inch, height=1 * inch, mask='auto')
            except:
                pass

            # Header
            c.setFont("Helvetica-Bold", 10)
            c.drawString(3.05 * inch, top - 0.4 * inch, "|| Shri Mahakooteshwar Prasanna ||")
            c.setFont("Times-Bold", 28)
            c.drawString(2.25 * inch, top - 0.8 * inch, "Shri  Guru  Transport")
            c.setFont("Helvetica", 10)
            c.drawString(2.4 * inch, top - 1.03 * inch, "H. O. : Moorusaviramath Compound,HUBBALLI-580028.")
            c.setFont("Helvetica-Bold", 10)
            c.drawString(0.3 * inch, top - 1.4 * inch, "GST No. : 29AEDPH2195A1ZT")
            c.setFont("Helvetica", 10)
            c.drawString(3.35 * inch, top - 1.4 * inch, "Subject to Hubli Jurisdiction")
            c.drawString(3.2 * inch, top - 1.2 * inch, "Cell : 9916092013 / 9739050515")

            # Bill Info
            c.setFont("Helvetica-Bold", 14)
            c.drawString(6.6 * inch, top - 0.6 * inch, "Bill No: ")
            c.drawString(7.4 * inch, top - 0.6 * inch, str(bill_number))
            c.drawString(6.6 * inch, top - 0.9 * inch, label)
            c.drawString(6.6 * inch, top - 1.2 * inch, 'Date:')
            c.drawString(7.2 * inch, top - 1.2 * inch, date)

            # Separator
            c.line(0.5 * inch, top - 1.5 * inch, 8 * inch, top - 1.5 * inch)

            # From/To
            c.drawString(0.8 * inch, top - 1.8 * inch, "From : HUBBALLI")
            c.drawString(2.8 * inch, top - 1.8 * inch, '"BOOKED AT OWNERS RISK"')
            c.drawString(6 * inch, top - 1.8 * inch, f"To : {bill_data['Destination']}")

            # Parties
            c.setFont("Helvetica", 10)
            c.drawString(0.6 * inch, top - 2.1 * inch, f"Consignor : {bill_data['Consignor']}")
            c.drawString(4.6 * inch, top - 2.1 * inch, f"Consignee : {bill_data['Consignee']}")
            c.drawString(0.6 * inch, top - 2.4 * inch, "GST No: _____________")
            c.drawString(4.6 * inch, top - 2.4 * inch, "GST No: _____________")

            # Table
            table_x = 0.5 * inch
            table_y = top - 2.5 * inch
            row_height = 0.28 * inch
            col_widths = [3 * inch, 2.5 * inch, 2 * inch]

            headers = [f"                            Description", "                     Particulars", "                 Amount"]
            y = table_y
            for col_idx, header in enumerate(headers):
                x = table_x + sum(col_widths[:col_idx])
                c.setFont("Helvetica-Bold", 10)
                c.rect(x, y, col_widths[col_idx], -row_height, stroke=1, fill=0)
                c.drawString(x + 4, y - row_height + 8, header)

            merged_rows = 5
            merged_height = row_height * merged_rows

            # Draw merged description cell
            c.rect(table_x, y - row_height, col_widths[0], -merged_height, stroke=1, fill=0)
            
            # Insert article info into description cell
            article_info = f"\n       → No. of Articles: {bill_data['NoArticles']}\n\n              - {bill_data['Article']}\n\n       → Weight: {bill_data['Weight']} kg"
            text_obj = c.beginText()
            text_obj.setTextOrigin(table_x + 5, y - row_height - 12)
            text_obj.setFont("Helvetica", 9)
            for line in article_info.split('\n'):
                text_obj.textLine(line)
            c.drawText(text_obj)


            c.setFont("Helvetica", 10)
            merged_rows = 5
            merged_height = row_height * merged_rows
            c.rect(table_x, y - row_height, col_widths[0], -merged_height, stroke=1, fill=0)

            particulars = ["Freight", "S T charge:", "GST", "Other", "Total"]

            amount = float(bill_data['Amount'])
            values = [ amount - 10, "10.00", ":_______", ":_______", amount ]


            for i, item in enumerate(particulars):
                row_y = y - row_height * (i + 1)
                x1 = table_x + col_widths[0]
                c.rect(x1, row_y, col_widths[1], -row_height, stroke=1, fill=0)
                c.drawString(x1 + 4, row_y - row_height + 5, item)
                x2 = x1 + col_widths[1]
                c.rect(x2, row_y, col_widths[2], -row_height, stroke=1, fill=0)
                c.drawString(x2 + 4, row_y - row_height + 5, str(values[i]))

            # Footer
            c.drawString(0.5 * inch, top - 4.3 * inch, "*Received the Consignment in good condition")
            c.drawString(1 * inch, top - 4.55 * inch, "Consignor Sign:")
            c.drawString(4 * inch, top - 4.55 * inch, "Consignee Sign:")
            c.drawString(6.2 * inch, top - 4.55 * inch, "Signature of Booking Clerk")
            c.line(0.5 * inch, top - 4.8 * inch, 8 * inch, top - 4.8 * inch)
            c.setFont("Helvetica", 9)
            c.drawString(0.6 * inch, top - 4.92 * inch, "Note:   Thereby agree to the terms and conditions.  & Loading and Unloading by Party")
            c.setStrokeColor(colors.grey)
            c.rect(0.2 * inch, top - 5.3 * inch, width - 0.4 * inch, 5.1 * inch)

        # Page-wise drawing
        # Choose copies based on logic
        labels = []

        if hasattr(self, 'print_driver_var') and self.print_driver_var.get():
            labels.append("Driver Copy")
        if hasattr(self, 'print_consignee_var') and self.print_consignee_var.get():
            labels.append("Consignee Copy")
        if hasattr(self, 'print_consignor_var') and self.print_consignor_var.get():
            labels.append("Consignor Copy")
        if hasattr(self, 'print_ho_var') and self.print_ho_var.get():
            labels.append("H.O. Copy")


        # labels = ["Driver Copy", "Consignor Copy", "Consignee Copy", "H.O. Copy"]
        offsets = [0, height / 2]
        for i in range(0, len(labels), 2):
            draw_single_copy(c, logo_filename, labels[i], offsets[0])
            if i + 1 < len(labels):
                draw_single_copy(c, logo_filename, labels[i + 1], offsets[1])
            c.showPage()


        c.save()
        messagebox.showinfo("PDF Generated", f"PDF generated successfully: {filename}")
        os.startfile(filename)



    #Print Bill Directly
    def print_selected_bill(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No selection", "Please select a bill to print.")
            return

        item = self.tree.item(selected_item)
        bill_data = self.parse_bill_row_data(item['values'])
        bill_number = bill_data['Bill_no']
        pdf_filename = f"Bill_{bill_number}.pdf"
        pdf_path = os.path.abspath(pdf_filename)

        # Step 1: Generate PDF
        self.generate_bill_pdf(bill_data)

        # Step 2: Open PDF file with default viewer (which shows the Print UI like your image)
        try:
            if platform.system() == "Windows":
                os.startfile(pdf_path)  # This opens with default viewer
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", pdf_path])
            elif platform.system() == "Linux":
                subprocess.run(["xdg-open", pdf_path])
            else:
                messagebox.showerror("Unsupported OS", "Cannot open PDF: OS not supported.")
        except Exception as e:
            messagebox.showerror("Error Opening PDF", f"Error:\n{e}")




    def generate_selected_pdf(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a bill to generate PDF.")
            return

        row_data = self.tree.item(selected[0])["values"]
        bill_data = self.parse_bill_row_data(row_data)
        self.generate_bill_pdf(bill_data)




    # TripSheet section
    def show_add_tripsheet_section(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Section Heading
        # Section Heading
        tk.Label(
            self.main_frame,
            text="📝  Create New Trip",
            font=("Georgia", 24, "bold"),
            bg="#ECF0F1",
            fg="#2C3E50"
        ).pack(pady=25)

        # Card-style horizontal layout for inputs
        form_frame = tk.Frame(
            self.main_frame,
            bg="white",
            padx=30,
            pady=20,
            relief="ridge",
            bd=3
        )
        form_frame.pack(pady=10, padx=20, fill="x")

        # Trip Date
        tk.Label(form_frame, text="Trip Date :", font=("Georgia", 13), bg="white").grid(row=0, column=0, padx=(10, 5), pady=10, sticky="e")
        self.trip_date = tk.StringVar(value=datetime.today().strftime("%d/%m/%Y"))
        tk.Entry(form_frame, textvariable=self.trip_date, font=("Georgia", 13), width=20, state="readonly", relief="groove", bd=2).grid(row=0, column=1, padx=(0, 20), pady=10)

        # Vehicle No
        tk.Label(form_frame, text="Vehicle Number :", font=("Georgia", 13), bg="white").grid(row=0, column=2, padx=(10, 5), pady=10, sticky="e")
        self.vehicle_var = tk.StringVar()
        self.vehicle_dropdown = ttk.Combobox(form_frame, textvariable=self.vehicle_var, font=("Georgia", 13), width=18, state="readonly")
        self.vehicle_dropdown.grid(row=0, column=3, padx=(0, 20), pady=10)

        # Driver ID
       # Driver Licence Entry (ComboBox with manual typing allowed)
        tk.Label(form_frame, text="Driver Licence No :", font=("Georgia", 13), bg="white").grid(row=0, column=4, padx=(10, 5), pady=10, sticky="e")

        self.driver_var = tk.StringVar()
        self.driver_dropdown = ttk.Combobox(form_frame, textvariable=self.driver_var, font=("Georgia", 13), width=30, state="normal")
        self.driver_dropdown.grid(row=0, column=5, padx=(5, 15), pady=10)

        # Populate dropdown with Driver IDs
        conn = self.connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT Driver_id FROM drivers")
            self.driver_dropdown['values'] = [row[0] for row in cursor.fetchall()]
            cursor.close()
            conn.close()

        # Load dropdown options
        self.load_vehicle_and_driver_options()


        # Bills Selection Area
        tk.Label(self.main_frame, text="Select Bills for Trip", font=("Georgia", 14, "bold"), bg="#ECF0F1").pack(pady=5)
        tree_frame = tk.Frame(self.main_frame)
        tree_frame.pack(pady=10, padx=20, fill="both", expand=True)

        columns = ("Bill No", "Date", "Consignor", "Consignee", "Destination", "No. of Articles", "Articles", "Weight", "Amount", "Payment Status")
        style = ttk.Style()
        style.configure("TripCreate.Treeview", font=("Georgia", 13), rowheight=28)
        style.configure("TripCreate.Treeview.Heading", font=("Georgia", 13, "bold"))

        self.bills_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", style="TripCreate.Treeview")
        for col in columns:
            self.bills_tree.heading(col, text=col)
            self.bills_tree.column(col, width=100)
        self.bills_tree.column("Bill No", width=20 )
        self.bills_tree.column("Date", width=30)
        self.bills_tree.column("Amount", width=40)
        self.bills_tree.column("Payment Status", width=20)
        self.bills_tree.column("No. of Articles", width=15)
        self.bills_tree.column("Articles", width=90)
        self.bills_tree.column("Weight", width=40)


        self.bills_tree.pack(fill="both", expand=True)

        self.load_available_bills()

        # Submit Button
        tk.Button(self.main_frame, text="Create Trip", bg="#1ABC9C", fg="white", font=("Georgia", 12), command=self.save_trip).pack(pady=10)
        #If error add .pack(pady=10) to below line and uncomment it
        tk.Button(self.main_frame,text="Create Trip",font=("Georgia", 12),bg="#1ABC9C",fg="white",command=self.create_trip_in_db)
    
        #Footer
        self.add_footer()


    def create_trip_in_db(self):

        raw_date = self.trip_date.get()
        try:
            # Expecting dd/mm/yyyy input
            trip_date_obj = datetime.strptime(raw_date, "%d/%m/%Y")
            trip_date = trip_date_obj.strftime("%Y-%m-%d")  # MySQL-friendly format
        except ValueError:
            messagebox.showerror("Invalid Date", "Please enter the Trip Date in dd/mm/yyyy format.")
            return

        vehicle_no = self.vehicle_var.get()
        driver_id = self.driver_var.get()
        selected_items = self.bills_tree.selection()

        if not (trip_date and vehicle_no and driver_id and selected_items):
            messagebox.showwarning("Missing Data", "Please fill all fields and select at least one bill.")
            return

        conn = self.connect_db()
        if conn:
            try:
                cursor = conn.cursor()
                print("Inserting trip:", trip_date, vehicle_no, driver_id)  # Debugging line

                # ✅ Step 1: Insert into tripsheet
                cursor.execute(
                    "INSERT INTO tripsheet (trip_date, vehicle_no, driver_id) VALUES (%s, %s, %s)",
                    (trip_date, vehicle_no, driver_id)
                )
                trip_id = cursor.lastrowid

                # ✅ Step 2: Link bills to the trip
                for item in selected_items:
                    bill_number = self.bills_tree.item(item, "values")[0]
                    cursor.execute(
                        "INSERT INTO trip_bills (trip_id, bill_number) VALUES (%s, %s)",
                        (trip_id, bill_number)
                    )

                conn.commit()
                messagebox.showinfo("Success", f"Trip #{trip_id} created with {len(selected_items)} bills.")
                self.show_view_tripsheet_section()

            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", f"Error: {e}")
            finally:
                cursor.close()
                conn.close()


    def load_vehicle_and_driver_options(self):
        conn = self.connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT vehicle_no FROM vehicles")
            vehicles = [row[0] for row in cursor.fetchall()]
            cursor.execute("SELECT Driver_id FROM drivers")
            drivers = [row[0] for row in cursor.fetchall()]
            cursor.close()
            conn.close()

            self.vehicle_dropdown['values'] = vehicles
            self.driver_dropdown['values'] = drivers

    def load_available_bills(self):
        conn = self.connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""SELECT 
                                bill_number, date, 
                                consignor_name, consignee_name, 
                                destination, No_Articles, article,
                                product_weight, total_amount, payments
                            FROM bill_details
                            WHERE trip_status = 'Unplanned'
                            ORDER BY bill_number DESC
                        """)


            for row in cursor.fetchall():
                row = list(row)
                try:
                    row[1] = datetime.strptime(row[1], "%Y-%m-%d").strftime("%d/%m/%Y")
                except:
                    pass
                self.bills_tree.insert("", tk.END, values=row)


            cursor.close()
            conn.close()

    def generate_tripsheet_pdf(self, trip_id):
        conn = self.connect_db()
        if not conn:
            return

        cursor = conn.cursor()
        try:
            # Fetch trip details
            cursor.execute("""
                SELECT ts.trip_id, ts.trip_date, ts.vehicle_no, ts.driver_id, d.D_name
                FROM tripsheet ts
                JOIN drivers d ON ts.driver_id = d.Driver_id
                WHERE ts.trip_id = %s
            """, (trip_id,))
            trip = cursor.fetchone()

            # Fetch associated bills
            # Fetch associated bills with additional fields
            cursor.execute("""
                SELECT bd.bill_number, bd.date, bd.consignor_name, bd.consignee_name, bd.No_Articles, bd.article,
                    bd.product_weight, bd.destination, bd.total_amount, bd.payments
                FROM trip_bills tb
                JOIN bill_details bd ON tb.bill_number = bd.bill_number
                WHERE tb.trip_id = %s
            """, (trip_id,))
            bills = cursor.fetchall()


            if not trip or not bills:
                messagebox.showerror("Data Error", "Trip data not found.")
                return


            filename = os.path.join(self.tripsheet_folder, f"Tripsheet_{trip_id}.pdf")


            logo_path = "Logo balck.png"
            c = canvas.Canvas(filename, pagesize=A4)
            width, height = A4

            def draw_header():
                top = height  # full page height
                logo_filename = "Logo balck.png"

                # Logo
                try:
                    c.drawImage(logo_filename, 0.3 * inch, top - 0.8 * inch - 0.5 * inch, width=1.5 * inch, height=1 * inch, mask='auto')
                except:
                    pass

                # Header text
                c.setFont("Helvetica-Bold", 10)
                c.drawString(3.05 * inch, top - 0.4 * inch, "|| Shri Mahakooteshwar Prasanna ||")

                c.setFont("Times-Bold", 28)
                c.drawString(2.25 * inch, top - 0.8 * inch, "Shri  Guru  Transport")

                c.setFont("Helvetica", 10)
                c.drawString(2.4 * inch, top - 1.03 * inch, "H. O. : Moorusaviramath Compound,HUBBALLI-580028.")

                c.setFont("Helvetica-Bold", 10)
                c.drawString(0.3 * inch, top - 1.4 * inch, "GST No. : 29AEDPH2195A1ZT")

                c.setFont("Helvetica", 10)
                c.drawString(3.35 * inch, top - 1.4 * inch, "Subject to Hubli Jurisdiction")
                c.drawString(3.2 * inch, top - 1.2 * inch, "Cell : 9916092013 / 9739050515")
                

            def draw_trip_info():
                y = height - 0.7 * inch
                y1 = height - 1.0 * inch
                y2 = height - 1.73 * inch
                c.setFont("Helvetica-Bold", 12)
                c.drawString(480, y, f"Trip ID: {trip[0]}")
                trip_date_formatted = trip[1].strftime("%d/%m/%Y")
                c.drawString(460, y1, f"Date: {trip_date_formatted}")
                c.drawString(50, y2, f"Vehicle No: {trip[2]}")
                c.drawString(350, y2, f"Driver: {trip[4]} ({trip[3]})")


            def draw_table_header(start_y):
                c.setFont("Helvetica-Bold", 9)
                c.drawString(20, start_y, "Bill No")
                c.drawString(55, start_y, "Bill Date")
                c.drawString(105, start_y, "Consignor")
                c.drawString(195, start_y, "Consignee")
                c.drawString(270, start_y, "No.Arti.")
                c.drawString(310, start_y, "Article")
                c.drawString(380, start_y, "Dest.")
                c.drawString(440, start_y, "Weight")
                c.drawString(490, start_y, "Amount")
                c.drawString(540, start_y, "Payment")
                c.line(20, start_y - 2, width - 20, start_y - 2)
                c.line(20, start_y + 8.8, width - 20, start_y + 8.8)
                c.line(20, start_y + 38, width - 20, start_y + 38)



            def draw_footer():
                c.setFont("Helvetica", 9)
                c.drawString(40, 30, "Note: Ensure loading/unloading is done by party. Subject to Hubli jurisdiction.")
                c.setStrokeColor(colors.grey)
                c.rect(15, 10, width - 30, height - 20)

            # Page drawing
            y = height - 2 * inch
            draw_header()
            draw_trip_info()
            draw_table_header(y)
            y -= 20

            c.setFont("Helvetica", 8)
            serial = 1

            for bill in bills:
                if y < 60:
                    draw_footer()
                    c.showPage()
                    y = height - 2 * inch
                    draw_header()
                    draw_trip_info()
                    draw_table_header(y)
                    y -= 20
                    c.setFont("Helvetica", 8)

            for bill in bills:
                c.drawString(20, y, str(bill[0]))                             # Bill No
                c.drawString(55, y, bill[1].strftime("%d-%m-%Y"))            # Date
                c.drawString(105, y, str(bill[2] or "N/A"))                   # Consignor
                c.drawString(190, y, str(bill[3] or "N/A"))                   # Consignee
                c.drawString(285, y, str(bill[4] or "1"))                   # No.Articles
                c.drawString(310, y, str(bill[5] or "N/A"))                   # Article
                c.drawString(380, y, str(bill[7] or "N/A"))                   # Destination
                c.drawString(450, y, str(bill[6] or "0"))                     # Weight
                c.drawString(490, y, str(bill[8] or "0.00"))                  # Amount
                c.drawString(540, y, str(bill[9] or "N/A"))                   # Payment

                y -= 18
                serial += 1


            draw_footer()
            c.save()
            messagebox.showinfo("PDF Generated", f"Trip sheet saved as {filename}")

        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Error: {e}")
        finally:
            cursor.close()
            conn.close()

    
    def ask_and_generate_tripsheet_pdf(self):

        trip_id = simpledialog.askinteger("Enter Trip ID", "Please enter the Trip ID to generate PDF:")
        if trip_id is not None:
            self.generate_tripsheet_pdf(trip_id)



    def save_trip(self):
        trip_date = self.trip_date.get()
        trip_date_raw = self.trip_date.get()
        try:
            trip_date_obj = datetime.strptime(trip_date_raw, "%d/%m/%Y")
            trip_date = trip_date_obj.strftime("%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Date Error", "Invalid trip date format. Please use dd/mm/yyyy.")
            return

        vehicle_no = self.vehicle_var.get()
        driver_id = self.driver_var.get()
        selected = self.bills_tree.selection()

        if not (trip_date and vehicle_no and driver_id and selected):
            messagebox.showwarning("Missing Data", "All fields and at least one bill must be selected.")
            return

        conn = self.connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                # Step 1: Insert the trip and get trip_id
                cursor.execute("""
                    INSERT INTO tripsheet (trip_date, vehicle_no, driver_id)
                    VALUES (%s, %s, %s)
                """, (trip_date, vehicle_no, driver_id))
                trip_id = cursor.lastrowid

                # Step 2: Link each selected bill
                for item in selected:
                    bill_number = self.bills_tree.item(item, "values")[0]
                    cursor.execute("""
                        INSERT INTO trip_bills (trip_id, bill_number)
                        VALUES (%s, %s)
                    """, (trip_id, bill_number))
                    cursor.execute("""
                        UPDATE bill_details
                        SET trip_status = 'Planned'
                        WHERE bill_number = %s
                    """, (bill_number,))

                conn.commit()

                # ✅ Now trip_id is defined, call PDF generator
                self.generate_tripsheet_pdf(trip_id)

                messagebox.showinfo("Success", f"Trip #{trip_id} created with {len(selected)} bills.")
                self.show_view_tripsheet_section()

            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", f"Error: {e}")
            finally:
                cursor.close()
                conn.close()

    def insert_into_tripsheet(self):
        trip_date = self.entry_Trip_Date.get()
        bill_number = self.entry_Bill_Number.get()
        driver_id = self.entry_Driver_ID.get()
        vehicle_no = self.entry_Vehicle_No.get()

        if trip_date and bill_number and driver_id and vehicle_no:
            conn = self.connect_db()
            if conn:
                cursor = conn.cursor()
                try:
                    cursor.execute("""
                        INSERT INTO tripsheet (trip_date, bill_number, driver_id, vehicle_no)
                        VALUES (%s, %s, %s, %s)
                    """, (trip_date, bill_number, driver_id, vehicle_no))
                    conn.commit()
                    messagebox.showinfo("Success", "Trip added successfully!")
                    self.clear_all_form_fields(self.main_frame)
                    self.entry_Vehicle_No.focus_set()
                except mysql.connector.Error as e:
                    messagebox.showerror("Error", f"Error: {e}")
                finally:
                    cursor.close()
                    conn.close()
        else:
            messagebox.showwarning("Input Error", "Please enter all fields.")

    def show_view_tripsheet_section(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        tk.Label(self.main_frame, text="📋 All Trips", font=("Georgia", 24, "bold"), bg="#ECF0F1", fg="#2C3E50").pack(pady=10)

        tree_frame = tk.Frame(self.main_frame, bg="white")
        tree_frame.pack(padx=20, pady=10, fill="both", expand=True)

        columns = ("Trip No", "Date", "Vehicle No", "Driver", "Bill No", "Bill Date", "Consignor",
                "Consignee", "Article", "Destination", "Weight", "Total Amt","To Pay/Paid")

        style = ttk.Style()
        style.configure("TripView.Treeview", font=("Georgia", 9), rowheight=28)
        style.configure("TripView.Treeview.Heading", font=("Georgia",10, "bold"))

        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", style="TripView.Treeview")

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        tree.column("Trip No", width=50)
        tree.column("Date", width=70)
        tree.column("Bill No", width=50)
        tree.column("Vehicle No", width=80)
        tree.column("Driver", width=120)
        tree.column("Bill Date", width=70)
        tree.column("Weight", width=60)
        tree.column("Total Amt", width=80)
        tree.column("To Pay/Paid", width=80)

        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        self.tree = tree  # if needed elsewhere

        # Load data
        conn = self.connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                query = """
                    SELECT ts.trip_id, ts.trip_date, ts.vehicle_no, ts.driver_id,
                        bd.bill_number, bd.date, bd.consignor_name, bd.consignee_name, bd.article,
                        bd.destination, bd.product_weight, bd.total_amount,bd.payments
                    FROM tripsheet ts
                    JOIN trip_bills tb ON ts.trip_id = tb.trip_id
                    JOIN bill_details bd ON tb.bill_number = bd.bill_number
                    ORDER BY ts.trip_id DESC
                """
                cursor.execute(query)
                for row in cursor.fetchall():
                    self.tree.insert("", tk.END, values=row)
            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", f"Error fetching trip data: {e}")
            finally:
                cursor.close()
                conn.close()

        # Add below your tree/table
        button_frame = tk.Frame(self.main_frame, bg="#ECF0F1")
        button_frame.pack(pady=15)
        tk.Button(button_frame, text="🖨️ Print TripSheet", font=("Georgia", 12), bg="#1ABC9C", fg="white", command=self.prompt_and_print_trip_pdf).pack(side="left", padx=10)

        view_btn = tk.Button(button_frame,text="👁️ View TripSheet",font=("Georgia", 12),bg="#1ABC9C",fg="white",command=self.prompt_and_view_trip_pdf)
        view_btn.pack(side="left", padx=10)


        self.add_footer()



    def prompt_and_print_trip_pdf(self):

        trip_id = simpledialog.askinteger("Print Trip PDF", "Enter Trip Number to print:")
        if not trip_id:
            return

        # Step 1: Generate the PDF
        self.generate_tripsheet_pdf(trip_id)

        # Step 2: Open PDF with default viewer so user can print manually
        # filename = f"TripSheet_{trip_id}.pdf"

        filename = os.path.join(self.tripsheet_folder, f"TripSheet_{trip_id}.pdf")
        

        filepath = os.path.abspath(filename)

        try:
            if platform.system() == "Windows":
                os.startfile(filepath)  # ⬅ Opens in default app like Edge/Chrome/Adobe
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", filepath])
            elif platform.system() == "Linux":
                subprocess.run(["xdg-open", filepath])
            else:
                messagebox.showerror("Unsupported OS", "Cannot open PDF: Unsupported operating system.")
        except Exception as e:
            messagebox.showerror("Open Error", f"Could not open PDF for printing:\n{e}")


    def generate_trip_pdf_from_data(self, trip_data):
        try:
            trip_id = trip_data[0]
            driver = trip_data[1]
            vehicle = trip_data[2]
            date = trip_data[3].strftime("%d/%m/%Y") if isinstance(trip_data[3], (datetime, date)) else str(trip_data[3])
            filename = f"Trip_{trip_id}.pdf"
            c = canvas.Canvas(filename, pagesize=A4)

            c.setFont("Helvetica-Bold", 16)
            c.drawString(100, 800, f"Trip Sheet - Trip No: {trip_id}")
            c.setFont("Helvetica", 12)
            c.drawString(100, 770, f"Driver: {driver}")
            c.drawString(100, 750, f"Vehicle: {vehicle}")
            c.drawString(100, 730, f"Date: {date}")

            # Add more details as needed

            c.save()
        except Exception as e:
            raise Exception(f"Failed to generate PDF: {e}")


    def prompt_and_view_trip_pdf(self):

        trip_number = simpledialog.askstring("View Trip PDF", "Enter Trip Number:")
        if trip_number:
            self.view_trip_pdf(trip_number.strip())

    def view_trip_pdf(self, trip_number):
        
        # pdf_path = f"TripSheet_{trip_number}.pdf"
        pdf_path = os.path.join("F:/TMS_Tripsheets", f"Tripsheet_{trip_number}.pdf")


        try:
            doc = fitz.open(pdf_path)
            last_page_index = len(doc) - 1
            page = doc.load_page(last_page_index)

            zoom = 2.0
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)

            full_img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            self.trip_pdf_img = ImageTk.PhotoImage(full_img)

            for widget in self.main_frame.winfo_children():
                widget.destroy()

            # Scrollable canvas setup
            canvas = tk.Canvas(self.main_frame, bg="white")
            scrollbar = tk.Scrollbar(self.main_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg="white")

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            # Show PDF image
            label = tk.Label(scrollable_frame, image=self.trip_pdf_img, bg="white")
            label.pack(pady=20)

        except Exception as e:
            tk.messagebox.showerror("Trip PDF Error", f"Could not open Trip PDF:\n{e}")



    def view_bill_pdf(self, bill_number):
        # pdf_path = f"Bill_{bill_number}.pdf"
        pdf_path = os.path.join("F:/TMS_Bills", f"Bill_{bill_number}.pdf")


        try:
            doc = fitz.open(pdf_path)
            page = doc.load_page(0)

            zoom = 1.5
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)

            full_img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            self.bill_full_img = ImageTk.PhotoImage(full_img)

            # Clear old content
            for widget in self.main_frame.winfo_children():
                widget.destroy()

            # Create scrollable canvas
            canvas_frame = tk.Canvas(self.main_frame, bg="white")
            canvas_frame.pack(side="left", fill="both", expand=True)

            scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=canvas_frame.yview)
            scrollbar.pack(side="right", fill="y")

            canvas_frame.configure(yscrollcommand=scrollbar.set)

            # Frame to hold image (centered)
            img_frame = tk.Frame(canvas_frame, bg="white")
            window_id = canvas_frame.create_window((0, 0), window=img_frame, anchor="n")

            # Center horizontally
            def center_image(event):
                canvas_width = event.width
                img_width = self.bill_full_img.width()
                x = max((canvas_width - img_width) // 2, 0)
                canvas_frame.coords(window_id, x, 0)

            canvas_frame.bind("<Configure>", lambda e: [canvas_frame.configure(scrollregion=canvas_frame.bbox("all")), center_image(e)])

            img_label = tk.Label(img_frame, image=self.bill_full_img, bg="white")
            img_label.pack()

        except Exception as e:
            messagebox.showerror("PDF View Error", str(e))


    def display_pdf_page(self):
        page = self.pdf_doc.load_page(self.pdf_current_page)
        matrix = fitz.Matrix(self.pdf_zoom, self.pdf_zoom)
        pix = page.get_pixmap(matrix=matrix)

        image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        self.pdf_image = ImageTk.PhotoImage(image)

        self.pdf_canvas.delete("all")
        self.pdf_canvas.create_image(0, 0, anchor="nw", image=self.pdf_image)
        self.pdf_canvas.config(scrollregion=self.pdf_canvas.bbox("all"))
        

    def show_next_pdf_page(self):
        if self.pdf_current_page < len(self.pdf_doc) - 1:
            self.pdf_current_page += 1
            self.display_pdf_page()

    def show_prev_pdf_page(self):
        if self.pdf_current_page > 0:
            self.pdf_current_page -= 1
            self.display_pdf_page()

    def zoom_in_pdf(self):
        self.pdf_zoom *= 1.25
        self.display_pdf_page()

    def zoom_out_pdf(self):
        self.pdf_zoom *= 0.8
        self.display_pdf_page()

    def open_selected_pdf_view(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a bill to view.")
            return

        bill_data = self.tree.item(selected_item, "values")
        bill_number = bill_data[0]
        self.view_bill_pdf(bill_number)


if __name__ == "__main__":
    root = tk.Tk()
    app = TransportManagementApp(root)
    root.mainloop()