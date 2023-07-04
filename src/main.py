from imageai.Detection import ObjectDetection
import os


def object_detection_on_an_image():
    exec_path = os.getcwd()

    detector = ObjectDetection()
    detector.setModelTypeAsRetinaNet()
    detector.setModelPath(os.path.join(
        exec_path, "retinanet_resnet50_fpn_coco-eeacb38b.pth")
    )
    detector.loadModel()

    list = detector.detectObjectsFromImage(
        input_image="/mnt/c/Projects_Learn/Parce_Flowers/istockphoto.jpg",
        output_image_path="/mnt/c/Projects_Learn/Parce_Flowers/out.jpg",
        minimum_percentage_probability=75,
        display_percentage_probability=True,
        display_object_name=False
    )

def main():
    # parce()
    object_detection_on_an_image()

if __name__ == "__main__":
    main()