from icecream import ic


def hello():
    ic("Hello from the hello-world package!")
    return "Hello, World!"


if __name__ == "__main__":
    result = hello()
    print(result)
