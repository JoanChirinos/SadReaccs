from datetime import datetime

COLOR_FILE="./data/colors.csv"

def get_rgb():
    now = datetime.now()
    midnight = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    seconds = (now - midnight).seconds

    print('SECONDS: {}'.format(seconds))
    index = int(seconds / 108)
    print('INDEX: {}'.format(index))

    with open(COLOR_FILE) as f:
        text = f.read()
        color_list = [i.split(',') for i in text.split('\n')]

        print('LEN OF COLOR LIST: {}'.format(len(color_list)))

        print('Color now: {}'.format(color_list[index]))

    return color_list[index]


if __name__ == '__main__':
    get_rgb()
