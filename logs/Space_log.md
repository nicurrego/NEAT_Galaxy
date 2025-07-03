# LAST DONE:
watched the training at 1500 FPS.

# NEXT:
- I can train a bunch of gens and then I can see them training. e.g. train fast 9 gens and I see the 10th, if its working I can train another 9 and then see the 20th. much faster and avoid seeing the robot hitting the wall for hours.
- I need to orginise this and merge with main


# Model Notes
6) New reward system.
- 50 gens. The agents move however it looks like overfitting.
- 32 gens. The red ship learned to avoid direct bullets. The yellow ship moves to the bottom and then no one seems to have interest in shooting.
- 22 gens. The ships don't understand nothing, but try to react to bullets.
- 12 gens. The ships act random.

        HIT_REWARD = 15        
        SURVIVAL_REWARD = 5
        STEP_REWARD = 0.01
        WIN_BONUS = 20
        MOVEMENT_REWARD = 0.005
        DODGE_REWARD = 0.1

5) No reward for shooting.
- 20 gens. The agents don't seem to like shooting at all XD
        HIT_REWARD = 10        
        SURVIVAL_REWARD = 1    
        STEP_REWARD = 0.02
        WIN_BONUS = 15
        MOVEMENT_REWARD = 0.01


4) little tewak.2
- 50 gens. The model learned to figth on the bottom, the yellow goes first and fires, the red ship react to the fire and tries to hide in the bottom running directly to the bullets and loosing.
- 20 gens. The yellow ship shows interest in avoiding bullets, not very well though, the red ship goes down and stars shooting without caring anything else.
- 25 gens. The yellow ship learnd to react to bullets, not quite well still. the red ship learend to win by constant firering in the bottom.
- 30 gens. The yellow losed the will of following the red ship, the red ship still on the bottom and fires when yellow goes near it.
        HIT_REWARD = 10        
        SURVIVAL_REWARD = 1    
        STEP_REWARD = 0.02
        WIN_BONUS = 15
        MOVEMENT_REWARD = 0.01 

3) little tewak
- after 30 gens. the model moves interestingly odd, it reacts to shooting but sill very lost in objective.
- after 50 gens. the model when playing yellow shows active shooting and not much of dodging, **however** the model when playing red show super clear patterns (when yellow is near the left wall it moves to the right wall, when the yellow ship is near de middle it fires and tries to get close to yellow in Y axis, when yello fires the red ship goes down and completely stops shooting).
- after 200 gens, the red ship hides on the top and nothing else, the red ship fires in the spot until the bullets disapear from the screen, then it moves up a little and repeat until it reaches the top.
(I don't know if this is overfitting, I'm going to see 70, 80 and 90 gens to compare before tweaking the reward system)
- 70 gens. seems to have overfitting already.
- 35 gens. still not clear objective, but some trends present.
- 10 gens. yellow ship shows reaction to reds bullets, tries to fire randomly. Red is a dummy.

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