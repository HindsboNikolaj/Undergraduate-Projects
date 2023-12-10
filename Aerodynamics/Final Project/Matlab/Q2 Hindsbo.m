clear all;
close all;
% RUN WITHOUT CLOSE ALL FOR PART E THEN CHANGE AR %
y_b=linspace(-0.5,0.5);
AR=6;
aoa=linspace(2,10,5);
aoa_radians=aoa.*pi/180;
figure;
for j=1:length(aoa)
    for k=1:length(y_b)
        gam_dist(j,k)=aoa_radians(j)./(2./(pi.*1/6.*sqrt(1-4.*y_b(k).^2))).*sqrt(1-4.*y_b(k).^2);
    end
    C_L_Elliptic(j)=gam_dist(j,length(y_b)/2).*pi.*AR;  
    C_Di_ell(j)=(C_L_Elliptic(j).^2)/(pi.*AR); 
    plot(y_b,gam_dist(j,:));
    hold on;
end
%------- CIRCULATION ALONG WINGSPAN --------%
xlabel('y/b [-]','FontSize',18);
ylabel('\Gamma(y)/(2bV_{\infty}) [-]','FontSize',18);
title("Circulation Distribution along Wing Span",'FontSize',24);
legend("\alpha=2 \circ","\alpha=4 \circ","\alpha=6 \circ","\alpha=8 \circ","\alpha=10 \circ");
grid on;
hold off;
figure;
% ------- COEFFICIENT OF LIFT _------- %
plot(aoa,C_L_Elliptic);
xlabel('\alpha [deg]','FontSize',18);
ylabel('C_L [-]','FontSize',18);
title("Coefficient of Lift Vs. Angle Of Attack - Elliptical Distribution",'FontSize',26);
set(gca,'FontSize',14);
grid on;
% --------------- COEFFICIENT OF DRAG -------%
figure;
plot(aoa,C_Di_ell);
xlabel('\alpha [deg]','FontSize',18);
ylabel('C_{D,i} [-]','FontSize',18);
title("Coefficient of Drag Vs. Angle of Attack - Elliptical Distribution",'FontSize',26);
set(gca,'FontSize',14);
grid on;

% -------- PART 2B --------- %
figure;
hold on 
N=2:1:16;
for i=1:length(N)
    theta_0=linspace(0.01, pi-0.01, N(i));
    for j=1:N(i)
        for k=1:N(i)
            LHS_temp(j,k,i)=((2/pi)*AR)*sin(k*theta_0(j))+k*(sin(k*theta_0(j))/sin(theta_0(j)));  %For rectangular wing --> AR=b/c.
        end    
    end
    LHS=LHS_temp(1:N(i),1:N(i),i);
    RHS=ones(N(i),1);
    An(1:N(i),i)=linsolve(LHS,RHS);
    plot(1:N(i),An(1:N(i),i),'*');
end
xlabel('N','FontSize',18);
ylabel('A_n/\alpha','FontSize',18);
title('Fourier Transform Coefficients Relative Values','FontSize',24);
set(gca,'FontSize',14);
legend('N=2','N=3','N=4','N=5','N=6','N=7','N=8','N=9','N=10','N=11','N=12','N=13','N=14','N=15','N=16');
hold off;
grid on;
yb=-cos(theta)./2;
for i=1:length(N)
    theta=linspace(0,pi); 
    for t=1:length(theta)
         gamma_dist(i,t)=sum(An(1:N(i),i).*sin((1:N(i))'.*theta(t)));
    end
end
figure;
hold on 
for a=1:length(aoa_radians)
    plot(yb,aoa_radians(a).*gamma_dist(15,:));
end
ylabel('\Gamma(y)/2bV_{\infty}');
xlabel('y/b');
title('Circulation Distribution Along the Wing N = 16','FontSize',24);
set(gca,'FontSize',12);
legend('\alpha=2 deg','\alpha=4 deg','\alpha=6 deg','\alpha=8 deg','\alpha=10 deg');
hold off;
grid on;
figure;
hold on 
for i=1:length(N)
    plot(yb,gamma_dist(i,:));
end
ylabel('\Gamma(y)/2bV_{\infty}\alpha');
xlabel('y/b');
title('Circulation Distribution Along the Wing N = 2-16','FontSize',24);
set(gca,'FontSize',12);
legend('N=2','N=3','N=4','N=5','N=6','N=7','N=8','N=9','N=10','N=11','N=12','N=13','N=14','N=15','N=16');
grid on;
hold off;
figure(13);
hold on;
C_L_first=An(1,end)*pi*AR;
C_Di_first=(C_L_first.^2/(pi*AR))*(1+sum((1:N(15))'.*An(:,15).^2)./An(1,15).^2);
C_L_vec=C_L_first*aoa_radians;
C_Di_vec=C_Di_first*aoa_radians;

plot(aoa, C_L_vec);
xlabel('\alpha [deg]','FontSize',18);
ylabel('C_L [-]','FontSize',18);
title("Coefficient of Lift Vs. Angle Of Attack - Fourier N = 16 series",'FontSize',26);
legend('AR=3','AR=6','AR=12','AR=20');
grid on;

figure;
plot(aoa, C_Di_vec);
xlabel('\alpha [deg]','FontSize',18);
ylabel('C_{D,i} [-]','FontSize',18);
title("Coefficient of Induced Drag Vs. Angle Of Attack - Fourier N = 16 series",'FontSize',26);
grid on;

