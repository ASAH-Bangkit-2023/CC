import tensorflow as tf
import numpy as np
import keras.utils as image
import io

load_model = tf.keras.models.load_model('tfmodel/checkpoint_model.h5')

def predict_image_classes(uploaded, IMG_SIZE=(224, 224), threshold=0.75):
        class_names = ['battery', 'biological', 'cardboard', 'clothes', 'glass', 'metal', 'paper', 'plastic', 'shoes', 'trash']

        class_info = get_class_info()

        info_dicts = []

        img = image.load_img(io.BytesIO(uploaded), target_size=IMG_SIZE + (3,))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)

        images = np.vstack([x])
        classes = load_model.predict(images, batch_size=10)
        outclass = np.argmax(classes)

        accuracy_percentage = classes[0][outclass] * 100 

        info_dict = {}  # Initialize info_dict as an empty dictionary

        if np.max(classes) < threshold:
            info_dict['prediction'] = 'No class detected'
            info_dict['message'] = 'Please try again with a different image'
            info_dict['accuracy_percentage'] = f"{accuracy_percentage:.2f}%"
            info_dicts.append(info_dict)
        else:
            if class_names[outclass] in class_info:
                info_dict = class_info[class_names[outclass]]
                info_dict['accuracy_percentage'] = f"{accuracy_percentage:.2f}%"
                info_dicts.append(info_dict)

        # We just only need info_dicts
        return info_dicts

def get_class_info():
    class_info = {
        'trash': {
            'prediction': 'Personal use waste',
            'message': 'Personal use waste refers to the type of waste generated from daily use by individuals. This can include items such as diapers, masks, pads, toothbrushes, and many more. Generally, this waste cannot be recycled due to sanitation issues and the complexity of separating and processing the materials contained in it.',
            'recycle_recommendation': 'Not recyclable',
            'action': 'Problems with sanitation issues and the complexity of separating and processing the materials contained in it make this type of waste non-recyclable.'
        },
        'glass': {
            'prediction': 'Glass',
            'message': 'A glass is a container that is usually cylindrical or conical in shape made from glass, ceramic, plastic, or metal. They are usually used for drinking, and can vary in size depending on their use. Yes, glass waste can be recycled. The glass recycling process involves collecting, breaking, and cleaning glass waste, before melting it and reshaping it into new glass products.',
            'recycle_recommendation': 'Recyclable',
            'action': 'Building materials, Glass product remanufacturing, Home decoration making, Jewelry making'
        },
        'plastic': {
            'prediction': 'Plastic',
            'message': 'Plastic is flexible, durable, lightweight, and easily molded into various shapes and sizes. Plastic waste refers to items that are made of plastic and have become useless or unwanted.',
            'recycle_recommendation': 'Recyclable',
            'action': 'Plant pots, Children toys, Home decorations, Shopping bags'
        },
        'cardboard': {
            'prediction': 'Cardboard',
            'message': 'Cardboard is a material generally made from recycled paper or wood pulp. It is strong, lightweight, and relatively cheap to produce, making it a popular choice for various packaging and shipping purposes. However, as is the case with plastic and other materials, cardboard can become waste once it is finished being used.',
            'recycle_recommendation': 'Recyclable',
            'action': 'Picture frame, Bed lamp, File storage, Room decoration, Drawer, Laptop stand'
        },
        'biological': {
            'prediction': 'Biological',
            'message': 'Biological waste, also known as organic waste or bio-waste, is waste that comes from living organisms or organic matter. This includes things like food waste, animal waste, leaves and tree branches, and so on.',
            'recycle_recommendation': 'Recyclable',
            'action': 'Pulp, Compost, Biogas production, Animal feed'
        },
        'battery': {
            'prediction': 'Battery',
            'message': 'Batteries are portable power sources that store and supply electrical energy. They are commonly used in various electronic devices and come in different sizes and types, such as alkaline, lithium-ion, and nickel-cadmium batteries.',
            'recycle_recommendation': 'Recyclable',
            'action': 'Battery recycling facilities, Proper disposal at designated collection points'
        },
        'clothes': {
            'prediction': 'Clothes',
            'message': 'Clothes are items of clothing worn by individuals to cover and protect their bodies. They can be made from various materials, including cotton, polyester, silk, and wool. When clothes are no longer needed or become worn-out, they can be considered waste.',
            'recycle_recommendation': 'Recyclable',
            'action': 'Donation to charitable organizations, Second-hand clothing stores, Textile recycling programs'
        },
        'metal': {
            'prediction': 'Metal',
            'message': 'Metal waste refers to discarded or unwanted items that are made primarily of metal. Common examples include aluminum cans, steel pipes, copper wires, and iron tools. Metal waste is highly recyclable and can be transformed into new metal products through processes like melting, purification, and reshaping.',
            'recycle_recommendation': 'Recyclable',
            'action': 'Metal recycling facilities, Scrap metal yards'
        },
        'shoes': {
            'prediction': 'Shoes',
            'message': 'Shoes are footwear items worn to protect and provide comfort to the feet. They can be made from various materials such as leather, rubber, fabric, and synthetic materials. When shoes are no longer in usable condition, they can be considered waste.',
            'recycle_recommendation': 'Recyclable',
            'action': 'Donation to charitable organizations, Shoe recycling programs'
        },
        'paper': {
            'prediction': 'Paper',
            'message': 'Paper is a versatile material made from wood pulp, recycled paper fibers, or other plant-based sources. It is widely used for writing, printing, packaging, and many other purposes. Paper waste includes items like newspapers, magazines, office paper, cardboard, and more.',
            'recycle_recommendation': 'Recyclable',
            'action': 'Paper recycling facilities, Repulping, Production of new paper products, Origami'
        }
    }
    return class_info