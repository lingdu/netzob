#!/usr/bin/python
# -*- coding: utf-8 -*-

#+---------------------------------------------------------------------------+
#|         01001110 01100101 01110100 01111010 01101111 01100010             | 
#+---------------------------------------------------------------------------+
#| NETwork protocol modeliZatiOn By reverse engineering                      |
#| ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+
#| @license      : GNU GPL v3                                                |
#| @copyright    : Georges Bossert and Frederic Guihery                      |
#| @url          : http://code.google.com/p/netzob/                          |
#| ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+
#| @author       : {gbt,fgy}@amossys.fr                                      |
#| @organization : Amossys, http://www.amossys.fr                            |
#+---------------------------------------------------------------------------+
#+---------------------------------------------------------------------------+ 
#| Standard library imports
#+---------------------------------------------------------------------------+
import array
import binascii
import logging.config
import uuid

#+---------------------------------------------------------------------------+
#| Related third party imports
#+---------------------------------------------------------------------------+
from xml.etree import ElementTree

#+---------------------------------------------------------------------------+
#| Local application imports
#+---------------------------------------------------------------------------+
from ... import ConfigurationParser
from ..NetworkMessage import NetworkMessage
#+---------------------------------------------------------------------------+
#| Configuration of the logger
#+---------------------------------------------------------------------------+
loggingFilePath = ConfigurationParser.ConfigurationParser().get("logging", "path")
logging.config.fileConfig(loggingFilePath)

#+---------------------------------------------------------------------------+
#| NetworkMessageFactory :
#|     Factory dedicated to the manipulation of network messages
#| @author     : {gbt,fgy}@amossys.fr
#| @version    : 0.2
#+---------------------------------------------------------------------------+

#+---------------------------------------------------------------------------+
class NetworkMessageFactory():
    
    @staticmethod
    #+---------------------------------------------------------------------------+
    #| loadFromXML :
    #|     Function which parses an XML and extract from it
    #[     the definition of a network message
    #| @param rootElement: XML root of the network message 
    #| @return an instance of a NetworkMessage
    #| @throw NameError if XML invalid
    #+---------------------------------------------------------------------------+
    def loadFromXML(rootElement):        
        # First we verify rootElement is a message
        if rootElement.tag != "message" :
            raise NameError("The parsed xml doesn't represent a message.")
        # Then we verify its a Network Message
        if rootElement.get("type", "abstract") != "network" :
            raise NameError("The parsed xml doesn't represent a network message.")
        # Verifies the data field
        if rootElement.find("data") == None or len(rootElement.find("data").text) == 0:
            raise NameError("The parsed message has no data specified")
        
        # Parse the data field and transform it into a byte array
        msg_data = bytearray(rootElement.find("data").text)
        
        # Retrieve the id (default = -1)
        msg_id = rootElement.get('id', "-1")
        
        if msg_id == "-1" :
            msg_id = str(uuid.uuid4()) 
        
        # Retrieves the timestamp (default = 0 )
        if rootElement.find("timestamp") != None :
            msg_timestamp = int(rootElement.find("timestamp").text)
        else :
            msg_timestamp = 0
        
        # Retrieves the ipSource (default 0.0.0.0)
        if rootElement.find("ipSource") != None :
            msg_ipSource = rootElement.find("ipSource").text
        else :
            msg_ipSource = "0.0.0.0"
            
        # Retrieves the ipTarget (default 0.0.0.0)
        if rootElement.find("ipTarget") != None :
            msg_ipTarget = rootElement.find("ipTarget").text
        else :
            msg_ipTarget = "0.0.0.0"
        
        # Retrieves the protocol (default Unknown)
        if rootElement.find("protocol") != None :
            msg_protocol = rootElement.find("protocol").text
        else :
            msg_protocol = "Unknown"
            
        # Retrieves the l4 source port (default 0)
        if rootElement.find("l4SourcePort") != None :
            msg_l4SourcePort = rootElement.find("l4SourcePort").text
        else :
            msg_l4SourcePort = 0
            
        # Retrieves the l4 target port (default 0)
        if rootElement.find("l4TargetPort") != None :
            msg_l4TargetPort = rootElement.find("l4TargetPort").text
        else :
            msg_l4TargetPort = 0
        
        # Craft the Network Message
        result = NetworkMessage()
        result.setID(msg_id)
        result.setData(msg_data)
        result.setTimestamp(msg_timestamp)
        result.setIPSource(msg_ipSource)
        result.setIPTarget(msg_ipTarget)
        result.setProtocol(msg_protocol)
        result.setL4SourcePort(msg_l4SourcePort)
        result.setL4TargetPort(msg_l4TargetPort)
        
        return result
    
    