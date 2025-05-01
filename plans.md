# Plan
Robots will run on one of a series of strategic protocols designed for specific situations. Robots will communicate with one another to determine which algorithm is the most useful at any given point.

### Protocols
> Attack - The robot determines the position of the ball, the goal and any enemies. The robot plans a course to bring the ball to the goal, avoiding all enemies.

> Interference - The robot determines the position of the ball, as well as both enemies. The robot attempts to collide with the nearest robot to the ball.

> Defence - The robot determines the position of the friendly goal and the ball. The robot places itself between the ball and the goal and advances towards the ball if possible.

> Default/Init - The robot chooses which mode to initialise in. it considers first if its teammate has already made a decision, then if it has a clear line of attack, then who is in possession of the ball, then makes a decision.