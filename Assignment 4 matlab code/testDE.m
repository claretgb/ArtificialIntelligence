path = '/Users/clara/Documents/GitHub/ArtificialIntelligence/Assignment 4 matlab code/';
addpath(genpath(path))

functions = [1 2 3 4 5 6 7 8 9 10]; %functions being solved
%example: functions = 1;
%example: functions = [2 4 9];
numF = size(functions,2);
nTimes = 20; % Number of times in which a function is going to be solved
dimension = 30; % Dimension of the problem
probabilityRecombination = 0.9;     
mutationF = 0.5; % F in [0,2]
populationSize = 50; % Adjust this to your algorithm

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
            % Mutate offspring.
            
            mutatedPopulation = zeros(populationSize,dimension);
            for indexMutation = 1:populationSize
                rands = randi([1, populationSize], 3, 1);
                mutatedPopulation(indexMutation,:) = population(rands(1),:) + mutationF*(population(rands(2),:)-population(rands(3),:));
            end
            
            % Recombination.
            
            offspring = population;
            for indexOffspring = 1:populationSize
                for indexDim = 1:dimension
                    randomValue = rand;
                    if(randomValue < probabilityRecombination)
                        offspring(indexOffspring,indexDim) = mutatedPopulation(indexOffspring,indexDim);
                        if offspring(indexOffspring,indexDim) > upper
                            offspring(indexOffspring,indexDim) = upper;
                        else
                            if offspring(indexOffspring,indexDim) < lower
                                offspring(indexOffspring,indexDim) = lower;
                            end
                        end
                    end
                end
            end
            
            % Selection.
            
            offspringFitness = calculateFitnessPopulation_2005(fitfun, offspring, o, A, M, a, alpha, b); %Fitness values of all individuals (smaller value is better)
            for indexNewPopulation = 1:populationSize
                if(offspringFitness(indexNewPopulation) < populationFitness(indexNewPopulation))
                    population(indexNewPopulation,:) = offspring(indexNewPopulation,:);
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
