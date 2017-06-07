import MySQLdb

user_id = [524811, 2135908, 2314026, 2454324, 2546039]
very_poor_uid = [386558, 696595, 1102783, 3240464, 3821755]
poor_uid = [4026932, 2639832, 7768096, 8730616, 7186222]
for uid in poor_uid:

    sql1 = 'select video_id, coverage from clickstream.HKUSTx_COMP102_1x_4T2015_user_video where user_id = ' + str(uid) + ';'
    sql2 = 'select video_id, sequence from Video_Basic_Info where module_number < 6 order by sequence;'
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
                result.append(float(row1[1]))
                found = True
        if not found:
            result.append(0)

    content = 'x\tvideo_id\t' + '\t'.join([str(x) for x in sequence]) + '\n'
    content += 'y\tcoverage\t' + '\t'.join(['0', '0.2', '0.4', '0.6', '0.8', '1.0']) + '\n'
    content += 'xtick\t' + '\t'.join([str(x) for x in range(len(sequence))]) + '\n'
    content += 'ytick\t' + '\t'.join(['0', '0.2', '0.4', '0.6', '0.8', '1.0']) + '\n'
    content += 'data\tdata\t' + '\t'.join([str(x) for x in result]) + '\n'

    with open('./figure_data/' + str(uid) + '.ld', 'w') as f:
        f.write(content)
