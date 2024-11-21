import time, hashlib


class generateUniqueString(object):
    def __init__(self, setID, *args):
        self.setID      = setID
        super(generateUniqueString, self).__init__(*args)
        
    def generateString(self):
        setID       = self.setID
        """ This is a helper function for generating unique string.\n
            Parameters include:\n
            setID (string) -- (optional) You can specify a merchant id to start references e.g. merchantId-12345678
        """
        rawTime = round(time.time() * 1000)
        timestamp = int(rawTime)
        if setID:
            return setID+"-"+str(timestamp)
        else:
            return "MC-"+str(timestamp)
    
    def generateStringNoHyphen(self):
        setID       = self.setID
        """ This is a helper function for generating unique string.\n
            Parameters include:\n
            setID (string) -- (optional) You can specify a merchant id to start references e.g. merchantId-12345678
        """
        rawTime = round(time.time() * 1000)
        timestamp = int(rawTime)
        if setID:
            return setID + str(timestamp)
        else:
            return "MC-"+str(timestamp)

class transactionKeyOPS(object):
    def __init__(self, string_to_hash, *args):
        self.string_to_hash     = string_to_hash
        super(transactionKeyOPS, self).__init__(*args)
    
    def transactionkey(self):
        string_to_hash      = self.string_to_hash
        sha256_hash         = hashlib.sha256()
        sha256_hash.update(string_to_hash.encode())
        hashed_string       = sha256_hash.hexdigest()
       
        return hashed_string

