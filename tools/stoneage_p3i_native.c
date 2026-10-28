/* P3I read-only DirectDraw primary observer. It never touches target process
   memory, private surfaces, original files, palette contents, or display mode. */
#define COBJMACROS
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <ddraw.h>
#include <wincrypt.h>
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#pragma comment(lib, "ddraw.lib")
#pragma comment(lib, "dxguid.lib")
#pragma comment(lib, "advapi32.lib")
#pragma comment(lib, "user32.lib")
#define H8(x) ((unsigned long)(unsigned int)(x))
static int bytes_sha256(const BYTE *p, size_t size, char hex[65]) {
    HCRYPTPROV cp=0;HCRYPTHASH ch=0;BYTE dig[32];DWORD n=32;
    if(!CryptAcquireContextW(&cp,NULL,NULL,PROV_RSA_AES,CRYPT_VERIFYCONTEXT))return 0;
    if(!CryptCreateHash(cp,CALG_SHA_256,0,0,&ch)){CryptReleaseContext(cp,0);return 0;}
    int ok=size<=0xffffffffu && CryptHashData(ch,p,(DWORD)size,0) &&
           CryptGetHashParam(ch,HP_HASHVAL,dig,&n,0) && n==32;
    if(ok){for(int i=0;i<32;i++)sprintf(hex+2*i,"%02x",(unsigned)dig[i]);hex[64]=0;}
    CryptDestroyHash(ch);CryptReleaseContext(cp,0);return ok;
}
int main(int argc,char **argv) {
    if(argc!=3)return 4;
    unsigned long long rawhwnd=_strtoui64(argv[1],NULL,10);
    DWORD expect=(DWORD)strtoul(argv[2],NULL,10),actual=0;
    HWND hwnd=(HWND)(uintptr_t)rawhwnd;
    WCHAR klass[64]={0};RECT cr;POINT loc={0,0};
    if(!IsWindow(hwnd) || !GetWindowThreadProcessId(hwnd,&actual) || actual!=expect ||
       !GetClassNameW(hwnd,klass,64) || lstrcmpW(klass,L"ＳｔｏｎｅＡｇｅ") ||
       !GetClientRect(hwnd,&cr) || cr.right!=640 || cr.bottom!=480 ||
       !ClientToScreen(hwnd,&loc))return 4;
    HRESULT created=E_FAIL,coop=E_FAIL,primary_result=E_FAIL,locked=E_FAIL,palette=E_FAIL;
    LPDIRECTDRAW dd=NULL; LPDIRECTDRAWSURFACE surf=NULL; LPDIRECTDRAWPALETTE pal=NULL;
    DDSURFACEDESC sd; memset(&sd,0,sizeof(sd));sd.dwSize=sizeof(sd);
    DWORD bitdepth=0, width=0,height=0;
    long pitch=0;
    unsigned long long zero=0, nonzero=0, distinct=0;
    int palette_read=0;
    char pixel_digest[65]="",palette_digest[65]="";
    created=DirectDrawCreate(NULL,&dd,NULL);
    if(SUCCEEDED(created)){
        coop=IDirectDraw_SetCooperativeLevel(dd,GetDesktopWindow(),DDSCL_NORMAL);
        if(SUCCEEDED(coop)){
            DDSURFACEDESC setup;memset(&setup,0,sizeof(setup));setup.dwSize=sizeof(setup);
            setup.dwFlags=DDSD_CAPS;setup.ddsCaps.dwCaps=DDSCAPS_PRIMARYSURFACE;
            primary_result=IDirectDraw_CreateSurface(dd,&setup,&surf,NULL);
        }
    }
    if(surf){
        palette=IDirectDrawSurface_GetPalette(surf,&pal);
        if(SUCCEEDED(palette) && pal){
            PALETTEENTRY entries[256];
            if(SUCCEEDED(IDirectDrawPalette_GetEntries(pal,0,0,256,entries)))
                palette_read=bytes_sha256((const BYTE*)entries,sizeof(entries),palette_digest);
        }
        locked=IDirectDrawSurface_Lock(surf,NULL,&sd,DDLOCK_READONLY|DDLOCK_DONOTWAIT,NULL);
        if(SUCCEEDED(locked)){
            width=sd.dwWidth;height=sd.dwHeight; pitch=sd.lPitch;
            bitdepth=sd.ddpfPixelFormat.dwRGBBitCount;
            unsigned stride=(bitdepth+7)/8;
            if(sd.lpSurface && width && height && pitch>0 &&
               (bitdepth==8 || bitdepth==16 || bitdepth==24 || bitdepth==32) &&
               loc.x>=0 && loc.y>=0 &&
               (uint64_t)loc.x+640<=width && (uint64_t)loc.y+480<=height &&
               (uint64_t)loc.x*stride+640*stride<=(uint64_t)pitch) {
                size_t rb=640u*stride,total=rb*480u;
                BYTE *data=(BYTE*)malloc(total);
                if(data){
                    for(int y=0;y<480;y++){
                        const BYTE *source=(const BYTE*)sd.lpSurface+(loc.y+y)*(size_t)pitch+loc.x*stride;
                        memcpy(data+y*rb,source,rb);
                    }
                    if(bytes_sha256(data,total,pixel_digest)) {
                        if(bitdepth==8){
                            unsigned long bins[256]={0};
                            for(size_t i=0;i<total;i++)bins[data[i]]++;
                            zero=bins[0];nonzero=total-zero;
                            for(int i=0;i<256;i++)if(bins[i])distinct++;
                        }
                    }
                    free(data);
                }
            }
            IDirectDrawSurface_Unlock(surf,NULL);
        }
    }
    printf("{\"schema\":\"stoneage.p3i.native_ddraw_primary.v1\","
           "\"target_owned_window_verified\":true,\"original_private_surface_read\":false,"
           "\"ddraw_create_hr\":\"0x%08lx\",\"cooperative_hr\":\"0x%08lx\","
           "\"primary_create_hr\":\"0x%08lx\",\"primary_lock_hr\":\"0x%08lx\","
           "\"palette_query_hr\":\"0x%08lx\","
           "\"palette_sha256\":\"%s\",\"palette_read\":%s,"
           "\"surface_width\":%lu,\"surface_height\":%lu,\"surface_pitch\":%ld,"
           "\"surface_bpp\":%lu,\"window_origin\":[%ld,%ld],"
           "\"sample_region\":[640,480],\"pixel_sha256\":\"%s\","
           "\"index_zero_pixels\":%llu,\"index_nonzero_pixels\":%llu,"
           "\"index_distinct\":%llu}\n",
           H8(created),H8(coop),H8(primary_result),H8(locked),H8(palette),
           palette_digest,palette_read?"true":"false",width,height,pitch,bitdepth,
           loc.x,loc.y,pixel_digest,zero,nonzero,distinct);
    if(pal)IDirectDrawPalette_Release(pal);
    if(surf)IDirectDrawSurface_Release(surf);
    if(dd)IDirectDraw_Release(dd);
    return 0;
}
