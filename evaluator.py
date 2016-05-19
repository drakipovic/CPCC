import os
import subprocess
from datetime import datetime

from celery import Celery
import yaml

from models import Submission


basedir = os.path.abspath(os.path.dirname(__file__))
DEST_FOLDER = basedir + '/contest_source_code/'
INPUT_FOLDER = basedir + '/input_files/task_'
OUTPUT_FOLDER = basedir + '/output_files/task_'
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
    
    os.system(command.format(DEST_FOLDER + source_code_name, DEST_FOLDER + remove_extension(source_code_name)))
    source_code_name = remove_extension(source_code_name)
    task_id = task.task_id
    status = True

    for input_file in os.listdir(INPUT_FOLDER + str(task_id)):
        user_output = subprocess.check_output(DEST_FOLDER + source_code_name + "< " + INPUT_FOLDER  + str(task_id) + '/' + input_file, shell=True)
        input_num = input_file.split('_')[1].split('.')[0]

        with open(OUTPUT_FOLDER + str(task_id) + '/' + 'output_' + input_num + '.txt') as f:
            output = f.readline()
            print output        
        status = user_output == output        
    
    accepted = 'Accepted' if status else 'Wrong Answer'

    submission = Submission(accepted, extension, datetime.utcnow(), task.name, user_id, task.task_id, contest.contest_id)
    submission.save()
