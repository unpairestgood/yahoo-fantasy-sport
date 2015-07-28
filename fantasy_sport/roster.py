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
    def xml_builder_add(self,):
        raise NotImplementedError

    @abc.abstractmethod
    def json_builder(self,):
        raise NotImplementedError
   
    def to_json(self,):
        """Return object as a json string
        """
        return json.dumps(self.json, ensure_ascii=True).encode('ascii')

    def to_xml(self,):
        """Return object as a xml string
        """
        return ctree.tostring(self.xml)
    """    
    @abc.abstractmethod
    def xml_builder_waiver(self,):
        raise NotImplementedError
        
    @abc.abstractmethod
    def xml_builder_pending_trade_put(self,):
        raise NotImplementedError
        
    @abc.abstractmethod
    def xml_builder_add(self,):
        raise NotImplementedError
        
    @abc.abstractmethod
    def xml_builder_drop(self,):
        raise NotImplementedError
        
    @abc.abstractmethod
    def xml_builder_adddrop(self,):
        raise NotImplementedError
        
    @abc.abstractmethod
    def xml_builder_pending_trade_post(self,):
        raise NotImplementedError
   """

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

        self.json_builder()
        self.xml_builder()

    def xml_builder(self,):
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

    def json_builder(self,):
        """Convert object to json
        """
        self.json = {
            'fantasy_content':{
                'roster':{
                    'coverage_type': self.coverage_type,
                    self.coverage_type : self.coverage,
                    'players': [ player.json for player in self.players ]
                }
            }
        }
        return self.json
    

class Player(Base):
    """player class
    - player_key
    - position
    """

    def __init__(self, player_key, type=None, position=None, destination_team_key=None, source_team_key=None,):
        """Initialize a player object
        """
        super(Base, self).__init__()

        self.player_key = player_key
        self.position = position
        
        
        self.xml_builder()
        self.json_builder()

    def xml_builder(self,):
        """Convert object into a xml object
        """
        player = ctree.Element('player')
        for key in sorted(vars(self).keys()):
            tag = ctree.SubElement(player, key)
            tag.text = vars(self).get(key)
        
        self.xml = player
        return self.xml

    def json_builder(self, ):
        """Kind of convert object to json
        """
        self.json = {
            'player_key': self.player_key,
            'position': self.position
        }

        return self.json
        
        
class Transaction(Base):
    """transaction class
    - transaction_key
    - type
    -- edit waiver
        - waiver_priority
        - faab_bid
    -- allow/disallow/vote against trades
        - action
    """
    
    #def __init__(self, type, transaction_key=None, waiver_priority=None, faab_bid=None, action=None, trade_note=None, voter_team_key=None, player_key=None, team_key=None):
    def __init__(self, type=None, player_key=None, team_key=None,):
        """Initialize a Transaction object
         - types
         -- PUT: waiver, pending_trade
         -- POST: add, drop, add/drop, pending_trade (for proposing trades)
         
        """
        super(Base, self).__init__()
        
        self.type = type
        #self.transaction_key = transaction_key
        #self.waiver_priority = waiver_priority
        #self.faab_bid = faab_bid
        #self.action = action
        #self.trade_note = trade_note
        #self.voter_team_key = voter_team_key
        self.player_key = player_key
        self.team_key = team_key
        
        #types = {'waiver': xml_builder_waiver, 'pending_trade': xml_builder_pending_trade_put, 'add': xml_builder_add, 'drop': xml_builder_drop, 'add/drop': xml_builder_adddrop}
        
        #if self.type in types:
            #types[self.type]()
        #else:
            #raise Exception("Method %s not implemented" % self.type
        
        self.xml_builder_add()    
        #self.xml_builder()
        #self.json_builder()
        
    def xml_builder_add(self,):
        """Convert object to xml for adding a player
        """
        
        content = ctree.Element('fantasy_content')
        transaction = ctree.SubElement(content, 'transaction')
        
        type = ctree.SubElement(transaction, 'type')
        type.text = self.type
        
        player = ctree.SubElement(transaction, 'player')
        
        player_key = ctree.SubElement(player, 'player_key')
        player_key.text = self.player_key
        
        transaction_data = ctree.SubElement(player, 'transaction_data')
        
        type = ctree.SubElement(transaction_data, 'type')
        type.text = self.type
        
        dest_team_key = ctree.SubElement(transaction_data, 'destination_team_key')
        dest_team_key.text = self.team_key
        
        self.xml = content
        
    def xml_builder(self,):
        """Convert object to xml
        """
        content = ctree.Element('fantasy_content')
        transaction = ctree.SubElement(content, 'transaction')

        if transaction_key:
            transaction_key = ctree.SubElement(transaction, 'transaction_key')
            transaction_key.text = self.transaction_key

        type = ctree.SubElement(transaction, 'type')
        type.text = self.type
        
        if waiver_priority:
            waiver_priority = ctree.SubElement(transaction, 'waiver_priority')
            waiver_priority.text = self.waiver_priority
            
        if faab_bid:
            faab_bid = ctree.SubElement(transaction, 'faab_bid')
            faab_bid.text = self.faab_bid

        if action:
            action = ctree.SubElement(transaction, 'action')
            action.text = self.action
            
        if trade_note:
            trade_note = ctree.SubElement(transaction, 'trade_note')
            trade_note.text = self.trade_note
            
        if voter_team_key:
            voter_team_key = ctree.SubElement(transaction, 'voter_team_key')
            voter_team_key.text = self.voter_team_key
        
        self.xml = content

    def json_builder(self,):
        """Convert object to json
        """
        self.json = {
            'fantasy_content':{
                'roster':{
                    'coverage_type': self.coverage_type,
                    self.coverage_type : self.coverage,
                    'players': [ player.json for player in self.players ]
                }
            }
        }
        return self.json


