import json_wrapper

f = open("/Users/maomaoyu/Downloads/e-learning/HKUSTx/hkustx-2016-09-11/HKUSTx-COMP102.1x-2T2015-prod.mongo")
of1 = open('/Users/maomaoyu/Downloads/e-learning/HKUSTx/hkustx-2016-09-11/commentthread.txt', 'w')
of2 = open('/Users/maomaoyu/Downloads/e-learning/HKUSTx/hkustx-2016-09-11/comment.txt', 'w')
line = f.readline()
# types = []
comment_text = []
commentthread_text = []
while line:
    obj = json_wrapper.loads(line)
    # print(obj['_type'])
    # threadtype
    if obj['_type'] == "CommentThread":
        commentthread_text = [obj['_id']['$oid'], obj['votes']['up_count'], obj['votes']['down_count'],
                              obj['votes']['count'], obj['votes']['point'], obj['thread_type'], obj['comment_count'],
                              obj['title'], obj['body'], obj['updated_at']['$date'], obj['created_at']['$date'],
                              obj['last_activity_at']['$date']]
        # for i in range(0, len(commentthread_text)):
        #     commentthread_text[i] = str(commentthread_text[i])
        commentthread_text = [str(x) for x in commentthread_text]
        output = '\t'.join(commentthread_text)
        output = output.replace('\n', '\\n')
        output += '\n'
        of1.write(output)


    if obj['_type'] == "Comment":
        comment_text = [obj['comment_thread_id']['$oid'], obj['votes']['up_count'], obj['votes']['down_count'],
                              obj['votes']['count'], obj['votes']['point'],
                              obj['body'], obj['updated_at']['$date'], obj['created_at']['$date']]
        comment_text = [str(x) for x in comment_text]
        output = '\t'.join(comment_text)
        output = output.replace('\n', '\\n')
        output += '\n'
        of2.write(output)

    line = f.readline()
f.close()
of1.close()
of2.close()

