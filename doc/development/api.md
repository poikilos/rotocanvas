# RotoCanvas API

## backends
Each backend should implement everything in the reference implementation, rc_av.py.

### analyze_video

See `def analyze_video` for any possible values that should be documented below.
- 'iframe_offsets': [], # byte offsets
- 'iframe_dts': [],  # see time_base in av.md
- 'iframe_pts': [],  # see time_base in av.md
- 'video_length_frames': 32110,
- 'video_length_timecode': '3211/3'
- 'total_streams': 2
- 'video_streams': 1
- 'audio_streams': 1
- 'other_streams': 0
- 'streams': [
  - {'index': 0
      - 'type': 'video'
      - 'codec': 'h264'
      - 'bit_rate': 199267
      - 'duration': 16440320
      - 'frames': 32110
      - 'time_base': '1/15360'
      - 'width': 576
      - 'height': 360
      - 'format': 'yuv420p'
      - 'average_rate': '30'}
  - {'index': 1
      - 'type': 'audio'
      - 'codec': 'aac'
      - 'bit_rate': 127999
      - 'duration': 47202304
      - 'frames': 46096
      - 'time_base': '1/44100'}]
