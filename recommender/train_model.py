import os
import django
import pandas as pd
import tensorflow as tf
import tensorflow_recommenders as tfrs

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "your_project_name.settings")
django.setup()

from Store.models import ReviewRating

# Load data
data = ReviewRating.objects.all().values('user_id', 'product_id')
df = pd.DataFrame(list(data))

# Convert to string
df['user_id'] = df['user_id'].astype(str)
df['product_id'] = df['product_id'].astype(str)

# Create dataset
dataset = tf.data.Dataset.from_tensor_slices({
    "user_id": df["user_id"].values,
    "product_id": df["product_id"].values
})

# Model
class Model(tfrs.Model):
    def __init__(self):
        super().__init__()

        self.user_model = tf.keras.Sequential([
            tf.keras.layers.StringLookup(vocabulary=df["user_id"].unique(), mask_token=None),
            tf.keras.layers.Embedding(len(df["user_id"].unique()) + 1, 32)
        ])

        self.item_model = tf.keras.Sequential([
            tf.keras.layers.StringLookup(vocabulary=df["product_id"].unique(), mask_token=None),
            tf.keras.layers.Embedding(len(df["product_id"].unique()) + 1, 32)
        ])

        self.task = tfrs.tasks.Retrieval()

    def compute_loss(self, features, training=False):
        user_embeddings = self.user_model(features["user_id"])
        item_embeddings = self.item_model(features["product_id"])
        return self.task(user_embeddings, item_embeddings)

model = Model()
model.compile(optimizer=tf.keras.optimizers.Adagrad(0.1))

# Train
model.fit(dataset.batch(32), epochs=3)

# Save model
model.save("recommender_model")

print("✅ Model trained and saved successfully")
