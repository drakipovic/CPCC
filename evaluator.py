import os
import re
import subprocess
from datetime import datetime

from celery import Celery
import yaml

from models import Submission


basedir = os.path.abspath(os.path.dirname(__file__)) + "/contests/"

DEST_FOLDER = basedir + 'contest_{}/user_source/'
INPUT_FOLDER = basedir + 'contest_{}/input_files/task_{}/'
OUTPUT_FOLDER = basedir + 'contest_{}/output_files/task_{}/'
celery = Celery('evaluator', broker='amqp://guest@localhost//')


def get_extension(source_code_name):
    return source_code_name.split('.')[1]


def remove_extension(source_code_name):
    return source_code_name.split('.')[0]


def get_command(extension):
    with open(basedir + '/compiler_commands.yaml') as f:
        return yaml.load(f).get(extension, None)


@celery.task
def evaluate(source_code_name, user_id, task, contest):
    extension = get_extension(source_code_name)
    command = get_command(extension)
    contest_id = contest.contest_id

    os.system(command.format(DEST_FOLDER.format(contest_id) + source_code_name, DEST_FOLDER.format(contest_id) + remove_extension(source_code_name)))
    source_code_name = remove_extension(source_code_name)
    task_id = task.task_id
    status = True

    for input_file in os.listdir(INPUT_FOLDER.format(contest_id, task_id)):
        if get_extension(input_file) == 'zip': continue
        user_output = subprocess.check_output(DEST_FOLDER.format(contest_id) + source_code_name + "< " + INPUT_FOLDER.format(contest_id, task_id) + input_file, shell=True)
        user_output = re.sub('[\s+]\\n', '\n', user_output)
        user_output = user_output.strip()
        input_num = input_file.split('_')[1].split('.')[0]


        with open(OUTPUT_FOLDER.format(contest_id, task_id) + 'out_' + input_num + '.out') as f:
            output = f.read().strip()

        print 'worker'
        print 'output\n {} \n user_output\n {}'.format(output, user_output)        
        status = user_output == output        
    
    accepted = 'Accepted' if status else 'Wrong Answer'

    submission = Submission(accepted, extension, datetime.utcnow(), task.name, user_id, task.task_id, contest.contest_id)
    submission.save()
