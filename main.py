# **********************************************************************************
# **********************************************************************************
# Program:      Bills Management System                                            **
# Programmer:   Masumbuko Alulea                                                   **
# Description:  This program helps users manage their personal income and expenses.**
#               It allows users to input income details, save weekly data, access  **
#               and display the data, track and categorize expenses, and provide   **
#               financial recommendations based on spending patterns. The program  **
#               also offers graphical and textual display options for data         **
#               visualization.                                                     **
#                                                                                  **
# Features:                                                                        **
# 1. Manage Income                                                                 **
# 2. Save Weekly Data to Separate Files                                            **
# 3. Access and Display Weekly Data                                                **
# 4. Track and Categorize Expenses                                                 **
# 5. Provide Financial Recommendations                                             **
# 6. Graphical and Textual Display Options                                         **
#                                                                                  **
# Implementation:                                                                  **
# This program uses a combination of C++ and Python. The core functionalities,     **
# such as managing income and saving records, are implemented in C++ for           **
# performance efficiency. These C++ functions are then exposed to Python using     **
# ctypes for seamless integration. The GUI and visualization components are        **
# handled in Python using Tkinter and Matplotlib.                                  **
#                                                                                  **
# Initiated: July 06, 2024                                                         **
# Predicted Completion Date: September 30, 2024                                    **
#                                                                                  **
# **********************************************************************************
# **********************************************************************************

import ctypes
import sys
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from datetime import datetime


class IncomeRecord(ctypes.Structure):
    _fields_ = [
        ("hourlyRate", ctypes.c_double),
        ("hoursWorked", ctypes.c_double),
        ("weekendHours", ctypes.c_double),
        ("totalPayment", ctypes.c_double),
        ("date", ctypes.c_char_p)
    ]

def initialize_library():
    try:
        lib = ctypes.CDLL('./libmanagement.so')
        print("Library loaded successfully")
    except OSError as e:
        print(f"Error loading library: {e}")
        sys.exit(1)

    # Define the argument and return types of the functions
    lib.Management_new.restype = ctypes.c_void_p
    lib.Management_manageIncome.argtypes = [ctypes.c_void_p, ctypes.c_double, ctypes.c_double, ctypes.c_double,
                                            ctypes.c_char, ctypes.c_double]
    lib.Management_manageIncome.restype = None
    lib.Management_displayMonthlySummary.argtypes = [ctypes.c_void_p]
    lib.Management_displayMonthlySummary.restype = None
    lib.Management_delete.argtypes = [ctypes.c_void_p]
    lib.Management_delete.restype = None
    lib.Management_getMonthlySummary.argtypes = [ctypes.c_void_p]
    lib.Management_getMonthlySummary.restype = ctypes.c_char_p
    lib.Management_getIncomeRecords.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)]
    lib.Management_getIncomeRecords.restype = ctypes.POINTER(IncomeRecord)

    return lib


def manage_income():
    try:
        hourly_rate = float(entry_hourly_rate.get())
        hours_worked = float(entry_hours_worked.get())
        weekend_hours = float(entry_weekend_hours.get())
        worked_weekend = weekend_var.get().encode('utf-8')
        weekend_additional_rate = float(entry_weekend_additional_rate.get())

        lib.Management_manageIncome(management, hourly_rate, hours_worked, weekend_hours, worked_weekend[0],
                                    weekend_additional_rate)
        messagebox.showinfo("Success", "Income details recorded successfully.")
    except ValueError as e:
        messagebox.showerror("Input Error", f"Invalid input: {e}")


def show_monthly_summary():
    summary = lib.Management_getMonthlySummary(management).decode('utf-8')
    messagebox.showinfo("Monthly Summary", summary)


def plot_income_trend(plot_type):
    size = ctypes.c_int()
    records_ptr = lib.Management_getIncomeRecords(management, ctypes.byref(size))
    records = records_ptr[:size.value]

    dates = []
    payments = []
    for record in records:
        dates.append(datetime.strptime(record.date.decode('utf-8'), "%Y-%m-%d"))
        payments.append(record.totalPayment)

    # Print the values to verify
    print("Dates and Payments Retrieved:")
    for date, payment in zip(dates, payments):
        print(f"Date: {date}, Payment: {payment}")

    # Only plot if values are correct
    plt.figure(figsize=(10, 6))

    if plot_type == 'line':
        plt.plot(dates, payments, marker='o', linestyle='-', color='b')
        plt.title("Income Trend (Line)")
    elif plot_type == 'bar':
        plt.bar(dates, payments, color='b')
        plt.title("Income Trend (Bar)")
    elif plot_type == 'scatter':
        plt.scatter(dates, payments, color='b')
        plt.title("Income Trend (Scatter)")

    plt.xlabel("Date")
    plt.ylabel("Total Payment ($)")
    plt.grid(True)
    plt.show()


def predict_annual_pay():
    try:
        size = ctypes.c_int()
        records_ptr = lib.Management_getIncomeRecords(management, ctypes.byref(size))
        records = records_ptr[:size.value]

        total_payment = sum(record.totalPayment for record in records)
        weeks = len(records)
        if weeks == 0:
            messagebox.showerror("Error", "No income data available for prediction.")
            return

        weekly_avg = total_payment / weeks
        annual_pay = weekly_avg * 52

        messagebox.showinfo("Annual Pay Prediction",
                            f"Estimated Annual Gross Pay: ${annual_pay:,.2f}\nWeekly Average: ${weekly_avg:,.2f}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while predicting annual pay: {e}")


def create_gui():
    global entry_hourly_rate, entry_hours_worked, entry_weekend_hours, entry_weekend_additional_rate, weekend_var

    root = tk.Tk()
    root.title("Bills Management System")

    tk.Label(root, text="Hourly Rate:").grid(row=0, column=0)
    entry_hourly_rate = tk.Entry(root)
    entry_hourly_rate.grid(row=0, column=1)

    tk.Label(root, text="Hours Worked:").grid(row=1, column=0)
    entry_hours_worked = tk.Entry(root)
    entry_hours_worked.grid(row=1, column=1)

    tk.Label(root, text="Weekend Hours:").grid(row=2, column=0)
    entry_weekend_hours = tk.Entry(root)
    entry_weekend_hours.grid(row=2, column=1)

    tk.Label(root, text="Worked Weekend (Y/N):").grid(row=3, column=0)
    weekend_var = tk.StringVar()
    tk.Entry(root, textvariable=weekend_var).grid(row=3, column=1)

    tk.Label(root, text="Weekend Additional Rate:").grid(row=4, column=0)
    entry_weekend_additional_rate = tk.Entry(root)
    entry_weekend_additional_rate.grid(row=4, column=1)

    tk.Button(root, text="Manage Income", command=manage_income).grid(row=5, column=0, columnspan=2)
    tk.Button(root, text="Show Monthly Summary", command=show_monthly_summary).grid(row=6, column=0, columnspan=2)
    tk.Button(root, text="Plot Income Trend (Line)", command=lambda: plot_income_trend('line')).grid(row=7, column=0,
                                                                                                     columnspan=2)
    tk.Button(root, text="Plot Income Trend (Bar)", command=lambda: plot_income_trend('bar')).grid(row=8, column=0,
                                                                                                   columnspan=2)
    tk.Button(root, text="Plot Income Trend (Scatter)", command=lambda: plot_income_trend('scatter')).grid(row=9,
                                                                                                           column=0,
                                                                                                           columnspan=2)
    tk.Button(root, text="Predict Annual Pay", command=predict_annual_pay).grid(row=10, column=0, columnspan=2)

    root.mainloop()


if __name__ == "__main__":
    lib = initialize_library()
    management = lib.Management_new()
    create_gui()
    lib.Management_delete(management)