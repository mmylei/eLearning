import MySQLdb

user_id = [524811, 2135908, 2314026, 2454324, 2546039]
for uid in user_id:

    sql1 = 'select user_id, video_id, sum(video_time_end - video_time_start) as watched_duration from clickstream.HKUSTx_COMP102_1x_4T2015_video_play_piece where user_id ='+ str(uid) + ' group by user_id, video_id;'
    sql2 = 'select video_id, sequence, duration from Video_Basic_Info where module_number < 6 order by sequence;'
    conn = MySQLdb.connect(host="localhost", user="eLearning", passwd="Mdb4Learn", db="eLearning")

    cursor = conn.cursor()
    cursor.execute(sql2)
    result2 = cursor.fetchall()
    cursor.execute(sql1)
    result1 = cursor.fetchall()
    result = []
    sequence = []
    for row in result2:
        sequence.append(row[1])
        found = False
        for row1 in result1:
            if row1[1] == row[0]:
                result.append(float(row1[2])/row[2])
                found = True
        if not found:
            result.append(0)

    content = 'x\tvideo_id\t' + '\t'.join([str(x) for x in sequence]) + '\n'
    content += 'y\tratio\t' + '\t'.join(['0', '0.5', '1', '1.5', '2', '2.5']) + '\n'
    content += 'xtick\t' + '\t'.join([str(x) for x in range(len(sequence))]) + '\n'
    content += 'ytick\t' + '\t'.join(['0', '0.5', '1', '1.5', '2', '2.5']) + '\n'
    content += 'data\tdata\t' + '\t'.join([str(x) for x in result]) + '\n'

    with open('./figure_data/' + str(uid) + '.bd', 'w') as f:
        f.write(content)
