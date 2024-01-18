from abc import abstractclassmethod, ABC


class DataStoreSpi(ABC):
    
    @abstractclassmethod
    def create_task(self,data):
        pass
    
    @abstractclassmethod
    def update_task(self,data):
        pass
    
    @abstractclassmethod
    def delete_task(self,data):
        pass
    
    @abstractclassmethod
    def get_task(self,data):
        pass
    
    @abstractclassmethod
    def create_user(self,data):
        pass
    
    @abstractclassmethod
    def update_user(self,data):
        pass
    
    @abstractclassmethod
    def delete_user(self,data):
        pass