close all;
clear all;

npan=140;
aoa=linspace(-12,12,25).*pi/180;
m=4/100;
p=4/10;
t=8/100;
V_inf=1;
for z=1:length(aoa)
    clear A B C D E F G H i j K L m N;
    npan=140;
    m=4/100;
    p=4/10;
    t=2/100;
    V_inf=1;
    [xpan, ypan] = panel_generation(npan, aoa(z), m, p, t);
    dY = diff(ypan); dX = diff(xpan);
    S = hypot(dX, dY);
    theta = atan2(dY,dX);
    phi = mod(theta + 2.*pi,2.*pi);
    beta = acos(-sin(phi));
    for i = 1:length(xpan)-1
        x(i) = xpan(i) + dX(i)./2;
        y(i) = ypan(i) + dY(i)./2;
    end
    %---------------------------------- Step 1 & 2 ----------------------------------------
    for i=1:length(xpan)-1
        for j=1:length(xpan)-1
            if i==j
                K(i,j)=1;
                H(i,j)=-1;
                R(i,j)=pi/2;
                T(i,j)=pi/2;
            else
                A=-(x(i)-xpan(j)).*cos(phi(j))-(y(i)-ypan(j)).*sin(phi(j));
                B=(x(i)-xpan(j)).^2+(y(i)-ypan(j)).^2;
                C=sin(phi(i)-phi(j));
                D=cos(phi(i)-phi(j));
                E=(x(i)-xpan(j)).*sin(phi(j))-(y(i)-ypan(j)).*cos(phi(j));
                F=log(1+(S(j).^2+2*A.*S(j))/B);
                G=atan2((E.*S(j)),(B+A.*S(j)));
                P=(x(i)-xpan(j)).*sin(phi(i)-2.*phi(j)) + (y(i)-ypan(j)).*cos(phi(i)-2.*phi(j));
                Q=(x(i)-xpan(j)).*cos(phi(i)-2.*phi(j)) - (y(i)-ypan(j)).*sin(phi(i)-2.*phi(j));
                K(i,j)=D+0.5*(Q.*F)/S(j)-(A.*C+D.*E).*G/S(j);
                H(i,j)=0.5*D.*F+C.*G-K(i,j);
                T(i,j)=C+0.5*(P.*F)/S(j)+(A.*D-C.*E).*G/S(j);
                R(i,j)=0.5*C.*F-D.*G-T(i,j);
            end
        end
    end
    K_reduced=K;
    K_rownew = 1:length(xpan)-1;
    K_colnew = 0:length(xpan)-1;
    K = [K_rownew; K];
    K = [K_colnew' K];  %Answer Checked

    %-------------------------------------- Step 3 ------------------------------------------
    for i=1:length(xpan)
        if i~=length(xpan)
            N(i)=-2*pi*V_inf.*sin(aoa(z)-phi(i));
            for j=1:length(xpan)
                if j==1
                    L(i,j)=H(i,j);
                else if j==length(xpan)
                    L(i,j)=K_reduced(i,j-1);
                end
                end
                for j=2:length(xpan)-1
                    L(i,j)=H(i,j)+K_reduced(i,j-1);
                end
            end
        end
        if i==length(xpan)
            N(i)=0;
            for j=1:length(xpan)
                L(i,j)=0;
                if j==1
                    L(i,j)=1;
                else if j==length(xpan)
                    L(i,j)=1;                   
                    end    
                end
            end
        end
    end
    gam_i=L\N'; 
    kutta_check=gam_i(1)+gam_i(length(xpan));   % Kutta Condition
    %figure(3);
    %plot(1:length(xpan),gam_i/V_inf);
    %ylim([-1.5 1.5]);
    %xlabel('i','FontSize',20);
    %ylabel('$\frac{\gamma}{V_inf}$', 'Interpreter','latex', 'FontSize',20);
    %title("Vortex Panel Strength with 140 Panels for NACA-2412 (AOA = 0 deg)",'FontSize',26);

    %-------------------------------- Step 4 -------------------------------------
    for i=1:length(xpan)-1
        for j=1:length(xpan)-1
            if j==1
                W(i,j)=R(i,j);
            else
                W(i,j)=R(i,j)+T(i,j-1);
            end
        end
    end
    W=[W T(:,length(xpan)-1)];
    Vsum=0;
    for j=1:length(xpan)
        Vsum=Vsum+W(:,j).*(gam_i(j)/(2*pi));
    end
    half_npan = npan/2;
    Vt=V_inf.*cos(aoa(z)-phi)+Vsum(1:length(xpan)-1)';
    Cp=1-(Vt./V_inf).^2;
    Cp_top = Cp(ceil(length(Cp)/2)+1:length(Cp));
    Cp_bot = flip(Cp(1:half_npan));
    Cl_bot = Cp_bot.*flip(sin(beta(1:half_npan)));
    Cl_top = Cp_top.*sin(beta((length(xpan)-1)/2+1:npan));
    Cl_bot = Cl_bot.*flip(S(1:half_npan));
    Cl_top = Cl_top.*S(half_npan+1:npan);
    Cl_net(z) = sum(Cl_bot)-sum(Cl_top);
    %figure(4);)
    Cd_bot = Cp_bot.*flip(cos(beta(1:half_npan)));
    Cd_top = Cp_top.*cos(beta(half_npan+1:npan));
    Cd_bot = Cd_bot.*flip(S(1:half_npan));
    Cd_top = Cd_top.*S(half_npan+1:npan);
    Cd_net(z) = sum(Cd_bot)+sum(Cd_top);
    
end
Alpha_XFLR = xlsread('NACA2412WB.xlsx', 1, 'A:A');
cl_XFLR = xlsread('NACA2412WB.xlsx',1,'B11:B43');
cd_XFLR = xlsread('NACA2412WB.xlsx',1,'C:C');
theta_p=acos(-(2*p-1));
alpha_L0 = (m/(4*pi*(p^2)*(p-1)^2))*((8*p-6)*(pi*p^2-2*p*theta_p+theta_p)+8*(2*p^2-3*p+1)*sin(theta_p)+(2*p-1)*sin(2*theta_p));
cl_airfoil = 2.*pi.*(aoa-alpha_L0);
aoa = aoa.*180./pi;
% ------- PART 1A ------------- % 
figure;
plot(aoa, cl_airfoil);
xlabel('\alpha [deg]','FontSize',20);
ylabel('C_l [-]','FontSize',20);
title("Thin Airfoil Theory Lift Coefficient vs. Angle of Attack for NACA-2412",'FontSize',26);
grid on;

% ----------- PART 1B -------%
% -- First part, vortex + Thin Airfoil Comparison --%
figure;
plot(aoa,cl_airfoil,aoa,Cl_net);
ylim([-0.5,1.5]);
xlim([-4,12])
xlabel('\alpha [deg]','FontSize',20);
ylabel('C_l [-]','FontSize',20);
title("Lift Coefficient vs. Angle of Attack for NACA-2412",'FontSize',26);
legend("Thin Airfoil Theory Method","Vortex Panel Method");
grid on;
% -- Second part, Cd versus alpha --%
figure;
plot(aoa,Cd_net);
xlabel('\alpha [deg]','FontSize',20);
ylabel('C_d [-]','FontSize',20);
title("Vortex Panel Method Drag Coefficient vs. Angle of Attack for NACA-2412",'FontSize',26);
grid on;
xlim([-4,12]);
% ---------- PART 1C ------------%
figure;
plot(aoa,Cl_net,aoa,cl_airfoil, Alpha_XFLR, cl_XFLR);
ylim([-0.5,1.5]);
xlim([-4,12]);
xlabel('\alpha [deg]','FontSize',20);
ylabel('C_l [-]','FontSize',20);
title("Lift Coefficient vs. Angle of Attack for NACA-2412",'FontSize',26);
legend("Thin Airfoil Theory Method","Vortex Panel Method", "XFLR Data");
grid on;
figure;
hold on;
plot(aoa,Cd_net);
plot(Alpha_XFLR,cd_XFLR);
legend("Vortex Panel Method", "XFLR Data");
xlabel('\alpha [deg]','FontSize',20);
ylabel('C_d [-]','FontSize',20);
title("Drag Coefficient vs. Angle of Attack for NACA-2412",'FontSize',26);
grid on;
xlim([-4,12]);


%----------------------------------------------------%
%------------ PART E - MACH NUMBER EFFECTS ----------%
% -- This is a comparison from VP method -- %
Cl_net_Mach1=Cl_net./sqrt(1-0.1^2);
Cl_net_Mach2=Cl_net./sqrt(1-0.4^2);
Cl_net_Mach3=Cl_net./sqrt(1-0.7^2);
figure;
plot(aoa,Cl_net_Mach1,aoa,Cl_net_Mach2,aoa, Cl_net_Mach3);
xlabel('\alpha [deg]','FontSize',20);
ylabel('C_l [-]','FontSize',20);
title("VP Method - Lift Coefficient vs. Angle of Attack for NACA-4412",'FontSize',26);
legend("M = 0.1","M = 0.4","M = 0.7");
xlim([-4,12]);
grid on;
% Mach Number Effects XLFR Data %
figure;
Alpha_01 = xlsread('m111.xlsx', 1, 'A:A');
Alpha_04 = xlsread('m444.xlsx', 1, 'A:A');
Alpha_07 = xlsread('m777.xlsx', 1, 'A:A');
Cl_01 =  xlsread('m111.xlsx', 1, 'B:B');
Cl_04 = xlsread('m444.xlsx', 1, 'B:B');
Cl_07 = xlsread('m777.xlsx', 1, 'B:B');
plot(Alpha_01, Cl_01, Alpha_04, Cl_04, Alpha_07, Cl_07);
xlabel('\alpha [deg]','FontSize',20);
ylabel('C_l [-]','FontSize',20);
title("XFLR Data - Lift Coefficient vs. Angle of Attack for NACA-4412 From XLFR Data",'FontSize',24);
legend("M = 0.1","M = 0.4","M = 0.7");
grid on;