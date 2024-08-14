def reward_function(params):
    '''
    Example of rewarding the agent to follow center line
    '''
    reward = 0.001
    # Read input parameters
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    speed = params['speed']
    
    if  params['is_offtrack']:
        return reward
        
    if params['is_reversed']:
        return reward
        
    if params['is_crashed']:
        return reward
    
    # This will penalize if agent is slower than 1m/s and give quadratic rewards if agent is over 1m/s
    return float(speed * speed)