def lerp(start, end, value):
    return (value * end) + ((1-value) * start)

def q_lerp(value : float, ease : float):
    """convert a linear value to an eased value accrding to the smoothness (0->1)"""
    return pow(value,ease) / (pow(value,ease) + pow(1-value,ease))

def clamp(value, minimum, maximum):
    return max(minimum,min(maximum,value))