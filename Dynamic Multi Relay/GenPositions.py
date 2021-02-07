
from random import randint

def random_generate_positions(n_fd, n_ru, x_, _x, y_, _y):
    positions = {
        'RUs':[],
        'FDs':[],
        'BS': [(x_ + _x) / 2, (y_ + _y) / 2]
    }


    for i in range(0, n_fd):
        temp_p = [randint(x_, _x), randint(y_, _y)]
        positions["FDs"].append(temp_p)

    for i in range(0, n_ru):
        temp_p = [randint(x_, _x), randint(y_, _y)]
        positions["RUs"].append(temp_p)

    return positions

if __name__ == '__main__':
    positions = random_generate_positions(100, 5, 0, 1000, 0, 1000)

    cnt = 0
    for i in positions["FDs"]:
        print '[',i[0],',',i[1],']',',',
        cnt += 1
        if cnt % 10 == 0:
            print
    print

    for i in positions['RUs']:
        print '[', i[0], ',', i[1], ']',',',
    print

    print '[',positions["BS"][0],',',i[1],']'