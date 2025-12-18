Hello!

This is readme on game of Battleship (aka python final project).

1. How your input format works?

   Simple! Player will input one ship at a time, by writing it's begin and end coordinated (like G2 G7). It can be a ship of any size, that's possible to include.


2. How you validate ship placements&

   Algorithm checks if ship are valid size, do not touch or cross any other ships (diagonals too). Also ship should be placed strictly horizontal or vertical and coordinates shouldn't be out of the 10X10 board.


3. How you update and display the game state?

   Through reading and updating .csv files with both player and bot boards. I also have game logs in another csv file, that i don't use, but assignment stated i should have it, so...
   In those scv's there are just simple tables with numbers, that identify current state if the cell.

4. Any design decisions or trade-offs

   I didn't make it so that player (or bot) could hit again without waiting for his turn, if he hits a ship. (Personally i think this rule is kinda unfair, one, who hit the ship is already at advantageous position...)

   Also i tried to display boards as pretty and easy to read as possible.


That's all.

made by Sofya Mikheeva, 301 group (3.1)