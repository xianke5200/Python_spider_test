queue = []


def enQ():
    queue.append(input("Enter New Queue element: ").strip())


def deQ():
    if len(queue) == 0:
        print("Cannot pop from an empty stack!")
    else:
        print("Removed [", repr(queue.pop(0)), ']')


def viewsQ():
    print(queue)  # calls str() internally


CMDs = {'e': enQ, 'd': deQ, 'v': viewsQ}


def showmenu():
    pr = """
    (E)nqueue
    (D)equeue
    (V)iew
    (Q)uit

    Enter choice: """

    while True:
        while True:
            try:
                choice = input(pr).strip()[0].lower()
            except(EOFError, KeyboardInterrupt, IndexError):
                choice = 'q'

            print("\nYou picked: [%s]" % (choice))
            if choice not in 'uovq':
                print("Invalid option, try again")
            else:
                break

        if choice == 'q':
            break
        CMDs[choice]()


if __name__ == '__main__':
    showmenu()