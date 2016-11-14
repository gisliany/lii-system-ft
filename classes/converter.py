import platform
import subprocess

class Converter:

    def __init__(self):
        self.__system = platform.system()

        send = '''format 8
                factor on
                ftree ft_smart_grid
                basic t1 exp(0.00000114)
                basic t2 exp(0.00000171)
                and or_1 t1 t2
                end
                var MTTFval mean(ft_smart_grid)
                echo Mean time to failure
                expr MTTFval
                var varianceVal
                end
                '''
        print self.__system
        exe = subprocess.Popen(["start", "/B", "C:\Sharpe-Gui\sharpe\sharpe"], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        result = exe.communicate(input=send)[0]
        print result[707:]


x = Converter()
