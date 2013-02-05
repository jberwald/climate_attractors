% u = ikeda parameter
% option = what to plot
%  'trajectory' - plot trajectory of random starting points
%  'limit' - plot the last few iterations of random starting points
function ikeda(u, option)
    P = 200;%how many starting points
    N = 1000;%how many iterations
    Nlimit = 20; %plot these many last points for 'limit' option
 
    x = randn(1,P)*10;%the random starting points
    y = randn(1,P)*10;
 
    for n=1:P,
        X = compute_ikeda_trajectory(u, x(n), y(n), N);
 
        switch option
        case 'trajectory' %plot the trajectories of a bunch of points
            plot_ikeda_trajectory(X);hold on;
 
        case 'limit'
            plot_limit(X, Nlimit); hold on;
 
        otherwise
            disp('Not implemented');
        end
    end
 
    axis tight; axis equal
    text(-25,-15,['u = ' num2str(u)]);
    text(-25,-18,['N = ' num2str(N) ' iterations']);
    end
 
    % Plot the last n points of the curve - to see end point or limit cycle
    function plot_limit(X,n)
    plot(X(end-n:end,1),X(end-n:end,2),'ko');
end
 
% Plot the whole trajectory
function plot_ikeda_trajectory(X)
    plot(X(:,1),X(:,2),'k');
    %hold on; plot(X(1,1),X(1,2),'bo','markerfacecolor','g'); hold off
end
 
%u is the ikeda parameter
%x,y is the starting point
%N is the number of iterations
function [X] = compute_ikeda_trajectory(u, x, y, N)
    X = zeros(N,2);
    X(1,:) = [x y];
 
    for n = 2:N
 
        t = 0.4 - 6/(1 + x^2 + y^2);
        x1 = 1 + u*(x*cos(t) - y*sin(t)) ;
        y1 = u*(x*sin(t) + y*cos(t)) ;
        x = x1;
        y = y1;
 
        X(n,:) = [x y];
 
    end
end
