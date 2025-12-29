
import time
from abc import ABC, abstractmethod
from collections import namedtuple
from functools import wraps

# ---------------- Q4 & Q9: Decorators ---------------- #

def log_execution(enabled=True):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if enabled:
                print(f"[LOG] Executing {func.__name__}")
            return func(*args, **kwargs)
        return wrapper
    return decorator


def time_execution(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"[TIME] {func.__name__} took {time.time() - start:.4f}s")
        return result
    return wrapper


def require_admin(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if self.get_role() != "ADMIN":
            raise PermissionError("Admin access required")
        return func(self, *args, **kwargs)
    return wrapper

# ---------------- Q1, Q2, Q3: User Modeling ---------------- #

class User(ABC):
    active_user_count = 0

    def __init__(self, user_id, name, email):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.active = True
        User.active_user_count += 1

    def deactivate(self):
        if self.active:
            self.active = False
            User.active_user_count -= 1

    @classmethod
    def from_string(cls, data):
        user_id, name, email = data.split(",")
        return cls(int(user_id), name, email)

    @staticmethod
    def is_valid_email(email):
        return "@" in email and "." in email

    @abstractmethod
    def get_role(self):
        pass

    def __str__(self):
        return f"{self.get_role()} User: {self.name}"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.user_id}, {self.name}, {self.email})"

    def __len__(self):
        return len(self.name)

    def __eq__(self, other):
        return self.user_id == other.user_id

    def __lt__(self, other):
        return self.user_id < other.user_id

    def __call__(self):
        return f"Callable User {self.name}"


class AdminUser(User):
    def get_role(self):
        return "ADMIN"

    @require_admin
    @log_execution()
    def delete_user(self):
        print("User deleted")


class RegularUser(User):
    def get_role(self):
        return "REGULAR"


# ---------------- Q5: Generator ---------------- #

class UserRepository:
    def __init__(self, users):
        self.users = users

    def stream_users(self):
        for user in self.users:
            yield user


# ---------------- Q6: Immutable Data ---------------- #

Config = namedtuple("Config", ["app_name", "version"])


class AppConfig:
    def __init__(self):
        self.config = Config("UserSystem", "1.0.0")


# ---------------- Q7: Loop-Else ---------------- #

def find_user(users, user_id):
    for user in users:
        if user.user_id == user_id:
            return user
    else:
        print("User not found")


# ---------------- Q10 & Q8: Main Execution ---------------- #

@time_execution
def main():
    admin = AdminUser(1, "Akash", "akash@test.com")
    user = RegularUser.from_string("2,Rahul,rahul@test.com")

    print(admin)
    print(repr(user))
    print("Active users:", User.active_user_count)

    print("Email valid:", User.is_valid_email(user.email))
    print("Name length:", len(admin))
    print("Callable:", admin())

    repo = UserRepository([admin, user])
    for u in repo.stream_users():
        print("Streamed:", u)

    find_user([admin, user], 99)

    config = AppConfig()
    print(f"Config: {config.config.app_name} v{config.config.version}")

    admin.delete_user()


if __name__ == "__main__":
    main()
