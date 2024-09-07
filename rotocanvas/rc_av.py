import av
import hashlib
import os
import time
import shutil

from logging import getLogger


logger = getLogger(__name__)


def cache_keyframes(video_path):
    cache_path = video_path + "_rotocanvas"
    if not os.path.isdir(cache_path):
        os.makedirs(cache_path)
    # See https://pyav.org/docs/stable/cookbook/basics.html#saving-keyframes
    with av.open(video_path) as container:
        # Signal that we only want to look at keyframes.
        stream = container.streams.video[0]
        stream.codec_context.skip_frame = "NONKEY"
        for frame in container.decode(stream):
            # if frame.is_keyframe:  # has no such attribute. See analyze_video
            #   but skip_frame = "NONKEY" is used above anyway.
            oops_path = cache_path + "{:04d}.jpg".format(frame.pts)
            f_path = os.path.join(cache_path, "{:04d}.jpg".format(frame.pts))
            if os.path.isfile(oops_path):
                shutil.move(oops_path, f_path)
                print("mv \"{}\" \"{}\"".format(oops_path, f_path))
            if os.path.isfile(f_path):
                continue
            # We use `frame.pts` as `frame.index` won't make must sense with the `skip_frame`.
            frame.to_image().save(
                f_path,
                quality=80,
            )


def analyze_video(video_path, callback):
    prefix = "[rc_av.analyze_video] "
    # Initialize the meta dictionary to store video metadata
    meta = {
        'iframe_offsets': [],
        'iframe_dts': [],
        'iframe_pts': [],
        'path_sha256': '',
        'video_length_frames': None,
        'video_length_timecode': None,
        'total_streams': 0,
        'video_streams': 0,
        'audio_streams': 0,
        'other_streams': 0,
        'streams': [],
    }

    # Compute the SHA256 checksum of the real path of the video file
    real_path = os.path.realpath(video_path)
    meta['path_sha256'] = hashlib.sha256(real_path.encode('utf-8')).hexdigest()

    # Get the size of the file
    file_size = os.path.getsize(real_path)

    # Open the video file
    container = av.open(video_path)
    meta['container'] = container
    meta['total_streams'] = len(container.streams)

    # Initialize the stream counter and collect stream information
    for stream in container.streams:
        stream_info = {
            'index': stream.index,
            'type': stream.type,
            'codec': stream.codec_context.name,
            'bit_rate': stream.bit_rate,
            'duration': stream.duration,
            'frames': stream.frames,
            'time_base': str(stream.time_base),
        }

        # Check for video-specific attributes
        if stream.type == 'video':
            meta['video_streams'] += 1
            stream_info.update({
                'width': stream.codec_context.width,
                'height': stream.codec_context.height,
                'format': stream.codec_context.format.name if stream.codec_context.format else 'unknown',
                'average_rate': str(stream.average_rate) if stream.average_rate else 'unknown',
            })
        elif stream.type == 'audio':
            meta['audio_streams'] += 1
        else:
            meta['other_streams'] += 1

        meta['streams'].append(stream_info)

    # Select the first video stream
    video_stream = next((s for s in container.streams if s.type == 'video'), None)

    if video_stream:
        # Get video length in frames and timecode if available
        meta['video_length_frames'] = video_stream.frames
        meta['video_length_timecode'] = str(video_stream.duration * video_stream.time_base) if video_stream.duration else None

        # Set variables for callback tracking
        update_time = None
        processed_bytes = 0
        offset = 0
        prev_dts = None
        # Iterate through packets in the video stream
        for packet in container.demux(video_stream):
            # av.packet.Packet
            processed_bytes += packet.size
            ratio = processed_bytes / file_size

            # Update progress periodically
            if update_time is None or time.time() - update_time > 1:
                callback({'ratio': ratio})
                update_time = time.time()

            # NOTE: I-Frame is independent,
            #   P-Frame is predictive (depends on previous)
            #   B-Frame is bidirectional
            #   (may depend on previous & next)

            # For members of packet, see doc/development/av.md

            # Check if the packet is a keyframe
            is_frame_start = (prev_dts is None) or (prev_dts != packet.dts)
            if packet.is_keyframe and is_frame_start:
                # duration of frame in seconds is:
                # packet.duration * packet.time_base
                # Example: 512 * Fraction(1/15360) == .03... (30fps)
                # meta['iframe_offsets'].append((packet.pos, offset))
                # ^ store offset since pos may be None
                # never matches, so ignore offset.
                # if packet.pos is not None:
                #     if offset != packet.pos:
                #         logger.warning(
                #             prefix+"offset {} will be changed to packet.pos {}"
                #             "".format(offset, packet.pos))
                #         offset = packet.pos
                meta['iframe_offsets'].append(packet.pos)

                if packet.dts is not None:
                    # decoding timestamp in time_base units
                    meta['iframe_dts'].append(packet.dts)
                else:
                    meta['iframe_dts'].append(None)

                if packet.pts is not None:
                    # presentation timestamp in time_base units
                    # "time at which the packet should be shown to the user"
                    # -<https://pyav.org/docs/stable/api/packet.html>
                    meta['iframe_pts'].append(packet.pts)
                else:
                    meta['iframe_pts'].append(None)

            offset += packet.size
            prev_dts = packet.dts


    # Ensure callback at the end
    callback({'ratio': 1.0})

    return meta


if __name__ == "__main__":
    def print_progress(status):
        # print("Progress: {:.2%}".format(status['ratio']))
        # ^ same result as:
        print("Progress: %.2f%%" % (status['ratio'] * 100))

    video_path = 'video.mp4'
    meta_info = analyze_video(video_path, print_progress)
    print(meta_info)
