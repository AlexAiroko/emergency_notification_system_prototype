from app.db.repositories_registry import REPOSITORIES
from app.db.session import session_maker


class UnitOfWork:
    def __init__(self):
        self.session = None

    def __enter__(self):
        self.session = session_maker()
        self.transaction = self.session.begin()
        self.transaction.__enter__()

        return self

    def __exit__(self, exc_type, exc, tb):
        self.transaction.__exit__(exc_type, exc, tb)
        self.session.close()
    
    def __getattr__(self, name: str):
        if name in REPOSITORIES:
            repo_class = REPOSITORIES[name]

            repo = repo_class(self.session)
            setattr(self, name, repo) # save repo

            return repo

        raise AttributeError(f"No repository: {name}")
