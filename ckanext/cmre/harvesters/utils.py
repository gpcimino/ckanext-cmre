def _my_log(msg):
    with open("/var/log/ckan/my_ckan.log", "a") as f:
        f.write(msg + "\n")