# -----------------------------------------------------------------------------
#                                   General
# -----------------------------------------------------------------------------
import os, google, io, glob, time, math, copy, logging, warnings, itertools, zlib, subprocess, pkg_resources

from os.path import join, isdir, isfile, basename, normpath, dirname, realpath, expanduser, splitext, exists

from functools import partial

import numpy as np
from scipy.stats.distributions import chi2
from sklearn.preprocessing import RobustScaler, StandardScaler, QuantileTransformer

import json
from pprint import pprint
from easydict import EasyDict as edict

import google.protobuf
from google.colab import drive, files

# from utils import get_data, calculate_iou, check_results
# -----------------------------------------------------------------------------
#                            Waymo Open Dataset
# -----------------------------------------------------------------------------
import waymo_open_dataset
from waymo_open_dataset import dataset_pb2, label_pb2
from waymo_open_dataset.utils import frame_utils, transform_utils, range_image_utils
# -----------------------------------------------------------------------------
#                                TensorFlow
# -----------------------------------------------------------------------------
import tensorflow as tf
import tensorflow_io as tfio
# -----------------------------------------------------------------------------
#                                Matplotlib
# -----------------------------------------------------------------------------
import matplotlib
from matplotlib import colors
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.ticker as ticker
import matplotlib.patches as patches
from matplotlib.patches import Rectangle
from matplotlib.transforms import Affine2D
from mpl_toolkits.axes_grid1 import ImageGrid
from matplotlib.animation import FuncAnimation

# change backend so that figure maximizing works on Mac as well
# matplotlib.use('wxagg')
# -----------------------------------------------------------------------------
#                                Visualization
# -----------------------------------------------------------------------------
import IPython
from IPython.display import HTML, Image, display

import open3d as o3d
# from open3d import JVisualizer
# from open3d.j_visualizer import JVisualizer

from shapely.geometry import Polygon

# from PIL import Image

# DisabledFunctionError: cv2.imshow() is disabled in Colab, because it causes Jupyter sessions
# to crash; see https://github.com/jupyter/notebook/issues/3935.
# As a substitution, consider using:
# import cv2
# from google.colab.patches import cv2_imshow


# =============================================================================
#                             show_camera_image
# =============================================================================
def show_camera_image(
      fig
    , ax
    , camera_image
    , camera_labels
    , cmap=None
    ):

    """
    Displays a camera image and overlays bounding boxes for detected objects on a matplotlib axis.

    This function takes an image from a specific camera and a list of labels for detected objects within that image,
    and overlays the objects' bounding boxes over the image. Each type of object is denoted by a different border color
    around its bounding box.

    Parameters:
    - fig (matplotlib.figure.Figure): The figure object that the image will be drawn on.
    - ax (matplotlib.axes.Axes): The axes object that the image will be drawn on.
    - camera_image (CameraImage): A camera image object, containing the encoded image and the camera's name.
    - camera_labels (list of CameraLabel): A list of camera label objects, each containing labels for detected objects
      within the image from a specific camera.
    - cmap (str, optional): The colormap used to display the image. If None, the image is displayed in its original colors.

    Raises:
    - ValueError: If 'camera_image' or 'camera_labels' are empty or if 'camera_image.name' does not match any 'camera_label.name'.

    Note:
    - CameraImage and CameraLabel are assumed to be objects structured according to the Waymo Open Dataset or similar.
    - This function does not return anything but modifies the matplotlib axes object 'ax' in place to display the image
      and bounding boxes.
    """
    if not camera_image or not camera_labels:
        raise ValueError("The camera image or camera labels are empty.")

    camera_view_name = dataset_pb2\
                      .CameraName\
                      .Name.Name(camera_image.name)\
                      .upper()

    image_displayed = False

    # Draw the camera labels
    for camera_label in camera_labels:

        # Ignore camera labels that do not correspond to this camera.
        if camera_label.name != camera_image.name:
            continue

        image_displayed = True

        # Iterate over the individual labels
        for label in camera_label.labels:

            # Set edgecolor based on label type
            edgecolor = {
                  label_pb2.Label.TYPE_PEDESTRIAN : 'blue'
                , label_pb2.Label.TYPE_VEHICLE    : 'red'
                , label_pb2.Label.TYPE_CYCLIST    : 'green'
                , label_pb2.Label.TYPE_SIGN       : 'yellow'
                , label_pb2.Label.TYPE_UNKNOWN    : 'black'
            }.get(label.type, 'white')

            # Draw the object bounding box.
            ax.add_patch(
                patches.Rectangle(
                      xy        = (label.box.center_x - 0.5 * label.box.length, label.box.center_y - 0.5 * label.box.width)
                    , width     = label.box.length
                    , height    = label.box.width
                    , linewidth = 1
                    , edgecolor = edgecolor
                    , facecolor = 'none'
                )
            )
    # -------------------------------------------------------------------------
    if not image_displayed:
        raise ValueError(f"No matching camera labels found for camera '{camera_image.name}'.")
    # -------------------------------------------------------------------------
    # Decode and display the camera image
    ax.imshow(
          tf.image.decode_jpeg(camera_image.image)
        , cmap=cmap
    )

    ax.set_title(
        camera_view_name
    )

    ax.grid(False)
    ax.axis('off')
# =============================================================================
#                         get_camera_labels_by_name
# =============================================================================
def get_camera_labels_by_name(
      frame
    , camera_name
    ):
    """
    Retrieves camera labels for a specific camera name within a given frame.

    This function searches through all camera labels in the provided frame object, looking for a match with the specified
    camera name. If a match is found, it returns the labels associated with that camera. If no matching camera is found,
    the function returns None, indicating that either the camera does not exist within the frame or there are no labels
    associated with it.

    Parameters:
    - frame (Frame): The frame object containing camera labels. The Frame object is expected to have a 'camera_labels' attribute
      that is iterable and contains elements with a 'name' attribute and a 'labels' attribute.
    - camera_name (str): The name of the camera for which labels are being requested.

    Returns:
    - list of Label or None: If the camera is found, returns a list of Label objects associated with the camera. Returns None
      if the camera is not found or there are no labels for the camera.

    Raises:
    - AttributeError: If the 'frame' object does not have a 'camera_labels' attribute, indicating it is not a valid frame object.
    - TypeError: If 'camera_name' is not a string, as camera names are expected to be string identifiers.

    Example usage:
    frame = ...  # Assume 'frame' is a properly loaded Frame object with camera labels
    camera_name = "FRONT"
    labels = get_camera_labels_by_name(frame, camera_name)
    if labels is not None:
        print(f"Found {len(labels)} labels for camera '{camera_name}'")
    else:
        print(f"No labels found for camera '{camera_name}'")
    """
    if not isinstance(camera_name, int):
        raise TypeError("The camera_name parameter must be an integer.")

    try:
        for camera_labels in frame.camera_labels:
            if camera_labels.name == camera_name:
                return camera_labels.labels
    except AttributeError:
        raise AttributeError("The provided 'frame' object does not have a 'camera_labels' attribute.")

    return None
# =============================================================================
#                        print_camera_labels_by_names
# =============================================================================
def print_camera_labels_by_names(
      frame
    , camera_names
    , map_id_to_name
    ):
    """
    Prints the camera labels for specified cameras within a frame.

    This function iterates through a list of camera names, retrieves the corresponding labels for each camera from the frame,
    and prints these labels. If a camera name does not have an associated label in the frame, a notification is printed instead.

    Parameters:
    - frame (Frame): The frame from which to retrieve camera labels.
    - camera_names (list of str): A list of camera names for which to print labels.
    - map_id_to_name (dict): A mapping from camera name to a human-readable string or identifier.

    Raises:
    - ValueError: If `camera_names` is empty or `map_id_to_name` does not contain mappings for one or more camera names provided.

    Example usage:
    frame = ...  # Assume frame is a loaded Frame object with camera labels
    camera_names = ['FRONT', 'SIDE_LEFT']
    map_id_to_name = {'FRONT': 'Front Camera', 'SIDE_LEFT': 'Left Side Camera'}
    print_camera_labels_by_names(frame, camera_names, map_id_to_name)
    """

    if not camera_names:
        raise ValueError("The list of camera names is empty.")

    for camera_name in camera_names:
        print(f"Camera: {camera_name} or '{map_id_to_name.get(camera_name, 'NOT FOUND')}'")
        camera_labels = get_camera_labels_by_name(frame, camera_name)

        print('-'*30)
        if camera_labels is not None:
            for label in camera_labels:
                print("Label:", label)
                print('-'*30)
        else:
            print(f"Camera labels for {camera_name} not found in the frame.")
# =============================================================================
#                               parse_frame
# =============================================================================
def parse_frame(
      frame
    , camera_name = 'FRONT'
    ):

    """
    Extracts the encoded image and bounding box annotations for a specific camera from a Waymo Open Dataset frame.

    This function navigates through the provided frame object, looking for image data and annotations that match the specified
    camera name. It then extracts the encoded JPEG image and a list of annotations for that camera.

    Parameters:
    - frame (dataset_pb2.Frame): A single frame from the Waymo Open Dataset, which includes images and annotations from various cameras.
    - camera_name (str, optional): The name of the camera to extract data for. Defaults to 'FRONT'.

    Returns:
    - encoded_jpeg (bytes or None): The encoded JPEG image of the specified camera, or None if no image is found.
    - annotations (list of dataset_pb2.Label): A list of bounding box annotations for the specified camera. Empty if no annotations are found.

    Raises:
    - ValueError: If `camera_name` does not match any camera in the frame.

    Example usage:
    frame = ...  # Assume frame is loaded from a TFRecord file
    encoded_jpeg, annotations = parse_frame(frame, camera_name='FRONT')
    """

    annotations  = []
    encoded_jpeg = None
    camera_found = False

    for im in frame.images:
        if dataset_pb2.CameraName.Name.Name(im.name) == camera_name:
            encoded_jpeg = im.image
            camera_found = True
            break

    if not camera_found:
        raise ValueError(f"Camera named {camera_name} not found in the frame.")

    for lab in frame.camera_labels:
        if dataset_pb2.CameraName.Name.Name(lab.name) == camera_name:
            annotations.extend(lab.labels)
            break

    if encoded_jpeg is None:
    # Optionally raise an exception if no image data could be found for the camera.
    # This depends on whether having a frame without image data is considered an error in your context.
        raise ValueError(f"No image data found for camera named {camera_name}.")

    return encoded_jpeg, annotations
# =============================================================================
#                              camera_frames
# =============================================================================
def camera_frames(
      class_colormap
    , ncols              = 5
    , figsize            = (24, 24)
    , num_frames         = None
    , camera_label       = 'FRONT'
    , tfrecord_file_name = os.environ['GCS_RECORD_NAME']
    , tfrecord_file_path = os.environ['FILE_PATH_DST']
    , display_output     = False
    ):

    """
    Extracts and displays images with bounding box annotations from a TFRecord file of the Waymo Open Dataset.

    This function iterates over a specified range of frames within a TFRecord file, extracts images and their
    corresponding bounding box annotations for a specified camera label, and displays these images in a grid format.

    Parameters:
    - class_colormap (dict): A dictionary mapping class IDs to colors for the bounding boxes.
    - ncols (int, optional): Number of columns in the image grid. Default is 5.
    - figsize (tuple, optional): Figure size for the plot (width, height) in inches. Default is (24, 24).
    - num_frames (range, optional): A range object specifying the frame indices to process. Default is range(50).
    - camera_label (str, optional): The camera label to extract frames from. Default is 'FRONT'.
    - tfrecord_file_name (str, optional): The name of the TFRecord file. Defaults to the 'GCS_RECORD_NAME' environment variable.
    - tfrecord_file_path (str, optional): The path to the TFRecord file. Defaults to the 'FILE_PATH_DST' environment variable.
    - display_output (bool, optional): Default is not displaying frames in the output after saving the animation.

    Returns:
    - images (list of np.ndarray): A list of images extracted from the specified frames.
    - annotations_list (list of lists): A nested list where each sublist contains bounding box annotations for a frame.

    Raises:
    - FileNotFoundError: If the specified TFRecord file does not exist.
    - ValueError: If `tfrecord_file_name` or `tfrecord_file_path` is not provided or invalid.
    """

    if not tfrecord_file_path or not exists(tfrecord_file_path):
        raise FileNotFoundError(f"TFRecord file does not exist at path: {tfrecord_file_path}")

    if not tfrecord_file_name:
        raise ValueError("TFRecord file name must be provided.")

    try:
        batch = tf.data.TFRecordDataset(
          tfrecord_file_path
        , compression_type=''
        )

        total_frames = 0
        for i, data in enumerate(batch):
            frame = dataset_pb2.Frame()
            total_frames += 1

        if num_frames is None:
            num_frames = range(total_frames)
            print(f"NOTE: The 'num_frames' argument passed as 'None' for this sequence, so all the {total_frames} frames will be displayed...")

        nrows = (len(num_frames) + ncols - 1) // ncols

        axes_pad = 0.2

        height = nrows * (figsize[1] / ncols)

        fig = plt.figure(
            figsize=(
                  figsize[0]
                , height
            )
        )

        grid = ImageGrid(
              fig
            , 111
            , axes_pad    = axes_pad
            , nrows_ncols = (nrows, ncols)
        )

        images           = []
        annotations_list = []

        # Prevent accessing more grid elements than available
        for i, frame_index in enumerate(num_frames):
            if i >= len(grid):
                break

            # Adjust this part to fetch the frame by its index if your batch supports it
            # This is a placeholder for fetching the frame data; adjust as per your dataset's structure
            data = batch\
                  .skip(frame_index)\
                  .take(1)\
                  .get_single_element()

            frame = dataset_pb2.Frame()
            frame.ParseFromString(bytearray(data.numpy()))

            image, labels = parse_frame(
                  frame
                , camera_label
            )

            images.append(
                tf.io.decode_image(image)
            )

            annotations_list.append(
                labels
            )

            grid[i].imshow(images[-1])
            grid[i].axis('off')

            # Set the title to the frame number
            grid[i].set_title(
                  f"Frame {frame_index}"
                , pad = 3
            )

            for lbl in labels:
                grid[i].add_patch(
                    patches.Rectangle(
                        xy        = (lbl.box.center_x - 0.5 * lbl.box.length, lbl.box.center_y - 0.5 * lbl.box.width)
                      , width     = lbl.box.length
                      , height    = lbl.box.width
                      , linewidth = 1
                      , facecolor = 'none'
                      , edgecolor = class_colormap[label_pb2.Label.Type.Name(lbl.type)]
                ))

        print(f"TFRecord File: '{tfrecord_file_name}'")
        print(f"Camera: '{camera_label}'")
        print(f"Frames: {min(num_frames)} to {max(num_frames)} (out of {total_frames})")
        print('Loading, please wait...\n')

        if display_output:
          plt.show()
        else:
          plt.close('all')

    except Exception as e:
        print(f"An error occurred: {e}")
        raise

    return images, annotations_list, num_frames
# =============================================================================
#                                 update
# =============================================================================
def update(
        ax
      , frame
      , images
      , annotations
      , class_colormap
      , title_text
    ):

    """
    Updates the given Axes object with the image and bounding box annotations for a specified frame.

    This function clears the current content of the Axes, displays the specified frame's image, and overlays bounding
    box annotations based on the provided annotations and class colormap. The bounding boxes are colored according to
    the class of each object, as defined in the class_colormap. It's designed to be used as part of an animation
    pipeline, where it updates the frame being displayed in an animation sequence.

    Parameters:
    - ax (matplotlib.axes.Axes): The matplotlib Axes object to update with the new frame and annotations.
    - frame (int): The index of the frame in the `images` list to display.
    - images (list of ndarray): A list of images (as numpy arrays) from which the frame's image will be displayed.
    - annotations (list of lists): A nested list where each sublist contains the bounding box annotations for a frame.
    - class_colormap (dict): A dictionary mapping class labels (as strings) to color strings. This colormap is used to
      color the bounding boxes according to their class.

    Returns:
    - list: A list of matplotlib.patches.Rectangle objects representing the bounding boxes for the current frame. This
      list is useful for managing the animation updates.

    Example usage:
    fig, ax = plt.subplots()
    artists = update(ax, 0, images, annotations, {'CAR': 'blue', 'PEDESTRIAN': 'green'})
    """

    # Clear the current content of the ax
    ax.clear()

    # Add the title text to the top of each frame
    ax.text(
          0.5
        , 1.05
        , title_text
        , ha        = 'center'
        , va        = 'bottom'
        , color     = 'black'
        , fontsize  = 10
        , transform = ax.transAxes
    )

    # Display the image
    ax.imshow(images[frame])

    # Optionally, set the axis limits to the size of the image
    ax.set_xlim(0, images[frame].shape[1])
    ax.set_ylim(images[frame].shape[0], 0)

    # Hide the axes details
    ax.axis('off')

    # Initialize an empty list to collect the artist objects
    artists = []

    # Add annotations for the current frame
    for lbl in annotations[frame]:
        rect = patches.Rectangle(
            xy=(lbl.box.center_x - 0.5 * lbl.box.length, lbl.box.center_y - 0.5 * lbl.box.width),
            width=lbl.box.length,
            height=lbl.box.width,
            linewidth=1,
            facecolor='none',
            edgecolor=class_colormap[label_pb2.Label.Type.Name(lbl.type)]
        )

        ax.add_patch(rect)
        artists.append(rect)

    return artists
# =============================================================================
#                           animation_pipeline
# =============================================================================
def animation_pipeline(
          class_colormap
        , gsutil_uri
        , camera_label
        , gif_fps
        , ncols            = 5
        , frames_range     = None
        , output_extension = "gif"
        , output_writer    = 'ffmpeg'
        , current_work_dir = os.environ['WORK_DIR_COLAB']
        , display_titles   = False
        , display_output   = False
    ):

    """
    Generates and saves an animation from a sequence of frames extracted from a TFRecord file within the Waymo Open Dataset.

    This function downloads the specified TFRecord file from Google Cloud Storage (GCS), extracts frames based on the given
    range and camera label, and creates an animation using the extracted frames. The animation is then saved as a file
    with the specified format and settings.

    Parameters:
    - class_colormap (dict): A dictionary mapping class labels to colors used in the bounding box annotations.
    - gsutil_uri (str): The Google Cloud Storage URI to the TFRecord file.
    - frames_range (range): A range object specifying the indices of the frames to include in the animation.
    - camera_label (str): The label of the camera to extract frames from. For example, 'FRONT', 'SIDE_LEFT', etc.
    - gif_fps (int): Frames per second for the output animation.
    - ncols (int, optional): The number of columns to use when displaying frames in a grid. Default is 5.
    - output_extension (str, optional): The file extension for the output animation. Default is 'gif'.
    - output_writer (str, optional): The backend writer to use for saving the animation. Default is 'ffmpeg'.
    - current_work_dir (str, optional): The working directory where the TFRecord file will be downloaded to and where the
      output file will be saved. Default is the current working directory.
    - display_output (bool, optional): Default is not displaying frames in the output after saving the animation.

    Returns:
    None. The function saves the generated animation to a file in the current working directory.

    Raises:
    - FileNotFoundError: If the TFRecord file cannot be downloaded from the GCS URI provided.
    - ValueError: If no frames are found for the specified camera label or frames range.

    Example usage:
    class_colormap = {'VEHICLE': 'r', 'PEDESTRIAN': 'g', 'CYCLIST': 'b'}
    gsutil_uri = 'gs://waymo_open_dataset_v_1_2_0_individual_files/training/<GCS_RECORD_NAME>.tfrecord'
    frames_range = range(20, 40)
    camera_label = 'FRONT'
    gif_fps = 10

    animation_pipeline(class_colormap=class_colormap, gsutil_uri=gsutil_uri, frames_range=frames_range,
                       camera_label=camera_label, gif_fps=gif_fps)
    """

    file_name_sequence = splitext(basename(gsutil_uri))[0]

    # Copy the blob from GCS to the current working directory
    if not isfile(join(current_work_dir, basename(gsutil_uri))):
        subprocess.run(
            [
                  'gsutil'
                , '-m'
                , 'cp'
                , gsutil_uri
                , current_work_dir
            ]
        )

    images, annotations, len_frames_range = camera_frames(
          class_colormap     = class_colormap
        , ncols              = ncols
        , num_frames         = frames_range
        , camera_label       = camera_label
        , tfrecord_file_name = file_name_sequence
        , tfrecord_file_path = join(current_work_dir, basename(gsutil_uri))
    )

    # Ensure images and annotations are not empty
    if not images or not annotations:
        print("Error: No images or annotations found.")
        return

    # Create animation and save it as a .gif file
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_autoscale_on(False)

    if display_titles:
        # Generate title text
        title_text = f"FPS: {gif_fps}\nCamera: '{camera_label}'\nFrames: '['{min(len_frames_range)}, {max(len_frames_range)}')'\n{basename(gsutil_uri)}"
    else:
      title_text = None

    anim = FuncAnimation(
          fig
        , lambda frame: update(ax, frame, images, annotations, class_colormap, title_text)
        , frames   = len(images)
        , interval = 1000 / gif_fps
        , blit     = True
    )

    # output animation filename
    filename_to_save_anim = f'{file_name_sequence}_{camera_label.lower()}_fr{min(len_frames_range)}-to-fr{max(len_frames_range)}.{output_extension}'

    path_to_save_anim = join(
          current_work_dir
        , filename_to_save_anim
    )

    anim.save(
          path_to_save_anim
        , fps    = gif_fps
        , writer = output_writer
        # , extra_args=['-b:v', '2M']  # Bitrate (2 Mbit/s)
    )

    # Close the plot if not displaying frames/animation to free up resources
    if display_output:
        plt.show()
    else:
        plt.close()

    if isfile(path_to_save_anim):
        print(f"[SUCCESS] - Animation was saved as {path_to_save_anim} !")
    else:
        print(f"[ERROR] - Failed to save the animation as {path_to_save_anim} !")

    # HTML(anim.to_html5_video())

    print('='*40)
