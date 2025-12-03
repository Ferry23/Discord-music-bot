import json
import os
import logging

class Storage:
    PLAYLISTS_FILE = 'data/playlists.json'
    HISTORY_FILE = 'data/history.json'

    @classmethod
    def ensure_data_dir(cls):
        os.makedirs('data', exist_ok=True)

    @classmethod
    def load_playlists(cls):
        cls.ensure_data_dir()
        try:
            if os.path.exists(cls.PLAYLISTS_FILE):
                with open(cls.PLAYLISTS_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logging.error(f"Error loading playlists: {e}")
        return {}

    @classmethod
    def save_playlists(cls, playlists):
        cls.ensure_data_dir()
        try:
            with open(cls.PLAYLISTS_FILE, 'w', encoding='utf-8') as f:
                json.dump(playlists, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logging.error(f"Error saving playlists: {e}")

    @classmethod
    def load_history(cls):
        cls.ensure_data_dir()
        try:
            if os.path.exists(cls.HISTORY_FILE):
                with open(cls.HISTORY_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logging.error(f"Error loading history: {e}")
        return []

    @classmethod
    def save_history(cls, history):
        cls.ensure_data_dir()
        try:
            with open(cls.HISTORY_FILE, 'w', encoding='utf-8') as f:
                json.dump(history, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logging.error(f"Error saving history: {e}")

    @classmethod
    def add_to_history(cls, track):
        history = cls.load_history()
        history.append(track)
        if len(history) > 50:
            history = history[-50:]
        cls.save_history(history)