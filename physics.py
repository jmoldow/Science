def applyConstantForce(obj, forceVector, dt):
    # This is the one to use!
    # Obj is any object with two properties: .pos is a 2-tuple of position values, and .vel is a 2-tuple of velocity values.
    # Force vector is a 2-tuple.
    # We don't use the advanced force-function capability yet, we just pass a constant force.
    objInitialState = State(obj._position, obj._velocity)
    objFinalState = integrate(objInitialState, 0.0, dt, (lambda s, t: forceVector))
    obj._position = objFinalState.pos
    obj._velocity = objFinalState.vel


class State(object):
    pos = [0, 0]
    vel = [0, 0]
    def __init__(self, pos, vel):
        self.pos = pos
        self.vel = vel

class Derivative(object):
    dPos = [0, 0]
    dVel = [0, 0]
    def __init__(self, dPos, dVel):
        self.dPos = dPos
        self.dVel = dVel
        
def evaluate(initial, t, dt, derivative, accelFn):
    # Return a derivative object for RK4.
    # accelFn is a lambda function which can take up to two parameters - (a state and time dependent acceleration?)
    # right now this functionality isn't used, and we assume a constant force vector.
    # and returns a dv tuple
    state = State([0,0],[0,0])
    state.pos[0] = initial.pos[0] + derivative.dPos[0] * dt
    state.pos[1] = initial.pos[1] + derivative.dPos[1] * dt
    state.vel[0] = initial.vel[0] + derivative.dVel[0] * dt
    state.vel[1] = initial.vel[1] + derivative.dVel[1] * dt

    output = Derivative([0,0],[0,0])
    output.dPos = state.vel
    output.dVel = accelFn(state, t+dt)
    return output

def integrate(state, t, dt, accelFn):
    # Runge Kutta integration
    a = evaluate(state, t, 0, Derivative([0,0],[0,0]), accelFn)
    b = evaluate(state, t + 0.5*dt, 0.5*dt, a, accelFn)
    c = evaluate(state, t + 0.5*dt, 0.5*dt, b, accelFn)
    d = evaluate(state, t + dt, dt, c, accelFn)

    dxdt = [0,0]
    dvdt = [0,0]
    dxdt[0] = (a.dPos[0] + 2*b.dPos[0] + 2*c.dPos[0] + d.dPos[0]) / 6.0
    dxdt[1] = (a.dPos[1] + 2*b.dPos[1] + 2*c.dPos[1] + d.dPos[1]) / 6.0
    dvdt[0] = (a.dVel[0] + 2*b.dVel[0] + 2*c.dVel[0] + d.dVel[0]) / 6.0
    dvdt[1] = (a.dVel[1] + 2*b.dVel[1] + 2*c.dVel[1] + d.dVel[1]) / 6.0

    state.pos[0] = state.pos[0] + dxdt[0] * dt
    state.pos[1] = state.pos[1] + dxdt[1] * dt
    state.vel[0] = state.vel[0] + dvdt[0] * dt
    state.vel[1] = state.vel[1] + dvdt[1] * dt
    return state

if __name__ == '__main__':
    myObj = State([50,100], [0,0])
    force = (5,10)
    sec = 1.0
    print 'initial pos = ' + str(myObj.pos) + ' initial vel = ' + str(myObj.vel)
    print 'using force = ' + str(force) + ' for ' + str(sec) + ' sec.'
    applyConstantForce(myObj, force, sec)
    print 'final pos = ' + str(myObj.pos) + ' final vel = ' + str(myObj.vel)
