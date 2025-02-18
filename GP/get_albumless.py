"""
Return the list or write to  a file the list of media items that aren't in any
album in the GP remote.

Created on 2025-02-15 by abppbd.
"""
from rclone_python import rclone


# Get all remote's media items as a list of IDs.
def fetch_media_all(remote):

    # Get all media items in remote.
    all_media = rclone.ls(remote + "media/all")

    # Get the IDs of all all media items in remote.
    all_media_id = [i["ID"] for i in all_media]

    # Associate the media item ID to the file name.
    all_media_id_to_name = {i["ID"]:i["Name"] for i in all_media}

    return all_media_id, all_media_id_to_name


# Get all remote's media items in any album as a list of IDs.
def fetch_media_in_album(remote):

    # Get list of albums in remote.
    all_album = [i["Name"] for i in rclone.ls(remote + "album")]

    # List of the media items in an album.
    album_media_id = []

    for album_name in all_album:

        # Fetch all media items' IDs in the album
        temp_media_id = [
            i["ID"] for i in rclone.ls(f"{remote}album/{album_name}")
            ]

        album_media_id += temp_media_id

    return album_media_id


# Get list of media not in any album.
def fetch_albumless(remote, useOutputFile=False, file_name = "albumless.txt"):

    all_media_id, all_media_id_to_name = fetch_media_all(remote)
    all_media_id = set(all_media_id)

    album_media_id = set(fetch_media_in_album(remote))

    albumless_id = ls_media_all_id.difference(ls_album_media_files)

    # Dict of albumless media item IDs and their names.
    albumless = {}

    for item_id in albumless_id:
        albumless[item_id] = all_media_id_to_name[item_id]

    # Output albumless dict to file:
    if useOutputFile:
        with open(file_name, "w") as file:
            file.write(str(albumless))

    return albumless
