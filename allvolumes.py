import inro.emme.database.emmebank as _bank    
    
def __fetch_scenario(bank):
    for scenario in bank.scenarios():
        if 2000 <= scenario.number < 3000:
            yield scenario                
                    
def __fetch_links(s):            
    network_links = self.bank.scenario(s).get_network().links()            
    for link in network_links:
        yield link

def __get_bank(path):
    self.bank = _bank.Emmebank(path)


def create(**kargs):
    self.__get_bank(kargs['path'])        
    d = []
    measure = kargs['measure'].upper()
    for s in self.__fetch_scenario(self.bank):    