# RetroFuture
A game based around 80s aesthetic, made in Python using pygame. Pilot your ship and shoot enemies to make it out alive. If you're good enough, you can try to make it through the gauntlet.

I made this game out of a love of that 80s squiggly art style visually, and a love of Geometry Wars: Retro Evolved mechanically, which was the hero of the Xbox 360 Live Arcade in the early days of that console's lifespan. I still think it's one of the best games ever.  I played that game a lot, and since I wrote the code for this game on top of that and decided the spawns and behaviours of all the enemies, I may have tuned the game to be quite difficult.

I created this game very crudely without any proper structure, not expecting myself to actually finish the project... but as I liked the style a lot I kept writing more and more code until it became very cool, but also very convoluted.  Different classes were reading and altering variables of each other's objects willynilly. Later I created more of a structure with a Game class handling the menu and the level, with the level then handling the enemy and the player, and finally the bullet object created by the player.  
The logic of the game from the ground up was overly mixed up, and it would have taken too long to actually properly separate the classes, so there is a lot of spaghetti code through this. I am able to understand it and could make alterations to it, but I am sure that anybody else would struggle greatly to decipher these hieroglyphs.

The basic game is split into 3 game types: Gauntlet, Endless and Survival.

Gauntlet is a series of levels with set enemies spawning in at set times, dictated by a spawn_data dictionary, hand crafted by me. Most levels have a win condition of defeating all the enemies from the spawn_data dictionary, but some have another objective which is to survive for x seconds with guns disabled.

Endless uses a function which takes a difficulty option from the player and uses it to adjust the maximum amount of enemies, and will continue to spawn enemies until that number is reached. It spawns enemies randomly across the different enemy types, with some types weighted more heavily than others.  The game ends when the player dies, and then the score is displayed next to the highscore, which is saved to a separate file and persistent across replays.

Survival is a combination of a spawn_data set of enemies, followed by endless enemies, but with a win condition of a time limit, also dictated by the difficulty chosen by the player.

The enemies are split into 5 types: Seeker, Bouncer, Palm, Wedge and Twirler.

Seeker: Uses the player's co-ordinates to always be moving towards them.

Bouncer: Grabs random co-ordinates around the edge of the arena and moves towards them, picking a new spot when reaching the last.

Palm: Moves from one side of the screen to the other then despawns if not already killed. Picks which side and direction randomly.

Wedge: Falls from the top of the screen to the bottom, then despawns if not already killed. Very similar to Palm.

Twirler: Stays in place and rotates 360 degrees. The least threatening enemy.


The player is a ship that moves in 8 directions and shoots in 4. It actually has a booster activated by the spacebar, though this information is not available outside of the readme, as it's sort of a finished but not well balanced feature, but it seemed a shame to take it out.

The ship has different speeds of firepower depending on conditions set in gauntlet levels or for other types, on the amount of enemies on screen.   The amount of bullets ranges from 0 on pacifist, time-based levels up to firing multiple bullets per turn with very little cooldown. The bullets have slight veer to their path to make it appear more interesting.

The player has no health and dies in one hit. All progress is lost on the gauntlet upon death. It's quite mean, really.
