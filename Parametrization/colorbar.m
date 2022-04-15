% Height map 
figure 
contourf(peaks)
colormap("gray")
c = colorbar;

c.Location = 'southoutside';

c.Ticks = [-6.5 8];
c.TickLabels = {'0 mm','70 mm'};
c.TickLabelInterpreter = 'latex';

c.Label.String = 'Mould height $h$';
c.Label.Interpreter = 'latex';

% Shear angle map
figure 
contourf(peaks)
colormap("gray")
c = colorbar;

c.Location = 'southoutside';

c.Ticks = [-6.5 8];
c.TickLabels = {'$0^\circ$','$\gamma_{12}^{\rm{lim}}$'};
c.TickLabelInterpreter = 'latex';

c.Label.String = 'In-plane shear angle $\gamma_{12}$';
c.Label.Interpreter = 'latex';