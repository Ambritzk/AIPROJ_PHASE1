import random 




    

class Level:
    def __init__(self,inputCount,outputCount):

        self.inputCount = inputCount
        self.outputCount = outputCount
        self.inputs = [None] * inputCount
        self.outputs = [None] * outputCount
        self.biases = [None] * outputCount#It's length must be the same as that of output

        self.weights = [[None]*outputCount for i in range(inputCount)]#It's a 2d array where the rows = inputcount and the columns = outputcount

        self.randomize()
    
    def FeedForward(givenInputs, level):
        for i in range(level.inputCount):
            level.inputs[i] = givenInputs[i]
        
        for i in range(level.outputCount):
            sum = 0
            for j in range(level.inputCount):
                sum += level.inputs[j]*level.weights[j][i]
            
            if sum > level.biases[i]:
                level.outputs[i] = 1
            else:
                level.outputs[i] = 0
        return level.outputs


    def randomize(level):
        for i in range(level.inputCount):
            for j in range(level.outputCount):
                level.weights[i][j] = random.random() * 2 - 1


                

        for j in range(len(level.biases)):        
            level.biases[j] = random.random() * 2 - 1



    


class NeuralNetwork:
    def __init__(self, neuronCounts: list):
        self.levels = []
        for i in range(len(neuronCounts) - 1):
            self.levels.append(Level(neuronCounts[i],neuronCounts[i + 1]))
    
    def feedForward(givenInputs,network):
        outputs = Level.FeedForward(givenInputs,network.levels[0])
        for i in range(1,len(network.levels)):
            outputs = Level.FeedForward(outputs,network.levels[i])
        return outputs