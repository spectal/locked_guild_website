import urllib2
import json


class GuildMember(object):

    def __init__(self, character_name):
        base_api_url = 'https://eu.api.battle.net/wow/'
        self.charactername = character_name
        self.guild_member_data = self.read_json(self.get_guild_member_data(base_api_url + 'guild/Perenolde/Locked?fields=members&locale=de_DE&apikey=XXXXXXXXXXXXXXXXXXXXXX'))
        class_map = self.read_json(self.get_class_info(base_api_url + 'data/character/classes?locale=de_DE&apikey=XXXXXXXXXXXXXXXXXXXXXXX'))
        self.local_class_mappings = self.create_static_class_name_map(class_map)
        self.guild_members = self.build_small_guild_member_dict()

    def __repr__(self):
        if self.charactername == 'all':
            return str(self.guild_members)
        else:
            return str(self.charactername + ' ' + str(self.guild_members.get(self.charactername)))

    def return_guild_member_data(self):
        if self.charactername == 'all':
            return self.guild_members
        else:
            return self.charactername, self.guild_members.get(self.charactername)

    def build_small_guild_member_dict(self):
        member_dict = self.guild_member_data.get('members')
        guild_member_chars = {}
        for character in member_dict:
            char_data = character.get('character')
            guild_rank = character.get('rank')
            if char_data.get('level') == 110 and char_data.get('spec') and guild_rank <= 3:
                member_char_class = self.local_class_mappings[char_data.get('class')]
                character_attributes = [char_data.get('spec')['name'].encode('latin1'), member_char_class.encode('latin1'), self.guild_rank_names(guild_rank).encode('latin1')]
                guild_member_chars[char_data.get('name').encode('latin1')] = character_attributes
        return guild_member_chars

    @staticmethod
    def guild_rank_names(rank):
        guild_ranks = {0: 'Gildenmeister', 1: 'Offizier', 2: 'Raider', 3: 'Member', 4: 'Test', 5: 'Twink'}
        return guild_ranks.get(rank)

    @staticmethod
    def get_class_info(api_call_url):
        class_info = urllib2.urlopen(api_call_url)
        class_info = class_info.read()
        return class_info

    @staticmethod
    def get_guild_member_data(api_call_url):
        guild_member_info = urllib2.urlopen(api_call_url)
        member_info = guild_member_info.read()
        return member_info

    @staticmethod
    def create_static_class_name_map(char_class_map):
        local_class_map = {}
        for class_name in char_class_map.get('classes'):
            local_class_map[class_name['id']] = class_name['name']
        return local_class_map

    @staticmethod
    def read_json(fetcher_method):
        my_fetcher_method = fetcher_method
        my_json_object = json.loads(my_fetcher_method)
        return my_json_object
