Hello!

This is a program that takes Steam game data and plots it using Pandas and Matplotlib. Both the Client and Server sides are written in Python.

Things to note with this program:
	- Currently, the server must be run in Linux (I've tested this in Debian and it works perfectly).
	- The server must be accessed using a .PEM file, as this is the only way I've implemented so far.
	- The servers files must be set up in this way:
		/home/username/steamgame --> gamedata(directory), games.txt, main.py, steamapi.py
	- Thus, a folder named 'steamgame' must be made at the username directory. Inside steamgame, there must be another folder named gamedata, followed by a file called games.txt, main.py, steamapi.py.
	- Due to the way my code is written, it is hard-coded so that this is necessary. In future versions, I will allow for a dynamic and automatic way of setting up the proper required files.
	
Once the server-side is set up properly, run main.py. I would recommend doing this in tmux so that you can exit the session and still have it running.
For more information on tmux, I'd recommend this article: https://linuxize.com/post/getting-started-with-tmux/

After the server-side is completely finished and main.py is running, your server is now collecting data on an hourly basis. You can change this interval in the main.py file, under the scheduler command, where it says 'hours=1'.
To start the client-side properly, ensure all of client-side files are in the same directory, and run window.py.

Put in the appropriate IP address and username. Clicking 'File...' will open your file browser. Select your .PEM file, and click 'Login'.
If the login attempt is successful, you should see:
	- A dropdown menu -> Select a game whose data you wish to view
	- 'Show Players' Button -> Plots active players over time of currently selected game
	- 'Show Rating' Button -> Plots game rating over time of currently selected game
	- 'Add Game' Button -> Input a new appid of a game you wish to track data of

Ideas for future updates:
	- Create a way to automatically set up server-side files
	- Allow for a dynamic directory to access the server-side, that way the directory doesn't have to be a hardcoded '/home/username/steamgame/...'
	- Combine multiple game graphs to compare to each other
	- Improve aesthetics of client-side
