def __init__(self, name = 'area',components=[],triggers =[], 
                 allComponents = []) -> None:
        self.name = name
        self.areaComponents =  components
        
        if allComponents == []:
            self.allComponents = self.areaComponents
        else:
            self.allComponents = allComponents
        
        self.startTrigger,self.stopTrigger = self.TriggerDef(triggers=triggers)         
        self.triggers = [self.startTrigger,self.stopTrigger]
        self.triggers = triggers
    
        self.relationships = self.relationAnalysis(self.areaComponents,self.allComponents)
        # print(self.relationships)
        areaSchedule = compScheduling(relationship_dict=self.relationships,title='Source_'+ self.name)
        # areaSchedule = cosimSchedule(self.relationships)
        self.cycleFlag = areaSchedule.cycleDetected
        self.cycleComp = areaSchedule.cycle_topological_order
        self.compSchedule = areaSchedule.topological_order
        self.cycleName = areaSchedule.cycleName
        
        self.exeComponents=[]
        for compName in self.compSchedule:
            for exeComp in self.allComponents:
                if exeComp.name == compName:
                    self.exeComponents.append(exeComp)
                    break