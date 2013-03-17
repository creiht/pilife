pilife
======

The game of life in Minecraft for the RaspberryPi

This was hacked together real quick during Pycon 2013 in the RaspberryPi Hack
Lab.  Many thanks to the organizers of Pycon for making this possible!

Using
-----

1.  Install Minecraft for your RaspberryPi from http://pi.minecraft.net
2.  Copy pilife.py to the mcpi/api/python/mcpi folder
3.  Start Minecraft
4.  Run a python shell from that folder, and from the shell run:

		from pilife import PiLife
		life = PiLife()
		# Create the life board with obsidian
		life.create_board() 
		# Place stone blocks on top of the board
		# Run the game of life simulation
		life.run()
		# Note that it will take a while to initialize

5.  Have fun! :)
