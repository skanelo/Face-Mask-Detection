import cv2
import glob
import os
import matplotlib.pyplot as plt
import argparse

def show_bounding_boxes(dir_path: str) -> None:
    """ Auxiliary function that displays the bounding boxes of images in folder <dir_path>.
        The folder should contain both the .png images and their corresponding .txt annotation files.
        The script follows the yolo format.
    """
    
    for image_file in glob.glob(dir_path + '/*.png'):
        image = cv2.imread(image_file)
        height, width, _ = image.shape

        with open(image_file.split(".")[0] +'.txt', 'r') as reader:
            annotations = reader.readlines()
            for annot in annotations:
                annot = annot.split()
                
                # Calculation of top left point and bottom right point of the bounding box           
                x1, y1 = int((float(annot[1]) - float(annot[3])/2)*width), int((float(annot[2]) - float(annot[4])/2)*height)
                x2, y2 = int((float(annot[1]) + float(annot[3])/2)*width), int((float(annot[2]) + float(annot[4])/2)*height)
                
                # BGR color format
                if annot[0] == '0':
                    color = (0,255,0)  # Mask is worn correctly (Green color)
                    label = 'Good'
                else:
                    color = (0,0,255)  # Mask is either not worn correctly or not worn at all (Red color)
                    label = 'Bad'
                
                cv2.putText(image,
                        label, 
                        (x1, y1 - 10),
                        fontFace=cv2.FONT_HERSHEY_TRIPLEX,
                        fontScale=0.5, 
                        color=color,
                        thickness=1) 
                
                cv2.rectangle(image, (x1, y1), (x2, y2), color, thickness=1)
        
        k = cv2.waitKey(0) & 0xFF
        cv2.imshow(image_file.split("sss")[-1], image)
        if k == 27:
            cv2.destroyAllWindows()
            break

def parser() -> None:
    parser = argparse.ArgumentParser(description="Display Bounding-Boxes on png images with yolo format (<label> <x_center> <y_center> <width> <height>).")
    parser.add_argument("--input", type=str, default="", help="The path of the folder that contains the png images with their corresponding txt annotations.")
    return parser.parse_args()

def check_arguments_errors(args : argparse.Namespace) -> None:
    if not os.path.exists(args.input):
        raise(ValueError("Invalid input folder path: {}".format(os.path.abspath(args.input))))

def main() -> None:
    args = parser()
    check_arguments_errors(args)   
    show_bounding_boxes(args.input)

if __name__ == "__main__":
    main()