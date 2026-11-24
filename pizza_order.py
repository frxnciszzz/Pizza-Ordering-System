import tkinter as tk
from tkinter import ttk, messagebox

menu_prices = {
    "Hawaiian": 240,
    "Pepperoni": 260,
    "Four Cheese": 250,
    "Spicy Salami": 285
}

crust_size_prices = {
    "Small": 0,
    "Medium": 55,
    "Large": 110
}

add_on_prices = {
    "Black Olives": 25,
    "Sweet Corn": 25,
    "Jalapenos": 35,
    "Extra Mozzarella": 45
}

app_win = tk.Tk()
app_win.title("Slice of the Day - Pizza Ordering System")
app_win.geometry("650x850")
app_win.resizable(True, True)
app_win.configure(bg="#662424")

flavor_choice = tk.StringVar(value="Hawaiian")
size_choice = tk.StringVar(value="Small")
pizza_qty = tk.IntVar(value=1)

add_on_states = {
    addon: tk.BooleanVar(value=False)
    for addon in add_on_prices
}

heading = tk.Label(
    app_win,
    text="SLICE OF THE DAY",
    font=("Arial", 22, "bold"),
    bg="#662424",
    fg="white"
)
heading.pack(pady=(20, 2))

sub_heading = tk.Label(
    app_win,
    text="Pizza Ordering System",
    font=("Arial", 12, "bold"),
    bg="#662424",
    fg="white"
)
sub_heading.pack(pady=(0, 14))

form_panel = tk.Frame(
    app_win,
    bg="#4d1a1a",
    padx=25,
    pady=20
)
form_panel.pack(padx=25, fill="x")

tk.Label(
    form_panel,
    text="Select Pizza Flavor:",
    font=("Arial", 12, "bold"),
    bg="#4d1a1a",
    fg="white"
).pack(anchor="w")

flavor_box = ttk.Combobox(
    form_panel,
    textvariable=flavor_choice,
    values=list(menu_prices.keys()),
    state="readonly",
    font=("Arial", 11)
)
flavor_box.pack(fill="x", pady=8)

tk.Label(
    form_panel,
    text="Select Pizza Size:",
    font=("Arial", 12, "bold"),
    bg="#4d1a1a",
    fg="white"
).pack(anchor="w", pady=(12, 5))

for size_name, size_cost in crust_size_prices.items():
    tk.Radiobutton(
        form_panel,
        text=f"{size_name} (+₱{size_cost})",
        variable=size_choice,
        value=size_name,
        font=("Arial", 11),
        bg="#4d1a1a",
        fg="white",
        selectcolor="#800000",
        activebackground="#4d1a1a",
        activeforeground="white"
    ).pack(anchor="w")

tk.Label(
    form_panel,
    text="Select Extra Toppings:",
    font=("Arial", 12, "bold"),
    bg="#4d1a1a",
    fg="white"
).pack(anchor="w", pady=(12, 5))

for addon_name, addon_cost in add_on_prices.items():
    tk.Checkbutton(
        form_panel,
        text=f"{addon_name} (+₱{addon_cost})",
        variable=add_on_states[addon_name],
        font=("Arial", 11),
        bg="#4d1a1a",
        fg="white",
        selectcolor="#800000",
        activebackground="#4d1a1a",
        activeforeground="white"
    ).pack(anchor="w")

tk.Label(
    form_panel,
    text="Quantity:",
    font=("Arial", 12, "bold"),
    bg="#4d1a1a",
    fg="white"
).pack(anchor="w", pady=(12, 5))

qty_spinner = tk.Spinbox(
    form_panel,
    from_=1,
    to=50,
    textvariable=pizza_qty,
    font=("Arial", 12),
    width=10,
    bg="#662424",
    fg="white",
    insertbackground="white"
)
qty_spinner.pack(anchor="w")


def calculate_total():
    chosen_flavor = flavor_choice.get()
    chosen_size = size_choice.get()

    try:
        count = int(pizza_qty.get())

        if count < 1 or count > 50:
            raise ValueError

    except (ValueError, tk.TclError):
        messagebox.showerror(
            "Invalid Quantity",
            "Please enter a quantity between 1 and 50."
        )
        return

    confirm = messagebox.askyesno(
        "Confirm Order",
        "Are you sure you want to place this order?"
    )

    if not confirm:
        return

    base_cost = menu_prices[chosen_flavor]
    extra_size_cost = crust_size_prices[chosen_size]

    picked_addons = [
        addon
        for addon, state in add_on_states.items()
        if state.get()
    ]

    addons_total = sum(
        add_on_prices[addon]
        for addon in picked_addons
    )

    price_each = base_cost + extra_size_cost + addons_total
    grand_total = price_each * count

    receipt_box.delete("1.0", tk.END)

    receipt_box.insert(
        tk.END,
        "===== SLICE OF THE DAY RECEIPT =====\n\n"
    )

    receipt_box.insert(tk.END, f"Pizza Flavor: {chosen_flavor}\n")
    receipt_box.insert(tk.END, f"Pizza Size: {chosen_size}\n")

    if picked_addons:
        for addon in picked_addons:
            receipt_box.insert(
                tk.END,
                f"{addon}: ₱{add_on_prices[addon]}\n"
            )
    else:
        receipt_box.insert(tk.END, "No extra toppings\n")

    receipt_box.insert(tk.END, f"Quantity: {count}\n")
    receipt_box.insert(tk.END, f"TOTAL AMOUNT: ₱{grand_total:,.2f}\n")


def reset_order():
    flavor_choice.set("Hawaiian")
    size_choice.set("Small")
    pizza_qty.set(1)

    for state in add_on_states.values():
        state.set(False)

    receipt_box.delete("1.0", tk.END)


action_panel = tk.Frame(
    app_win,
    bg="#662424"
)
action_panel.pack(pady=15)

order_btn = tk.Button(
    action_panel,
    text="PLACE ORDER",
    font=("Arial", 11, "bold"),
    bg="#2e7d32",
    fg="white",
    width=18,
    command=calculate_total
)
order_btn.grid(row=0, column=0, padx=8)

clear_btn = tk.Button(
    action_panel,
    text="RESET",
    font=("Arial", 11, "bold"),
    bg="#800000",
    fg="white",
    width=12,
    command=reset_order
)
clear_btn.grid(row=0, column=1, padx=8)

tk.Label(
    app_win,
    text="ORDER SUMMARY",
    font=("Arial", 14, "bold"),
    bg="#662424",
    fg="white"
).pack(pady=5)

receipt_box = tk.Text(
    app_win,
    height=12,
    width=65,
    font=("Consolas", 11),
    bg="#4d1a1a",
    fg="white",
    insertbackground="white"
)
receipt_box.pack(padx=25, pady=10)

app_win.mainloop()
