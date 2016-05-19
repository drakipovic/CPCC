from collections import defaultdict
import operator

from models import User

def get_contest_statistics(contest_submissions):
    accepted_tasks = set()
    
    for submission in contest_submissions:
        if submission.status == 'Accepted':
            user = User.query.get(submission.user_id)
            accepted_tasks.add((user.username, submission.task_id))


    results = defaultdict(int)
    for user_task in accepted_tasks:
        results[user_task[0]] += 1
    
    results = sorted(results.items(), key=operator.itemgetter(1), reverse=True)
    print results
    return results
