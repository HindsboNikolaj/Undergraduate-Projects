clear all;
close all;
alpha = -12:0.01:12;
alpha = alpha.*pi/180;
cl = 2.*pi.*(alpha+0.036);
figure(1);
plot(alpha.*180./pi, cl)
grid on;
xlabel("\alpha (deg) [-]");
ylabel("Coefficient of Lift [-]");
