import sys

if __name__ == "__main__":
    user = sys.argv[1].strip()
    user_group = sys.argv[2].strip()
    working_directory = sys.argv[3].strip()

    with open('gunicorn.service.template', 'r') as f:
        tmp = "".join(f.readlines())
    with open('gunicorn.service', 'w') as f:
        f.writelines(tmp.format(**{"user": user, "user_group": user_group, "working_directory": working_directory}))
