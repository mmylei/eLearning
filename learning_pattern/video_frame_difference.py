import cv2
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os


def draw_diff(vid):
    result = []
    cap = cv2.VideoCapture('/disk02/data/eLearning/raw_teaching_material/Java_video/' + vid + '.mp4')
    # cap = cv2.VideoCapture('/Users/maomaoyu/Desktop/4a2f0738f6074e8a887911b6df66bf1c.mp4')
    fps = cap.get(cv2.CAP_PROP_FPS)
    flag, prev_frame = cap.read()
    cv2.waitKey(10)
    while True:
        flag, frame = cap.read()
        if flag:
            s = cv2.norm(prev_frame, frame, cv2.NORM_L1)
            # print s
            result.append(s)
            prev_frame = frame
            if cv2.waitKey(10) == 27:
                break
        else:
            break

    plt.figure(figsize=(9.6, 9.6))
    # plt.plot(range(width), count_repeat)
    # plt.plot(range(width), count_distinct)
    plt.plot(result)
    frame_count = len(result)
    plt.xlabel('Video Time(Second)', fontsize=5)
    ticks = range(0, frame_count, frame_count / 10)
    labels = [str(x / fps) for x in ticks]
    plt.xticks(ticks, labels, fontsize=5)
    plt.ylabel('Difference', fontsize=5)
    # plt.yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5], ['1', '1.1', '1.2', '1.3', '1.4', '1.5'], fontsize=5)
    plt.savefig('./diff_images/frame_diff_' + vid + '.eps', bbox_inches='tight', pad_inches=0)
    # plt.savefig('4a2f0738f6074e8a887911b6df66bf1c.eps', bbox_inches='tight', pad_inches=0)


for file in os.listdir('/disk02/data/eLearning/raw_teaching_material/Java_video/'):
    if file.split('.')[-1] == 'mp4':
        draw_diff(file.split('.')[0])
# draw_diff('4a2f0738f6074e8a887911b6df66bf1c')
