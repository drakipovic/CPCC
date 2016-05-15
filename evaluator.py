import os

from celery import Celery

from main import basedir

DEST_FOLDER = basedir + '/contest_source_code/'
INPUT_FOLDER = basedir + '/input_files/'
celery = Celery('evaluator', broker='amqp://guest@localhost//')

def remove_extension(source_code_name):
    return source_code_name.split('.')[0]

@celery.task
def evaluate(source_code_name):
    os.system("g++ " + DEST_FOLDER + source_code_name + " -o " + DEST_FOLDER + remove_extension(source_code_name))
    source_code_name = remove_extension(source_code_name)
    for input_file in os.listdir(INPUT_FOLDER):
        print input_file
        os.system(DEST_FOLDER + source_code_name + "< " + INPUT_FOLDER + input_file)

    
