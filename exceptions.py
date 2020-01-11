

class ConException(Exception):
    def __init__(self,*args,**kwargs):
        self.action = kwargs.pop('action',None)
        self.errmsg = kwargs.pop('errmsg',None)
        super(ConException,self).__init__(self,*args,**kwargs)
    def __str__(self):
        return "\nOups! something went wrong while "+self.action + \
        "\nI received the following error: "+self.errmsg
