
import manager.Manager as Manager
import gui.Window as Window

def main():
    print('main()')
    m = Manager.Manager()
    w = Window.Window(m)
    w.run()

if __name__ == '__main__':
    main()