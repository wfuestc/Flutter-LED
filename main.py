import socket, time, re
from machine import Pin
import network

SSID = "HUAWEI"
PASSWORD = "wangfei520"


def do_connect():
  wlan = network.WLAN(network.STA_IF)
  wlan.active(True)
  if not wlan.isconnected():
    print("connecting to network...")
    wlan.connect(SSID, PASSWORD)

  start = time.time()
  while not wlan.isconnected():
    time.sleep(1)
    if time.time() - start > 5:
      print("connect timeout!")
      break

  if wlan.isconnected():
    print("network config:", wlan.ifconfig())
    return wlan
  print("OK!")


if __name__ == "__main__":
  
  wlan = do_connect()
  
  ip = wlan.ifconfig()[0]
  port = 80
  print("服务器地址:%s:%d" %(ip,port))
  
  #创建套接字
  webserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   
  #设置给定套接字选项的值
  webserver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  
  #webserver.settimeout(2000)
  webserver.bind((ip, port))   #绑定IP地址和端口号
  webserver.listen(5)          #监听套接字
  
  
  led = Pin(5, Pin.OUT)
 

  while True:
     #接受一个连接，conn是一个新的socket对象
    conn, addr = webserver.accept()                               
    #print("in %s" % str(addr))
    #从套接字接收1024字节的数据
    request = conn.recv(1024) 
    
    if len(request)>0:
      request = request.decode()
      print("XXX:"+request)
      result = re.search("(.*?) (.*?) HTTP/1.1", request)
      if result:
        method = result.group(1)
        url_infos = result.group(2)
        url,infos = url_infos.split("?")
        
        if method == "GET":
          if infos:
            lists = infos.split("&")
            payload = {}
            for list in lists:
              k,v = list.split("=")
              payload[k]=v
            print(payload)
        
          if url == "/led":
            status = payload.get("status")
            if status=="on":
              led.value(1)
            elif status=="off":
              led.value(0)
          
      else:
        print("not found url")
    else:
      print("no request")
    conn.close()


