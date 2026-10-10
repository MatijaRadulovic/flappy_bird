import random
import numpy as np
import math
import copy    
from scipy.special import expit

class Network:
               
                
    
    def __init__(self,input_size,hidden_size,output_size,hid_layer_num):
        
        self.input_size=input_size
        self.hidden_size=hidden_size
        self.output_size=output_size
        self.hid_layer_num=hid_layer_num    
        
        
        self.weights=[]    
        
        
        self.biases=[]   

        
        self.weights.append( np.zeros((self.input_size, self.hidden_size)) )

        for n in range(1,hid_layer_num):
            self.weights.append( np.zeros((self.hidden_size, self.hidden_size)) )

        self.weights.append( np.zeros((self.hidden_size, self.output_size)))

        
        
        
        for n in range(hid_layer_num):
            self.biases.append( np.zeros(self.hidden_size))
        self.biases.append (np.zeros(self.output_size))
        
        
    

    def SetValues(self,layer,from_node,to_node,weight,bias):
        pass
    
    def MutantClone(self, prob, amount):
        clone=copy.deepcopy(self)

        for n in range(1,self.hid_layer_num+2):

            (layer_weights,layer_biases)=clone.get_values_for_layer(n)
            
            num_weights=len(layer_weights)
            num_nodes=len(layer_biases)
            
            for i in range(num_nodes):
                p=random.random()
                if p<prob:
                    layer_biases[i]+= random.gauss(0,amount)
        
                for j in range(num_weights):
                    if random.random()<prob:
                        layer_weights[j,i]+= random.gauss(0,amount)
                        
                
        return clone
    
    @staticmethod
    def MakeChild(parent1,parent2,cross_prob=0): 
        clone= copy.deepcopy(parent1)
        
        for n in range(1,parent1.hid_layer_num+2):

            (layer_weights1,layer_biases1)=parent1.get_values_for_layer(n)
            (layer_weights2,layer_biases2)=parent2.get_values_for_layer(n)
            (layer_weightsc,layer_biasesc)=clone.get_values_for_layer(n)
            
            num_weights=len(layer_weights1)
            num_nodes=len(layer_biases1)
            
            for i in range(num_nodes):
                if random.random()<cross_prob:
                    layer_biasesc[i]= (layer_biases1[i]+layer_biases2[i])/2
                else:
                    if random.random()<0.5:
                        layer_biasesc[i]=layer_biases1[i]
                    else:
                        layer_biasesc[i]=layer_biases2[i]

                for j in range(num_weights):
                    if random.random()<cross_prob:
                        layer_weightsc[j,i]= (layer_weights1[j,i]+layer_weights2[j,i])/2
                    else:
                        if(random.random()<0.5):
                            layer_weightsc[j,i]=layer_weights1[j,i]
                        else:
                            layer_weightsc[j,i]=layer_weights2[j,i]

        return clone

    @staticmethod
    
    def __Sigmoid(x):
        y=expit(x)
        return y
       

     
    def get_values_for_layer(self,layer):
        return (self.weights[layer-1],self.biases[layer-1])
    
    def get_values_for_node(self,layer,node): 
        (layer_wights,layer_biases)=self.get_values_for_layer(layer)
        return (layer_wights[:,node],layer_biases[node])
    
    def NodeCalculateOutput(self,layer,node,inputs):
        weights,bias=self.get_values_for_node(layer,node)
        return np.dot(inputs,weights)+bias   
    
    def NodeOutput(self,layer,node,inputs):
        x=self.NodeCalculateOutput(layer,node,inputs)
        return Network.__Sigmoid(x)



    
    @staticmethod        
    def __LayerOutputs(inputs, weights, biases):
        func=np.vectorize(Network.__Sigmoid)
        return  func(np.add( np.dot(inputs,weights),biases))

    def Output(self,inputs):
  
        curr_layer_out= inputs
        
        for i in range(1,self.hid_layer_num+2):
            (weights,biases)=self.get_values_for_layer(i)
            curr_layer_out= Network.__LayerOutputs(curr_layer_out,weights,biases)

        return curr_layer_out

    
    def pprint(self):
        b=''
        for i in range(self.hid_layer_num+1):
            for y in self.weights[i]:
                b+=('\t'.join('%0.3f' %x for x in y))+'\n'
                
            c= '\t'.join('%0.3f' %y for y in self.biases[i])
            ret=b+c+'\n'
        return ret


    def Draw():
        pass