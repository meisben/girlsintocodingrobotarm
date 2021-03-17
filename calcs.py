import math

x = 0
y = 0

len_1 = 9
len_2 = 9

current_theta_1 = 0
current_theta_2 = 0

def get_turn_angle(current, target, limit):
        diff = target - current
        if abs(diff) > (limit/2):
            return "over limit"
        else: 
            return diff

while(1):
    x = float(input("\nInput X:"))
    y = float(input("\nInput Y:"))
    # theta_2 = math.acos((x**2 + y**2 - len_1**2 - len_2**2)/(2*len_1*len_2))
    # theta_1 = math.atan2(y,x) - math.atan2((len_2*math.sin(theta_2)),(len_1+len_2*math.cos(theta_2)))

    theta_2 = math.acos(((x**2) + (y**2) - (len_1**2) - (len_2**2))/(2*len_1*len_2))
    theta_1 = math.atan2(y,x) - math.atan2((len_2*math.sin(theta_2)),(len_1+(len_2*math.cos(theta_2))))

    t_ang_1 = get_turn_angle(current_theta_1, theta_1, math.pi)
    t_ang_2 = get_turn_angle(current_theta_2, theta_2, math.pi*1.5)

    if t_ang_1 == "over limit" or t_ang_2 == "over limit":
        print("Joint angle limit error")
    else:
        current_theta_1 = theta_1
        current_theta_2 = theta_2
        t_ang_1=math.degrees(t_ang_1)
        t_ang_2=math.degrees(t_ang_2)
    print(f"\nCurrent 2 = {math.degrees(current_theta_2)} and current 1 = {math.degrees(current_theta_1)}")
    print(f"\nTheta 2 = {t_ang_2} and theta 1 = {t_ang_1}")
    x = len_1*math.cos(current_theta_1) + len_2*math.cos(current_theta_2 + current_theta_1)
    y = len_1*math.sin(current_theta_1) + len_2*math.sin(current_theta_2 + current_theta_1)
    print(f"Forward kine: X = {x}, Y = {y}")