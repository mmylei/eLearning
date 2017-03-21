import MySQLdb
from PIL import Image, ImageDraw
import os

size = (512, 64)
backgroud = (255, 255, 255, 255)
color = (51, 153, 255, 1)
linewidth = 1
dir = "./"

def draw_rect(img, coor, color):
    im2 = Image.new('RGBA', size, (255, 255, 255, 0))
    draw2 = ImageDraw.Draw(im2)
    draw2.rectangle(coor, color)
    return Image.alpha_composite(img, im2)


def draw_line(img, coor, color, linewidth):
    im2 = Image.new('RGBA', size, (255, 255, 255, 0))
    draw2 = ImageDraw.Draw(im2)
    draw2.line(coor, color, linewidth)
    return Image.alpha_composite(img, im2)


def draw(video_id, duration, drags):
    im_forward = Image.new('RGBA', size, backgroud)
    im_backward = Image.new('RGBA', size, backgroud)
    for drag in drags:
        x1 = int(drag[0] / duration * size[0])
        x2 = int(drag[1] / duration * size[0])
        if x1 < x2:
            im_forward = draw_line(im_forward, [(x1, 0), (x2, size[1])], color, linewidth)
            # im_forward = draw_rect(im_forward, [(x1, 0), (x2, size[1])], color)
        else:
            im_backward = draw_line(im_backward, [(x1, 0), (x2, size[1])], color, linewidth)
            # im_backward = draw_rect(im_backward, [(x2, 0), (x1, size[1])], color)
    im_forward.save(dir + video_id + '_forward.png', 'PNG')
    im_backward.save(dir + video_id + '_backward.png', 'PNG')

terms = [
        # 'COMP102.1x-4T2015',
        'COMP107x-2016_T1'
    ]

conn = MySQLdb.connect(host="localhost", user="eLearning", passwd="Mdb4Learn", db="clickstream")
for term in terms:
    print('start draw term ' + term)
    dir = term + '/'
    if not os.path.exists(dir):
        os.mkdir(dir)
    table_name = ('HKUSTx-' + term + '-clickstream').replace('-', '_').replace('.', '_')
    cursor = conn.cursor()
    cursor.execute('SELECT distinct(user_id) FROM ' + table_name + ';')
    tables = cursor.fetchall()
    if len(tables) == 0:
        continue
    cursor.execute('SELECT distinct(video_id) FROM ' + table_name + ';')
    result = cursor.fetchall()
    for row in result:
        if row[0] is None:
            continue
        video_id = row[0]
        print('start draw video ' + video_id)
        cursor.execute('SELECT old_time, new_time'
                       ' FROM ' + table_name +
                       ' WHERE video_id=\'' + video_id + '\' and event_type=\'seek_video\';')
        result_video = cursor.fetchall()
        drags = []
        for time in result_video:
            if time[0] is not None and time[1] is not None:
                drags.append((float(time[0]), float(time[1])))
        cursor.execute('SELECT duration'
                       ' FROM eLearning.Video_Basic_Info'
                       ' WHERE video_id=\'' + video_id + '\';')
        d_result = cursor.fetchall()
        if len(d_result) == 0:
            print 'cannot find video info:', video_id
            continue
        duration = float(d_result[0][0])
        draw(video_id, duration, drags)
