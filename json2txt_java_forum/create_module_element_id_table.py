import json_wrapper
import MySQLdb
import sys


def create_table(conn, table):
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS `" + table + "`;")
    conn.commit()
    c.execute("CREATE TABLE " + table + "(module_id varchar(32), module_name varchar(64),"
                                        "element_type varchar(64), element_id varchar(64));")
    conn.commit()


def insert_table(conn, p, table):
    c = conn.cursor()
    c.execute("INSERT INTO " + table + " VALUES(%s, %s, %s, %s);", p)
    conn.commit()


def process(file_name, conn, term, module_id, split_type, split_id):
    f = open(file_name)
    term = term.replace('.', '_').replace('-', '_')
    create_table(conn, term + '_element')
    element = {}
    obj = json_wrapper.loads(f.read())
    discussion_dict = {}
    for key in obj:
        if split_type(key) == 'discussion' and 'discussion_id' in obj[key]['metadata']:
            discussion_dict[split_id(key)] = obj[key]['metadata']['discussion_id']
    for key in obj:
        child = []
        if split_type(key) == 'course':
            continue
        else:
            for children in obj[key]['children']:
                if split_type(children) == 'discussion':
                    child.append(split_type(children) + '@' + discussion_dict[split_id(children)])
                else:
                    child.append(split_type(children) + '@' + split_id(children))
            element[split_type(key) + '@' + split_id(key)] = child
    for mid in module_id:
        name = mid.split('@')[0]
        num = mid.split('@')[-1]
        sequential = element['chapter@' + num]
        for sqt in sequential:
            vertical = element[sqt]
            for vert in vertical:
                real_element = element[vert]
                for relment in real_element:
                    if len(element[relment]) > 0:
                        lib_problem = element[relment]
                        for lproblem in lib_problem:
                            eid = lproblem.split('@')[-1]
                            etype = lproblem.split('@')[0]
                            print(etype + ' ' + eid)
                            text = [num, name, etype, eid]
                            insert_table(conn, text, term + '_element')
                    else:
                        eid = relment.split('@')[-1]
                        etype = relment.split('@')[0]
                        print(etype + '-------' + eid)
                        text = [num, name, etype, eid]
                        insert_table(conn, text, term + '_element')

    f.close()

if __name__ == '__main__':
    old_terms = ['102.1x-2T2015', '102.1x-2T2016', '102.1x-4T2015', '102.2x-1T2016', '102.2x-2T2016', '102.2x-4T2015',
             '102x-2T2014', '102.1x-3T2016', '102.2x-3T2016']
    # terms = ['102.1x-2T2015']

    java_2terms = ['COMP102.2x-2T2016', 'COMP102.2x-4T2015',
                   'COMP102.2x-3T2016', 'COMP102.2x-1T2016']
    # java_table_prefix = [x.replace('.', '_').replace('-', '_') for x in java_terms]
    java_1terms = ['COMP102.1x-4T2015']
    # 'COMP102.1x-2T2015', 'COMP102.1x-2T2016', 'COMP102.1x-3T2016']

    java_2xterm = ['COMP102x-2T2014']

    android_terms = ['COMP107x-2016_T1']
    # android_table_prefix = [x.replace('.', '_').replace('-', '_') for x in android_terms]

    speaking_terms = ['EBA101x-1T2016', 'EBA101x-3T2014']

    speaking_terms2014 = [ 'EBA101x-3T2016']
    # speaking_table_prefix = [x.replace('.', '_').replace('-', '_') for x in speaking_terms]

    writing_terms = ['EBA102x-1T2016', 'EBA102x-4Q2015']
    # have not create table for this term yet
    writing_terms4q2015 = []

    writing_terms3T2016 = ['EBA102x-3T2016']
    # writing_table_prefix = [x.replace('.', '_').replace('-', '_') for x in writing_terms]

    dir = sys.argv[1]
    if not dir.endswith('/'):
        dir += '/'
    conn = MySQLdb.connect(host="localhost", user="eLearning", passwd="Mdb4Learn", db="eLearning")
    terms = speaking_terms
    #Java_102.1x
    # module_id = ['pre@ae687c1204b84885a4797f517715722a', 'M01@1ee4603833d742e698d27695d2aa25b5',
    #              'M02@db78e7f298c345f3af42589e06c470a2', 'M03@b57525ba4b974719b9ce4eca914e1c39',
    #              'M04@668fb99bb9684644822889e460197fe9', 'M05@3f0585f6e4574bac95384a227d50ef5f',
    #              'Exam@1020d90b174142239fcdefc2f8555d55', 'post@fd8a124c47d940dfa7d88a8ac37a7cc5']
    #Java_102.2x
    # module_id = ['pre@ae687c1204b84885a4797f517715722a', 'M01@2dedce7b2d7240d59bd69fed8ed6d375',
    #              'M02@0e9380db36894e7cbd23b50742464bf2', 'M03@356a9cd3ced348f18695f1c2e3202196',
    #              'M04@5ce89fe48f9e4cb8adc08c83c29da49f', 'M05@a889242857844579902cda2842e3a84b',
    #              'Exam@1020d90b174142239fcdefc2f8555d55', 'post@fd8a124c47d940dfa7d88a8ac37a7cc5']
    #Android
    # module_id = ['pre@72365fc2f807409582f1db38f3ac6879', 'M01@234fa80753b1476592ae17d37b17bb9e',
    #              'M02@9fd029452bf2495f819dd083fe769a5d', 'M03@b254be2e401a44a794c1a6961adffcc5',
    #              'M04@4f6e3c6c28564d2f84289d7eaceebcb1', 'M05@93ca675ee54240d79cddc6219556011f']

    # Speaking
    module_id = ['pre@7bb6213618344dd9a3d6eed0679cd1da', 'M01@786a1e9b72a4426aa0faae7ea8dfd458',
                 'M02@9f97ebac81584d4d82c2278c04466f72', 'M03@0347ec2e8ed84434a3ffdd0aeb9b29ca',
                 'M04@8dfb41aede1b4adc98354c5ff05335d8', 'M05@d49f74961ee74674950be979f2365f82',
                 'M06@d0f02e09d13c41d1a1e1135ecb54cbe9', 'M07@c588e52413634310b2fd1aa257f840e3',
                 'post@428e6b7750e54d92a2c5bae1561a3b62']

    # Writing 1T2016
    # module_id = ['pre@4efc576a67bc4d3f97c9e5826cc1af83', 'M01@df20fa07b6ae4e84bd0d51cd7c407e56',
    #              'M02@174183c4cc9844508e4a98556614b7f0', 'M03@16b9fe2877fc413d88e2a0008a85b36e',
    #              'M04@81f50f96e4c44d87ae19452270f1aa6d', 'M05@d2e89afb6cd743218d80f92272c98bff',
    #              'M06@60ffad0df6d94b8f8016ede87ebca6bd', 'M07@2406dcc97b9c4aa1a2b8fd8ebd38d7b7',
    #              'post@7bcb47d024034947b7db98ebc1a0d8b5']

    # Writing 3T2016
    # module_id = ['pre@e6495aee35324f588fd4c87963b4b841', 'M01@df20fa07b6ae4e84bd0d51cd7c407e56',
    #              'M02@174183c4cc9844508e4a98556614b7f0', 'M03@16b9fe2877fc413d88e2a0008a85b36e',
    #              'M04@81f50f96e4c44d87ae19452270f1aa6d', 'M05@d2e89afb6cd743218d80f92272c98bff',
    #              'M06@60ffad0df6d94b8f8016ede87ebca6bd', 'M07@2406dcc97b9c4aa1a2b8fd8ebd38d7b7',
    #              'post@7bcb47d024034947b7db98ebc1a0d8b5']

    for term in terms:
        file_name = dir + "HKUSTx-" + term + "-course_structure-prod-analytics.json"
        if term in ['COMP102x-2T2014', 'EBA101x-3T2014', 'EBA102x-4Q2015']:
            process(file_name, conn, term, module_id, lambda x: x.split('/')[-2], lambda x: x.split('/')[-1])
        else:
            process(file_name, conn, term, module_id, lambda x: x.split('@')[-2].split('+')[0], lambda x: x.split('@')[-1])
    conn.close()
