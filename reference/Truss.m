% Truss Analysis Code provided by Professor Mercado.

clear
close all
%Assume all force directions as tension



%Ax     Ay      Ey      AB      AH      HG      BH      BC      BG      CD      CG      GD      DF      GF       DE      EF
K=[
%joint A
-1      0       0       1     cosd(45)   0       0       0       0       0       0       0       0       0        0    0;  
0       -1      0       0     sind(45)     0       0       0       0       0       0       0       0        0      0     0;
%joint B
0       0       0        -1       0       0     -cosd(45)  1    cosd(45)  0       0       0        0       0        0    0;    
0       0      0        0         0       0      sind(45)  0     sind(45)  0       0       0        0       0        0    0; %=9.81
%joint C
0       0       0        0       0       0       0       -1        0       1       0       0        0       0       0    0; 
0       0       0        0       0       0       0       0         0       0       1       0        0       0       0    0;
%joint D
0       0       0        0       0       0       0       0           0       -1     0  -cosd(45)   cosd(45)   0     1      0  ;
0       0       0        0       0       0       0       0           0       0     0    sind(45)    sind(45)  0    0      0  ;
%joint E
0       0       0        0       0       0       0       0           0       0     0      0         0         0    -1     -cosd(45)  ;
0       0       -1        0       0       0       0       0           0       0     0      0         0         0    0      sind(45);
%joint F
0       0       0        0       0       0       0       0           0       0     0      0         -cosd(45)        -1    0    cosd(45)  ;
0       0       0        0       0       0       0       0           0       0     0      0         -sind(45)         0    0     -sind(45);
%joint G
0       0       0        0       0      -1       0       0      -cosd(45)    0      0   cosd(45)     0      1        0    0;
0       0       0        0       0       0       0       0      -sind(45)    0     -1   -sind(45)    0      0        0    0;
%joint H
0       0       0        0     -cosd(45)  1    cosd(45)   0       0       0       0       0        0       0        0    0;
0       0       0        0     -sind(45)  0   -sind(45)   0       0       0       0       0        0       0       0    0;
]; 


Eq=[
0    ;%Ax  
0    ;%Ay
0    ;%Bx 
0    ;%By
0    ;%Cx 
9.81   ;%Cy
0    ;%Dx
0   ;%Dy
0    ;%Ex
0    ;%Ey
0    ;%Fx
0    ;%Fy
0    ;%Gx
0    ;%Gy
0    ;%Hx
0    ;%Hy
];

F=K\Eq;

%Coordinates of nodes
Nodes =[ 
-1   0 ;%Ax0   1  
0   -1;%Ay0   2
30   -1;%Ey0   3 
0 0; %A    4
10 0; %B   5
15 0; %C  6
20 0; %D  7
30 0; %E  8
25 5; %F  9
15 5; %G  10
5  5; %H  11
];

%Indices of nodes conforming a member
Members=[
1   4    ;%Ax     
2   4    ;%Ay  
3   8    ;%Ey  
4   5    ;%AB  
4  11    ;%AH  
11    10    ;%HG
5    11    ;%BH
5    6    ;%BC
5    10    ;%BG
6    7    ;%CD
6    10    ;%CG
10    7    ;%GD
7    9    ;%DF
10      9    ;%GF
7      8    ;%DE
8      9    ;%EF
];




figure(2)

%Force limits
Fabs = abs(F);
Fmax = max(Fabs);


% Line thickness scaling
minW = 1.5;   % minimum line width
maxW = 10;     % maximum line width





for k = 1:size(Members,1)
        
        %Number of the first (i) and second (j) node of a member
        i = Members(k,1); 
        j = Members(k,2);

        %Coordinates of first (i) and second (j) node of a member
        x = [Nodes(i,1), Nodes(j,1)];
        y = [Nodes(i,2), Nodes(j,2)];

        %Coordinates of middle of member
        xm = (Nodes(i,1)+ Nodes(j,1))/2;
        ym = (Nodes(i,2)+ Nodes(j,2))/2;

    % --- 1. Scale thickness by absolute force ---
    lw = minW + (maxW - minW) * (Fabs(k)/Fmax);
    
    % --- 2. Scale color from red (-) to blue (+) ---
        % Map F(k) in range [-Fmax, Fmax] → color between red [1 0 0] and blue [0 0 1]
        %ratio = (F(k) + Fmax) / (2*Fmax);   % 0 = red, 1 = blue
        %color = [1-ratio, 0, ratio];        % RGB interpolation between red and blue
    
    % --- 2. color red (-) or blue (+) ---
        if F(k)<0;color = [1, 0, 0];  end
         if F(k)>0;color = [0, 0, 1];  end
        if F(k)==0;color = [0, 0, 0];  end
    
    plot(x, y, 'Color', color,'LineWidth', lw);
    text(xm-0.8, ym+0.3, sprintf('%.1f', F(k)), 'HorizontalAlignment', 'center', 'FontSize', 12);
    
    ylim([-2 7])
    xlim([-5 35])

hold on
end


%X forces
for k = 1:2:length(Eq) 

x0= Nodes(ceil(k/2)+3,1);
y0=Nodes(ceil(k/2)+3,2); %Adds 3 because nodes cooresponing to supports

dx= Eq(k)/10;
dy=0; 

%plot(Nodes(ceil(k/2)+3,1)+F(k),  Nodes(ceil(k/2)+3,2)  )

quiver(x0, y0, dx, dy, 0, 'MaxHeadSize', 0.5, ...
       'Color', 'k', 'LineWidth', 4);
end


%Y forces
for k = 2:2:length(Eq) 

x0= Nodes(ceil(k/2)+3,1);
y0=Nodes(ceil(k/2)+3,2); %Adds 3 because nodes cooresponing to supports

dx= 0;
dy=-Eq(k)/10; 

%plot(Nodes(ceil(k/2)+3,1)+F(k),  Nodes(ceil(k/2)+3,2)  )

quiver(x0, y0, dx, dy, 0, 'MaxHeadSize', 0.5, ...
       'Color', 'k', 'LineWidth', 4);
end




hold off