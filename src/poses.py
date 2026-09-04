import math


def angle_between_points(a, b, c):
    """
    Angle between three points (in degrees)
    """

    ba = (a.x - b.x, a.y - b.y)
    bc = (c.x - b.x, c.y - b.y)

    dot_product = ba[0] * bc[0] + ba[1] * bc[1]

    magnitude_ba = math.sqrt(
        ba[0] ** 2 + ba[1] ** 2
    )

    magnitude_bc = math.sqrt(
        bc[0] ** 2 + bc[1] ** 2
    )

    if magnitude_ba == 0 or magnitude_bc == 0:
        return 0

    cosine = dot_product / (magnitude_ba * magnitude_bc)
    cosine = max(-1, min(1, cosine))

    return math.degrees(math.acos(cosine))

def is_peace(hand):
    """
    Normal peace sign

    Index  = extended
    Middle = extended
    Ring   = folded
    Pinky  = folded
    """

    index_open = hand[8].y < hand[6].y
    middle_open = hand[12].y < hand[10].y
    ring_closed = hand[16].y > hand[14].y
    pinky_closed = hand[20].y > hand[18].y

    return (
        index_open
        and middle_open
        and ring_closed
        and pinky_closed
    )

def is_upside_down_peace(hand):
    """
    Upside-down peace sign

    Index  = extended downward
    Middle = extended downward
    Ring   = folded
    Pinky  = folded
    """

    index_open = hand[8].y > hand[6].y
    middle_open = hand[12].y > hand[10].y
    ring_closed = hand[16].y < hand[14].y
    pinky_closed = hand[20].y < hand[18].y

    return (
        index_open
        and middle_open
        and ring_closed
        and pinky_closed
    )

def is_gyaru_peace(hands):
    """
    Weiii! Upside-down peace signs
    """

    if len(hands) != 2:
        return False

    return (
        is_upside_down_peace(hands[0])
        and is_upside_down_peace(hands[1])
    )

def is_horizontal(a, b, tolerance=15):
    angle = math.degrees(
        math.atan2(
            b.y - a.y,
            b.x - a.x,
        )
    )

    return abs(angle) <= tolerance or abs(angle) >= 180 - tolerance

def is_helios_peace_arm(pose):
    """
    Right elbow points outward
    Right forearm folds inward
    """

    right_shoulder = pose[12]
    right_elbow = pose[14]
    right_wrist = pose[16]

    elbow_angle = angle_between_points(
        right_shoulder,
        right_elbow,
        right_wrist,
    )

    upper_arm_straight = is_horizontal(
        right_shoulder,
        right_elbow,
    )

    elbow_outward = right_elbow.x < right_shoulder.x
    wrist_inward = right_wrist.x > right_elbow.x

    return (
        upper_arm_straight
        and elbow_outward
        and wrist_inward
        and 0 <= elbow_angle <= 40
    )

def is_helios_peace(hand, pose):
    """
    Hand:
    Thumb   = extended
    Index   = extended
    Middle  = extended
    Ring    = folded
    Pinky   = folded

    Pose:
    Right elbow points outward
    Right forearm folds inward
    """

    thumb_open = hand[4].x > hand[3].x
    index_open = hand[8].y < hand[6].y
    middle_open = hand[12].y < hand[10].y
    ring_closed = hand[16].y > hand[14].y
    pinky_closed = hand[20].y > hand[18].y

    hand_pose =  (
        thumb_open
        and index_open
        and middle_open
        and ring_closed
        and pinky_closed
    )

    arm_pose = is_helios_peace_arm(pose)

    return hand_pose and arm_pose

