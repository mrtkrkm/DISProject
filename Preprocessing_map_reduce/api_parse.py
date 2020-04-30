from mrjob.job import MRJob

class MRCountSum(MRJob):
    def mapper(self, _, line):
        value = []
        index = line.find("\"localtime\"")
        key = line[index+22:index+24] + line[index+19:index+21] + line[index+14:index+18]
        index = line.find("\"wind_dir\"")
        tmp = ""
        while True:
            if line[index] == ',':
                break
            tmp += line[index]
            index += 1
        tmp = tmp.split(":")[1].replace("\"", "").strip()
        value.append(tmp)

        index = line.find("\"avgtemp_c\"")
        tmp = ""
        while True:
            if line[index] == ',':
                break
            tmp += line[index]
            index += 1
        tmp = tmp.split(":")[1].replace("\"", "").strip()
        value.append(tmp)
        yield key, value

def reducer(self, key, value):
    yield key, value

if __name__ == '__main__':
    MRCountSum.run()