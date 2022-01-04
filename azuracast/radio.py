import logging
import httpx

logger = logging.getLogger(__name__)


class RadioInfo:
    def __init__(self, url, station_idx=0):
        self.url = url
        self.station_idx = station_idx
        self.radio_station_name = None
        self.radio_station_description = None
        self.current_listeners = None
        self.unique_listeners = None
        self.total_listeners = None
        self.streamer_name = None
        self.now_playing_playlist = None
        self.now_playing_song_title = None
        self.now_playing_song_artist = None
        self.now_playing_song_album = None
        self.next_playing_playlist = None
        self.next_playing_song_title = None
        self.next_playing_song_artist = None
        self.next_playing_song_album = None

    def update(self):
        logger.debug(f"Getting info for station {self.station_idx}")
        radio_info = self.get_json_data()
        self.update_info(radio_info)

    def get_json_data(self):
        r = httpx.get(self.url)
        return r.json()[self.station_idx]

    def shape_data(self, radio_info):
        for key, value in radio_info.items():
            if isinstance(value, dict):
                self.shape_data(value)
            else:
                if value is None:
                    radio_info[key] = {}
                if value == '':
                    radio_info[key] = '-'
        return radio_info

    def update_info(self, radio_info):
        self.radio_station_name = self.traverse_dict_node(radio_info, ['station', 'name'])
        self.radio_station_description = self.traverse_dict_node(radio_info,
                                                                 ['station', 'description'])
        self.current_listeners = self.traverse_dict_node(radio_info, ['listeners', 'current'])
        self.unique_listeners = self.traverse_dict_node(radio_info, ['listeners', 'unique'])
        self.total_listeners = self.traverse_dict_node(radio_info, ['listeners', 'total'])
        self.streamer_name = self.get_streamer_name(radio_info)
        self.now_playing_playlist = self.traverse_dict_node(radio_info,
                                                            ['now_playing', 'playlist'])
        self.now_playing_song_title = self.traverse_dict_node(radio_info,
                                                              ['now_playing', 'song', 'title'])
        self.now_playing_song_artist = self.traverse_dict_node(radio_info,
                                                               ['now_playing', 'song', 'artist'])
        self.now_playing_song_album = self.traverse_dict_node(radio_info,
                                                              ['now_playing', 'song', 'album'])
        self.next_playing_playlist = self.traverse_dict_node(radio_info,
                                                             ['playing_next', 'playlist'])
        self.next_playing_song_title = self.traverse_dict_node(radio_info,
                                                               ['playing_next', 'song', 'title'])
        self.next_playing_song_artist = self.traverse_dict_node(radio_info,
                                                                ['playing_next', 'song', 'artist'])
        self.next_playing_song_album = self.traverse_dict_node(radio_info,
                                                               ['playing_next', 'song', 'album'])

    @staticmethod
    def traverse_dict_node(dictionary, node_keys):
        value = None
        for key in node_keys:
            if dictionary is None:
                dictionary = {}
            dictionary = dictionary.get(key)
            value = dictionary
            if value == '' or value is None:
                value = '-'
        return value

    @staticmethod
    def get_streamer_name(radio_info):
        streamer_name = radio_info["live"].get("streamer_name", "-")
        if not streamer_name:
            return "AutoDJ"
        else:
            return streamer_name

    def get_now_playing(self):
        return f"<h4>playlist now</h4>\
                {self.now_playing_playlist}<br>\
                <h4>song</h4>\
                <b>title :</b> {self.now_playing_song_title}<br>\
                <b>artist :</b> {self.now_playing_song_artist}<br>\
                <b>album :</b> {self.now_playing_song_album}<br>"

    def get_next_playing(self):
        return f"<h4>playlist next</h4>\
                {self.next_playing_playlist}<br>\
                <h4>song</h4>\
                <b>title :</b> {self.next_playing_song_title}<br>\
                <b>artist :</b> {self.next_playing_song_artist}<br>\
                <b>album :</b> {self.next_playing_song_album}<br>"

    def get_listeners(self):
        return "<h4>listeners</h4>**current:** {} **unique:** {} **total:** {}<br>".format(
            self.current_listeners,
            self.unique_listeners,
            self.total_listeners)

    def get_streamer(self):
        return "<h4>streamer</h4> {}".format(self.streamer_name)

    def get_all(self):
        return self.get_listeners() + self.get_now_playing() + self.get_next_playing() + self.get_streamer()
