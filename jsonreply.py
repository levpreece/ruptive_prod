import numpy as np
import json
import globals

'''
A container for the cosine similarity value we want our sticky to be greater than or equal to
and the desired min size of the group(s) returned to the requestor. 
The initial values are the "imposible to match" settings.
'''
class RequestRequirements:
    threshold = 1
    groupSize = float('inf')
    _sessionIdentifier = ''

class RetVal:
    def __init__(self):
        self._indexes = []
        self._guids = []
        self._descriptions = []
        self._headers = [] #lplp1313 new value
        self._cos_sims = []
        self._targetGuid = ''
        self._targetDesc = ''
        self._targetHead = ''

    @property
    def targetGuid(self):
        return self._targetGuid

    @targetGuid.setter
    def targetGuid(self, guid):
        self._targetGuid = guid
        
    @property
    def targetDesc(self):
        return self._targetDesc

    @targetDesc.setter
    def targetDesc(self, desc):
        self._targetDesc = desc
    
    @property #lplp1313 new value
    def targetHead(self):
        return self._targetHead

    @targetHead.setter #lplp1313 new value
    def targetHead(self, head):
        self._targetHead = head

    @property
    def indexes(self):
        return self._indexes

    @indexes.setter
    def indexes(self, indxs):
        self._indexes.append(indxs)

    @property
    def guids(self):
        return self._guids

    @guids.setter
    def guids(self, gs):
        self._guids.append(gs)

    @property
    def descriptions(self):
        return self._descriptions

    @descriptions.setter
    def descriptions(self, descs):
        self._descriptions.append(descs)

    @property #lplp1313 new value 
    def headers(self):
        return self._headers

    @headers.setter #lplp1313 new value
    def headers(self, heads):
        self._headers.append(heads)

    @property
    def cos_sims(self):
        return self._cos_sims

    @cos_sims.setter
    def cos_sims(self, cs):
        self._cos_sims.append(cs)        

class StickyNotes:
    guids = []
    cos_sims = []
    descriptions = []
    headers = []  #lplp1313 new value
    indexs = []
    invalid = True
    _requirements = RequestRequirements()

    _jsonContent = ''
    _stickyNoteVector = None

    def getJson(self, JsonContentOrFilename, isFileName=True):
        if isFileName: #the json is in a file we'll open and return the content
            strJsonContent = globals._NOTFOUND
            try:
                with open(JsonContentOrFilename, 'rt', encoding='utf-8') as f:
                    strJsonContent = f.read()
            except FileNotFoundError:
                print("file not found!")    
        else:
            strJsonContent = JsonContentOrFilename
        return strJsonContent        

    def processStickyNotes(self, jsonContent='', filename='RutiveFile.json'):   
        stickies = None
        if jsonContent == '':
            jsonContent = self.getJson(filename)
            stickies = json.loads(jsonContent)
        else:
            stickies = jsonContent        

        self._requirements.threshold = stickies['data']['threshold'] 
        self._requirements.groupSize = stickies['data']['groupMinSize'] 
        self._requirements._sessionIdentifier = stickies['data']['id'] 

        ### below, remove unintended duplicates from the input sticky list
        ### collect the dict, separate into a list of tuples, then create a set
        ### move the set back to a dict list and replace the original dict list
        guidList = []
        descList = []
        headList = [] #lplp1313 new value

        [headList.append(h['header']) for h in stickies['data']['stickies']] #lplp1313 new value
        [descList.append(d['description']) for d in stickies['data']['stickies']]
        [guidList.append(g['guid']) for g in stickies['data']['stickies']]
        zippedUp = zip(headList, descList, guidList)
        setMatch = set(zippedUp)
        setMatch = list(setMatch)

        updated = []
        for i in range(len(setMatch)):
            element = {}
            element['header']=setMatch[i][0]
            element['description']=setMatch[i][1]
            element['guid']=setMatch[i][2] #lplp1313 new value
            updated.append(element)

        jsonContent['data']['stickies'] = updated

        self.guids = [guid['guid'] for guid in stickies['data']['stickies']] #WAS stickyListGuids 
        self.descriptions = [description['description'] for description in stickies['data']['stickies']] #WAS stickyListDescriptions 
        self.headers = [header['header'] for header in stickies['data']['stickies']] #lplp1313 new value 

class GroupSticky(object):
    """
    describes the sticky to be returned - its GUID and the Cosine Value that qulified it as a member of the group ID
    """
    def __init__(self):
        self._guid = ""
        self._desc = ""
        self._head = "" #lplp1313 new value
        self._cosineVal = 0

    @property
    def guid(self):
        return self._guid

    @guid.setter
    def guid(self, guid):
        self._guid = guid

    @property
    def desc(self):
        return self._desc

    @desc.setter
    def desc(self, desc):
        self._desc = desc

    @property #lplp1313 new value
    def head(self):
        return self._head

    @head.setter #lplp1313 new value
    def head(self, head):
        self._head = head

    @property
    def cosineVal(self):
        return self._cosineVal

    @cosineVal.setter
    def cosineVal(self, cosVal):
        self._cosineVal = cosVal

class Group(object):
    """
    describes the specific group with its ID and list of group sticky notes
    """
    def __init__(self):
        self._groupID = ""
        self._desc = ""
        self._targetSticky = {}
        self._groupStickies = []

    @property
    def targetSticky(self):
        return self._targetSticky

    @targetSticky.setter #lplp1313 new value
    def targetSticky(self, guid, desc, head, cosval=1.0):
        self._targetSticky["guid"] = guid
        self._targetSticky["desc"] = desc
        self._targetSticky["head"] = head
        self._targetSticky["cosineVal"] = str(cosval)

    @property
    def groupID(self):
        return self._groupID

    @groupID.setter
    def groupID(self, groupid):
        self._groupID = groupid

    @property
    def groupStickies(self):
        return self._groupStickies

    @groupStickies.setter
    def groupStickies(self, grpStickyList):
        self._groupStickies.append(grpStickyList)

class JsonReply:
    def __init__(self):
        self._data = {}
        self._id = ''
        self._groups = []

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def groups(self):
        return self._groups

    @groups.setter
    def groups(self, groups):
        self._groups.append(groups)

    def writeOutput(self): 
        o = {} #used to house the final json dict        
        data = {} #used to house the data for "o"
        data["id"]=self._id
        groups = [] #container for the array of group dicts

        for group in self._groups: #add each group member
            grp={}
            grp["groupID"]=group.groupID
            grp["targetSticky"]=group.targetSticky
            grp["groupStickies"]=[]
            for grpSticky in group.groupStickies:
                grp["groupStickies"].append({"guid":grpSticky.guid, "header":grpSticky.head, "cosineVal":str(grpSticky.cosineVal)}) #lplp1313 changed from desc to head in retval

            groups.append(grp)

        data["groups"] = groups #finish the json construct
        o["data"] = data

        return json.dumps(o)

class GroupMembership:
 
    def CreateGroup(self, guid, stickyNotes, modelVector):
        '''
        1. select the candidate - #see if this will find matches >= threshold AND form a group >= grpsize
        2. create temp vector based on original vector. Set all vector[index] to "1" to exclude from candidates group
        3. compare candidate sticky with the stickiesVector. 
        4. Pull out a subset of matches>=threshold and create a new group IFF the subset size >= grpsize
        5. Set the groupMembers array to True 
        6. Loop through all Sticky Notes until there's nothing left to review. 
        '''
        #############

        targetIndex = stickyNotes.guids.index(guid)
        vectorCopy = np.copy(modelVector.numpy())

        tvec  = np.copy(vectorCopy[targetIndex]) 

        #change the sticky note vector array from a tensor to a numpy type so we can edit
        vectorCopy[targetIndex] = np.zeros(len(vectorCopy[targetIndex])) #zero out the one doc we've select so we don't consider it

        #perform the matrix multiplication (cosine similarity - largest array value will be the closest sematic doc)
        cos_sims = np.transpose(np.inner(tvec,vectorCopy))

        #...and the winners are?
        headers  = [stickyNotes.headers[i] for i in np.where(cos_sims > stickyNotes._requirements.threshold)[0]] #lplp1313 new value
        descriptions = [stickyNotes.descriptions[i] for i in np.where(cos_sims > stickyNotes._requirements.threshold)[0]]        
        guids = [stickyNotes.guids[i] for i in np.where(cos_sims > stickyNotes._requirements.threshold)[0]] 
        indexes = list(np.where(cos_sims > stickyNotes._requirements.threshold)[0])
        cos_sims = cos_sims[indexes]
        
        #make sure we've a group worth returning (size matters)
        if (len(indexes) < stickyNotes._requirements.groupSize):
            return None

        retval = RetVal()
        retval.targetGuid = guid
        retval.targetDesc = stickyNotes.descriptions[targetIndex]
        retval.targetHead = stickyNotes.headers[targetIndex] #lplp1313 new value
        retval.indexes = indexes
        retval.guids = guids
        retval.descriptions = descriptions
        retval.headers = headers
        retval.cos_sims = cos_sims

        return retval

    def UpdateGroupMembership(self, newMembers):
        """
        check to see if there are any new members, update if there are
        no need to return value
        """
        globals.groupMembers[newMembers.targetGuid] = True #remove the target Sticky

        for guid in newMembers.guids[0]:
            globals.groupMembers[guid]=True

        group = Group()
        globals._groupNumber = globals._groupNumber+1
        group.groupID = globals._groupName + str(globals._groupNumber)
        group.targetSticky["guid"] = newMembers.targetGuid
        group.targetSticky["desc"] = newMembers.targetDesc
        group.targetSticky["head"] = newMembers.targetHead #lplp1313 new value

        guidSims = tuple(zip(newMembers.guids[0], newMembers.descriptions[0], newMembers.headers[0], list(newMembers.cos_sims[0]))) #lplp1313 new value 
        for g, d, h, c in guidSims:
            gs = GroupSticky()
            gs.guid=g
            gs.desc=d
            gs.head=h #lplp1313 new value
            gs.cosineVal=c
            group.groupStickies.append(gs)

        globals._jsonReply._groups.append(group)
