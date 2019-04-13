path = '/Users/clara/Documents/GitHub/ArtificialIntelligence/Assignment 4 matlab code/';
addpath(genpath(path))

functions = [1 2 3 4 5 6 7 8 9 10]; %functions being solved
%example: functions = 1;
%example: functions = [2 4 9];
numF = size(functions,2);
nTimes = 20; % Number of times in which a function is going to be solved
dimension = 30; % Dimension of the problem
populationSize = 20; % Adjust this to your algorithm
alp = 0.25;
delta = 0.15;
mutationProbability = 0.1;
numberOfParticipants = int8(populationSize/4);

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
        
        % Algorithm loop
        
        while(objetiveValue < bestSolutionFitness && currentEval < maxEval)
            
            % Your algorithm goes here

            % Select parents and create offspring.
            [~,indexBest] = min(populationFitness);
            parentI = population(indexBest,:);
            offspring = zeros(populationSize, dimension);
            for halfNumberOfChildren = 1:populationSize
                child = zeros(1,dimension);
                indexParentJ = indexBest;
                while indexParentJ == indexBest
                    indexParentJ = int8(1+(populationSize-1).*rand);
                end
                parentJ = population(indexParentJ,:);
                for indexCrossover = 1:dimension
                    minFrame = min(parentI(indexCrossover), parentJ(indexCrossover));
                    maxFrame = max(parentI(indexCrossover), parentJ(indexCrossover));
                    difference = maxFrame - minFrame;
                    randGene = ((maxFrame+difference*alp)-(minFrame-difference*alp)).*rand + (minFrame-difference*alp);
                    child(indexCrossover) = randGene;
                end
                offspring(halfNumberOfChildren,:) = child;
            end
            for indexMutation = 1:populationSize
                randomProbability = rand;
                if randomProbability < mutationProbability
                    if indexMutation ~= indexBest
                        for indexMutation2 = 1:dimension
                            population(indexMutation,indexMutation2) = offspring(indexMutation,indexMutation2) + sqrt(delta)*randn(1);
                        end
                    end
                end
            end
            
            % Your algorithm stops here
            
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
        bestSolutionFitness = min(populationFitness);
        fprintf('%dth run, The best individual fitness is %d\n', t, bestSolutionFitness);
        arrayForMean(t) = bestSolutionFitness;
    end
    fprintf('Mean: %d\n', mean(arrayForMean));
end
