import tkinter as tk
from tkinter import font

def submit():
    eth_network = network_var.get()
    execution_client_delete = execution_delete_var.get()
    execution_client_install = execution_install_var.get()
    root.destroy()
    
    return eth_network, execution_client_delete, execution_client_install

root = tk.Tk()
root.title("Ethereum Validator Installer")
root.configure(background="#282C34")

network_var = tk.StringVar()
execution_delete_var = tk.StringVar()
execution_install_var = tk.StringVar()

label_font = font.nametofont("TkDefaultFont").copy()
label_font.config(size=20)

# Ethereum network selection
network_label = tk.Label(root, text="Ethereum network:", bg="#282C34", fg="#ABB2BF", font=label_font, anchor='e')
network_label.grid(column=0, row=0, padx=30, pady=30, sticky='e')

networks = ('Mainnet', 'Goerli', 'Sepolia')
network_menu = tk.OptionMenu(root, network_var, *networks)
network_menu.config(bg="#4CAF50", fg="#FFFFFF", activebackground="#8BC34A", activeforeground="#FFFFFF", font=label_font, takefocus=True)
network_menu["menu"].config(bg="#4CAF50", fg="#FFFFFF", activebackground="#8BC34A", activeforeground="#FFFFFF", font=label_font)
network_menu.grid(column=1, row=0, padx=30, pady=30, ipadx=40, ipady=10)

# Execution client selection (to delete)
execution_delete_label = tk.Label(root, text="Execution Client to DELETE:", bg="#282C34", fg="#ABB2BF", font=label_font, anchor='e')
execution_delete_label.grid(column=0, row=1, padx=30, pady=30, sticky='e')

execution_clients = ('Nethermind', 'Besu', 'Geth')
execution_delete_menu = tk.OptionMenu(root, execution_delete_var, *execution_clients)
execution_delete_menu.config(bg="#2196F3", fg="#FFFFFF", activebackground="#64B5F6", activeforeground="#FFFFFF", font=label_font, takefocus=True)
execution_delete_menu["menu"].config(bg="#2196F3", fg="#FFFFFF", activebackground="#64B5F6", activeforeground="#FFFFFF", font=label_font)
execution_delete_menu.grid(column=1, row=1, padx=30, pady=30, ipadx=40, ipady=10)

# Execution client selection (to install)
execution_install_label = tk.Label(root, text="Execution Client to INSTALL:", bg="#282C34", fg="#ABB2BF", font=label_font, anchor='e')
execution_install_label.grid(column=0, row=2, padx=30, pady=30, sticky='e')

execution_install_menu = tk.OptionMenu(root, execution_install_var, *execution_clients)
execution_install_menu.config(bg="#FF9800", fg="#FFFFFF", activebackground="#FFA726", activeforeground="#FFFFFF", font=label_font, takefocus=True)
execution_install_menu["menu"].config(bg="#FF9800", fg="#FFFFFF", activebackground="#FFA726", activeforeground="#FFFFFF", font=label_font)
execution_install_menu.grid(column=1, row=2, padx=30, pady=30, ipadx=40, ipady=10)

# Submit button
submit_button = tk.Button(root, text="Install", command=submit, bg="#282C34", fg="#ABB2BF", activebackground="#61AFEF", activeforeground="#282C34", font=label_font, takefocus=True)
submit_button.grid(column=1, row=3, padx=30, pady=60)

root.mainloop()

# Define User Input Variables
eth_network = root.saved_data[0]
execution_client_delete = root.saved_data[1]
execution_client_install = root.saved_data[2]

# Print User Input Variables
print("\n##### User Selected Inputs #####")
print(f"Ethereum Network: {eth_network}")
print(f"Execution Client to DELETE: {execution_client_delete}")
print(f"Execution Client to INSTALL: {execution_client_install}\n")

