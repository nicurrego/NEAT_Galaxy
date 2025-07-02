The human_play script is working, it loads the spaceship images, however I will need to modify the core module to load it from there.

next I will be working on the environment to train the agents using NEAT.

# LAST DONE:
tried best picke, triend some of the examples of the play_match.py

# NEXT:
add penalty for recieving hits, (keep it minimal)


# Model Notes

3) little tewak
- after 30 gens. the model moves interestingly odd, it reacts to shooting but sill very lost in objective.
- after 50 gens. the model when playing yellow shows active shooting and not much of dodging, **however** the model when playing red show super clear patterns (when yellow is near the left wall it moves to the right wall, when the yellow ship is near de middle it fires and tries to get close to yellow in Y axis, when yello fires the red ship goes down and completely stops shooting).

        HIT_REWARD = 10        
        SURVIVAL_REWARD = 2    
        STEP_REWARD = 0.03
        WIN_BONUS = 15
        MOVEMENT_REWARD = 0.07 

2) new reward system
- I trained a 50 gen. model and it tries to shoot and then hides in the top corner the rest of the game.
- after 93 generations the model learns almost not to die, and it fires constantly, however it still does not look for confrontation.

        HIT_REWARD = 10
        SURVIVAL_REWARD = 5
        STEP_REWARD = 0.01
        WIN_BONUS = 20
        MOVEMENT_REWARD = 0.02
        

1) only rewarded if hit
The Model fires and don't show any interest in dodge the bullets or follow the enemy ship