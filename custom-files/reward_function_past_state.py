class PARAMS:
    prev_speed = None
    prev_steering_angle = None
    prev_steps = None
    prev_direction_diff = None
    prev_normalized_distance_from_route = None

def reward_function(params):
    import math

    # Read input parameters
    speed = params['speed']
    steering_angle = params['steering_angle']
    heading = params['heading']
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    is_offtrack = params['is_offtrack']
    steps = params['steps']

    # Constants
    ABS_STEERING_THRESHOLD = 5
    MAX_SPEED = 4.0
    MIN_SPEED = 2.0
    DIRECTION_THRESHOLD = 30.0
    LOOKAHEAD_COVERAGE = 3  # Number of waypoints to look ahead to calculate track direction

    # Initialize reward
    reward = 1.0

    # Calculate 3-point lookahead track direction
    def calculate_track_direction(waypoints, closest_waypoints, lookahead=3):
        next_point = waypoints[min(closest_waypoints[1] + lookahead, len(waypoints) - 1)]
        prev_point = waypoints[closest_waypoints[0]]
        track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0])
        track_direction = math.degrees(track_direction)
        return track_direction

    track_direction = calculate_track_direction(waypoints, closest_waypoints, LOOKAHEAD_COVERAGE)
    
    # Calculate the direction difference between the track direction and the car's heading direction
    direction_diff = abs(track_direction - heading)
    if direction_diff > 180:
        direction_diff = 360 - direction_diff

    # Normalize distance from center
    normalized_distance_from_route = distance_from_center / (track_width / 2.0)
    
    # Use past state stored in PARAMS
    if PARAMS.prev_speed is not None:
        # Penalize slowing down without good reason on straight portions
        if abs(steering_angle) < ABS_STEERING_THRESHOLD and speed < PARAMS.prev_speed:
            reward *= 0.8  # penalize for slowing down without a good reason on straights

        # Penalize making the heading direction worse
        if direction_diff > PARAMS.prev_direction_diff:
            reward *= 0.9
    
    # 1. Speed Reward
    if abs(steering_angle) < ABS_STEERING_THRESHOLD:
        if speed >= 3.5:
            reward += 1.0  # reward high speed on straight path
    else:
        if 2.0 < speed < 3.3:
            reward += 0.5  # reward moderate speed on curved path

    # 2. Distance from Center Line
    reward += 1 - normalized_distance_from_route  # more reward for being closer to center

    # 3. Heading Direction of the vehicle
    if direction_diff < 10.0:
        reward += 1.0  # reward for good heading direction
    elif direction_diff < 20.0:
        reward += 0.5  # lesser reward for okay heading direction

    # 4. Unpardonable Actions
    if is_offtrack or direction_diff > DIRECTION_THRESHOLD:
        reward = 1e-3  # minimum reward for going off track or bad direction difference

    # Update the stored state in PARAMS
    PARAMS.prev_speed = speed
    PARAMS.prev_steering_angle = steering_angle
    PARAMS.prev_steps = steps
    PARAMS.prev_direction_diff = direction_diff
    PARAMS.prev_normalized_distance_from_route = normalized_distance_from_route

    return float(reward)
