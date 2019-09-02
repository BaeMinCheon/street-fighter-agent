
import manager.Manager as Manager
import gui.Widget as Widget

def main():
    m = Manager.Manager()
    w = Widget.Widget(m)
    w.run()

if __name__ == '__main__':
    main()