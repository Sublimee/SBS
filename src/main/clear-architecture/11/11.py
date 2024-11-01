from cleaning_state import CleaningState
from pure_robot import RobotState, move, turn, set_state, start, stop
from state_monad import StateMonad

initial_state = RobotState(x=0, y=0, angle=0, state=CleaningState.WATER)
monad = StateMonad(initial_state)
monad = (monad >> move(100) >> turn(-90) >> set_state('soap') >> start() >> move(50) >> stop())

for output in monad.outputs:
    print(output)
