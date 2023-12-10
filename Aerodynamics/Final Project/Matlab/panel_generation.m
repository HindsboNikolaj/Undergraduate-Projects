%vortex panel method for arbitrary NACA#### profile
%Only works for cambered profiles
%Only works with EVEN number of panels
%It only works up to a max. number of panels that varies from shape to shape
%BEFORE USING MUST UPDATE VALUES OF (npts), npan, m, p, t, alpha
% m = #1/100
% p = #2/10
% t = (#3,#4)/100
function [xpan, ypan] = panel_generation(npan, aoa, m, p, t)

npts=8000;

alpha=aoa*pi/180;

thetacircle=(0:0.001:1)*2*pi;
xcircle=0.5+0.5*cos(thetacircle);
ycircle=0.5*sin(thetacircle);
x_of_x_axis=0:1/npts:1;
y_of_x_axis=zeros(1,npts+1);
y_on_x_axis_pan_gen=zeros(1,npan+1);

xcntr=zeros(1,npan);
ycntr=zeros(1,npan);
xpan=zeros(1,npan);
ypan=zeros(1,npan);
phi=zeros(1,npan);
sl=zeros(1,npan);
vt=zeros(1,npan);

hh=zeros(npan,npan);
k=zeros(npan,npan);
ll=zeros(npan+1, npan+1);
nn=zeros(1,npan+1);
rr=zeros(npan,npan);
tt=zeros(npan,npan);
ww=zeros(npan,npan+1);

%camber line and local slope
xl=0:1/npts:p;
xr=p+1/npts:1/npts:1;

ycl=m/p^2*(2*p*xl-xl.^2);
ycr=m/(1-p)^2*(1-2*p+2*p*xr-xr.^2);

thl=atan(2*m/p^2*(p-xl));
thr=atan(2*m/(1-p)^2*(p-xr));

x=[xl,xr];
yc=[ycl,ycr];
th=[thl,thr];
%camber line and local slope

%thickness
yt=t/0.2*(0.2969*x.^0.5-0.126*x-0.3516*x.^2+0.2843*x.^3-0.1015*x.^4);
%thickness

%profile
xu=x-yt.*sin(th);
yu=yc+yt.*cos(th);
xl=x+yt.*sin(th);
yl=yc-yt.*cos(th);
%profile

%figure; hold on;
%plot(xl,yl,xu,yu,x,yc);
axis equal;hold on;
xx=[-3,.1,3];y=0*xx;
%plot(xx,y,'--');

%panel generation scheme

%circle division
eta=0:1/npan:1;
eta=eta*2*pi;
%circle division

%points on the circle
x_pan_gen=0.5+0.5*cos(eta);
y_pan_gen=0.5*sin(eta);
%points on the circle


xc=0.5*(1+cos(eta));

% 
j=npts;
for i=2:(npan/2+1)
    while(xl(j) > xc(i))
         j=j-1;
    end
    xpan(i)=xl(j);
    ypan(i)=yl(j);
end

j=1;
for i=(npan/2+2):npan
    while(xc(i) > xu(j))
         j=j+1;
    end
    xpan(i)=xu(j);
    ypan(i)=yu(j);
end

xpan(1)=1;
xpan(npan+1)=1;
ypan(1)=0;
ypan(npan+1)=0;




% plot the panels 
%figure
%hold on;
%plot(xu,yu);
%axis([-0.01 1.01 -0.5 0.5])
%plot(xl,yl)
%xlabel('x/c');
%ylabel('y/c');
%title(['NACA' num2str(m*100) num2str(p*10) num2str(t*100) ' profile modeled with ' num2str(npan) ' vortex panels']);
for i=1:1:npan
    %plot([xpan(i),xpan(i+1)],[ypan(i),ypan(i+1)],'-dr')
end
%plot(x,yc);
%plot(xcircle,ycircle,'k');
%plot(x_of_x_axis,y_of_x_axis,'k');
%plot(x_pan_gen,y_pan_gen,'og');
%plot(x_pan_gen,y_on_x_axis_pan_gen,'og');
for i=1:npan+1
    %plot([x_pan_gen(i) x_pan_gen(i)],[y_pan_gen(i) y_on_x_axis_pan_gen(i)],'g');
end