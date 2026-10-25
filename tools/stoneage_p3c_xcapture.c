/* X11 indexed capture using each drawable's own colormap. No game bytes.
 * Writes private PPM/palette/index files; stdout contains geometry only. */
#include <X11/Xlib.h>
#include <X11/Xutil.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static Display *d;
static Window root;
static const char *out;
static int count = 0, errors = 0;
static int error(Display *display, XErrorEvent *event) { errors++; return 0; }

static void colors(Colormap map, unsigned char rgb[768]) {
    XColor c[256];
    for (int i=0;i<256;i++) c[i].pixel=i;
    XQueryColors(d,map,c,256);
    for (int i=0;i<256;i++) {
        rgb[3*i]=c[i].red/257; rgb[3*i+1]=c[i].green/257; rgb[3*i+2]=c[i].blue/257;
    }
}
static int capture(Window w) {
    XWindowAttributes a;
    if (!XGetWindowAttributes(d,w,&a) || a.map_state!=IsViewable || a.depth!=8 ||
        a.visual->class!=PseudoColor || !a.colormap || a.width<160 || a.height<120 ||
        a.width>800 || a.height>600 || count>=12) return 0;
    XImage *im=XGetImage(d,w,0,0,a.width,a.height,AllPlanes,ZPixmap);
    if (!im) return 0;
    unsigned char rgb[768],wrong[768]; colors(a.colormap,rgb);
    Colormap default_map=DefaultColormap(d,DefaultScreen(d)); colors(default_map,wrong);
    char path[4096]; FILE *f[4];
    const char *suffix[4]={"map.ppm","rootmap.ppm","indices.bin","palette.bin"};
    for (int i=0;i<4;i++) {
        snprintf(path,sizeof(path),"%s/window-%lu-%s",out,w,suffix[i]);
        f[i]=fopen(path,"wb"); if (!f[i]) exit(4);
    }
    fprintf(f[0],"P6\n%d %d\n255\n",a.width,a.height);
    fprintf(f[1],"P6\n%d %d\n255\n",a.width,a.height);
    fwrite(rgb,1,768,f[3]);
    for(int y=0;y<a.height;y++) for(int x=0;x<a.width;x++) {
        unsigned long p=XGetPixel(im,x,y); if(p>255) exit(5);
        unsigned char index=p; fwrite(&index,1,1,f[2]);
        fwrite(rgb+3*p,1,3,f[0]); fwrite(wrong+3*p,1,3,f[1]);
    }
    for(int i=0;i<4;i++) fclose(f[i]); XDestroyImage(im);
    if(count++) putchar(',');
    printf("{\"window\":%lu,\"colormap\":%lu,\"default_colormap\":%lu,\"map_installed\":%s,\"depth\":%d,\"visual_class\":%d,\"width\":%d,\"height\":%d}",
           w,a.colormap,default_map,a.map_installed?"true":"false",a.depth,a.visual->class,a.width,a.height);
    return 1;
}
static void tree(Window w,int depth) {
    if(depth>8 || count>=12) return;
    if(w!=root) capture(w);
    Window r,p,*children=NULL; unsigned n=0;
    if(XQueryTree(d,w,&r,&p,&children,&n)) {
        for(unsigned i=0;i<n;i++) tree(children[i],depth+1);
        if(children) XFree(children);
    }
}
int main(int argc,char **argv) {
    if(argc<2 || argc>3) return 2;
    out=argv[1]; d=XOpenDisplay(NULL); if(!d) return 3;
    XSetErrorHandler(error); root=DefaultRootWindow(d);
    printf("{\"schema\":\"stoneage.p3c.x11_own_colormap.v1\",\"windows\":[");
    if(argc==3 && strcmp(argv[2],"--selftest")==0) {
        XWindowAttributes a; XGetWindowAttributes(d,root,&a);
        if(a.depth!=8 || a.visual->class!=PseudoColor) return 6;
        Colormap c=XCreateColormap(d,root,a.visual,AllocAll); XColor cells[256];
        for(int i=0;i<256;i++) { cells[i].pixel=i; cells[i].red=cells[i].green=cells[i].blue=0; cells[i].flags=DoRed|DoGreen|DoBlue; }
        cells[42].red=222*257; cells[99].green=200*257; cells[99].blue=80*257;
        XStoreColors(d,c,cells,256);
        XSetWindowAttributes v={0};v.colormap=c;v.border_pixel=0;v.background_pixel=0;
        Window w=XCreateWindow(d,root,0,0,320,160,0,8,InputOutput,a.visual,CWColormap|CWBorderPixel|CWBackPixel,&v);
        XMapRaised(d,w); GC gc=XCreateGC(d,w,0,NULL);
        XSetForeground(d,gc,42);XFillRectangle(d,w,gc,0,0,160,160);
        XSetForeground(d,gc,99);XFillRectangle(d,w,gc,160,0,160,160);
        XSync(d,False);capture(w);XFreeGC(d,gc);XDestroyWindow(d,w);XFreeColormap(d,c);
    } else tree(root,0);
    XSync(d,False);printf("],\"x_errors\":%d}\n",errors);XCloseDisplay(d);
    return errors?7:0;
}
