# av
The av module is also known as PyAV, and supercedes (merged) the pyav module.

The types below were analyzed using PyAV 12.3.0 (as reported by `av.__version__`) on Python 3.8.19

The documentation says:
- time_base is a tick (fraction per second) that serves as a lowest common denominator for typical frame rates.
  - dts and pts are in time_base units (such as: time_base = Fraction(1/15360) of a second)
- dts is decoding timestamp
- pts is presentation timestamp
  when data should be shown to user


## frame

Analyzed via:
```Python
            print(frame)
            for key in dir(frame):
                if key.startswith("__"):
                    continue
                _v  =  getattr(frame, key)
                print("{} = {}({})".format(key, type(_v).__name__, _v))
            raise NotImplementedError("type(frame)={}".format(type(frame)))
```
- `<av.VideoFrame, pts=15564800 yuv420p 576x360 at 0x7fbf400d6580>`
  - `av.video.frame.VideoFrame` is defined in C.

```
_image_fill_pointers_numpy = method(<bound method VideoFrame._image_fill_pointers_numpy of <av.VideoFrame, pts=0 yuv420p 576x360 at 0x7efe66ed57c0>>)
color_range = int(1)
colorspace = int(1)
dts = int(77312)
format = VideoFormat(<av.VideoFormat yuv420p, 576x360>)
from_image = cython_function_or_method(<cyfunction VideoFrame.from_image at 0x7efe67a84380>)
from_ndarray = cython_function_or_method(<cyfunction VideoFrame.from_ndarray at 0x7efe67a845f0>)
from_numpy_buffer = cython_function_or_method(<cyfunction VideoFrame.from_numpy_buffer at 0x7efe67a84450>)
height = int(360)
interlaced_frame = int(0)
is_corrupt = bool(False)
key_frame = int(1)
make_writable = method(<bound method Frame.make_writable of <av.VideoFrame, pts=0 yuv420p 576x360 at 0x7efe66ed57c0>>)
pict_type = PictureType(I)
planes = tuple((<av.VideoPlane 230400 bytes; buffer_ptr=0x563f2a6ab100; at 0x7efe66ee47c0>, <av.VideoPlane 57600 bytes; buffer_ptr=0x563f2a861a80; at 0x7efe66ee4860>, <av.VideoPlane 57600 bytes; buffer_ptr=0x563f2a6e7680; at 0x7efe66ee48b0>))
pts = int(0)
reformat = method(<bound method VideoFrame.reformat of <av.VideoFrame, pts=0 yuv420p 576x360 at 0x7efe66ed57c0>>)
side_data = SideDataContainer(<av.sidedata.sidedata.SideDataContainer object at 0x7efe66ee47c0>)
time = float(0.0)
time_base = Fraction(1/15360)
to_image = method(<bound method VideoFrame.to_image of <av.VideoFrame, pts=0 yuv420p 576x360 at 0x7efe66ed57c0>>)
to_ndarray = method(<bound method VideoFrame.to_ndarray of <av.VideoFrame, pts=0 yuv420p 576x360 at 0x7efe66ed57c0>>)
to_rgb = method(<bound method VideoFrame.to_rgb of <av.VideoFrame, pts=0 yuv420p 576x360 at 0x7efe66ed57c0>>)
width = int(576)
```

## packet
Analyzed via:
```Python
            if packet.is_keyframe:
                for key in dir(packet):
                    if key.startswith("__"):
                        continue
                    _v  =  getattr(packet, key)
                    print("{} = {}({})".format(key, type(_v).__name__, _v))

```
- `av.packet.Packet` is defined in C
dir(packet) only has:
'buffer_ptr', 'buffer_size', 'decode', 'dts', 'duration', 'is_corrupt', 'is_discard', 'is_disposable', 'is_keyframe', 'is_trusted', 'pos', 'pts', 'size', 'stream', 'stream_index', 'time_base', 'update':
```
buffer_ptr = int(93828640830336)
buffer_size = int(2534)
decode = method(<bound method Packet.decode of <av.Packet of #0, dts = -512, pts = 0; 2534 bytes at 0x7fa4cc74dbd0>>)
dts = int(-512)
duration = int(512)
is_corrupt = bool(False)
is_discard = bool(False)
is_disposable = bool(False)
is_keyframe = bool(True)
is_trusted = bool(False)
pos = int(387218)
pts = int(0)
size = int(2534)
stream = VideoStream(<av.VideoStream #0 h264, yuv420p 576x360 at 0x7fa4cbbad580>)
stream_index = int(0)
time_base = Fraction(1/15360)
update = method(<bound method Buffer.update of <av.Packet of #0, dts = -512, pts = 0; 2534 bytes at 0x7fa4cc74dbd0>>)
```
