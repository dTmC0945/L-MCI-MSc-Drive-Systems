
% Parameters of a typical induction machine.
rs=6.03; %Stator resistance
rr=6.085; %Rotor resistance
Ls=489.3e-3;%Stator inductance
Lr=489.3e-3;%Rotor inductance
M=450.3e-3; % Mutual inductance
P=4;	%Poles
J=0.0228;%Inertia
sigma=(Ls*Lr)-(M*M);
B=0.000;
sls=sigma/Lr;
tr=Lr/rr;
sigma1=sigma/(Lr*Ls);
c1=(Lr/M);
c2=(Ls*Lr-M*M)/(M);
lst=sigma/Lr;

time = vertcat(Torque.time);
torque = vertcat(Torque.signals.values);
ias = vertcat(Ias.signals.values);
ibs = vertcat(Ibs.signals.values);
ics = vertcat(Ics.signals.values);
ids = vertcat(Ids.signals.values);
iqs = vertcat(Iqs.signals.values);
Nr = vertcat(nr.signals.values);
iar = vertcat(Iar.signals.values);
ibr = vertcat(Ibr.signals.values);
icr = vertcat(Icr.signals.values);
vds = vertcat(Vds.signals.values);
vqs = vertcat(Vqs.signals.values);
idr = vertcat(Idr.signals.values);
iqr = vertcat(Iqr.signals.values);

vds = [vds; 0; 0;0];

newdata = [time,torque, ias, ibs, ics,ids,iqs,iar, ibr, icr, Nr, vds, vqs, idr, iqr];
csvwrite('DynInd.csv',newdata)

plot(time,vds)
hold on
plot(time,vqs)
%writetable(struct2table(Torque), 'DynInTorque.csv')
