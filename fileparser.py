# encoding:utf-8
from collections import defaultdict

# # parse file to get initial data
class subject():
    def __init__(self, name, group):
        self.name = name
        self.group = group


def read_assignments():
    """ Returns profs_asg which corresponds to a defaultdict whose keys
    represents professor names and its values are related to the subjects that they have"""
    profs_asg = defaultdict(set)
    with open('assignments2.txt') as p:
        for line in p.readlines():
            if line[0] == ':':
                professor = line[1:-1]
            else:
                repetitions = line.split()
                len = int(repetitions.__len__()/2)
                for n in range(len):
                    subjectName = repetitions.pop(0)
                    group = repetitions.pop(0)
                    subj = subject(subjectName, group)
                    profs_asg[professor].add(subj)
    for key, value in profs_asg.items():
        print("\n")
        print("Teacher " + key + " has assigned the following subjects:")
        for subj in value:
            print(subj.name + ' group ' + subj.group)
    return profs_asg




