path = '/Users/clara/Documents/GitHub/ArtificialIntelligence/Assignment 4 matlab code/';
addpath(genpath(path))

functions = 1; %functions being solved
%example: functions = 1;
%example: functions = [2 4 9];
numF = size(functions,2);
nTimes = 1; % Number of times in which a function is going to be solved
dimension = 30; % Dimension of the problem
populationSize = 100; % Adjust this to your algorithm

for i = 1:numF
    
    fitfun = functions(i); %fitfun is the function that we are solving
    
    fprintf('\n-----  Function %d started  -----\n\n', fitfun);
    
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
        
        % Algorithm loop
        
        while(objetiveValue < bestSolutionFitness && currentEval < maxEval)
            
%             % Your algorithm goes here
%             
%             % Select parents and create offspring.
%             indexBest = 0;
%             x = 0;
%             while(x ~= bestSolutionFitness)
%                 indexBest = indexBest + 1;
%                 x = populationFitness(indexBest);
%             end
%             parentI = population(indexBest,:);
%             indexSecondBest = 0;
%             y = 0;
%             bestSoFar = 0;
%             for indexPop = 1:10
%                 indexSecondBest = indexSecondBest + 1;
%                 y = populationFitness(indexSecondBest);
%                 if(y > bestSolutionFitness)
%                     if(y < bestSoFar)
%                         bestSoFar = y;
%                     end
%                 end
%             end
%             parentJ = population(indexSecondBest,:);
%             newPopulation = zeros(populationSize, dimension);
%             for inx = 1:9
%                 firstLimit = int8(1 + ((dimension-1)-1).*rand);
%                 secondLimit = int8(1 + ((dimension-firstLimit-1)-1).*rand) + firstLimit;
%                 auxArray = zeros(1,secondLimit-firstLimit);
%                 for index2 = firstLimit:secondLimit
%                     auxArray(1,index2-firstLimit+1) = parentI(1,index2);
%                 end
%                 child = zeros(1,dimension);
%                 counter = 1;
%                 for index3 = 1:dimension
%                     truthValue = ismember(parentJ(index3), auxArray);
%                     if(~truthValue)
%                         child(counter) = parentJ(index3);
%                         counter = counter+1;
%                     end
%                 end
%                 for index4 = firstLimit:secondLimit
%                     child(index4) = auxArray(index4-firstLimit+1);
%                 end
%                 newPopulation(inx,:) = child;
%             end
%             newPopulation(10,:) = parentI;
%             population = newPopulation;






   % Your algorithm goes here
            
            % Select parents and create offspring.
            [~,indexBest] = min(populationFitness);
            
            parentI = population(indexBest,:);
            newPopulation = zeros(populationSize, dimension);
            for inx = 1:populationSize-1
                parentJ = population(inx+1,:);
                child = zeros(1,dimension);
                for indexChild = 1:dimension
                    child(indexChild) = (parentI(indexChild) + parentJ(indexChild))/2;
                end
                newPopulation(inx,:) = child;
            end
            newPopulation(10,:) = parentI;
            population = newPopulation;







            
            % Mutate offspring.
            
            rand3 = int8(1 + (9-1).*rand);
            for indexMutation = rand3:9
                rand1 = int8(1 + (dimension-3).*rand);
                rand2 = int8(rand1 + (dimension-1-rand1).*rand);
                difference = rand2 - rand1;
                for indexDif = 1:difference
                    child = population(indexMutation,:);
                    auxMutation = child(1,rand1);
                    child(1,rand1) = child(1,rand2);
                    child(1,rand2) = auxMutation;
                end
            end
            
            % Your algorithm stops here
            
            populationFitness = calculateFitnessPopulation_2005(fitfun, population, o, A, M, a, alpha, b); %Fitness values of all individuals (smaller value is better)
            bestSolutionFitness = min(populationFitness);
            currentEval = currentEval + populationSize;
            if bestSolutionFitness < globalFitness
                globalFitness = bestSolutionFitness;
                fprintf('GlobalFitness: %d, Generations: %d\n', globalFitness, g);
            end
            
            g = g + 1;
            
            % Your algorithm goes here
            
            % Is there anything that should go here?
            
            % Your algorithm stops here
            
        end
        
        % best individual
        bestSolutionFitness = min(populationFitness);
        fprintf('%dth run, The best individual fitness is %d\n', t, bestSolutionFitness);
        
    end
    
end
