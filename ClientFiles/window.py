import paramiko as pm
import tkinter
import tkinter.messagebox
import sshfuncs
import steamapi
import files
import matplotlib
import matplotlib.figure as fig
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from tkinter.filedialog import askopenfile
from tkinter.simpledialog import askstring
from tkinter.messagebox import showinfo
from tkinter import filedialog
from tkinter.ttk import *

file_path = ''
ssh = pm.SSHClient()
top_list = []

sshfuncs_obj = sshfuncs

add_gm_msg = 'Click \'Add Game\' to start tracking a game!'

# Sets the file_path variable to the path of the given .PEM file
def get_file():
    global file_path
    pem_file = filedialog.askopenfilename(filetypes=[('PEM', '.pem')])
    file_path = pem_file
    

# --- LOGIN --- #
# Attempts a login given the given credentials.
# This currently only supports .PEM files as passwords at this moment.
def login():

    password = pm.RSAKey.from_private_key_file(file_path)

    # Removes all widgets from main window.
    # main.login returns a boolean
    if sshfuncs.login(ip_field.get(), user_field.get(), password, ssh):
        ip_label.pack_forget()
        ip_field.pack_forget()
        user_label.pack_forget()
        user_field.pack_forget()
        file_button.pack_forget()
        login_button.pack_forget()
        
        login_successful()
    else:
        tkinter.messagebox.showinfo('Error', 'Could not connect. Please double check your credentials.')
    
# --- ADD GAME --- #
# Inserts new game into text file on the server.
def add_game():
    
    # Popup window to receive appid
    game_to_add = askstring('New Game', 'Insert appid')
    
    # sshfuncs.add_game() returns a boolean.
    # Returns false if game is already in list.
    if game_to_add is not None and sshfuncs.add_game(game_to_add, ssh):
        tkinter.messagebox.showinfo('Add Game', steamapi.game_name(int(game_to_add)) + ' (' + game_to_add + ') added')
    elif game_to_add is not None:
        tkinter.messagebox.showinfo('Add Game', steamapi.game_name(int(game_to_add)) + ' (' + game_to_add + ') already in list. If you are looking for the graph, please wait until an iteration (one hour), as there currently no data for this game.')
        

# --- GET GRAPH PLAYER COUNT --- #
# Creates a plot of player count using Matplotlib of the selected game
def get_graph_pcount():
    
    # These conditions check if the game is a valid ID.
    if g_combobox.get() == add_gm_msg:
        tkinter.messagebox.showinfo('Error', 'Please add a valid game using the \'Add Game\' Button.')
        return
    if g_combobox.get() == '':
        tkinter.messagebox.showinfo('Error', 'Please select a game.')
        return
        
    # Removes all widgets from main window
    g_combobox.forget()
    g_add_game.forget()
    g_get_graph_players.forget()
    g_get_graph_rating.forget()
    
    # files.get_df() returns the file using SFTP.
    cur_df = files.get_df(ssh, 'steamgame/gamedata/' + str(g_list_id[g_combobox.current()]) + '.csv')
    
    # Desginates each axis of the graph using the column name.
    # In all cases with line graphs, the x axis will be a date_time value.
    # For this case, the y axis will be the current number of players at the given date_time stamp.
    x_vals = cur_df['date_time']
    y_vals = cur_df['current players']
  
    # Entering dimensions of the graph
    f = plt.figure(figsize=(6,6), dpi=100)
    
    # Creating the graph
    plt.plot(x_vals, y_vals)
    
    # Setting up X label and making date_time vertical and smaller for readability.
    plt.xlabel('Date/Time')
    plt.xticks(x_vals, rotation=270, fontsize=6)
    
    # Setting up Y label
    plt.ylabel('Player Count')
    
    # Setting up title at top of graph
    plt.title(g_combobox.get())
    
    # Converting graph size into window size to allow for graph, toolbar, and back button
    # f.get_size_inches()[0] is the width, and f.get_size_inches()[1] is the height.
    # f.dpi is Dots Per Inch, which, when multiplied with the width/height, will give the size in number of pixels.
    # Give extra room (0.12 * the respective dimension) to allow for space for the back button and toolbar
    c_width = f.get_size_inches()[0] * f.dpi + (f.get_size_inches()[0] * f.dpi * 0.12)
    c_height = f.get_size_inches()[1] * f.dpi + (f.get_size_inches()[1] * f.dpi * 0.12)
    center_window(c_width, c_height)
    
    # Creates canvas to insert the new plot, and the plot is then added and packed to the main window.    
    canvas = FigureCanvasTkAgg(f, top)
    canvas.draw()
    canvas.get_tk_widget().pack()
    
    # Adds the Matplotlib toolbar
    toolbarFrame = Frame(master=top)
    toolbarFrame.pack()
    toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
    
    # Proper dimensions to include things like X/Y labels and the graph title
    plt.subplots_adjust(left=0.14, bottom=0.20, right=0.96, top=0.93)
    
    # --- BACK BUTTON --- #
    # This button removes all graph window components that were initially added, then re-adds the main menu buttons (show player count graph, show rating graph, add game)
    back_button = tkinter.Button(top, text = 'Back', command = lambda: [canvas.get_tk_widget().pack_forget(),
                                                                        toolbarFrame.pack_forget(),
                                                                        back_button.pack_forget(),
                                                                        toolbar.pack_forget(),
                                                                        login_successful()])
    back_button.pack(pady=2)
        
# --- GET GRAPH PLAYER RATING --- #
# Creates a plot of player rating using Matplotlib of the selected game
# NOTE: Over a short period of time, this value will be very stagnant, essentially a horizontal line.
def get_graph_prating():
    
    # These conditions check if the game is a valid ID.
    if g_combobox.get() == add_gm_msg:
        tkinter.messagebox.showinfo('Error', 'Please add a valid game using the \'Add Game\' Button.')
        return
    if g_combobox.get() == '':
        tkinter.messagebox.showinfo('Error', 'Please select a game.')
        return
    
    # Removes all widgets from main window
    g_combobox.forget()
    g_add_game.forget()
    g_get_graph_players.forget()
    g_get_graph_rating.forget()
    
    # files.get_df() returns the file using SFTP.
    cur_df = files.get_df(ssh, 'steamgame/gamedata/' + str(g_list_id[g_combobox.current()]) + '.csv')
    
    # Desginates each axis of the graph using the column name.
    # In all cases with line graphs, the x axis will be a date_time value.
    # For this case, the y axis will be the current rating at the given date_time stamp.
    x_vals = cur_df['date_time']
    y_vals = cur_df['rating']
  
    # Entering dimensions of the graph
    f = plt.figure(figsize=(6,6), dpi=100)
    
    # Creating the graph
    plt.plot(x_vals, y_vals)
    
    # Setting up X label and making date_time vertical and smaller for readability.
    plt.xlabel('Date/Time')
    plt.xticks(x_vals, rotation=270, fontsize=6)
    
    # Setting up Y label/axis
    # Because of the way Matplotlib reads small values, it uses a weird notation.
    # This is circumvented by putting a limit on the Y Axis, as no game will ever
    # have a rating under 0.0, nor will it ever go over 1.00.
    plt.ylabel('Player Rating')
    plt.ylim([0, 1.0])
    
    # Setting up title at top of graph
    plt.title(g_combobox.get())
    
    # Converting graph size into window size to allow for graph, toolbar, and back button
    # f.get_size_inches()[0] is the width, and f.get_size_inches()[1] is the height.
    # f.dpi is Dots Per Inch, which, when multiplied with the width/height, will give the size in number of pixels.
    # Give extra room (0.12 * the respective dimension) to allow for space for the back button and toolbar
    c_width = f.get_size_inches()[0] * f.dpi + (f.get_size_inches()[0] * f.dpi * 0.12)
    c_height = f.get_size_inches()[1] * f.dpi + (f.get_size_inches()[1] * f.dpi * 0.12)
    center_window(c_width, c_height)
    
    # Creates canvas to insert the new plot, and the plot is then added and packed to the main window.
    canvas = FigureCanvasTkAgg(f, top)
    canvas.draw()
    canvas.get_tk_widget().pack()
    
    # Adds the Matplotlib toolbar
    toolbarFrame = Frame(master=top)
    toolbarFrame.pack()
    toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
    
    # Proper dimensions to include things like X/Y labels and the graph title
    plt.subplots_adjust(left=0.14, bottom=0.20, right=0.96, top=0.93)
    
    # --- BACK BUTTON --- #
    # This button removes all graph window components that were initially added, then re-adds the main menu buttons (show player count graph, show rating graph, add game)
    back_button = tkinter.Button(top, text = 'Back', command = lambda: [canvas.get_tk_widget().pack_forget(),
                                                                        toolbarFrame.pack_forget(),
                                                                        back_button.pack_forget(),
                                                                        toolbar.pack_forget(),
                                                                        login_successful()])
    back_button.pack(pady=2)
    

# Creates the main menu.
# This isn't only called on a successful login, but when the user
# wishes to go back to the main menu.
def login_successful():
    global g_combobox
    global g_add_game
    global g_get_graph_players
    global g_get_graph_rating
    
    # Resets window size to default
    center_window()
    
    # This ssh command and loop gets a list of all game that has active data
    # The list will then populate the Combobox
    num_list = sshfuncs.output('ls steamgame/gamedata', ssh).split()
    g_list = []
    for i in num_list:
        fixed_str = i.replace('.csv', '').strip()
        if fixed_str.isalpha():
            continue
        # g_list is the list that will be added to the Combobox.
        # g_list_id has the appids so that pulling the graphs are easier
        try:
            g_list.append(steamapi.game_name(int(fixed_str)) + ' (' + fixed_str + ')')
            g_list_id.append(int(fixed_str))
        except:
            print('Invalid appid')
            
    # If there are no appids with value, add a temp message that will let the user know to add a game
    if not g_list:
        g_list.append(add_gm_msg)
    
    # Creates the Combobox with properties, such as being uneditable, and getting rid of the highlight effect    
    g_combobox = tkinter.ttk.Combobox(top, state='readonly', width=len(max(g_list, key=len)), justify='center')
    g_combobox.bind('<<ComboboxSelected>>', lambda e: top.focus())
    
    # Populates the combobox with the previous list
    g_combobox['values'] = g_list
    
    # Creates the buttons that will bring the user to their respective graphs    
    g_get_graph_players = tkinter.Button(top, text='Show Players', command = get_graph_pcount)
    g_get_graph_rating = tkinter.Button(top, text='Show Rating', command = get_graph_prating)
    
    # Button to add game to list
    g_add_game = tkinter.Button(top, text='Add Game', command = add_game)
    
    # Adding each component to the main window
    g_combobox.pack(pady=5)
    g_get_graph_players.pack(pady=5)
    g_get_graph_rating.pack(pady=5)
    g_add_game.pack(pady=5)
    

# Properly resizes the window and puts in the middle of the screen
def center_window(w=400, h=150):
    mon_width = top.winfo_screenwidth()
    mon_height = top.winfo_screenheight()
    
    x = (mon_width / 2) - (w / 2)
    y = (mon_height / 2) - (h / 2)
    
    top.geometry('%dx%d+%d+%d' % (w, h, x, y))
    
    
# Debugging command to ensure widgets have been properly removed
# Also makes sure the window size is correct
def print_dimensions():
    w = top.winfo_width()
    h = top.winfo_height()
    
    print('width: ' + str(w) + ', height: ' + str(h))
    

# Main Window
top = tkinter.Tk()

# IP Address Input
ip_label = tkinter.Label(top, text='IP Address')
ip_field = tkinter.Entry(top)

# Username Input
user_label = tkinter.Label(top, text='Username')
user_field = tkinter.Entry(top)

# Buttons
file_button = tkinter.Button(top, text='File...', command = get_file)
login_button = tkinter.Button(top, text='Login', command = login)

# Combobox containing games that have data
g_combobox = None

# Add Game Button
g_add_game = None

# Show active player graph button
g_get_graph_players = None

# Show current rating graph Button
g_get_graph_rating = None

# List of appids that have data
g_list_id = []

# Put all widgets/slaves into the main window (variable is top)
ip_label.pack()
ip_field.pack()
user_label.pack()
user_field.pack()
file_button.pack(pady=5)
login_button.pack()

top.resizable(False, False)

# Sets default size
center_window()

# Makes window visible
top.mainloop()
