
import os
import sys
lib_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'manager'))
sys.path.append(lib_path)

import Manager

def main():
    print("main()")
    m = Manager.Manager()
    m.Run()

if __name__ == '__main__':
    main()