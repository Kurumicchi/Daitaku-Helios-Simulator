def is_peace(hand):
    """
    Detect a normal peace sign.

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
    Detect one upside-down peace sign.

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
    Detect two upside-down peace signs.
    """

    if len(hands) != 2:
        return False

    return (
        is_upside_down_peace(hands[0])
        and is_upside_down_peace(hands[1])
    )