from display import app, db
from display.model import Jobs, PrettyJobs, Monitor, required_jobs, Builds, Changes

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Jobs': Jobs, 'PrettyJobs':PrettyJobs, 'Monitor':Monitor, 'required_jobs':required_jobs, 'Builds':Builds, 'Changes':Changes }

