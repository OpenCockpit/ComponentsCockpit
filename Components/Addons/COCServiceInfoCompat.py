# Copyright (C) 2018-2026 by xcentaurix
# License: GNU General Public License v3.0


# The audio/video codec tables and helpers that COCServiceInfoBar takes from OpenViX's
# Components/Converter/ServiceInfo.py. openATV has no such module-level helpers, so the addon falls back to
# this copy there (the definitions below are copied unchanged from that file, except getVideoHeight()).

from enigma import iServiceInformation

try:
    from Components.Converter.VAudioInfo import StdAudioDesc
except ImportError:
    def StdAudioDesc(desc):
        return desc


# Skin-facing audio codec booleans.  Values are exact descriptions from
# iAudioTrackInfo after the codec work in eServiceMP3/eServiceDVB.  Legacy
# aliases are accepted so skins also work with older/native service paths.
AUDIO_CODEC_TYPES = {
    "IsDolbyDigital": ("Dolby Digital", "AC3"),
    "IsAudioAC3": ("Dolby Digital", "AC3"),
    "IsDolbyDigitalPlus": ("Dolby Digital +", "Dolby Digital Plus", "EAC3", "AC3+"),
    "IsAudioEAC3": ("Dolby Digital +", "Dolby Digital Plus", "EAC3", "AC3+"),
    "IsDolbyAtmos": ("Dolby Atmos", "Dolby Atmos (TrueHD)"),
    "IsAudioAtmos": ("Dolby Atmos", "Dolby Atmos (TrueHD)"),
    "IsDolbyTrueHD": ("Dolby TrueHD", "TrueHD", "Dolby Atmos (TrueHD)"),
    "IsAudioTrueHD": ("Dolby TrueHD", "TrueHD", "Dolby Atmos (TrueHD)"),
    "IsDolbyAC4": ("Dolby AC-4", "Dolby AC4", "AC-4", "AC4"),

    "IsDTS": ("DTS",),
    "IsDTSHD": ("DTS-HD", "DTSHD"),
    "IsDTSHDMA": ("DTS-HD MA", "DTSHD MA", "DTS-HD Master Audio", "DTSHD Master Audio", "DTS-HD MA + DTS:X", "DTS-HD MA + DTS:X IMAX"),
    "IsDTSHDHRA": ("DTS-HD HRA", "DTSHD HRA", "DTS-HD High Resolution", "DTSHD High Resolution", "DTS-HD High Resolution Audio", "DTSHD High Resolution Audio"),
    "IsDTSX": ("DTS:X", "DTS-HD MA + DTS:X"),
    "IsDTSXIMAX": ("DTS:X IMAX", "DTS-HD MA + DTS:X IMAX"),
    "IsDTSXPro": ("DTS:X Pro",),
    "IsDTSExpress": ("DTS Express",),
    "IsDTSES": ("DTS-ES", "DTS ES"),
    "IsDTS9624": ("DTS 96/24", "DTS 96-24"),

    "IsAAC": ("AAC",),
    "IsAACLC": ("AAC-LC", "AACLC"),
    "IsAACLD": ("AAC-LD", "AACLD"),
    "IsAACELD": ("AAC-ELD", "AACELD"),
    "IsHEAAC": ("HE-AAC", "HEAAC"),
    "IsHEAACV2": ("HE-AAC v2", "HEAAC v2"),
    "IsXHEAAC": ("xHE-AAC", "xHEAAC"),

    "IsFLAC": ("FLAC",),
    "IsALAC": ("ALAC",),
    "IsOpus": ("Opus",),
    "IsVorbis": ("Vorbis",),
    "IsWavPack": ("WavPack",),
    "IsAPE": ("APE",),
    "IsTTA": ("TTA",),
    "IsMLP": ("MLP",),
    "IsRealAudio": ("RealAudio", "RealAudio 14.4", "RealAudio 28.8"),
    "IsRealAudio144": ("RealAudio 14.4",),
    "IsRealAudio288": ("RealAudio 28.8",),
    "IsWMALossless": ("WMA Lossless",),
    "IsWMAPro": ("WMA Pro",),
    "IsWMA": ("WMA",),
    "IsAMRWB": ("AMR-WB", "AMRWB"),
    "IsAMR": ("AMR",),
    "IsSpeex": ("Speex",),
    "IsDSD": ("DSD",),
    "IsMP3": ("MP3",),
    "IsMP2": ("MP2",),
    "IsMPEGLayer1": ("MPEG Layer I",),
    "IsMPEG1LayerII": ("MPEG1 Layer II",),
    "IsALaw": ("A-law", "A law"),
    "IsMuLaw": ("mu-law", "mu law"),
    "IsPCM": ("PCM",),
    "IsLPCM": ("LPCM", "IPCM"),
}

AUDIO_CODEC_DESCRIPTIONS = frozenset(
    description
    for descriptions in AUDIO_CODEC_TYPES.values()
    for description in descriptions
)

# Canonical selected-track codec label and dynamic icon key.  The icon key is
# deliberately path- and extension-free; the skin chooses its own icon path.
# AudioIcon prefers <path>/icon_<key>.svg, then falls back to .png.
AUDIO_CODEC_DISPLAY = (
    (("Dolby Digital", "AC3"), "Dolby Digital", "dolby-digital"),
    (("Dolby Digital +", "Dolby Digital Plus", "EAC3", "AC3+"), "Dolby Digital +", "dolby-digital-plus"),
    (("Dolby Atmos",), "Dolby Atmos", "dolby-atmos"),
    (("Dolby Atmos (TrueHD)",), "Dolby Atmos (TrueHD)", "dolby-atmos"),
    (("Dolby TrueHD", "TrueHD"), "Dolby TrueHD", "dolby-truehd"),
    (("Dolby AC-4", "Dolby AC4", "AC-4", "AC4"), "Dolby AC-4", "dolby-ac4"),

    (("DTS",), "DTS", "dts"),
    (("DTS-HD", "DTSHD"), "DTS-HD", "dts-hd"),
    (("DTS-HD MA", "DTSHD MA", "DTS-HD Master Audio", "DTSHD Master Audio"), "DTS-HD MA", "dts-hd-ma"),
    (("DTS-HD HRA", "DTSHD HRA", "DTS-HD High Resolution", "DTSHD High Resolution", "DTS-HD High Resolution Audio", "DTSHD High Resolution Audio"), "DTS-HD HRA", "dts-hd-hra"),
    (("DTS:X",), "DTS:X", "dts-x"),
    (("DTS-HD MA + DTS:X",), "DTS-HD MA + DTS:X", "dts-x"),
    (("DTS:X IMAX",), "DTS:X IMAX", "dts-x-imax"),
    (("DTS-HD MA + DTS:X IMAX",), "DTS-HD MA + DTS:X IMAX", "dts-x-imax"),
    (("DTS:X Pro",), "DTS:X Pro", "dts-x-pro"),
    (("DTS Express",), "DTS Express", "dts-express"),
    (("DTS-ES", "DTS ES"), "DTS-ES", "dts-es"),
    (("DTS 96/24", "DTS 96-24"), "DTS 96/24", "dts-96-24"),

    (("AAC",), "AAC", "aac"),
    (("AAC-LC", "AACLC"), "AAC-LC", "aac-lc"),
    (("AAC-LD", "AACLD"), "AAC-LD", "aac-ld"),
    (("AAC-ELD", "AACELD"), "AAC-ELD", "aac-eld"),
    (("HE-AAC", "HEAAC"), "HE-AAC", "he-aac"),
    (("HE-AAC v2", "HEAAC v2"), "HE-AAC v2", "he-aac-v2"),
    (("xHE-AAC", "xHEAAC"), "xHE-AAC", "xhe-aac"),

    (("FLAC",), "FLAC", "flac"),
    (("ALAC",), "ALAC", "alac"),
    (("Opus",), "Opus", "opus"),
    (("Vorbis",), "Vorbis", "vorbis"),
    (("WavPack",), "WavPack", "wavpack"),
    (("APE",), "APE", "ape"),
    (("TTA",), "TTA", "tta"),
    (("MLP",), "MLP", "mlp"),
    (("RealAudio",), "RealAudio", "realaudio"),
    (("RealAudio 14.4",), "RealAudio 14.4", "realaudio-14-4"),
    (("RealAudio 28.8",), "RealAudio 28.8", "realaudio-28-8"),
    (("WMA Lossless",), "WMA Lossless", "wma-lossless"),
    (("WMA Pro",), "WMA Pro", "wma-pro"),
    (("WMA",), "WMA", "wma"),
    (("AMR-WB", "AMRWB"), "AMR-WB", "amr-wb"),
    (("AMR",), "AMR", "amr"),
    (("Speex",), "Speex", "speex"),
    (("DSD",), "DSD", "dsd"),
    (("MP3",), "MP3", "mp3"),
    (("MP2",), "MP2", "mp2"),
    (("MPEG Layer I",), "MPEG Layer I", "mpeg-layer-i"),
    (("MPEG1 Layer II",), "MPEG1 Layer II", "mpeg1-layer-ii"),
    (("A-law", "A law"), "A-law", "a-law"),
    (("mu-law", "mu law"), "mu-law", "mu-law"),
    (("PCM",), "PCM", "pcm"),
    (("LPCM", "IPCM"), "LPCM", "lpcm"),
)

AUDIO_CODEC_INFO = {
    description: (label, icon)
    for descriptions, label, icon in AUDIO_CODEC_DISPLAY
    for description in descriptions
}

# Exact selected-track channel-count flags.  These use the negotiated channel
# count exposed by iAudioTrackInfo; they do not infer layout from codec names.
AUDIO_CHANNEL_TYPES = {
    "IsAudioMono": 1,
    "IsAudio10": 1,
    "IsAudioStereo": 2,
    "IsAudio20": 2,
    "IsAudio51": 6,
    "IsAudio71": 8,
}

AUDIO_CHANNELS_DISPLAY = (
    (1, "Mono", "mono"),
    (2, "Stereo", "stereo"),
    (6, "5.1", "5-1"),
    (8, "7.1", "7-1"),
)

AUDIO_CHANNELS_INFO = {chCount: (label, icon) for chCount, label, icon in AUDIO_CHANNELS_DISPLAY}

AUDIO_CHANNEL_LABELS = {
    1: "1.0",
    2: "2.0",
    6: "5.1",
    8: "7.1",
}


def getCurrentAudioChannels(service):
    audio = service and service.audioTracks()
    if not audio:
        return 0
    current = audio.getCurrentTrack()
    if current < 0 or current >= audio.getNumberOfTracks():
        return 0
    track = audio.getTrackInfo(current)
    # openATV's iAudioTrackInfo has no getChannels(): no channel count, so no channel icon there
    getChannels = getattr(track, "getChannels", None)
    return getChannels() if getChannels else 0


def getCurrentAudioCodec(service):
    audio = service and service.audioTracks()
    if not audio:
        return ""
    current = audio.getCurrentTrack()
    if current < 0 or current >= audio.getNumberOfTracks():
        return ""
    track = audio.getTrackInfo(current)
    if not track:
        return ""
    description = track.getDescription() or ""
    # Preserve exact known codec names before the legacy normalizer.  This is
    # important for names such as ALAC and the refined DTS-HD/DTS:X labels.
    if description not in AUDIO_CODEC_DESCRIPTIONS:
        description = StdAudioDesc(description)
    return description


# Canonical video codec label and dynamic icon key, keyed by the raw
# iServiceInformation.sVideoType stream-type value.  The icon key is
# deliberately path- and extension-free; the skin chooses its own icon path.
VIDEO_CODEC_DISPLAY = (
    (0, "MPEG-2", "h262"),
    (1, "H.264", "h264"),
    (2, "H.263", "h263"),
    (3, "VC-1", "vc1"),
    (4, "MPEG-4", "mpeg4"),
    (5, "VC-1 SM", "vc1-sm"),
    (6, "MPEG-1", "mpeg1"),
    (7, "H.265", "hevc"),
    (8, "VP8", "vp8"),
    (9, "VP9", "vp9"),
    (10, "XVID", "xvid"),
    (13, "DIVX 3.11", "divx"),
    (14, "DIVX 4", "divx"),
    (15, "DIVX 5", "divx"),
    (16, "AVS", "avs"),
    (18, "VP6", "vp6"),
    (21, "SPARK", "spark"),
    (40, "AVS2", "avs2"),
)

VIDEO_CODEC_INFO = {videoType: (label, icon) for videoType, label, icon in VIDEO_CODEC_DISPLAY}


def getCurrentVideoCodec(info):
    videoType = info.getInfo(iServiceInformation.sVideoType)
    # Some stream-relay paths never report a video type; assume HEVC as that is
    # the only codec such relays are used for.
    if videoType == -1 and info.getInfoString(iServiceInformation.sServiceref).startswith("5002"):
        return 7
    return videoType


def getVideoHeight(info):
    # eAVControl on openATV, eAVSwitch on OpenViX
    try:
        from enigma import eAVControl as av
    except ImportError:
        from enigma import eAVSwitch as av
    val = av.getInstance().getResolutionY(0)
    return val if val else info.getInfo(iServiceInformation.sVideoHeight)
