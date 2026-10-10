while True:
    name = input("who are you? ")
    if name != 'Joe':
        continue
    passw = input("what's the pass: ")
    if passw == 'nana':
        break
    print("done get in")
