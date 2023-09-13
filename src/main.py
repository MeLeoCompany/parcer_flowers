import logging
from parcer.parcer import Parcer
from parcer.services import init_db_connection, init_logger

# def object_detection_on_an_image():
#     exec_path = os.getcwd()

#     detector = ObjectDetection()
#     detector.setModelTypeAsRetinaNet()
#     detector.setModelPath(os.path.join(
#         exec_path, "retinanet_resnet50_fpn_coco-eeacb38b.pth")
#     )
#     detector.loadModel()

#     list = detector.detectObjectsFromImage(
#         input_image="/mnt/c/Projects_Learn/Parce_Flowers/istockphoto.jpg",
#         output_image_path="/mnt/c/Projects_Learn/Parce_Flowers/out.jpg",
#         minimum_percentage_probability=75,
#         display_percentage_probability=True,
#         display_object_name=False
# )

def main():
    init_logger()
    logging.info('Запуск системы..')
    collection = init_db_connection()
    parcer = Parcer()
    parcer.run(collection)
    # source = dict(zip(titles, source_urls))
    # collect_pic(source)

if __name__ == "__main__":
    main()