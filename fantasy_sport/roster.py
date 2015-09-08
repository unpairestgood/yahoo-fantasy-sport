from __future__ import absolute_import, unicode_literals

import six
import abc
import json

from xml.etree import cElementTree as ctree

@six.add_metaclass(abc.ABCMeta)
class Base(object):
    """Base class for Roster and Player
    """

    @abc.abstractmethod
    def xml_builder_player(self,):
        raise NotImplementedError
        
    @abc.abstractmethod
    def xml_builder_player_proposetrade(self,):
        raise NotImplementedError
    
    @abc.abstractmethod
    def xml_builder_roster(self,):
        raise NotImplementedError
        
    #@abc.abstractmethod
    #def xml_builderpost(self,):
        #raise NotImplementedError

    #@abc.abstractmethod
    #def json_builder(self,):
        #raise NotImplementedError
   
    #def to_json(self,):
        #"""Return object as a json string
        #"""
        #return json.dumps(self.json, ensure_ascii=True).encode('ascii')
        
    def to_xml(self,):
        """Return object as a xml string
        """
        return ctree.tostring(self.xml)


class Roster(Base):
    """Roster class
    """

    def __init__(self, players, week=None, date=None):
        """Initialize a roster class
        """
        super(Base, self).__init__()

        self.players = players

        if week:
            self.coverage = week
            self.coverage_type = 'week'
        else:
            self.coverage = date
            self.coverage_type = 'date'

        #self.json_builder()
        self.xml_builder_roster()

    def xml_builder_roster(self,):
        """Convert object to xml
        """
        content = ctree.Element('fantasy_content')
        roster = ctree.SubElement(content, 'roster')

        coverage_type = ctree.SubElement(roster, 'coverage_type')
        coverage_type.text = self.coverage_type

        coverage = ctree.SubElement(roster, self.coverage_type)
        coverage.text = self.coverage

        players = ctree.SubElement(roster, 'players')
        for player in self.players :
            players.append(player.xml)

        self.xml = content
        

    #def json_builder(self,):
        #"""Convert object to json
        #"""
        #self.json = {
            #'fantasy_content':{
                #'roster':{
                    #'coverage_type': self.coverage_type,
                    #self.coverage_type : self.coverage,
                    #'players': [ player.json for player in self.players ]
                #}
            #}
        #}
        #return self.json
    
    def xml_builder_player(self,):
        return None
        
    def xml_builder_player_proposetrade(self,):
        return None
    

class Player(Base):
    """player class
    - player_key
    - position
    """

    def __init__(self, player_key, type=None, position=None,
                 destination_team_key=None, source_team_key=None
        ):
        """Initialize a player object
        """
        super(Base, self).__init__()

        self.player_key = player_key
        self.position = position
        self.type = type
        self.destination_team_key = destination_team_key
        self.source_team_key = source_team_key
        
        if self.type == 'pending_trade':
            self.xml_builder_player_proposetrade()
        else:
            self.xml_builder_player()

    def xml_builder_player(self,):
        """Convert object into a xml object
        """
        player = ctree.Element('player')
        
        player_key = ctree.SubElement(player, 'player_key')
        player_key.text = self.player_key
        
        if self.position:
            position = ctree.SubElement(player, 'position')
            position.text = self.position
        
        if self.type:
            transaction_data = ctree.SubElement(player, 'transaction_data')
            type = ctree.SubElement(transaction_data, 'type')
            type.text = self.type
        
        if self.destination_team_key:
            destination_team_key = ctree.SubElement(transaction_data, 'destination_team_key')
            destination_team_key.text = self.destination_team_key
        
        if self.source_team_key:
            source_team_key = ctree.SubElement(transaction_data, 'source_team_key')
            source_team_key.text = self.source_team_key
        
        self.xml = player
        return self.xml
        
    def xml_builder_player_proposetrade(self,):
        """Convert player object into xml object
        """
        player = ctree.Element('player')
        
        player_key = ctree.SubElement(player, 'player_key')
        player_key.text = self.player_key
        
        transaction_data = ctree.SubElement(player, 'transaction_data')
        
        type = ctree.SubElement(transaction_data, 'type')
        type.text = self.type
        
        source_team_key = ctree.SubElement(transaction_data, 'source_team_key')
        source_team_key.text = self.source_team_key
        
        destination_team_key = ctree.SubElement(transaction_data, 'destination_team_key')
        destination_team_key.text = self.destination_team_key
        
        self.xml = player
        return self.xml

    #def json_builder(self, ):
        #"""Kind of convert object to json
        #"""
        #self.json = {
        #    'player_key': self.player_key,
        #    'position': self.position
        #}

        #return self.json
        
    def xml_builder_roster(self,):
        return None
        