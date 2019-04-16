path = '/Users/clara/Documents/GitHub/ArtificialIntelligence/Assignment 4 matlab code/';
addpath(genpath(path))

functions = [1 2 3 4 5 6 7 8 9 10]; %functions being solved
%example: functions = 1;
%example: functions = [2 4 9];
numF = size(functions,2);
nTimes = 20; % Number of times in which a function is going to be solved
dimension = 30; % Dimension of the problem
populationSize = 200; % Adjust this to your algorithm
Vmax = 1.5; % Maximum movement that the particle will take in every generation.
phy1 = 0.05;
phy2 = 2;

for i = 1:numF
    
    fitfun = functions(i); %fitfun is the function that we are solving
    
    fprintf('\n-----  Function %d started  -----\n\n', fitfun);
    
    arrayForMean = zeros(1,nTimes);
    
    for t = 1:nTimes
        
        maxEval = 10000*dimension; % maximum number of evaluation
        [value, upper,lower,objetiveValue, o, A, M, a, alpha, b] = getInformation_2005(fitfun, dimension);
        
        currentEval = 0;
        
        % Start generating the initial population
        
        population = zeros(populationSize, dimension);
        
        for j =1:populationSize
            
            population(j,:) = lower + (upper-lower).*rand(1,dimension);
            
        end
        
        populationFitness = calculateFitnessPopulation_2005(fitfun, population, o, A, M, a, alpha, b); %Fitness values of all individuals (smaller value is better)
        bestSolutionFitness = min(populationFitness);
        currentEval = currentEval + populationSize;
        globalFitness = bestSolutionFitness;
        g = 1;
        
         %Particle creation.
            %X = zeros(populationSize,dimension); % Location of the particle.
            %pBest = X;
            pBest = population;
            x_fitness = populationFitness;
            V = zeros(populationSize,dimension); % Gradient (direction, velocity) that the particle will move.
            pBest_fitness = x_fitness;
            
            for ind = 1:populationSize
                for idx = 1:dimension
                    %X(ind,idx) = (upper - lower).*rand + lower;
                    V(ind,idx) = (Vmax + Vmax).*rand - Vmax;
                end
            end
        
        
        % Algorithm loop
        
        while(objetiveValue < bestSolutionFitness && currentEval < maxEval)
            
            % Your algorithm goes here
            
            [~,gid] = min(x_fitness);
            
            for ind = 1:populationSize
                for idx = 1:dimension
                    %V(ind,idx) = V(ind,idx) + phy1*rand*(pBest(ind,idx)-X(ind,idx)) + phy2*rand*(X(gid,idx) - X(ind,idx));
                    V(ind,idx) = V(ind,idx) + phy1*rand*(pBest(ind,idx)-population(ind,idx)) + phy2*rand*(population(gid,idx) - population(ind,idx));
                    if V(ind,idx) > Vmax
                        V(ind,idx) = Vmax;
                    elseif V(ind,idx) < -Vmax
                        V(ind,idx) = -Vmax;
                    end
                end
            end
            
            %X = X + V;
            population = population + V;
            
            for ind = 1:populationSize
                for idx = 1:dimension
                    if population(ind,idx) > upper
                        population(ind,idx) = upper;
                    elseif population(ind,idx) < lower
                        population(ind,idx) = lower;
                    end
                end
            end
            
            
            %x_fitness = calculateFitnessPopulation_2005(fitfun, X, o, A, M, a, alpha, b); %Fitness values of all individuals (smaller value is better)
            x_fitness = calculateFitnessPopulation_2005(fitfun, population, o, A, M, a, alpha, b); %Fitness values of all individuals (smaller value is better)
            
            for idxFit = 1:populationSize
                if x_fitness(idxFit) < pBest_fitness(idxFit)
                    pBest_fitness(idxFit) = x_fitness(idxFit);
                    %pBest(idxFit) = X(idxFit);
                    pBest(idxFit) = population(idxFit);
                end
            end
            
            
            % Your algorithm stops here
            
            %populationFitness = calculateFitnessPopulation_2005(fitfun, X, o, A, M, a, alpha, b); %Fitness values of all individuals (smaller value is better)
            populationFitness = calculateFitnessPopulation_2005(fitfun, population, o, A, M, a, alpha, b); %Fitness values of all individuals (smaller value is better)
            bestSolutionFitness = min(populationFitness);
            currentEval = currentEval + populationSize;
            if bestSolutionFitness < globalFitness
                globalFitness = bestSolutionFitness;
                %fprintf('GlobalFitness: %d, Generations: %d\n', globalFitness, g);
            end
            
            g = g + 1;
            
            % Your algorithm goes here
            
            % Is there anything that should go here?
            
            % Your algorithm stops here
            
        end
        
        % best individual
        bestSolutionFitness = min(pBest_fitness);
        fprintf('%dth run, The best individual fitness is %d\n', t, bestSolutionFitness);
        arrayForMean(t) = bestSolutionFitness;
    end
    fprintf('Mean: %d\n', mean(arrayForMean));
end
