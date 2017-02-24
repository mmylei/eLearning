import json_wrapper
import MySQLdb
import sys
import commentthread, comment


def process(file_name, conn, term):
    f = open(file_name)
    line = f.readline()
    term = term.replace('.', '_').replace('-', '_')
    commentthread.create_table(conn, term + '_commentthread')
    comment.create_table(conn, term + '_comment')
    while line:
        obj = json_wrapper.loads(line)
        if obj['_type'] == "CommentThread":
            commentthread_text = [obj['_id']['$oid'], obj['votes']['up_count'], obj['votes']['down_count'],
                                  obj['votes']['count'], obj['votes']['point'], obj['thread_type'], obj['comment_count'],
                                  obj['title'], obj['body'], obj['updated_at']['$date'], obj['created_at']['$date'],
                                  obj['last_activity_at']['$date'], obj['commentable_id'].split('-')[-1], obj['author_id'], obj['author_username']]
            commentthread.insert_table(conn, commentthread_text, term + '_commentthread')

        if obj['_type'] == "Comment":
            comment_text = [obj['comment_thread_id']['$oid'], obj['votes']['up_count'], obj['votes']['down_count'],
                                  obj['votes']['count'], obj['votes']['point'],
                                  obj['body'], obj['updated_at']['$date'], obj['created_at']['$date'], obj['author_id'], obj['author_username']]
            comment.insert_table(conn, comment_text, term + '_comment')
        line = f.readline()
    f.close()

if __name__ == '__main__':
    terms = ['102.1x-2T2015', '102.1x-2T2016', '102.1x-4T2015', '102.2x-1T2016', '102.2x-2T2016', '102.2x-4T2015',
             '102x-2T2014', '102.1x-3T2016', '102.2x-3T2016']
    # terms = ['102.1x-2T2015']
    dir = sys.argv[1]
    if not dir.endswith('/'):
        dir += '/'
    conn = MySQLdb.connect(host="localhost", user="eLearning", passwd="Mdb4Learn", db="eLearning")
    for term in terms:
        file_name = dir + "HKUSTx-COMP" + term + "-prod.mongo"
        process(file_name, conn, term)
    conn.close()
