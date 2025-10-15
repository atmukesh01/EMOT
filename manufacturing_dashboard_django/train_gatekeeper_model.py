import tensorflow as tf
from tensorflow.keras.utils import image_dataset_from_directory
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
import os

# --- Configuration ---
DATASET_PATH = 'manufacturing_dashboard_django/gatekeeper_dataset'
IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32
MODEL_SAVE_PATH = os.path.join('predictor', 'plastic_gatekeeper_model.keras')

# --- Check for Dataset ---
if not os.path.isdir(DATASET_PATH) or not os.listdir(DATASET_PATH):
    print(f"❌ Error: Dataset folder '{DATASET_PATH}' not found or is empty.")
    print("Please create this folder with 'plastic' and 'not_plastic' subfolders inside.")
    exit()

# 1. Load the dataset
print("Loading 'Plastic vs. Not Plastic' dataset...")
train_dataset = image_dataset_from_directory(
    DATASET_PATH, validation_split=0.2, subset="training", seed=123,
    image_size=IMAGE_SIZE, batch_size=BATCH_SIZE
)
validation_dataset = image_dataset_from_directory(
    DATASET_PATH, validation_split=0.2, subset="validation", seed=123,
    image_size=IMAGE_SIZE, batch_size=BATCH_SIZE
)
class_names = train_dataset.class_names
print(f"Found classes: {class_names}")

# 2. Set up MORE AGGRESSIVE data augmentation
print("Applying more aggressive data augmentation...")
AUTOTUNE = tf.data.AUTOTUNE
data_augmentation = tf.keras.Sequential([
  tf.keras.layers.RandomFlip('horizontal'),
  tf.keras.layers.RandomRotation(0.2),
  tf.keras.layers.RandomZoom(0.2),
  # New additions for harder training
  tf.keras.layers.RandomBrightness(factor=0.2),
  tf.keras.layers.RandomContrast(factor=0.2),
])
train_dataset = train_dataset.map(lambda x, y: (data_augmentation(x, training=True), y), num_parallel_calls=AUTOTUNE).prefetch(buffer_size=AUTOTUNE)
validation_dataset = validation_dataset.prefetch(buffer_size=AUTOTUNE)

# 3. Create the model
print("Building the Gatekeeper model...")
base_model = MobileNetV2(input_shape=IMAGE_SIZE + (3,), include_top=False, weights='imagenet')
base_model.trainable = False

x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dropout(0.2)(x)
predictions = Dense(1, activation='sigmoid')(x)
model = Model(inputs=base_model.input, outputs=predictions)

# 4. Initial training phase with LONGER training time
print("\n--- Starting Initial Training (Longer) ---")
model.compile(optimizer=Adam(learning_rate=0.001),
              loss='binary_crossentropy',
              metrics=['accuracy'])
# Increased epochs from 5 to 8
history = model.fit(train_dataset, epochs=8, validation_data=validation_dataset)

# 5. Fine-tuning phase with DEEPER unfreezing and LONGER training
print("\n--- Starting Fine-Tuning (Deeper & Longer) ---")
base_model.trainable = True

# We will unfreeze the top 50 layers instead of just 20
print("Unfreezing more layers for deep fine-tuning...")
for layer in base_model.layers[:-50]:
    layer.trainable = False

# Re-compile the model with a very low learning rate
model.compile(optimizer=Adam(learning_rate=0.0001), # 1e-4
              loss='binary_crossentropy',
              metrics=['accuracy'])

# Increased fine-tuning epochs from 5 to 7
history_fine = model.fit(train_dataset, epochs=7, validation_data=validation_dataset, initial_epoch=history.epoch[-1])

# 6. Save the final, more powerful model
print("\n--- Training Complete ---")
model.save(MODEL_SAVE_PATH)
print(f"✅ Advanced Gatekeeper model saved successfully to: {MODEL_SAVE_PATH}")