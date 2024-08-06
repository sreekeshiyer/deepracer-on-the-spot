def reward_function(params):
    '''
    Reward function for AWS DeepRacer
    '''
    # Read input parameters
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    steering_angle = abs(params['steering_angle']) # only need the absolute steering angle
    speed = params['speed']
    progress = params['progress']
    all_wheels_on_track = params['all_wheels_on_track']

    # Define the reward parameters
    center_line_reward = 100.0
    speed_reward = 100.0
    curve_penalty = 100.0
    off_track_penalty = 100.0
    
    # Reward for staying on the center line
    if distance_from_center <= 0.1 * track_width:
        center_line_reward *= 1.0
    elif distance_from_center <= 0.25 * track_width:
        center_line_reward *= 0.5
    elif distance_from_center <= 0.5 * track_width:
        center_line_reward *= 0.2
    else:
        center_line_reward = 1e-3  # likely very close to off track or off track

    # Reward for speed, higher speed on straight paths
    if steering_angle < 10: # straight path
        if speed > 3.2:
            speed_reward *= 1.0
        else:
            speed_reward *= 0.5
    else: # for curves
        if speed < 2.6:
            speed_reward *= 1.0
        else:
            speed_reward = 1e-3

    # Penalize if the car goes off track
    if not all_wheels_on_track:
        off_track_penalty = 1e-3

    # Calculate the final reward
    reward = (center_line_reward + speed_reward) / 2 * off_track_penalty

    return float(reward)

