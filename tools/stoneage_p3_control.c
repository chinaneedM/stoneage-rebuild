/* Independently built synthetic Win32/DirectDraw control and read-only window
 * inspector. No original game code/assets are present in this program. */
#define COBJMACROS
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <ddraw.h>
#include <stdio.h>
#include <string.h>

static void json_wide(const WCHAR *s) {
    putchar('"');
    for(int i=0;s[i] && i<160;i++) {
        unsigned c=(unsigned short)s[i];
        if(c=='"'||c=='\\')printf("\\%c",c);
        else if(c>=32 && c<127)putchar(c);
        else printf("\\u%04x",c);
    }
    putchar('"');
}
static int child_count=0;
static BOOL CALLBACK child(HWND w,LPARAM unused) {
    WCHAR title[161]={0},klass[161]={0};
    GetWindowTextW(w,title,161);GetClassNameW(w,klass,161);
    if(!title[0]||child_count>=24)return TRUE;
    if(child_count++)putchar(',');
    printf("{\"class\":");json_wide(klass);printf(",\"text\":");json_wide(title);putchar('}');
    return TRUE;
}
static int window_count=0;
static BOOL CALLBACK window(HWND w,LPARAM unused) {
    if(!IsWindowVisible(w)||window_count>=16)return TRUE;
    WCHAR title[161]={0},klass[161]={0},path[1024]={0};
    RECT r;DWORD pid=0;GetWindowRect(w,&r);GetWindowThreadProcessId(w,&pid);
    GetWindowTextW(w,title,161);GetClassNameW(w,klass,161);
    HANDLE process=OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION,FALSE,pid);
    if(process){DWORD size=1024;QueryFullProcessImageNameW(process,0,path,&size);CloseHandle(process);}
    if(window_count++)putchar(',');
    printf("{\"pid\":%lu,\"class\":",(unsigned long)pid);json_wide(klass);
    printf(",\"title\":");json_wide(title);printf(",\"image_path\":");json_wide(path);
    printf(",\"rect\":[%ld,%ld,%ld,%ld],\"children\":[",r.left,r.top,r.right,r.bottom);
    child_count=0;EnumChildWindows(w,child,0);printf("]}");return TRUE;
}
static LRESULT CALLBACK proc(HWND w,UINT message,WPARAM a,LPARAM b) {
    if(message==WM_PAINT){
        PAINTSTRUCT p;HDC dc=BeginPaint(w,&p);
        RECT left={0,0,120,120},right={120,0,240,120};
        HBRUSH red=CreateSolidBrush(RGB(222,0,0)),green=CreateSolidBrush(RGB(0,200,80));
        FillRect(dc,&left,red);FillRect(dc,&right,green);DeleteObject(red);DeleteObject(green);
        EndPaint(w,&p);return 0;
    }
    if(message==WM_TIMER){DestroyWindow(w);return 0;}
    if(message==WM_DESTROY){PostQuitMessage(0);return 0;}
    return DefWindowProcW(w,message,a,b);
}
int WINAPI WinMain(HINSTANCE instance,HINSTANCE previous,LPSTR command,int show) {
    if(strstr(command,"inspect")){
        printf("{\"schema\":\"stoneage.p3.win32_window_inspection.v1\",\"windows\":[");
        EnumWindows(window,0);printf("]}\n");fflush(stdout);return 0;
    }
    WNDCLASSW cls={0};cls.lpfnWndProc=proc;cls.hInstance=instance;cls.lpszClassName=L"StoneAgeP3Synthetic";
    RegisterClassW(&cls);
    HWND w=CreateWindowW(cls.lpszClassName,L"SYNTHETIC 32-bit observation control",WS_OVERLAPPEDWINDOW|WS_VISIBLE,
                         30,30,280,190,NULL,NULL,instance,NULL);
    LPDIRECTDRAW dd=NULL;LPDIRECTDRAWSURFACE surface=NULL;LPDIRECTDRAWPALETTE pal=NULL;
    HRESULT create=DirectDrawCreate(NULL,&dd,NULL),cooperative=E_FAIL,create_surface=E_FAIL,create_palette=E_FAIL,attach=E_FAIL,current_mode=E_FAIL;
    DWORD current_bpp=0;
    if(SUCCEEDED(create)){
        DDSURFACEDESC current={0};current.dwSize=sizeof(current);
        current_mode=IDirectDraw_GetDisplayMode(dd,&current);
        if(SUCCEEDED(current_mode))current_bpp=current.ddpfPixelFormat.dwRGBBitCount;
        cooperative=IDirectDraw_SetCooperativeLevel(dd,w,DDSCL_NORMAL);
        DDSURFACEDESC desc={0};desc.dwSize=sizeof(desc);desc.dwFlags=DDSD_CAPS|DDSD_WIDTH|DDSD_HEIGHT|DDSD_PIXELFORMAT;
        desc.dwWidth=64;desc.dwHeight=64;desc.ddsCaps.dwCaps=DDSCAPS_OFFSCREENPLAIN|DDSCAPS_SYSTEMMEMORY;
        desc.ddpfPixelFormat.dwSize=sizeof(DDPIXELFORMAT);desc.ddpfPixelFormat.dwFlags=DDPF_RGB|DDPF_PALETTEINDEXED8;
        desc.ddpfPixelFormat.dwRGBBitCount=8;
        create_surface=IDirectDraw_CreateSurface(dd,&desc,&surface,NULL);
        PALETTEENTRY colors[256];for(int i=0;i<256;i++){colors[i].peRed=i;colors[i].peGreen=255-i;colors[i].peBlue=i/2;colors[i].peFlags=0;}
        create_palette=IDirectDraw_CreatePalette(dd,DDPCAPS_8BIT|DDPCAPS_ALLOW256,colors,&pal,NULL);
        if(surface&&pal)attach=IDirectDrawSurface_SetPalette(surface,pal);
    }
    FILE *f=fopen("synthetic-control.json","wb");
    if(!f)return 2;
    fprintf(f,"{\"schema\":\"stoneage.p3.synthetic_control.v1\",\"pointer_bytes\":%u,\"windows_acp\":%u,\"reported_windows_version\":%lu,\"window_created\":%s,\"directdraw_create\":%ld,\"cooperative\":%ld,\"surface_8bit_create\":%ld,\"palette_create\":%ld,\"palette_attach\":%ld,\"get_display_mode\":%ld,\"current_display_bpp\":%lu,\"original_client_executed\":false}\n",
            (unsigned)sizeof(void*),(unsigned)GetACP(),(unsigned long)GetVersion(),w?"true":"false",(long)create,(long)cooperative,(long)create_surface,(long)create_palette,(long)attach,(long)current_mode,(unsigned long)current_bpp);
    fclose(f);UpdateWindow(w);SetTimer(w,1,12000,NULL);
    MSG msg;while(GetMessageW(&msg,NULL,0,0)>0){TranslateMessage(&msg);DispatchMessageW(&msg);}
    if(pal)IDirectDrawPalette_Release(pal);if(surface)IDirectDrawSurface_Release(surface);if(dd)IDirectDraw_Release(dd);
    return 0;
}
