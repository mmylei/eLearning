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
    old_terms = ['102.1x-2T2015', '102.1x-2T2016', '102.1x-4T2015', '102.2x-1T2016', '102.2x-2T2016', '102.2x-4T2015',
             '102x-2T2014', '102.1x-3T2016', '102.2x-3T2016']
    # terms = ['102.1x-2T2015']

    java_terms = ['102.1x-2T2015', '102.1x-2T2016', '102.1x-4T2015', '102.2x-1T2016', '102.2x-2T2016', '102.2x-4T2015',
                  '102x-2T2014', '102.1x-3T2016', '102.2x-3T2016']
    # java_table_prefix = [x.replace('.', '_').replace('-', '_') for x in java_terms]

    android_terms = ['107x-3T2016', '107x-2016_T1', '107x-1T2016']
    # android_table_prefix = [x.replace('.', '_').replace('-', '_') for x in android_terms]

    speaking_terms = ['101x-3T2016', '101x-3T2014', '101x-1T2016']
    # speaking_table_prefix = [x.replace('.', '_').replace('-', '_') for x in speaking_terms]

    writing_terms = ['102x-4Q2015', '102x-3T2016', '102x-1T2016']
    # writing_table_prefix = [x.replace('.', '_').replace('-', '_') for x in writing_terms]

    dir = sys.argv[1]
    if not dir.endswith('/'):
        dir += '/'
    conn = MySQLdb.connect(host="localhost", user="eLearning", passwd="Mdb4Learn", db="eLearning")
    terms = speaking_terms
    for term in terms:
        file_name = dir + "HKUSTx-EBA" + term + "-prod.mongo"
        process(file_name, conn, term)
    conn.close()
