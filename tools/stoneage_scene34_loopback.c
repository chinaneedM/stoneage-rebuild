/* Own finite TCP/IPv4 prerequisite probe. No game binary, injection or account. */
#define WIN32_LEAN_AND_MEAN
#include <winsock2.h>
#include <ws2tcpip.h>
#include <windows.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int write_result(const char *path, int connected, int error, int echo) {
    FILE *f = NULL;
    if (fopen_s(&f, path, "wb") || !f) return 31;
    fprintf(f, "{\"connected\":%s,\"wsa_error\":%d,\"echo_exact\":%s,\"pid\":%lu}\n",
        connected ? "true" : "false", error, echo ? "true" : "false", GetCurrentProcessId());
    return fclose(f) ? 32 : 0;
}

static int ready(const char *path, int port) {
    FILE *f = NULL;
    if (fopen_s(&f, path, "wb") || !f) return 33;
    fprintf(f, "{\"ready\":true,\"bind_address\":\"127.0.0.1\",\"port\":%d,\"pid\":%lu,\"pointer_bytes\":%u}\n", port, GetCurrentProcessId(), (unsigned)sizeof(void*));
    return fclose(f) ? 34 : 0;
}

static int wait_socket(SOCKET s, int writing, int seconds) {
    fd_set f; struct timeval timeout;
    FD_ZERO(&f); FD_SET(s, &f); timeout.tv_sec=seconds; timeout.tv_usec=0;
    return select(0, writing ? NULL : &f, writing ? &f : NULL, NULL, &timeout);
}

static int client(const char *ip, int port, const char *path, int echo) {
    SOCKET s=socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    struct sockaddr_in a; u_long blocking=1; int error=0, length=sizeof(error), ok=0, exact=0;
    DWORD timeout=2000; char reply[8];
    if(s==INVALID_SOCKET) return write_result(path,0,WSAGetLastError(),0);
    memset(&a,0,sizeof(a)); a.sin_family=AF_INET; a.sin_port=htons((u_short)port);
    if(InetPtonA(AF_INET,ip,&a.sin_addr)!=1) {closesocket(s); return 35;}
    if(ioctlsocket(s,FIONBIO,&blocking)) {error=WSAGetLastError(); goto done;}
    if(connect(s,(struct sockaddr*)&a,sizeof(a))==0) ok=1;
    else {
        error=WSAGetLastError();
        if(error==WSAEWOULDBLOCK) {
            int selected=wait_socket(s,1,5);
            if(selected>0 && getsockopt(s,SOL_SOCKET,SO_ERROR,(char*)&error,&length)==0) ok=(error==0);
            else error=(selected==0) ? WSAETIMEDOUT : WSAGetLastError();
        }
    }
    if(ok && echo) {
        blocking=0; ioctlsocket(s,FIONBIO,&blocking);
        setsockopt(s,SOL_SOCKET,SO_RCVTIMEO,(char*)&timeout,sizeof(timeout));
        setsockopt(s,SOL_SOCKET,SO_SNDTIMEO,(char*)&timeout,sizeof(timeout));
        if(send(s,"S34CHECK",8,0)==8 && recv(s,reply,8,MSG_WAITALL)==8) exact=(memcmp(reply,"S34CHECK",8)==0);
        if(!exact) error=WSAGetLastError();
    }
done:
    closesocket(s); return write_result(path,ok,error,exact);
}

static int server(int port, const char *ready_path, const char *result_path) {
    SOCKET s=socket(AF_INET,SOCK_STREAM,IPPROTO_TCP), peer=INVALID_SOCKET;
    struct sockaddr_in a; int error=0, exact=0, connected=0; char payload[8]; DWORD timeout=2000;
    if(s==INVALID_SOCKET) return write_result(result_path,0,WSAGetLastError(),0);
    memset(&a,0,sizeof(a)); a.sin_family=AF_INET; a.sin_port=htons((u_short)port); a.sin_addr.s_addr=htonl(INADDR_LOOPBACK);
    if(bind(s,(struct sockaddr*)&a,sizeof(a)) || listen(s,1)) {error=WSAGetLastError(); goto done;}
    if(ready(ready_path,port)) {closesocket(s); return 36;}
    if(wait_socket(s,0,8)<=0) {error=WSAETIMEDOUT; goto done;}
    peer=accept(s,NULL,NULL);
    if(peer==INVALID_SOCKET) {error=WSAGetLastError(); goto done;}
    connected=1;
    setsockopt(peer,SOL_SOCKET,SO_RCVTIMEO,(char*)&timeout,sizeof(timeout));
    setsockopt(peer,SOL_SOCKET,SO_SNDTIMEO,(char*)&timeout,sizeof(timeout));
    if(recv(peer,payload,8,MSG_WAITALL)==8 && memcmp(payload,"S34CHECK",8)==0 && send(peer,payload,8,0)==8) exact=1;
    else error=WSAGetLastError();
done:
    if(peer!=INVALID_SOCKET) closesocket(peer);
    closesocket(s); return write_result(result_path,connected,error,exact);
}

int main(int argc,char **argv) {
    WSADATA data; int port,result;
    if(argc==2 && strcmp(argv[1],"hold")==0) {Sleep(30000); return 0;}
    if(argc!=6) return 10;
    port=atoi(argv[3]); if(port<1 || port>65535) return 11;
    if(WSAStartup(MAKEWORD(2,2),&data)) return 12;
    if(strcmp(argv[1],"listen")==0) result=server(port,argv[4],argv[5]);
    else if(strcmp(argv[1],"echo")==0 || strcmp(argv[1],"canary")==0)
        result=client(argv[2],port,argv[4],strcmp(argv[1],"echo")==0);
    else result=13;
    WSACleanup(); return result;
}
