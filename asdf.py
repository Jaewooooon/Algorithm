# 1. 내 공과 목표 공이 있을 때 어떤 홀에 넣을지 정하기

import math

HOLES = [[0, 0], [127, 0], [254, 0], [0, 127], [127, 127], [254, 127]]
r = 5.73 / 2


def find_distance1(s, e):
    x1, y1 = s
    x2, y2 = e

    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def find_distance(mine, hole, target):
    a = find_distance1(mine, hole)
    b = find_distance1(hole, target)
    c = find_distance1(target, mine)

    return a, b, c


# 1. 목적공으로부터 내 공의 각도가 기준/ 나 - 목적공 - 6개의 홀을 이루는 각도를 계산해서 가장 각도가 큰(힘을 잘 전달할 수 있는 공 선택) 홀 고르기
# 타겟 홀을 정하는 함수 - 각도가 큰 순으로 리스트에 담아두자
# (내공좌표, 표적공좌표, 홀리스트[])
def find_target_hole(mine, target):
    hole_priority = []

    for i in range(len(HOLES)):
        hole = HOLES[i]
        a, b, c = find_distance(mine, hole, target)

        mth_angle = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))

        print(f"mth = {mth_angle}")

        if abs(math.degrees(mth_angle)) >= 91:
            hole_priority.append([i, mth_angle])

    hole_priority.sort(reverse=True, key=lambda x:x[1])

    print(hole_priority)

    return hole_priority

find_target_hole([220, 60], [170, 60])


# 2. 경로에 장애물이 있는지 확인하기
# 내공 / 목표공 / 홀이 정해졌으면 장애물 검사
def is_disrupted(mine, hole, target):
    x, y = mine
    hx, hy = hole
    tx, ty = target
    # 경로에 장애물이 있는지 확인하는 방법
    # 직선의 방정식을 구하고 범위안에 다른 공과 직선의 거리가 지름보다 가까우면 장애물존재
    # 1. 내공 - 목표공 사이의 장애물
    slope1, y_intercept1 = line_equation(mine, target)




    slope2, y_intercept2 = line_equation(target, hole)




    pass


# 장애물이 없으면 슛


def line_equation(mine, hole):
    x, y = mine
    hx, hy = hole

    slope = (hy - y) / (hx - x)

    y_intercept = y - slope * x

    return slope, y_intercept


def angle_type(mine, hole, target):
    x, y = mine
    hx, hy = hole
    tx, ty = target

    slope, y_intercept = line_equation(mine, hole)

    print(slope, y_intercept)
    # 내공 기준 홀의 위치 -
    # 오른쪽 위 -  일차방정식에 타겟의 x좌표를 넣었을 때 y보다 크면
    if hx >= x and hy >= y:
        print()
        if ty <= slope * tx + y_intercept:
            print("as")
            return True
    # 왼쪽 위 - 일차방정식에 타겟의 x좌표를 넣었을 때 y보다 크면 오른쪽
    elif hx <= x and hy >= y:
        if ty <= slope * tx + y_intercept:
            return True

    # 왼쪽 아래
    elif hx <= x and hy <= y:
        if ty >= slope * tx + y_intercept:
            return True

    # 오른쪽 아래
    elif hx >= x and hy >= y:
        if ty >= slope * tx + y_intercept:
            return True

    return False


def shoot(mine, hole, target):
    x, y = mine
    hx, hy = hole
    tx, ty = target
    # 필요한 것 - 나홀표
    # a = 내공부터 홀까지 거리
    # b = 홀부터 표적까지 거리
    # c = 표적부터 내공까지 거리
    a, b, c = find_distance(mine, hole, target)
    print(f"a = {a}, b = {b}, c={c}")

    # 가 = 내공기준 홀방향 각도
    hole_abs_angle = math.atan2((hx - x), (hy - y))
    print(f"hole_abs_angle = {math.degrees(hole_abs_angle)}")

    # 공이 직선기준 오른쪽인지 왼쪽인지 판별해야 함
    # 공위치와 홀위치 비교 -> 직선의방정식 구하기 -> 타겟공의 방향 구하기 ->
    is_plus = angle_type(mine, hole, target)

    # 내공이 목적구를 쳐야 할 각도를 계산하기 위해 목적지까지 거리를 알아야 함
    # 다 : 나-홀-타겟 각도
    mht_angle = math.acos((a ** 2 + b ** 2 - c ** 2) / (2 * a * b))
    print(f"mht_angle = {math.degrees(mht_angle)}")

    # d 의 길이
    d = math.sqrt(a ** 2 + (b + 2 * r) ** 2 - 2 * a * (b + 2 * r) * math.cos(mht_angle))
    print(f"d = {d}")

    destination_angle = math.acos((a ** 2 + d ** 2 - (b + 2 * r) ** 2) / (2 * a * d))
    print(f"destination angle = {math.degrees(destination_angle)}")

    if is_plus:
        shooting_angle = hole_abs_angle + destination_angle
    else:
        shooting_angle = hole_abs_angle - destination_angle

    distance = d + b + 2 * r

    power = distance * 1
    return (shooting_angle, power)


# mine = [50, 50]
# target = [40.01, 60]
# hole = [30, 70]

# mine = [50, 50]
# target = [40.01, 40]
# hole = [30, 30]
#
# mine = [10, 10]
# target = [30, 30]
# hole = [50, 50]
#
# angle, power = shoot(mine, hole, target)
# print(math.degrees(angle), power)

# mine = [100, 100]
# # target = [80, 20]
# target = [20, 80]
# hole = [0, 0]
#
# angle, power = shoot(mine, hole, target)
# print(math.degrees(angle), power)
#
# mine = [100, 100]
# target = [80, 20]
# # target = [20, 80]
# hole = [0, 0]
#
# angle, power = shoot(mine, hole, target)
# print(math.degrees(angle), power)


# 1 -1. 1사분면
# mine = [0, 0]
# target = [20, 80]
# hole = [100, 100]
#
# angle, power = shoot(mine, hole, target)
# print(math.degrees(angle), power)
#
# # 1 -2. 1사분면에서
#
# mine = [0, 0]
# target = [80, 20]
# hole = [100, 100]
#
# angle, power = shoot(mine, hole, target)
# print(math.degrees(angle), power)
