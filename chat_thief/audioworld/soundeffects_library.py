from pathlib import Path
from typing import List, Set, Optional

THEME_SONGS_PATH = "/home/begin/stream/Stream/Samples/theme_songs"
SAMPLES_PATH = "/home/begin/stream/Stream/Samples/"
ALLOWED_AUDIO_FORMATS = [".mp3", ".m4a", ".wav", ".opus", ".ogg"]


class SoundeffectsLibrary:
    @staticmethod
    def find_sample(name: str) -> Optional[Path]:
        samples = [
            sample
            for sample in SoundeffectsLibrary.fetch_soundeffect_samples()
            if name == sample.name[: -len(sample.suffix)]
        ]
        if samples:
            return samples[0]
        else:
            return None

    @staticmethod
    def fetch_theme_songs() -> List[str]:
        return [
            theme.name[: -len(theme.suffix)]
            for theme in Path(THEME_SONGS_PATH).glob("*")
        ]

    @staticmethod
    def soundeffects_only() -> Set[str]:
        return set(SoundeffectsLibrary.fetch_soundeffect_names()) - set(
            SoundeffectsLibrary.fetch_theme_songs()
        )

    @staticmethod
    def fetch_soundeffect_samples() -> Set[Path]:
        return {
            p.resolve()
            for p in Path(SAMPLES_PATH).glob("**/*")
            if p.suffix in ALLOWED_AUDIO_FORMATS
        }

    @staticmethod
    def fetch_soundeffect_names() -> List[str]:
        sound_files = SoundeffectsLibrary.fetch_soundeffect_samples()

        return [
            sound_file.name[: -len(sound_file.suffix)] for sound_file in sound_files
        ]

    @staticmethod
    def find_soundeffect_files(name: str) -> List[Path]:
        return [
            p
            for p in Path(SAMPLES_PATH).glob("**/*")
            if p.suffix in ALLOWED_AUDIO_FORMATS
            if p.name[: -len(p.suffix)] == name
        ]
