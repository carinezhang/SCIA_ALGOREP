from master import init

def main():
    app = init(max_size=6)
    print('Allocation of value 5555 in b:')
    v = app.allocate(5555)
    print(v)
    print('Allocation of list [1,2,3,4] in v2')
    v2 = app.allocate([i for i in range(1,5)])
    print(v2)
    print('Allocation of list [1,2,3,4,5,6,7,8,9] in v3')
    v3 = app.allocate([i for i in range(1,10)])
    print(v3)

    print('read v:', app.read(v))
    print('modify v to 56 :', app.modify(v, 56, 7))
    print('read v:', app.read(v))
    print('free v:', app.free(v))
    print('freed v value:', app.read(v))
    app.terminate_slaves()

if __name__ == "__main__":
    main()