
class NetworkController:
    @property
    def link_status(self) -> bool:
        raise NotImplementedError
    
    @property
    def socket(self):
        raise NotImplementedError
    
    @property
    def interface(self):
        raise NotImplementedError
    
    def debug_info():
        raise NotImplementedError
