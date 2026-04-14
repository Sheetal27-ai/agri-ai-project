"""
AgriProfit AI - ML Pipeline for Soil Image Classification
This script outlines the process of training a lightweight CNN (MobileNetV2) on a public soil dataset.
Suitable for hackers wanting to extend the rule-based logic to a true Deep Learning system.
"""

import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# 1. Dataset Configuration (Assuming dataset structure: /data/train/Sandy/, /data/train/Clayey/, etc.)
DATA_DIR = "./data"
IMSZ = 224
BATCH_SIZE = 32

# 2. Data Augmentation & Preprocessing
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True,
    validation_split=0.2
)

train_generator = train_datagen.flow_from_directory(
    DATA_DIR, target_size=(IMSZ, IMSZ), batch_size=BATCH_SIZE, class_mode='categorical', subset='training'
)

val_generator = train_datagen.flow_from_directory(
    DATA_DIR, target_size=(IMSZ, IMSZ), batch_size=BATCH_SIZE, class_mode='categorical', subset='validation'
)

# 3. Model Architecture (Transfer Learning)
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(IMSZ, IMSZ, 3))
base_model.trainable = False  # Freeze base model

x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(128, activation='relu')(x)
predictions = Dense(train_generator.num_classes, activation='softmax')(x)

model = Model(inputs=base_model.input, outputs=predictions)

# 4. Compilation & Training
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

print("Starting training pipeline...")
# model.fit(train_generator, validation_data=val_generator, epochs=10)

# 5. Save the final model model for FastAPI inference
# model.save('soil_classifier_v1.h5')
print("Pipeline script saved. Run this to generate .h5 model for app.py")
