/* Own synthetic Windows qualification; no original game resources or execution. */
#define WIN32_LEAN_AND_MEAN
#define COBJMACROS
#include <winsock2.h>
#include <ws2tcpip.h>
#include <windows.h>
#include <ddraw.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int dd_count=0;
static HRESULT WINAPI mode_callback(LPDDSURFACEDESC s,LPVOID unused) {
    (void)unused;
    printf("%s[%lu,%lu,%lu]",dd_count++?",":"",s->dwWidth,s->dwHeight,s->ddpfPixelFormat.dwRGBBitCount);
    return DDENUMRET_OK;
}
static void connect_probe(const char *ip,int port) {
    WSADATA w;int startup=WSAStartup(MAKEWORD(2,2),&w),error=0,ok=0;
    if(!startup) {
        SOCKET s=socket(AF_INET,SOCK_STREAM,IPPROTO_TCP);
        if(s==INVALID_SOCKET)error=WSAGetLastError();
        else {
            u_long nonblock=1;ioctlsocket(s,FIONBIO,&nonblock);
            struct sockaddr_in a={0};a.sin_family=AF_INET;a.sin_port=htons((u_short)port);InetPtonA(AF_INET,ip,&a.sin_addr);
            if(connect(s,(struct sockaddr*)&a,sizeof(a))==0)ok=1;
            else {
                error=WSAGetLastError();
                if(error==WSAEWOULDBLOCK) {
                    fd_set write_set,exception_set;FD_ZERO(&write_set);FD_ZERO(&exception_set);
                    FD_SET(s,&write_set);FD_SET(s,&exception_set);struct timeval wait={5,0};
                    int selected=select(0,NULL,&write_set,&exception_set,&wait);
                    if(selected>0) {int size=sizeof(error);getsockopt(s,SOL_SOCKET,SO_ERROR,(char*)&error,&size);ok=error==0;}
                    else error=selected==0?WSAETIMEDOUT:WSAGetLastError();
                }
            }
            closesocket(s);
        }
        WSACleanup();
    }
    printf("{\"connected\":%s,\"wsa_error\":%d,\"startup_error\":%d}\n",ok?"true":"false",error,startup);
}
int main(int argc,char **argv) {
    if(argc==4 && !strcmp(argv[1],"connect")) {connect_probe(argv[2],atoi(argv[3]));return 0;}
    HDC dc=GetDC(NULL);int bpp=GetDeviceCaps(dc,BITSPIXEL)*GetDeviceCaps(dc,PLANES);ReleaseDC(NULL,dc);
    UINT acp=GetACP(),cp=GetConsoleCP(),out=GetConsoleOutputCP();
    BOOL set_in=SetConsoleCP(950),set_out=SetConsoleOutputCP(950);
    WCHAR sample[3]={0x77f3,0x5668,0};char encoded[16]={0};BOOL fallback=FALSE;
    int n=WideCharToMultiByte(950,WC_NO_BEST_FIT_CHARS,sample,2,encoded,sizeof(encoded),NULL,&fallback);
    printf("{\"pointer_bytes\":%u,\"display_bpp\":%d,\"acp_before\":%u,\"acp_after_console950\":%u,",(unsigned)sizeof(void*),bpp,acp,GetACP());
    printf("\"console_before\":[%u,%u],\"console_set_return\":[%s,%s],\"console_after\":[%u,%u],",cp,out,set_in?"true":"false",set_out?"true":"false",GetConsoleCP(),GetConsoleOutputCP());
    printf("\"cp950_installed\":%s,\"cp950_sample_bytes\":[",IsValidCodePage(950)?"true":"false");
    for(int j=0;j<n;j++)printf("%s%u",j?",":"",(unsigned char)encoded[j]);
    printf("],\"cp950_sample_fallback\":%s,\"display_modes\":[",fallback?"true":"false");
    DEVMODEA m={0};m.dmSize=sizeof(m);int count=0;
    for(DWORD i=0;EnumDisplaySettingsA(NULL,i,&m);i++) {
        printf("%s[%lu,%lu,%lu,%lu]",count++?",":"",m.dmPelsWidth,m.dmPelsHeight,m.dmBitsPerPel,m.dmDisplayFrequency);
        memset(&m,0,sizeof(m));m.dmSize=sizeof(m);
    }
    memset(&m,0,sizeof(m));m.dmSize=sizeof(m);m.dmPelsWidth=640;m.dmPelsHeight=480;m.dmBitsPerPel=8;
    m.dmFields=DM_PELSWIDTH|DM_PELSHEIGHT|DM_BITSPERPEL;
    LONG test=ChangeDisplaySettingsA(&m,CDS_TEST); /* Test only; never alter desktop mode. */
    printf("],\"cds_test_640_480_8\":%ld,\"desktop_mode_changed\":false,",test);
    LPDIRECTDRAW dd=NULL;HRESULT created=DirectDrawCreate(NULL,&dd,NULL),enumerated=E_FAIL,current=E_FAIL;
    DDSURFACEDESC desc={0};desc.dwSize=sizeof(desc);
    printf("\"ddraw_modes\":[");
    if(dd) {enumerated=IDirectDraw_EnumDisplayModes(dd,0,NULL,NULL,mode_callback);current=IDirectDraw_GetDisplayMode(dd,&desc);}
    printf("],\"ddraw_create\":%ld,\"ddraw_enum\":%ld,\"ddraw_current_result\":%ld,\"ddraw_current\":[%lu,%lu,%lu],\"original_executed\":false}\n",(long)created,(long)enumerated,(long)current,desc.dwWidth,desc.dwHeight,desc.ddpfPixelFormat.dwRGBBitCount);
    if(dd)IDirectDraw_Release(dd);
    if(cp)SetConsoleCP(cp);if(out)SetConsoleOutputCP(out);
    return 0;
}
