function G = diffusionMap( dataname, nvecs )

% Diffusion Map script (requires DiffusionGeometry package from
% M. Maggioni: http://www.math.duke.edu/~mauro/code.html)
% 
% Data -- N x D dimensional array. (I.e. N points in D dimensions.)
%
% nvecs -- number of eigenvectors
%
% Returns a Graph diffusion object G. See GraphDiffusion.m for details.
%

if nargin < 1, fprintf( 'Provide path to data file\n' ); end;
if nargin < 2, nvecs = 7; end;
data = load( dataname );
data = data.C;

% Note: tolerance is hardcoded for now!
G = GraphDiffusion( data, 0, struct('kEigenVecs', nvecs, ...
                                    'Normalization','markov', 'kNN', ...
                                    2));

% plot the first 2 and three eigenfuncstions
figure;
clf;
%subplot(1,2,1);
% the embedded points correspond to the small spiral
% $$$ plot( G.EigenVecs(1:2001,2), G.EigenVecs(1:2001,3), 'r.' );
% $$$ hold on;
% $$$ % the points embedded in this part correspond to the larger
% $$$ % attractor 
% $$$ plot( G.EigenVecs(2002:4002,2), G.EigenVecs(2002:4002,3), 'b.' );
% $$$ subplot(1,2,2);
plot3( G.EigenVecs(1:2001,2), G.EigenVecs(1:2001,3), ...
       G.EigenVecs(1:2001,4), 'ro', 'MarkerFaceColor', 'r' );
hold on;
plot3( G.EigenVecs(2002:4002,2), G.EigenVecs(2002:4002,3), ...
       G.EigenVecs(2002:4002,4), 'bo', 'MarkerFaceColor', 'b' );
xlabel( 'x' );
ylabel( 'y' );
zlabel( 'z' );
grid on;
set(gca,'Color',[0.8 0.8 0.8]);
hold off;
% $$$ figure;
% $$$ subplot(1,2,1);
% $$$ plot( G.EigenVecs(:,5), G.EigenVecs(:,6), '.' );
% $$$ subplot(1,2,2);
% $$$ plot3( G.EigenVecs(:,5), G.EigenVecs(:,6), G.EigenVecs(:,7), '.' );

% The first eigenval/vec is ommitted since that vector/function corresponds to the
% constant function
