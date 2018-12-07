from datetime import datetime

COLOR_FILE="./data/colors.csv"

def get_rgb(offset):
    print('offset: {}'.format(offset))
    now = datetime.now()
    NY_offset = -5
    search_offset = offset - NY_offset
    print('overall offset: {}'.format(search_offset))
    print('NOW: {}:{}:{}'.format(now.hour, now.minute, now.second))
    midnight = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    seconds = (now - midnight).seconds
    print('seconds before: {}'.format(seconds))
    seconds += search_offset * 60 * 60
    print('seconds after: {}'.format(seconds))
    seconds %= (60 * 60 * 24)
    print('modding by: {}'.format(60 * 60 * 24))
    print('seconds after: {}'.format(seconds))
    print('which is basically: {}:{}:{}'.format(int(seconds / (60 * 60)), int(seconds / (60) % 60), seconds % 60))

    print('SECONDS: {}'.format(seconds))
    index = int(seconds / 108)
    print('INDEX: {}'.format(index))

    with open(COLOR_FILE) as f:
        text = f.read()
        color_list = [i.split(',') for i in text.split('\n')]

        print('LEN OF COLOR LIST: {}'.format(len(color_list)))

        print('Color now: {}\n\n'.format(color_list[index]))

    return color_list[index]


if __name__ == '__main__':
    get_rgb(-3)
    get_rgb(-8)
    get_rgb(-5)
    get_rgb(5)
