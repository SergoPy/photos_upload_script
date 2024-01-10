def load_proxies(filename):
    with open(filename, 'r') as file:
        proxies = file.read().splitlines()
    return proxies
