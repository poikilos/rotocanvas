import os

dot_ext_mimetypes = {
    ".alac": "audio/alac",
    ".flac": "audio/flac",
    ".wav": "audio/wav",
    ".mp3": "audio/mp3",
    ".aac": "audio/aac",
    ".avif": "image/avif",
    ".jpg": "image/jpg",
    ".jpe": "image/jpg",
    ".jpeg": "image/jpg",
    ".png": "image/png",
    ".avi": "video/avi",
    ".m4v": "video/m4v",
    ".mp4": "video/mp4",
}

mimetype_animations = set([
    "image/avif",
    "image/gif",
    "image/tif",
])


def dot_ext_mimetype(dot_ext):
    return dot_ext_mimetypes.get(dot_ext.lower())


def path_mimetype(path):
    path_lower = path.lower()
    dot_ext = os.path.splitext(path_lower)[1]
    return dot_ext_mimetypes.get(dot_ext)
