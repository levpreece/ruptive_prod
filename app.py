import globals
import os
import numpy as np
import jsonreply 
import json
from singletonmodel import SingletonModel 
import tensorflow as tf
# import tensorflow_hub as hub

from flask import Flask, jsonify, request, session
from flask_cors import CORS, cross_origin
app = Flask(__name__)
CORS(app)

def initGlobals():
    globals._stickyNotes = None
    globals._stickyNotesCopy = None
    globals._theRequirements = None
    globals._jsonReply = None

    globals._stickyNotes = jsonreply.StickyNotes()
    globals._stickyNotesCopy = jsonreply.StickyNotes()
    globals._theRequirements = jsonreply.RequestRequirements()
    globals._jsonReply = jsonreply.JsonReply()
    globals._groupNumber = 0
    globals._groupName = "Group"
    globals.groupMembers = {}
    # globals.ModelPath = "home/USE_MODEL"
    # globals.ModelPath = "USE_MODEL"

#############################################
@app.route('/')
@cross_origin()
def home():
    try:
        #adding code to id model path local
        initGlobals()
        # model_path = ''
        # model_path = globals.ModelPath    
        # isDir = os.path.isdir(model_path)
        return "This is the root page of RUPTIVE ML that confirms the root address is correct and working."
    except Exception as ex:
        return "ERROR: {}".format(ex), 500

#############################################
@app.route('/groups/<reqID>', methods = ['GET'])
@cross_origin()
def groups(reqID):
    if request.method == 'GET':
        if (reqID == '123'):
            jsonStuff = jsonify({"id":reqID,"message":"This is the 123 request for groups based on the request ID {}.".format(reqID)})
        elif (reqID == "456"):
            jsonStuff = jsonify({"id":reqID,"message":"These would be the request for the 456 groups based on the request ID {}.".format(reqID)})
        else:
            jsonStuff = jsonify({"id":reqID,"message":"This is unhandled and you'd get groups based on the request ID {}.".format(reqID)})
        
        response = jsonStuff
        return response
      
    else:
        act="ERROR"

    return act
############################################
@app.route('/createGroups', methods = ['POST'])
@cross_origin()
def stickyNotes():
    initGlobals()
    req = ''
    if request.method == 'POST':
        try:
            req = request.get_json()
            # print(req) ###lplp1313: removed debug code...left here in case useful later
        ##################################################################  
            if req != None:  #Step 1: populate the stickies struct 
                globals._stickyNotes.processStickyNotes(jsonContent=req, filename=None)
            else: 
                globals._stickyNotes.processStickyNotes(filename="RuptiveFile.json")  

        ############################################
        # Populate the USE model to create sticky note vectors from array of notes            
            modelVector = SingletonModel()(globals._stickyNotes.descriptions)   
            
            # model_path = globals.ModelPath
            # model_path = "https://tfhub.dev/google/universal-sentence-encoder/4"
            # model = tf.saved_model.load(model_path)
            # model = hub.load(model_path)
            # modelVector = model(globals._stickyNotes.descriptions)   

            groupMembers = dict(zip(globals._stickyNotes.guids, np.zeros(len(globals._stickyNotes.guids),dtype=bool))) #Step 3: Setup the containers for the groups an the list of group members    
            
            globals._jsonReply.id = globals._stickyNotes._requirements._sessionIdentifier #Step 4: Begin the process of getting the return JSON together by create the object and setting its ID
            
            for guid in globals._stickyNotes.guids: #run through all the docs to discover if there are groups and not just pairs of similar stickies
                if groupMembers[guid]: #first, check stickyNote_vec[idx] to see if already a member. Continue if True
                    continue        

                gm = jsonreply.GroupMembership()
                retval = gm.CreateGroup(guid, globals._stickyNotes, modelVector) 
                if retval != None:
                    gm.UpdateGroupMembership(retval)

            output = json.loads(globals._jsonReply.writeOutput())
            # with open("JsonReply_" + str(globals._jsonReply.id) + ".json", "w") as outfile:
            #     json.dump(output, outfile)
        ##################################################################
            return jsonify(output), 200
        except Exception as ex:
            return "ERROR: possibly invalid JSON was submitted. Error Value was: {}".format(ex), 500

