path = '/Users/clara/Documents/GitHub/ArtificialIntelligence/Assignment 4 matlab code/';
addpath(genpath(path))

%functions = [1 2 3 4 5 6 7 8 9 10]; %functions being solved
%example: 
functions = 1;
%example: functions = [2 4 9];
numF = size(functions,2);
nTimes = 20; % Number of times in which a function is going to be solved
dimension = 30; % Dimension of the problem
populationSize = 100; % Adjust this to your algorithm
alp = 0.1;
delta = 0.005;
mutationProbability = 0.4;
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
            
            offspring = zeros(populationSize, dimension);
            intermediate = zeros(populationSize, dimension);
            newPopulation = zeros(populationSize, dimension);
            for halfNumberOfChildren = 1:2:populationSize
                % Choose participants.
                participants = randi([1,populationSize],1,numberOfParticipants);
                % Select two best.
                parents = [];
                [~, sortedIndexes] = sort(populationFitness);
                for indexSorted = 1:populationSize
                    if ismember(sortedIndexes(indexSorted), participants)
                        indexPop = sortedIndexes(indexSorted);
                        indexParents = length(parents)+1;
                        parents(indexParents,:) = population(indexPop,:);
                    end
                    if length(parents) == 2
                        break
                    end
                end
                child1 = zeros(1,dimension);
                for indexCrossover = 1:dimension
                    minFrame = min(parents(1,indexCrossover), parents(2,indexCrossover));
                    maxFrame = max(parents(1,indexCrossover), parents(2,indexCrossover));
                    difference = maxFrame - minFrame;
                    randGene = ((maxFrame+difference*alp)-(minFrame-difference*alp)).*rand + (minFrame-difference*alp);
                    child1(indexCrossover) = randGene;
                end
                intermediate(halfNumberOfChildren,:) = child1;
                randomProbability = rand;
                if randomProbability < mutationProbability
                    for indexMutation = 1:dimension
                        offspring(halfNumberOfChildren,indexMutation) = intermediate(halfNumberOfChildren,indexMutation) + sqrt(delta)*randn(1);
                    end
                end
                child1Fitness = calculateFitness_2005(fitfun, offspring(halfNumberOfChildren,:), o, A, M, a, alpha, b);
                child2 = zeros(1,dimension);
                for indexCrossover = 1:dimension
                    minFrame = min(parents(1,indexCrossover), parents(2,indexCrossover));
                    maxFrame = max(parents(1,indexCrossover), parents(2,indexCrossover));
                    difference = maxFrame - minFrame;
                    randGene = ((maxFrame+difference*alp)-(minFrame-difference*alp)).*rand + (minFrame-difference*alp);
                    child2(indexCrossover) = randGene;
                end
                intermediate(halfNumberOfChildren+1,:) = child2;
                randomProbability = rand;
                if randomProbability < mutationProbability
                    for indexMutation = 1:dimension
                        offspring(halfNumberOfChildren+1,indexMutation) = intermediate(halfNumberOfChildren+1,indexMutation) + sqrt(delta)*randn(1);
                    end
                end
                child2Fitness = calculateFitness_2005(fitfun, offspring(halfNumberOfChildren+1,:), o, A, M, a, alpha, b);
                toSortArray = zeros(1,4);
                toSortArray(1,1) = child1Fitness;
                toSortArray(1,2) = child2Fitness;
                toSortArray(1,3) = populationFitness(sortedIndexes(1));
                toSortArray(1,4) = populationFitness(sortedIndexes(2));
                [~, ind] = sort(toSortArray);
                elementsArray = zeros(4,dimension);
                elementsArray(1,:) = child1;
                elementsArray(2,:) = child2;
                elementsArray(3,:) = parents(1);
                elementsArray(4,:) = parents(2);
                newPopulation(halfNumberOfChildren,:) = elementsArray(ind(1),:);
                newPopulation(halfNumberOfChildren+1,:) = elementsArray(ind(2),:);
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
        arrayForMean(t) = bestSolutionFitness;
    end
    fprintf('Mean: %d\n', mean(arrayForMean));
end
