import Server
import Agent


def main():
    s = Server.Server('127.0.0.1', 7000)
    a = Agent.Agent()

    while True:
        s.Accept()

        while True:
            if s.Receive():
                s.Print()

                a.Train(s.GetFeatures())

                s.Send(a.Action())
            else:
                break


if __name__ == '__main__':
    main()