import sys

if __name__ == "__main__":
    port = sys.argv[1].strip()
    server_names = sys.argv[2].strip()
    working_directory = sys.argv[3].strip()

    with open('nginx.service.template', 'r') as f:
        tmp = "".join(f.readlines())
    with open('nginx.service', 'w') as f:
        f.writelines(
            tmp.format(**{"port": port, "server_names": server_names, "working_directory": working_directory}).replace(">>>", "}").replace(
                "<<<", "{"))
