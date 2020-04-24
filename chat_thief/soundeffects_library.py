from pathlib import Path

THEME_SONGS_PATH = "/home/begin/stream/Stream/Samples/theme_songs"
SAMPLES_PATH = "/home/begin/stream/Stream/Samples/"
ALLOWED_AUDIO_FORMATS = [".mp3", ".m4a", ".wav", ".opus"]


class SoundeffectsLibrary:
    @staticmethod
    def find_sample(name):
        samples = [
            sample
            for sample in SoundeffectsLibrary.fetch_soundeffect_samples()
            if name == sample.name[: -len(sample.suffix)]
        ]
        if samples:
            return samples[0]

        # We should add a best guess
        # raise ValueError(f"Not a Valid Sample: {name}")

    @staticmethod
    def fetch_theme_songs():
        return [
            theme.name[: -len(theme.suffix)]
            for theme in Path(THEME_SONGS_PATH).glob("*")
        ]

    @staticmethod
    def soundeffects_only():
        return set(SoundeffectsLibrary.fetch_soundeffect_names()) - set(
            SoundeffectsLibrary.fetch_theme_songs()
        )

    @staticmethod
    def fetch_soundeffect_samples():
        return {
            p.resolve()
            for p in Path(SAMPLES_PATH).glob("**/*")
            if p.suffix in ALLOWED_AUDIO_FORMATS
        }

    @staticmethod
    def fetch_soundeffect_names():
        return [
            sound_file.name[: -len(sound_file.suffix)]
            for sound_file in SoundeffectsLibrary.fetch_soundeffect_samples()
        ]

    @staticmethod
    def find_soundeffect_files(name):
        return [
            p
            for p in Path(SAMPLES_PATH).glob("**/*")
            if p.suffix in ALLOWED_AUDIO_FORMATS
            if p.name[: -len(p.suffix)] == name
        ]
