path = '/Users/clara/Documents/GitHub/ArtificialIntelligence/Assignment 4 matlab code/';
addpath(genpath(path))

functions = 1; %functions being solved
%example: functions = 1;
%example: functions = [2 4 9];
numF = size(functions,2);
nTimes = 1; % Number of times in which a function is going to be solved
dimension = 30; % Dimension of the problem
probabilityRecombination = 0.5;     
mutationF = 0.5; % F in [0,2]
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
            
            % Your algorithm goes here
            
            % Select parents and create offspring.
            % Mutate offspring.
           
            mutatedPopulation = population; %zeros(populationSize, dimension);
            for indexMutation = 1:populationSize
                rand1 = int8(1 + (populationSize-1).*rand);
                rand2 = rand1;
                while(rand2 == rand1)
                    rand2 = int8(1 + (populationSize-1).*rand);
                end
                rand3 = rand2;
                while(rand3 == rand2 || rand3 == rand1)
                    rand3 = int8(1 + (populationSize-1).*rand);
                end
                mutatedPopulation(indexMutation,randGene) = population(rand1) + mutationF*(population(rand2)-population(rand3));
            end
            
            % Recombination.
            
            offspring = population; %zeros(populationSize, dimension);
            randomValue = rand;
            for indexOffspring = 1:populationSize
                if(randomValue < probabilityRecombination)
                    offspring(indexOffspring) = mutatedPopulation(indexOffspring);
                end
            end
            
            % Selection.
            
            newPopulation = population; %zeros(populationSize, dimension);
            offspringFitness = calculateFitnessPopulation_2005(fitfun, offspring, o, A, M, a, alpha, b); %Fitness values of all individuals (smaller value is better)
            for indexNewPopulation = 1:populationSize
                if(populationFitness(indexNewPopulation) > offspringFitness(indexNewPopulation))
                    newPopulation(indexNewPopulation) = offspring(indexNewPopulation);
                end
            end
            
            population = newPopulation;
            
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