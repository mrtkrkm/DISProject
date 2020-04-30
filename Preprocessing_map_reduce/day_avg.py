from mrjob.job import MRJob

class MRCountSum(MRJob):

    def mapper(self, _, s):
        isDataInDailyBasis = False    # needs to be considered when dataset changes
        s = s.strip()
        index = s.find(' ')
        key = s[0:index-5].splt('.')
        try:
            key = key[0] + key[1]
        except:
            print("skipping line")
        else:
            if isDataInDailyBasis:
                secondKey = s[index+1:index+6].split(':')
                secondKey = secondKey[0] = secondKey[1]
                key = key + secondKey

            index = s.find(' ')
            value = s[index+1:].replace(" ", "").split(',')
            fVal = []
            for val in value:
                fVal.append(float(val))
            yield key, [fVal, 1]

    def reducer(self, key, values):
        columnSize = 15    # needs to be considered when dataset changes
        sum = 0.0
        count = 0
        val = [0] * columnSize
        for x, y in values:
            for i in range(len(x)):
                val[i] = val[i] + x[i]
            count = count + y
        for i in range(len(val)):
            val[i] = val[i] / count
        yield key, val